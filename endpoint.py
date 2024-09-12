# -*- coding: utf-8 -*-
"""endpoint.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1n5CxQEa96kFDZ9VN1Iao-XybIAy2dyie
"""

# import requests

# def fetch_all_data(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             print(f"Error: {response.status_code}, Detail: {response.json()['detail']}")
#     except requests.RequestException as e:
#         print(f"Failed to make the request: {e}")

# # URL do endpoint
# url = "https://web-production-c353.up.railway.app/retrieve_all"

# # Chamando a função
# all_data = fetch_all_data(url)
# print(all_data)

# # prompt: transforme um json em uma tabela, o nome do jso é all_data

# import pandas as pd

# df = pd.DataFrame(all_data)
# display(df)

# df.dtypes

# # prompt: transforme esse df em um excel

# df.to_excel('dados.xlsx', index=False)

# # @title FLAG_NEGATIVACAO_JORNADA

# from matplotlib import pyplot as plt
# import seaborn as sns
# df.groupby('FLAG_NEGATIVACAO_JORNADA').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
# plt.gca().spines[['top', 'right',]].set_visible(False)

# # @title FLAG_VOO_JORNADA

# from matplotlib import pyplot as plt
# import seaborn as sns
# df.groupby('FLAG_VOO_JORNADA').size().plot(kind='barh', color=sns.palettes.mpl_palette('Dark2'))
# plt.gca().spines[['top', 'right',]].set_visible(False)

# all_data[-1].get('RAW_DATA')

#!pip install dash dash_bootstrap_components

#pip install flask

# from flask import Flask
# import dash
# from dash import dcc, html, Input, Output
# import dash_bootstrap_components as dbc
# import plotly.express as px
# import pandas as pd
# import requests
# from datetime import datetime, timedelta

# # Configuração do servidor Flask
# server = Flask(__name__)

# # Inicializar o app Dash com o servidor Flask
# app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])


# # Função para buscar todos os dados do endpoint
# def fetch_all_data(url):
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             return pd.DataFrame(data)  # Converte os dados em um DataFrame
#         else:
#             print(f"Error: {response.status_code}, Detail: {response.json().get('detail', 'No detail provided')}")
#     except requests.RequestException as e:
#         print(f"Failed to make the request: {e}")
#         return pd.DataFrame()

# # URL do endpoint
# url = "https://web-production-c353.up.railway.app/retrieve_all"

# # Chamando a função e obtendo os dados

# all_data = fetch_all_data(url)
# df = pd.DataFrame(all_data)


# # Verificação básica dos dados
# if df.empty:
#     print("Os dados não foram carregados corretamente. Verifique o endpoint ou o formato dos dados.")
#     exit()

# # Função para calcular o tempo em cada etapa com base nas colunas de timestamp
# def calculate_stage_duration(row):
#     created_at = pd.to_datetime(row['created_at'], errors='coerce')
#     last_modified = pd.to_datetime(row['last_modified'], errors='coerce')
#     if pd.isnull(created_at) or pd.isnull(last_modified):
#         return 0  # Retorna 0 se houver erro de conversão
#     duration = (last_modified - created_at).total_seconds() / 60  # Duração em minutos
#     return duration

# # Função para extrair a última etapa (flag) alcançada na jornada
# def extract_final_stage(raw_data):
#     try:
#         flags = {
#             'voo': int(raw_data.get('FLAG_VOO_JORNADA', 0)),
#             'negativacao': int(raw_data.get('FLAG_NEGATIVACAO_JORNADA', 0)),
#             'telefonia': int(raw_data.get('FLAG_SERV_TELEF_JORNADA', 0)),
#             'bancario': int(raw_data.get('FLAG_SERV_BANCARIO_JORNADA', 0)),
#             'compra_online': int(raw_data.get('FLAG_COMPRA_ONLINE_JORNADA', 0)),
#             'outros': int(raw_data.get('FLAG_OUTROS_JORNADA', 0)),
#             'hospedagem': int(raw_data.get('FLAG_HOSPEDAGEM_JORNADA', 0))
#         }
#         final_stage = max(flags.values())  # Encontra a maior flag para determinar a etapa final
#         return final_stage
#     except Exception as e:
#         print(f"Erro ao extrair etapa final: {e}")
#         return 0

# # Aplicar as funções ao dataframe
# df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
# df['Tempo_na_Etapa'] = df.apply(calculate_stage_duration, axis=1)
# df['Etapa_Final'] = df['RAW_DATA'].apply(extract_final_stage)

