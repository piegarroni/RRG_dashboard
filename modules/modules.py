import pandas as pd
import plotly.graph_objs as go
from dash import Dash

import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
from datetime import datetime

# external css static
external_stylesheets = [dbc.themes.SLATE]

# dash app with external stylesheet
app = Dash(__name__, external_stylesheets=external_stylesheets)



# define date range
start_date = "2000-01-22"
end_date  = datetime.today().strftime('%Y-%m-%d')

date_range = pd.date_range(start=start_date, end=end_date, freq="B")


def rs_ratio(prices_df, benchmark, rolling = 6, pct_change = 5):
    
    """
    Function that returns dataframe with relative strength ratio for each symbol (days)
    """
    
    # create new dataframe
    index = prices_df.index
    ratio_df = pd.DataFrame(index=index)
    ratio_df.index = pd.to_datetime(ratio_df.index)
    
    benchmark = benchmark.rolling(rolling).mean()
    benchmark = benchmark.pct_change(pct_change)
    
    #plt.plot(benchmark[-200:])

    for column in prices_df:
        prices_df[column] = prices_df[column].rolling(rolling).mean()
        prices_df[f'{column}_return'] = prices_df[column].pct_change(pct_change)
        prices_df[f'{column}_ratio'] = prices_df[f'{column}_return'] - benchmark
        
    return prices_df.rolling(10).mean()



def rs_momentum(ratio_df, rolling = 2, shift = 5):
    index = ratio_df.index

    momentum_df = pd.DataFrame(index=index)

    for column in ratio_df:
        name = column.split('_')[0]
        rs_momentum = ratio_df[column] - ratio_df[column].shift(shift)
        momentum_df[f'{name}_momentum'] = rs_momentum.rolling(rolling).mean()
        
    return momentum_df



def resample_weekly(df):
    dff = df.copy()
    weekly_averages = dff.resample('W').mean()

    # Reset the index to make the datetime column a regular column
    weekly_averages = weekly_averages.reset_index()
    return weekly_averages.set_index('Date')



def visualize_asset_benchmark(df, asset_symbols, benchmark_symbol):
    """
    Function to visualize the RS ratio and Momentum on two separate graphs, given one symbol
    """
    # make a copy of the dataframe
    dff = df.copy()

    # if asset is a string then add column, otherwise add columns
    if type(asset_symbols) == str:
        asset = dff[("Adj Close", asset_symbols)]
    else:
        asset = dff[[("Adj Close", i) for i in asset_symbols]]

    # define benchmark column
    benchmark = dff[("Adj Close", benchmark_symbol)]

    # make graph
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

    # for every asset add a trace in the graph
    for column in asset:
        fig.add_trace(
            go.Scatter(x=asset.index, y=asset[column], name=f"Asset ({column[1]})"), row=1, col=1
        )
    
    # on the second graph plot only the benchmark
    fig.add_trace(
        go.Scatter(x=benchmark.index, y=benchmark, name=f"Benchmark ({benchmark_symbol})"), row=2, col=1
    )

    fig.update_layout(
        title=f"Benchmark ({benchmark_symbol}) vs asset ({asset_symbols})", 
        height=600, 
    )

    return fig

def visualize_rs(df, symbols):
    """
    Function to visualize the RS ratio and Momentum on two separate graphs, given one symbol
    """
    # make a copy of the dataframe
    dff = df.copy()

    # if symbols is string then add one column, else add multiple columns
    if type(symbols) == str:
        rs_ratio = dff[f"{symbols}_ratio"]
        rs_momentum = dff[f"{symbols}_momentum"]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
        fig.add_trace(
            go.Scatter(x=rs_ratio.index, y=rs_ratio, name="RS Ratio"), row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=rs_momentum.index, y=rs_momentum, name="RS Momentum"), row=2, col=1
        )

        fig.update_layout(
            title=f"RS Ratio and Momentum for {symbols}", height=600, 
        )
    else:
        rs_ratio = dff[[f"{i}_ratio" for i in symbols]]
        rs_momentum = dff[[f"{i}_momentum" for i in symbols]]

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)

        for ratio, momentum in zip(rs_ratio.columns, rs_momentum.columns):
            column =momentum.split("_")[0]
            fig.add_trace(
                go.Scatter(x=rs_ratio.index, y=rs_ratio[ratio], name=f"RS Ratio {column}"), row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(x=rs_momentum.index, y=rs_momentum[momentum], name=f"RS Momentum {column}"), row=2, col=1
            )

        fig.update_layout(
            title=f"RS Ratio and Momentum for {symbols}", height=600, 
        )
    return fig


def visualize_rrg(df, symbols, period, frequency = 'days'):
    """
    Function to visualize the Relative Rotation Graph of the selected symbol
    """
    # make a copy of the dataframe
    dff = df.copy()

    # select last date
    dff = dff.iloc[-period:]

    # last datapoint
    past = dff.iloc[:-1]
    last = dff.iloc[-1]

    # plot figure
    fig = go.Figure()

    for i in symbols:
        fig.add_trace(
            go.Scatter(
                x=dff[f"{i}_ratio"],
                y=dff[f"{i}_momentum"],
                mode="lines",
                name=i,

            )
        )

        fig.add_trace(
            go.Scatter(
                x=[last[f"{i}_ratio"]],
                y=[last[f"{i}_momentum"]],
                mode="markers",
                marker=dict(size=7),
                showlegend=False,
            )
        )

        fig.add_trace(
            go.Scatter(
                x=past[f"{i}_ratio"],
                y=past[f"{i}_momentum"],
                mode="markers",
                marker=dict(symbol="x"),
                showlegend=False,
            )
        )

    fig.update_layout(
        title=f"RRG graph ({frequency})",
        xaxis_title="RS ratio",
        yaxis_title="RS momentum",
        xaxis = dict(zerolinecolor='black'),
        yaxis = dict(zerolinecolor='black')
    )

    return fig
