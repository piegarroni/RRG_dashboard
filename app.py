import dash
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
from dash import (
    Dash,
    dcc,
    html,
    dcc,
    html,
) 
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from datetime import datetime
from modules import modules
import json
# external css static
external_stylesheets = [dbc.themes.SLATE]

# dash app with external stylesheet
app = Dash(__name__, external_stylesheets=external_stylesheets)

# open symbols' files
with open("data/assets.json", "r") as f:
    assets = json.load(f)
with open("data/stocks.json", "r") as f:
    stocks = json.load(f)
with open("data/cryptos.json", "r") as f:
    cryptos = json.load(f)
with open("data/indeces.json", "r") as f:
    indeces = json.load(f)

# merge all symbols
available_symbols = {}
available_symbols.update(assets)
available_symbols.update(indeces)
available_symbols.update(cryptos)
available_symbols.update(stocks)

benchmarks = {}
benchmarks.update(assets)
benchmarks.update(indeces)
benchmarks.update({'Bitcoin (BTC-USD)': 'BTC-USD', 'Ethereum (ETH-USD)': 'ETH-USD'})


# define date range
start_date = "2000-01-22"
end_date  = datetime.today().strftime('%Y-%m-%d')

date_range = pd.date_range(start=start_date, end=end_date, freq="B")


# ----------------------------------------------------------------------------------------------------------------------

app.layout = html.Div(
    [
        html.H1("Visualizing RS Ratio and Momentum (Daily)"),
        html.Label("Select a symbol:"),
        dcc.Dropdown(
            id="symbol-dropdown",
            options=[
                {"label": symbol, "value": available_symbols[symbol]}
                for symbol in available_symbols
            ],
            value=available_symbols["US bond (QLTA)"],
            multi=True
        ),
        html.Br(),

        html.Label("Select a benchmark:"),
        dcc.Dropdown(
            id="benchmark-dropdown",
            options=[
                {"label": symbol, "value": benchmarks[symbol]}
                for symbol in benchmarks
            ],
            value=available_symbols["S&P 500 (SPY)"],
        ),
        html.Br(),
        html.Br(),
        html.Label("Select time range (from 01-2000 to today):"),

        dcc.RangeSlider(
            id="time-range",
            min=0,
            max=len(date_range.copy()) - 1,
            value=[len(date_range.copy()) - 1000, len(date_range.copy()) - 1],
            allowCross=False,
            marks=None
        ),

        dcc.Graph(id="comparison-plot"),
        html.Br(),

        dcc.Graph(id="rs-plot"),

        html.Br(),
        html.Br(),
        html.Label("Select tail length (weeks):"),
        dcc.Slider(
            id="tail-length",
            min=5,
            max=50,
            value=20,
            marks={i: str(i) for i in range(2, 51)},
        ),
        html.Br(),
        html.Label("Selected period:"),

        html.Div(id="output_container", children=[]),
        html.Br(),
        dcc.Graph(
            id="rrg-plot",
            figure={},
            style={"width": "60%", "height": "67vh", "backgroundColor": "black"},
        ),
        html.Br(),
        html.Br(),
        html.Br(),
        #--------------------------------------------------------------------------
        html.H1("Visualizing RS Ratio and Momentum (Weekly)"),
        html.Label("Select a symbol:"),
        
        html.Br(),
        html.Br(),
        
        #dcc.Graph(id="comparison-plot"),
        dcc.Graph(id="rs-plot-weekly"),

        html.Br(),

        html.Label("Selected period:"),

        html.Div(id="output_container", children=[]),
        html.Br(),
        dcc.Graph(
            id="rrg-plot-weekly",
            figure={},
            style={"width": "60%", "height": "67vh", "backgroundColor": "black"},
        ),
        html.Br(),
    ],
    style={"margin": "35px 5% 75px 5%"},
)


data = yf.download(['QLTA', 'SPY'], start_date, end_date)

@app.callback(
    dash.dependencies.Output("comparison-plot", "figure"),
    dash.dependencies.Output("rs-plot", "figure"),
    dash.dependencies.Output("rrg-plot", "figure"),
    dash.dependencies.Output("rs-plot-weekly", "figure"),
    dash.dependencies.Output("rrg-plot-weekly", "figure"),   
    dash.dependencies.Output("output_container", "children"),
    [
        dash.dependencies.Input("symbol-dropdown", "value"),
        dash.dependencies.Input("benchmark-dropdown", "value"),
        dash.dependencies.Input("tail-length", "value"),
        dash.dependencies.Input("time-range", "value"),
    ],
)
def update_plots(symbols, benchmark, tail_len, time_range):


    # define date range start and end
    
    last_date = date_range[time_range[1]]
    first_date = date_range[time_range[0]]

    # create a list with all symbols (assets and benchmark)
    all_symbols= []
    if type(symbols) == str:
        all_symbols.append(symbols)
        symbols = [symbols]
    else:
        all_symbols = symbols
    all_symbols.append(benchmark)
    # create list of symbols excluding benchmark
    assets = [i for i in all_symbols if i != benchmark]
    # Download data from Yahoo Finance
    data = yf.download(all_symbols, start_date, end_date)
    data = data.dropna()

    # subset within selected range
    data_copy = data.copy()
    data_loc = data_copy.loc[(data_copy.index > first_date) & (data_copy.index <= last_date)]
    
    # Retrieve rs ratio and momentum (daily)
    ratio_df = modules.rs_ratio(data_loc["Adj Close"], data_loc[("Adj Close", benchmark)])
    momentum_df = modules.rs_momentum(ratio_df)

    # Merge rs ratio and momentum data (daily)
    df = pd.merge(
        ratio_df, momentum_df, left_on=ratio_df.index, right_on=momentum_df.index
    ).set_index("key_0")

    # container for inputs information
    container = f"Displaying RRG graph for {symbols} from {df.index[0]} until {str(last_date)}, with tail length {tail_len*5} days"

     # subset within selected range -+------------------------------------------------
    data_copy = data.copy()
    data_loc = data_copy.loc[(data_copy.index > first_date) & (data_copy.index <= last_date)]

    # resample dataset from daily to weekly
    data_loc = modules.resample_weekly(data_loc)
    
    # Retrieve rs ratio and momentum (daily)
    ratio_df = modules.rs_ratio(data_loc["Adj Close"], data_loc[("Adj Close", benchmark)], 3, 3)
    momentum_df = modules.rs_momentum(ratio_df, 1, 3)

    # Merge rs ratio and momentum data (daily)
    df_weekly = pd.merge(
        ratio_df, momentum_df, left_on=ratio_df.index, right_on=momentum_df.index
    ).set_index("key_0")

    # container for inputs information
    container = f"Displaying RRG graph for {symbols} from {df.index[0]} until {str(last_date)}, with tail length {tail_len} weeks"

    # CREATE COPY IN MODULES FUNCTIONS
    data_copy = data.copy()
    data_loc = data_copy.loc[(data_copy.index > first_date) & (data_copy.index <= last_date)]
    return (
        modules.visualize_asset_benchmark(data_loc, assets, benchmark), 
        modules.visualize_rs(df, assets),
        modules.visualize_rrg(df, assets, int(tail_len)*5),
        modules.visualize_rs(df_weekly, assets),
        modules.visualize_rrg(df_weekly, assets, int(tail_len), 'weeks'),
        container,
    )


if __name__ == "__main__":
    app.run_server(debug=True)