# # Remover outliers com base no percentil para todos os problemas
# q_low = df['Tempo_na_Etapa'].quantile(0.01)  # Percentil inferior
# q_high = df['Tempo_na_Etapa'].quantile(0.99)  # Percentil superior
# df_filtered = df[(df['Tempo_na_Etapa'] >= q_low) & (df['Tempo_na_Etapa'] <= q_high)]

# # Remover números de WhatsApp com tempo de etapa zero ou ausentes
# df_filtered = df_filtered[df_filtered['Tempo_na_Etapa'] > 0]

# # Inicializar o app Dash
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# # Layout do Dashboard com Dash e Bootstrap Components
# app.layout = dbc.Container([
#     dbc.Row([
#         dbc.Col([
#             html.H2("Dashboard de Leads", className="display-4"),
#             html.Hr(),
#             html.P("Selecione o tipo de problema:", className="lead"),
#             dcc.Dropdown(
#                 id='problema-dropdown',
#                 options=[{'label': problema, 'value': problema} for problema in df['PROBLEMA'].unique()],
#                 value=df['PROBLEMA'].unique()[0] if not df.empty else None,  # Valor padrão
#                 clearable=False,
#                 style={'margin-bottom': '20px'}
#             ),
#             html.P("Selecione o intervalo de datas:", className="lead"),
#             dcc.DatePickerRange(
#                 id='date-picker-range',
#                 start_date=datetime.now() - timedelta(days=30),
#                 end_date=datetime.now(),
#                 display_format='DD/MM/YYYY',
#                 style={'margin-bottom': '20px'}
#             ),
#         ], width=3, style={'background-color': '#f8f9fa'}),

#         dbc.Col([
#             html.H1("Visão Geral dos Dados", style={'textAlign': 'center'}),
#             dbc.Row([
#                 dbc.Col(dcc.Graph(id='stage-duration-graph'), width=12),
#             ]),
#             html.Div(id='leads-info', style={'textAlign': 'center', 'marginTop': 20})
#         ], width=9),
#     ])
# ], fluid=True)

# # Callbacks para atualizar os gráficos e métricas dinamicamente
# @app.callback(
#     [Output('stage-duration-graph', 'figure'),
#      Output('leads-info', 'children')],
#     [Input('problema-dropdown', 'value'),
#      Input('date-picker-range', 'start_date'),
#      Input('date-picker-range', 'end_date')]
# )
# def update_stage_duration_graph(selected_problema, start_date, end_date):
#     if selected_problema is None or df_filtered.empty:
#         fig_empty = px.scatter(title='Nenhum dado disponível')
#         return fig_empty, "Nenhum dado disponível"

#     # Filtrar o DataFrame pelo problema selecionado e pelo intervalo de datas
#     df_filtered_by_problem = df_filtered[(df_filtered['PROBLEMA'] == selected_problema) &
#                                          (df_filtered['created_at'] >= pd.to_datetime(start_date)) &
#                                          (df_filtered['created_at'] <= pd.to_datetime(end_date))]

#     # Remover outliers com base no percentil para o problema selecionado
#     if not df_filtered_by_problem.empty:
#         q_low = df_filtered_by_problem['Tempo_na_Etapa'].quantile(0.01)  # Percentil inferior
#         q_high = df_filtered_by_problem['Tempo_na_Etapa'].quantile(0.99)  # Percentil superior
#         df_filtered_by_problem = df_filtered_by_problem[(df_filtered_by_problem['Tempo_na_Etapa'] >= q_low) &
#                                                         (df_filtered_by_problem['Tempo_na_Etapa'] <= q_high)]

#     # Remover números de WhatsApp com tempo de etapa zero ou ausentes
#     df_filtered_by_problem = df_filtered_by_problem[df_filtered_by_problem['Tempo_na_Etapa'] > 0]

#     if df_filtered_by_problem.empty:
#         fig_empty = px.scatter(title='Nenhum dado disponível para o problema selecionado')
#         return fig_empty, "Nenhum dado disponível para o problema selecionado"

#     # Gráfico de barras para duração na etapa com hover informando a etapa final
#     fig = px.bar(
#         df_filtered_by_problem,
#         x='numero_wpp',
#         y='Tempo_na_Etapa',
#         title='Tempo na Etapa por Lead',
#         labels={'Tempo_na_Etapa': 'Tempo na Etapa (minutos)', 'numero_wpp': 'Número WhatsApp'},
#         hover_data={'Etapa_Final': True}  # Adiciona a etapa final ao hover
#     )

