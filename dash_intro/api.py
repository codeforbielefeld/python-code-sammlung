import numpy as np
import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html
from flask import Flask

server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname="/dash/")


@app.callback(
    Output(component_id="histogramm", component_property="figure"),
    [
        Input(component_id="verteilung-dropdown", component_property="value"),
        Input(component_id="n-input", component_property="value"),
    ],
)
def hist(verteilung, n):
    data = None
    if verteilung == "normal":
        data = np.random.normal(loc=0, scale=1, size=n)
    elif verteilung == "binomial":
        data = np.random.binomial(n=10, p=0.5, size=n)
    elif verteilung == "chisquared":
        data = np.random.chisquare(df=5, size=n)
    elif verteilung == "pandas":
        data = pd.DataFrame(
            {
                "Art": ["Dickbauchpanda", "Dünnbauchpanda", "Kung-Fu Panda"],
                "Anzahl Europa": [2, 3, 1],
                "Anzahl Asien": [10, 15, 1],
            }
        )
    else:
        print("Diese Verteilung wird noch nicht unterstützt!")
        return
    print(type(data))
    print(data)
    # return px.histogram(data)
    return px.bar(
        data,
        barmode="group",
        x="Art",
        y=["Anzahl Europa", "Anzahl Asien"],
        color_discrete_map={"Anzahl Europa": "green", "Anzahl Asien": "black"},
        labels={
            "Art": "Art__",
            "variable": "variable__",
            "value": "value__",
        },
    )


app.title = "Our first dashboard"
app.layout = html.Div(
    children=[
        html.H1(children="Verteilungen"),
        html.Div(
            children=[
                html.H2("Inputs"),
                html.Div(
                    children=[
                        html.P("Verteilung"),
                        dcc.Dropdown(
                            id="verteilung-dropdown",
                            options=[
                                {"label": "Normal", "value": "normal"},
                                {"label": "Binomial", "value": "binomial"},
                                {"label": "Chi²", "value": "chisquared"},
                                {"label": "Pandas DF", "value": "pandas"},
                            ],
                            value="normal",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.P("Stichprobengröße"),
                        dcc.Input(
                            id="n-input",
                            placeholder="Stichprobengröße",
                            type="number",
                            value=100,
                        ),
                    ],
                ),
            ],
            # mit style kann man CSS-Formatierungen verwenden
            style={
                "backgroundColor": "#DDDDDD",
                "maxWidth": "800px",
                "padding": "10px 20px",
            },
        ),
        html.Div(
            children=[
                html.H2("Histogramm"),
                dcc.Graph(id="histogramm", config={"scrollZoom": True}),
            ],
            style={
                "backgroundColor": "#DDDDDD",
                "maxWidth": "800px",
                "marginTop": "10px",
                "padding": "10px 20px",
            },
        ),
    ]
)


if __name__ == "__main__":
    app.run_server(debug=False)
