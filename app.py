from time import time
from unicodedata import name
from dash import Dash, dcc, html, Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

app = Dash(__name__)

df = pd.read_excel("dashboard.xlsx")

states = df.State.unique().tolist()
dates = df.Date
maxd = dates.max()
mind = dates.min()
outcome = df.Outcome.unique().tolist()
# states.insert(0, "all")
outcome.insert(0, "all")


# part a
# https://www.tutorialspoint.com/how-to-plot-multiple-lines-on-the-same-y-axis-in-python-plotly
def part_a(outcome):

    fig1 = px.line(x=totac.index, y=totac.values)
    fig1.add_scatter(x=totsuc.index, y=totsuc.values, name="Success")
    fig1.add_scatter(x=totnsuc.index, y=totnsuc.values, name="Failure")

    if outcome == "Success":
        pass
    else:
        fig1.add_scatter(x=totsuc.index, y=totsuc.values *
                         100/totac[totsuc.index], name="Ratio")

    return fig1


def part_b():
    fig2 = px.bar(x=totacs.index, y=totacs.values)
    fig2.add_bar(x=totsucs.index, y=totsucs.values, name="Success")
    fig2.add_bar(x=totnsucs.index, y=totnsucs.values, name="Failure")

    return fig2


def part_c():
    data1 = df.groupby("Outcome")["Outcome"].count()
    fig3 = px.pie(values=data1.values, names=data1.index)

    return fig3


def part_d():
    dfr = (totsucs.values*100/totacs[totsucs.index]).sort_values()
    fig4 = px.bar(x=dfr.index, y=dfr.values)

    return fig4


def part_e():
    # https://plotly.com/python/pie-charts/
    totac = df.groupby('State')['Outcome'].count()

    labels = totac.index
    vals = totac.values.flatten()

    fig5 = go.Figure(data=[go.Pie(labels=labels, values=vals, hole=.3)])
    fig5.update_layout(margin=dict(t=0, b=0, l=0, r=0))

    return fig5


def part_f():

    try:
        fig6 = px.bar(df1_modify, x=df1_modify.Time_Period,
                      y=df1_modify.Outcome)
        return fig6
    except Exception as e:
        pass


def filter_date(outcome, state, start_date, end_date):

    global df, totac, totacs, totnsuc, totsucs, tottime, totnsucs, totsuc, df1_modify

    df = pd.read_excel("dashboard.xlsx")

    if outcome == "all" and state == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
    elif outcome == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.State.isin(state)]
    elif state == "all":
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.Outcome == outcome]
    else:
        df = df[(df.Date >= start_date) & (df.Date <= end_date)]
        df = df[df.State.isin(state)]
        df = df[df.Outcome == outcome]

    totac = df.groupby('Date')['Outcome'].count()
    totsuc = df[df['Outcome'] == 'Success'].groupby('Date')['Outcome'].count()
    totnsuc = df[df['Outcome'] == 'Failure'].groupby('Date')['Outcome'].count()
    tottime = df[df['Outcome'] == 'Time out'].groupby('Date')[
        'Outcome'].count()
    totacs = df.groupby('State')['Outcome'].count()
    totsucs = df[df['Outcome'] == 'Success'].groupby('State')[
        'Outcome'].count()
    totnsucs = df[df['Outcome'] == 'Failure'].groupby('State')[
        'Outcome'].count()

    df1_modify = (
        df[df["Outcome"] == "Success"]
        .groupby("Time_Period")["Outcome"]
        .count()
        .reset_index()
    )