#     fig.update_traces(hovertemplate='<b>Número WhatsApp:</b> %{x}<br>' +
#                                      '<b>Tempo na Etapa:</b> %{y} minutos<br>' +
#                                      '<b>Etapa Final:</b> %{customdata[0]}')  # Customiza o texto do hover

#     # Calcular métricas de leads
#     leads_captados_total = len(df_filtered[(df_filtered['created_at'] >= pd.to_datetime(start_date)) &
#                                            (df_filtered['created_at'] <= pd.to_datetime(end_date))])
#     leads_captados = len(df_filtered_by_problem)
#     proporcao_responderam = (leads_captados / leads_captados_total) * 100 if leads_captados_total > 0 else 0

#     leads_info = [
#         html.H4(f"Leads Captados no Problema Selecionado: {leads_captados}"),
#         html.H4(f"Total de Leads Captados: {leads_captados_total}"),
#         html.H4(f"Proporção de Leads no Problema Selecionado: {proporcao_responderam:.2f}%"),
#     ]

#     return fig, leads_info

# # Rodar o app
# if __name__ == '__main__':
#     app.run_server(debug=True)

from flask import Flask
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests
from datetime import datetime, timedelta

# Configuração do servidor Flask
server = Flask(__name__)

# Inicializar o app Dash com o servidor Flask
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Função para buscar todos os dados do endpoint
def fetch_all_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return pd.DataFrame(data)  # Converte os dados em um DataFrame
        else:
            print(f"Error: {response.status_code}, Detail: {response.json().get('detail', 'No detail provided')}")
    except requests.RequestException as e:
        print(f"Failed to make the request: {e}")
        return pd.DataFrame()

# URL do endpoint
url = "https://web-production-c353.up.railway.app/retrieve_all"

# Chamando a função e obtendo os dados
df = fetch_all_data(url)

# Verificação básica dos dados
if df.empty:
    print("Os dados não foram carregados corretamente. Verifique o endpoint ou o formato dos dados.")
    exit()

# Função para calcular o tempo em cada etapa com base nas colunas de timestamp
def calculate_stage_duration(row):
    created_at = pd.to_datetime(row['created_at'], errors='coerce')
    last_modified = pd.to_datetime(row['last_modified'], errors='coerce')
    if pd.isnull(created_at) or pd.isnull(last_modified):
        return 0  # Retorna 0 se houver erro de conversão
    duration = (last_modified - created_at).total_seconds() / 60  # Duração em minutos
    return duration

# Função para extrair a última etapa (flag) alcançada na jornada
def extract_final_stage(raw_data):
    try:
        flags = {
            'voo': int(raw_data.get('FLAG_VOO_JORNADA', 0)),
            'negativacao': int(raw_data.get('FLAG_NEGATIVACAO_JORNADA', 0)),
            'telefonia': int(raw_data.get('FLAG_SERV_TELEF_JORNADA', 0)),
            'bancario': int(raw_data.get('FLAG_SERV_BANCARIO_JORNADA', 0)),
            'compra_online': int(raw_data.get('FLAG_COMPRA_ONLINE_JORNADA', 0)),
            'outros': int(raw_data.get('FLAG_OUTROS_JORNADA', 0)),
            'hospedagem': int(raw_data.get('FLAG_HOSPEDAGEM_JORNADA', 0))
        }
        final_stage = max(flags.values())  # Encontra a maior flag para determinar a etapa final
        return final_stage
    except Exception as e:
        print(f"Erro ao extrair etapa final: {e}")
        return 0

# Aplicar as funções ao dataframe
df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
df['Tempo_na_Etapa'] = df.apply(calculate_stage_duration, axis=1)
df['Etapa_Final'] = df['RAW_DATA'].apply(extract_final_stage)

# Remover outliers com base no percentil para todos os problemas
q_low = df['Tempo_na_Etapa'].quantile(0.01)  # Percentil inferior
q_high = df['Tempo_na_Etapa'].quantile(0.99)  # Percentil superior
df_filtered = df[(df['Tempo_na_Etapa'] >= q_low) & (df['Tempo_na_Etapa'] <= q_high)]

# Remover números de WhatsApp com tempo de etapa zero ou ausentes
df_filtered = df_filtered[df_filtered['Tempo_na_Etapa'] > 0]

