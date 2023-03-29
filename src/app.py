import pathlib
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

app = Dash(__name__)
server = app.server

def load_data(data_file: str) -> pd.DataFrame:
    '''
    Load data from /data directory
    '''
    PATH = pathlib.Path(__file__).parent
    DATA_PATH = PATH.joinpath("data").resolve()
    return pd.read_csv(DATA_PATH.joinpath(data_file))


data = load_data("data-out.csv")

# data = pd.read_csv("data/data-out.csv")
# g_city = data.groupby("City")
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
# cities = [city for city,df in data.groupby("City")]
# app = Dash(__name__)



  # spm = sales per month



app.layout = html.Div(children=[
                                html.H1("Sales Report", style={"textAlign": "left"
                                                                 }),
                                # html.H2("The following plot shows the sales over the year for the selected city.",
                                #        style={"fontsize":"5"}),
                                dcc.Dropdown(
                                    id="spm-dropdown",
                                    options=[{"label": city,"value":city} for city in data["City"].unique()],
                                    placeholder = "Select a city ...",
                                    value = data["City"].iloc[0],
                                    style={"width": "40%"}
                                ),

                                dcc.Graph(id="fig_spm", style={"width":"50%"
                                                                  }),
                                dcc.Graph(id="fig_spp", style={"width": "50%"
                                                               }),
                                dcc.Graph(id="fig_sph", style={"width": "50%"
                                                               ,'position': 'absolute', 'top': 116, 'right': 0}),
                                # dcc.Graph(id="empty",  style={"width": "50%"}),
                                html.Div([html.Div([
                                html.H2(id = "sum_sales"),
                                html.H2(id = "sum_orders")
                                ])], style={'position': 'absolute', 'top': 650, 'right': 200}),


                               # dcc.Graph(id="fig_spp", style={"width": "40%", "justify-content": "right"}),
                               #
                                # dcc.Dropdown(
                                #     # {"label":[month for month in months],"value":[month for month in data["Month"].sort_values(ascending=True).unique()]},
                                #     # options= [{"label":month,"value":month} for month in months and data["Month"].sort_values(ascending=True).unique()],
                                #     options = [{"label":i,"value":i} for i in data["Month"].sort_values(ascending=True).unique()],
                                #     # options=("label":months, "value":month) for months in months for month in data["Month"].sort_values(ascending=True).unique(),
                                #     id="spa-dropdown",
                                #     value=data["Month"].iloc[0],
                                #     placeholder= "Select a month ...",
                                #     style={"width": "35%", "position":"absolute", "top": 255 , "right": 350}
                                # ),
                                # dcc.Graph(id="fig_spa", style={"width":"40%","position":"absolute", "top": 565 , "right": 250}),
                               ],
)

@app.callback(Output("fig_spm", "figure"),
              Input("spm-dropdown", "value")
              )
def update_spm(city):
    # data = load_data("data-out.csv")
    data_filtered = data[data["City"] == city]
    monthly_sales = data_filtered.groupby("Month").sum()["Sales"]
    fig_spm = go.Figure(go.Bar(x = months, y = monthly_sales.values))
    fig_spm.update_xaxes(title_text="Month", title_font={"size": 25}, tickfont={"size": 15})
    fig_spm.update_yaxes(title_text="Sum of Sales", tickfont={"size": 15}, title_font={"size": 25})
    fig_spm.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="LightSteelBlue",
    )
    # fig_spm = {
    #     "data":[{"x":months, "y": monthly_sales.values, "type": "bar"}],
    #     "layout" : {"title" : f"Monthly Sales in{city}"}
    # }
    sum_sales = sum(data_filtered["Sales"])
    return fig_spm


@app.callback(Output("fig_spp", "figure"),
              Input("spm-dropdown", "value")
              )
def update_spp(city):
    # data = load_data("data-out.csv")
    data_filtered = data[data["City"] == city]
    sales_pp = data_filtered.groupby("Product").sum()["Sales"]
    fig_spp = go.Figure(go.Bar(x = sales_pp.index, y = sales_pp.values))
    fig_spp.update_xaxes(title_text = "Product", title_font= {"size":25}, tickfont = {"size":13}, tickangle = 45)
    fig_spp.update_yaxes(title_text = "Sum of Sales",tickfont = {"size":15} , title_font= {"size":25})
    fig_spp.update_layout(margin = dict(l = 20, r = 20, t = 20, b = 20), paper_bgcolor = "LightSteelBlue")
    # fig_spp = {
    #     "data":[{"x":sales_pp.index, "y": sales_pp.values, "type": "bar"}],
    #     "layout" : {"title" : f"Yearly Sales per product in{city}"}
    # }
    return fig_spp


@app.callback(Output("fig_sph", "figure"),
              Input("spm-dropdown", "value")
              )
def update_spp(city):
    # data = load_data("data-out.csv")
    data_filtered = data[data["City"] == city]
    sales_ph = data_filtered.groupby("Hour").sum()["Sales"]
    fig_sph = go.Figure(go.Scatter(x = sales_ph.index, y = sales_ph.values, mode="lines+markers"))
    fig_sph.update_xaxes(type='linear', tickfont = {"size": 20}, dtick = 2, title_text = "Time of the day", title_font = {"size": 25})
    fig_sph.update_yaxes(type='linear', tickfont = {"size": 20}, title_text = "Sum of Sales", title_font = {"size": 25})
    fig_sph.update_layout(margin = dict(l = 20, r = 20, t= 20, b = 20), paper_bgcolor = "LightSteelBlue")


    # fig_sph = {
    #     "data":[{"x":sales_ph.index, "y": sales_ph.values, "type": "scatter" }],
    #     "layout" : {"title" : f"Hourly Sales in{city}"}
    # }
    return fig_sph


@app.callback(Output("sum_sales", "children" ),
              Input("spm-dropdown", "value"))
def get_sum_sales(city):
    # data = load_data("data-out.csv")

    data_filtered = data[data["City"] == city]
    monthly_sales = data_filtered.groupby("Month").sum()["Sales"]
    sum_sales = data_filtered["Sales"].sum()
    return f"Sales in 2019 in {city}: ${sum_sales:,.2f}"
@app.callback(Output("sum_orders", "children"),
              Input("spm-dropdown", "value"))
def get_sum_orders(city):
    data = load_data("data-out.csv")

    df = data[data["City"] == city]
    sum_orders = df["Quantity Ordered"].sum()
    return f"Number of orders in 2019 in {city}: {sum_orders:,.2f}"

# app.layout(html.Div(html.H1("This should be a second part")))

# @app.callback(Output("fig_spa", "figure"),
#               Input("spa-dropdown", "value"))
# def update_spa(month):
#     filtered_data = data[data["Month"] == month]
#     # filtered_data = filtered_data.sort_values(ascending=True)
#     sales_per_city = filtered_data.groupby("City").sum()["Sales"]
#     fig_spa = {
#         "data": [{"x": cities, "y": sales_per_city.values, "type":"bar"}],
#         "layout": {"title": f"Sales per city in {month}"}
#     }
#     return fig_spa

if __name__ == "__main__":
    app.run_server(debug = True)

