import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_TABLE = os.getenv("DB_TABLE")

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

query = f"SELECT coin_name, timestamp, price, market_cap, volume FROM {DB_TABLE} ORDER BY timestamp;"
df = pd.read_sql(query, engine)
df["date"] = pd.to_datetime(df["timestamp"])


def compute_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))


df["RSI"] = df.groupby("coin_name")["price"].transform(lambda x: compute_rsi(x))

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.H1(
            "Crypto Market Dashboard",
            style={"text-align": "center", "font-size": "32px"},
        ),
        html.Div(
            [
                html.Label(
                    "Select Coin:", style={"font-size": "18px", "margin-right": "20px"}
                ),
                dcc.Dropdown(
                    id="coin-selector",
                    options=[
                        {"label": coin, "value": coin}
                        for coin in df["coin_name"].unique()
                    ],
                    value=df["coin_name"].unique()[0],
                    multi=False,
                    style={"width": "250px", "font-size": "16px"},
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "center",
                "margin-top": "50px",
            },
        ),
        html.Div(
            [
                dcc.Graph(
                    id="price-chart",
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "margin-top": "20px",
                    },
                ),
                dcc.Graph(
                    id="market-cap-chart",
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "margin-top": "20px",
                    },
                ),
                dcc.Graph(
                    id="volume-chart",
                    style={
                        "width": "32%",
                        "display": "inline-block",
                        "margin-top": "20px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "flex-start",
                "margin-top": "50px",
            },
        ),
        html.Div(
            [
                dcc.Graph(
                    id="rsi-chart",
                    style={
                        "width": "50%",
                        "display": "inline-block",
                        "margin-top": "20px",
                    },
                ),
            ],
            style={
                "display": "flex",
                "justify-content": "center",
                "align-items": "flex-start",
                "margin-top": "50px",
            },
        ),
    ]
)


@app.callback(
    [
        dash.Output("price-chart", "figure"),
        dash.Output("market-cap-chart", "figure"),
        dash.Output("volume-chart", "figure"),
        dash.Output("rsi-chart", "figure"),
    ],
    [dash.Input("coin-selector", "value")],
)
def update_charts(selected_coin):
    df_filtered = df[df["coin_name"] == selected_coin]

    fig_price = px.line(
        df_filtered, x="date", y="price", title="Price (USD)", markers=True
    )
    fig_price.update_traces(line=dict(color="blue"))

    fig_market_cap = px.line(
        df_filtered, x="date", y="market_cap", title="Market Cap (USD)", markers=True
    )
    fig_market_cap.update_traces(line=dict(color="red"))

    fig_volume = px.line(
        df_filtered, x="date", y="volume", title="Volume (USD)", markers=True
    )
    fig_volume.update_traces(line=dict(color="green"))

    fig_rsi = px.line(
        df_filtered, x="date", y="RSI", title="RSI Indicator", markers=True
    )
    fig_rsi.update_traces(line=dict(color="purple"))
    fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")  # Overbought level
    fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")  # Oversold level

    return fig_price, fig_market_cap, fig_volume, fig_rsi


if __name__ == "__main__":
    app.run_server(debug=True)
