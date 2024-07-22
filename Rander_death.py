# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 22:42:57 2024

@author: Jeanne
"""
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from Functions import determine_season

# 1. Data imports & data processing
url = "https://raw.githubusercontent.com/bessje17/Render_app/main/daily_death.csv"
data = pd.read_csv(url, index_col=0, dtype={'tranche_age': str, 'age_deces':
                                            int}, parse_dates=['date_mort'])
data['Saison'] = data.date_mort.dt.month.apply(determine_season)

# 2. Dash layout
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    html.H1("Visualisation des décès quotidiens toutes causes"),
    dcc.DatePickerRange(
        id='date-range',
        start_date=data['date_mort'].min(),
        end_date=data['date_mort'].max(),
        display_format='YYYY-MM-DD'
    ),
    dcc.Checklist(
        id='sexe-selector',
        options=[
            {'label': 'Homme', 'value': 1},
            {'label': 'Femme', 'value': 2},
            {'label': 'Total', 'value': 0}
        ],
        value=[0],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Checklist(
        id='age-group-selector',
        options=[
            {'label': '0-24', 'value': '0-24'},
            {'label': '25-49', 'value': '25/49'},
            {'label': '50-64', 'value': '50-64'},
            {'label': '65+', 'value': '+65'},
            {'label': 'Toutes tranches d\'âges', 'value': 'All'}
        ],
        value=['All'],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='deces-graph')
])

@app.callback(
    Output('deces-graph', 'figure'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('sexe-selector', 'value'),
    Input('age-group-selector', 'value')
)
def update_graph(start_date, end_date, sexe_values, age_group_values):
    # 1. Filtrer les data en fonction de la plage de dates
    df_sub_data = data[(data['date_mort'] >= start_date) & (data['date_mort']
                                                            <= end_date)]

    fig = go.Figure()

    if 'All' in age_group_values:
        if 0 in sexe_values:
            df_sub_data_total = df_sub_data.groupby('date_mort',
                                                    as_index=False)[
                                                        'nombre_deces'].sum()
            fig.add_trace(go.Scatter(
                x=df_sub_data_total['date_mort'],
                y=df_sub_data_total['nombre_deces'],
                mode='lines',
                name='Total (Toutes tranches d\'âges)'
            ))

        if 1 in sexe_values:
            df_sub_data_homme = df_sub_data[df_sub_data['sexe'] == 1].groupby(
                'date_mort', as_index=False)['nombre_deces'].sum()
            fig.add_trace(go.Scatter(
                x=df_sub_data_homme['date_mort'],
                y=df_sub_data_homme['nombre_deces'],
                mode='lines',
                name='Homme (Toutes tranches d\'âges)'
            ))

        if 2 in sexe_values:
            df_sub_data_femme = df_sub_data[df_sub_data['sexe'] == 2].groupby(
                'date_mort', as_index=False)['nombre_deces'].sum()
            fig.add_trace(go.Scatter(
                x=df_sub_data_femme['date_mort'],
                y=df_sub_data_femme['nombre_deces'],
                mode='lines',
                name='Femme (Toutes tranches d\'âges)'
            ))

    for age_group in age_group_values:
        if age_group == 'All':
            continue

        if 0 in sexe_values:
            df_sub_data_total = df_sub_data[df_sub_data['tranche_age'] ==
                                            age_group].groupby('date_mort',
                                                               as_index=False
                                                               )['nombre_deces'
                                                                 ].sum()
            fig.add_trace(go.Scatter(
                x=df_sub_data_total['date_mort'],
                y=df_sub_data_total['nombre_deces'],
                mode='lines',
                name=f'Total ({age_group})'
            ))

        if 1 in sexe_values:
            df_sub_data_homme = df_sub_data[(df_sub_data['sexe'] == 1) & (
                df_sub_data['tranche_age'] == age_group)].groupby(
                    'date_mort', as_index=False)['nombre_deces'].sum()
            fig.add_trace(go.Scatter(
                x=df_sub_data_homme['date_mort'],
                y=df_sub_data_homme['nombre_deces'],
                mode='lines',
                name=f'Homme ({age_group})'
            ))

        if 2 in sexe_values:
            df_sub_data_femme = df_sub_data[(df_sub_data['sexe'] == 2) & (
                df_sub_data['tranche_age'] == age_group)].groupby(
                    'date_mort', as_index=False)['nombre_deces'].sum()
            fig.add_trace(go.Scatter(
                x=df_sub_data_femme['date_mort'],
                y=df_sub_data_femme['nombre_deces'],
                mode='lines',
                name=f'Femme ({age_group})'
            ))

    fig.update_layout(title='Nombre de décès par date', xaxis_title='Date',
                      yaxis_title='Nombre quotidien de décès')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
