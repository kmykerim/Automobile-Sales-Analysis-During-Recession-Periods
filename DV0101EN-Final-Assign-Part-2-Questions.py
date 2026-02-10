#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv"
)

# Initialize the Dash app
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# Dropdown options
dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]

# List of years
year_list = [i for i in range(1980, 2024, 1)]

# ---------------------------------------------------------------------------------------
# Layout
app.layout = html.Div(
    [
        # TASK 2.1
        html.H1(
            "Automobile Sales Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 24},
        ),

        # TASK 2.2 - Dropdowns
        html.Div(
            [
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    value="Select Statistics",
                    placeholder="Select a report type",
                    style={
                        "width": "80%",
                        "padding": "3px",
                        "fontSize": "20px",
                        "textAlignLast": "center",
                    },
                ),
            ]
        ),

        html.Div(
            dcc.Dropdown(
                id="select-year",
                options=[{"label": i, "value": i} for i in year_list],
                value="Select-year",
                placeholder="Select-year",
            )
        ),

        # TASK 2.3 output container (must be id='output-container', className='chart-grid', display flex)
        html.Div(
            [
                html.Div(
                    id="output-container",
                    className="chart-grid",
                    style={"display": "flex"},
                )
            ]
        ),
    ]
)

# ---------------------------------------------------------------------------------------
# TASK 2.4: Callback to enable/disable year dropdown
@app.callback(
    Output(component_id="select-year", component_property="disabled"),
    Input(component_id="dropdown-statistics", component_property="value"),
)
def update_input_container(selected_statistics):
    # Enable year dropdown only for Yearly Statistics
    if selected_statistics == "Yearly Statistics":
        return False
    return True

# ---------------------------------------------------------------------------------------
# TASK 2.5 + TASK 2.6: Callback to update output container
@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="dropdown-statistics", component_property="value"),
        Input(component_id="select-year", component_property="value"),
    ],
)
def update_output_container(selected_statistics, input_year):

    # ----------- Recession Period Statistics -----------
    if selected_statistics == "Recession Period Statistics":
        recession_data = data[data["Recession"] == 1]

        # Plot 1: Year-wise avg automobile sales during recession
        yearly_rec = recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Automobile Sales Fluctuation Over Recession Period (Year-wise)",
            )
        )

        # Plot 2: Avg sales by vehicle type during recession (bar)
        average_sales = recession_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Automobile Sales by Vehicle Type During Recession",
            )
        )

        # Plot 3: Total advertising expenditure share by vehicle type (pie)
        exp_rec = recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertising Expenditure Share by Vehicle Type (Recession)",
            )
        )

        # Plot 4: Effect of unemployment on sales by vehicle type (bar)
        unemp_data = (
            recession_data.groupby(["unemployment_rate", "Vehicle_Type"])["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                labels={
                    "unemployment_rate": "Unemployment Rate",
                    "Automobile_Sales": "Average Automobile Sales",
                },
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                style={"display": "flex"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                style={"display": "flex"},
            ),
        ]

    # ----------- Yearly Statistics -----------
    elif (input_year and selected_statistics == "Yearly Statistics" and isinstance(input_year, int)):
        yearly_data = data[data["Year"] == input_year]

        # Plot 1: Yearly avg automobile sales (whole period)
        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x="Year",
                y="Automobile_Sales",
                title="Yearly Automobile Sales",
            )
        )

        # Plot 2: Total monthly automobile sales (whole period)
        mas = data.groupby("Month")["Automobile_Sales"].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x="Month",
                y="Automobile_Sales",
                title="Total Monthly Automobile Sales",
            )
        )

        # Plot 3: Avg vehicles sold by vehicle type in selected year
        avr_vdata = yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type in the year {}".format(input_year),
            )
        )

        # Plot 4: Total ad expenditure by vehicle type in selected year (pie)
        exp_data = yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertisment Expenditure for Each Vehicle",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                style={"display": "flex"},
            ),
            html.Div(
                className="chart-item",
                children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                style={"display": "flex"},
            ),
        ]

    # Default (nothing selected yet)
    return []


# Run the Dash app
if __name__ == "__main__":
    app.run(debug=True)