app.layout = html.Div([
    html.H1("Coursework 2", style={'text-align': 'center', "color": "white",
            "font-weight": "bold", "font-size": "48px"}, className="topName"),

    html.Div([

        html.P("1. We want to see this data in a graph with a time series legend. Then we want to see in the same graph the ratio of success /total calls as a function of date.",
               style={'text-align': 'left', "padding": "10px", "font-size": "30px"}),

        html.Div(children=[
            dcc.Dropdown(
                options=["Success", "Failure"],
                value='all',
                id="input1",
           
            ),
            dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input2",
                        #   style={
                        #     "width": "40%",
                        #     "margin":"5px",}
                         ),
            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="input3",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            )],
            className="dropdown1"),

        dcc.Graph(id="output1"),




        html.P("2. We want to see another graph that presents the success and failure by State in the form of a bargraph.", style={
               'text-align': 'left', "padding": "10px", "font-size": "30px"}),
        html.Div(children=[
            dcc.Dropdown(
                options=["Success", "Failure"],
                value='all',
                id="input4"),

            dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input5"),
            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="input6",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            )
        ], className="dropdown1"),

        dcc.Graph(id="output2"),


        html.P("3. We want to see a piechart that displays failure-success-timeout as a percentage",
               style={'text-align': 'left', "padding": "10px", "font-size": "30px"}),
        html.Div(children=[

            dcc.Dropdown(
                options=["Success", "Failure"],
                value='all',
                id="input7"),

            dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input8"),
            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="input9",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            ),
            ], className="dropdown1"),
            dcc.Graph(id="output3"),


        html.P("4. We want to see at the end which state was the most ' successful ' in share ratios.", style={
               'text-align': 'left', "padding": "10px", "font-size": "30px"}),
        html.Div(children=[

            dcc.Dropdown(
                options=["Success"],
                value='all',
                id="input10"),

            dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input11"),
            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="input12",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            ),
            ], className="dropdown1"),
            dcc.Graph(id="output4"),


        html.P("5. We also want to see a double piechart that displays the total number of actions/ State and number of success / state .",
               style={'text-align': 'left', "padding": "10px", "font-size": "30px"}),
        html.Div(children=[

            dcc.Dropdown(
                options=["Success", "Failure"],
                value='all',
                id="input13"),

            dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input14"),
            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="input15",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            ),
            ], className="dropdown1"),
            dcc.Graph(id="output5"),


        html.P("6. We want to know the number of succes by Time_Period (be careful with the ordering)", style={
               'text-align': 'left', "padding": "10px", "font-size": "30px"}),
        html.Div(children=[

            dcc.Dropdown(
                options=["Success", "Failure"],
                value='all',
                id="input16",
                style={
                    "display":"none"
                }),
                

            dcc.Dropdown(states,
                         multi=True,
                         value='all',
                         placeholder="all",
                         id="input17"),
            dcc.DatePickerRange(
                end_date_placeholder_text='M-D-Y-Q',
                id="input18",
                start_date=mind,
                end_date=maxd,
                min_date_allowed=mind,
                max_date_allowed=maxd,
            ),
            ], className="dropdown1"),
            dcc.Graph(id="output6"),

    ], className="mainDiv")
])


@ app.callback(
    Output('output1', 'figure'),
    Input('input1', "value"),
    Input('input2', "value"),
    Input('input3', "start_date"),
    Input('input3', "end_date"),
)
def update_output(value1, value2, value3, value4):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter_date(value1, value2, value3, value4)

    return part_a(value1)


@ app.callback(
    Output('output2', 'figure'),
    Input('input4', "value"),
    Input('input5', "value"),
    Input('input6', "start_date"),
    Input('input6', "end_date"),
)
def update_output(value1, value2, value3, value4):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter_date(value1, value2, value3, value4)

    return part_b()


@ app.callback(
    Output('output3', 'figure'),
    Input('input7', "value"),
    Input('input8', "value"),
    Input('input9', "start_date"),
    Input('input9', "end_date"),
)
def update_output(value1, value2, value3, value4):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter_date(value1, value2, value3, value4)

    return part_c()


@ app.callback(
    Output('output4', 'figure'),
    Input('input10', "value"),
    Input('input11', "value"),
    Input('input12', "start_date"),
    Input('input12', "end_date"),
)
def update_output(value1, value2, value3, value4):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter_date(value1, value2, value3, value4)

    return part_d()


@ app.callback(
    Output('output5', 'figure'),
    Input('input13', "value"),
    Input('input14', "value"),
    Input('input15', "start_date"),
    Input('input15', "end_date"),
)
def update_output(value1, value2, value3, value4):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter_date(value1, value2, value3, value4)

    return part_e()


@ app.callback(
    Output('output6', 'figure'),
    Input('input16', "value"),
    Input('input17', "value"),
    Input('input18', "start_date"),
    Input('input18', "end_date"),
)
def update_output(value1, value2, value3, value4):

    if value2 == None or len(value2) == 0:
        value2 = "all"

    if value1 == None or len(value1) == 0:
        value1 = "all"

    filter_date(value1, value2, value3, value4)

    return part_f()


if __name__ == "__main__":
    app.run_server(debug=True)