# Layout do Dashboard com Dash e Bootstrap Components
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Dashboard de Leads", className="display-4"),
            html.Hr(),
            html.P("Selecione o tipo de problema:", className="lead"),
            dcc.Dropdown(
                id='problema-dropdown',
                options=[{'label': problema, 'value': problema} for problema in df['PROBLEMA'].unique()],
                value=df['PROBLEMA'].unique()[0] if not df.empty else None,  # Valor padrão
                clearable=False,
                style={'margin-bottom': '20px'}
            ),
            html.P("Selecione o intervalo de datas:", className="lead"),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now(),
                display_format='DD/MM/YYYY',
                style={'margin-bottom': '20px'}
            ),
        ], width=3, style={'background-color': '#f8f9fa'}),

        dbc.Col([
            html.H1("Visão Geral dos Dados", style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col(dcc.Graph(id='stage-duration-graph'), width=12),
            ]),
            html.Div(id='leads-info', style={'textAlign': 'center', 'marginTop': 20})
        ], width=9),
    ])
], fluid=True)

# Callbacks para atualizar os gráficos e métricas dinamicamente
@app.callback(
    [Output('stage-duration-graph', 'figure'),
     Output('leads-info', 'children')],
    [Input('problema-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_stage_duration_graph(selected_problema, start_date, end_date):
    if selected_problema is None or df_filtered.empty:
        fig_empty = px.scatter(title='Nenhum dado disponível')
        return fig_empty, "Nenhum dado disponível"

    # Filtrar o DataFrame pelo problema selecionado e pelo intervalo de datas
    df_filtered_by_problem = df_filtered[(df_filtered['PROBLEMA'] == selected_problema) &
                                         (df_filtered['created_at'] >= pd.to_datetime(start_date)) &
                                         (df_filtered['created_at'] <= pd.to_datetime(end_date))]

    # Remover outliers com base no percentil para o problema selecionado
    if not df_filtered_by_problem.empty:
        q_low = df_filtered_by_problem['Tempo_na_Etapa'].quantile(0.01)  # Percentil inferior
        q_high = df_filtered_by_problem['Tempo_na_Etapa'].quantile(0.99)  # Percentil superior
        df_filtered_by_problem = df_filtered_by_problem[(df_filtered_by_problem['Tempo_na_Etapa'] >= q_low) &
                                                        (df_filtered_by_problem['Tempo_na_Etapa'] <= q_high)]

    # Remover números de WhatsApp com tempo de etapa zero ou ausentes
    df_filtered_by_problem = df_filtered_by_problem[df_filtered_by_problem['Tempo_na_Etapa'] > 0]

    if df_filtered_by_problem.empty:
        fig_empty = px.scatter(title='Nenhum dado disponível para o problema selecionado')
        return fig_empty, "Nenhum dado disponível para o problema selecionado"

    # Gráfico de barras para duração na etapa com hover informando a etapa final
    fig = px.bar(
        df_filtered_by_problem,
        x='numero_wpp',
        y='Tempo_na_Etapa',
        title='Tempo na Etapa por Lead',
        labels={'Tempo_na_Etapa': 'Tempo na Etapa (minutos)', 'numero_wpp': 'Número WhatsApp'},
        hover_data={'Etapa_Final': True}  # Adiciona a etapa final ao hover
    )

    fig.update_traces(hovertemplate='<b>Número WhatsApp:</b> %{x}<br>' +
                                     '<b>Tempo na Etapa:</b> %{y} minutos<br>' +
                                     '<b>Etapa Final:</b> %{customdata[0]}')  # Customiza o texto do hover

    # Calcular métricas de leads
    leads_captados_total = len(df_filtered[(df_filtered['created_at'] >= pd.to_datetime(start_date)) &
                                           (df_filtered['created_at'] <= pd.to_datetime(end_date))])
    leads_captados = len(df_filtered_by_problem)
    proporcao_responderam = (leads_captados / leads_captados_total) * 100 if leads_captados_total > 0 else 0

    leads_info = [
        html.H4(f"Leads Captados no Problema Selecionado: {leads_captados}"),
        html.H4(f"Total de Leads Captados: {leads_captados_total}"),
        html.H4(f"Proporção de Leads no Problema Selecionado: {proporcao_responderam:.2f}%"),
    ]

    return fig, leads_info

# Rodar o servidor com Gunicorn
if __name__ == '__main__':
    app.run_server(debug=True)

