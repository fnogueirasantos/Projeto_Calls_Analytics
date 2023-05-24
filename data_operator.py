import pandas as pd
from datetime import date
import numpy as np
import pandas as pd
from prophet import Prophet
import datetime


def importa_dados():
    df = pd.read_csv("dados.csv", encoding='utf-8', sep=';')
    df = df.query('Year >= 2021')
    df = df.groupby(['Call_Date','Team','Category', 'Module', 'Channel_Origin', 'Day_week','Month','Year']).agg({'Call_Id' : ['count'],
        'Wait_Time' : ['mean'],'Time_Resolution' : ['mean']},axis=1)
    df.columns = [
    '_'.join(col).rstrip('_') for col in df.columns.values
    ]
    df = df.reset_index()

    return(df)


def dados_boxplot():
    df = pd.read_csv("dados.csv", encoding='utf-8', sep=';')
    df = df.query('Year >= 2019')
    df = df.groupby(['Call_Date','Team','Category', 'Module', 'Channel_Origin', 'Day_week','Month','Year']).agg({'Call_Id' : ['count'],
        'Wait_Time' : ['sum'],'Time_Resolution' : ['sum']},axis=1)
    df.columns = [
    '_'.join(col).rstrip('_') for col in df.columns.values
    ]
    df = df.reset_index()

    return(df)

def trata_outliers_tme(df, variavel): #deve ser passado uma coluna ou uma lista de colunas
    Q1, Q3 = df[f'{variavel}'].quantile(0.25), df[f'{variavel}'].quantile(0.75)
    IQR = Q3 - Q1
    cut_off = IQR * 1.5
    lower, upper = Q1 - cut_off, Q3 + cut_off
    df[f'{variavel}'] = np.where(df[f'{variavel}'] > upper, upper, df[f'{variavel}'])
    df[f'{variavel}'] = np.where(df[f'{variavel}'] < lower, lower, df[f'{variavel}'])
    return(df)

def dados_stack_bar():
    df = pd.read_csv("dados.csv", encoding='utf-8', sep=';')
    df = df.query('Year >= 2019')
    df = df.reset_index()
    return(df)

def importa_dados_pag2():
    df = pd.read_csv("dados.csv", encoding='utf-8', sep=';')
    df = df.query('Year >= 2019')
    return(df)

def forecast_pag3():
    df = pd.read_csv("dados.csv", encoding='utf-8', sep=';')
    df = df.query('Year >= 2019')
    dfprep = df.groupby(['Call_Date'])['Call_Id'].agg('count').reset_index()
    dfprep['Call_Date'] = pd.to_datetime(dfprep['Call_Date'])
    dfprep = dfprep.sort_values(by='Call_Date',ascending=True)
    df_treino = dfprep.rename(columns = {"Call_Date": "ds", "Call_Id": "y"})
    modelo = Prophet()
    modelo.fit(df_treino)
    periodo = 400
    futuro = modelo.make_future_dataframe(periods = periodo)
    forecast = modelo.predict(futuro)
    df_forecast = forecast[['ds','yhat']]
    df_forecast.rename(columns={'ds':'Date_Forecast','yhat':'Number_Calls'}, inplace=True)
    df_forecast['Date_Forecast'] = pd.to_datetime(df_forecast['Date_Forecast'])
    df_forecast['Need_Workers'] = round(df_forecast['Number_Calls'] / 12,0).astype('int64')
    df_forecast['Number_Calls'] = round(df_forecast['Number_Calls'],0).astype('int64')
    df_forecast['Year'] = df_forecast['Date_Forecast'].dt.year
    df_forecast = df_forecast.query('Year == 2023')
    df_forecast['Month'] = df_forecast['Date_Forecast'].dt.month
    df_forecast['Day'] = df_forecast['Date_Forecast'].dt.day
    mapdata = {1:'Janeiro',2:'Fevereiro',3:'Março',4:'Abril',5:'Maio',6:'Junho',7:'Julho',8:'Agosto',
            9:'Setembro',10:'Outubro',11:'Novembro',12:'Dezembro'}
    df_forecast['Month'] = df_forecast['Month'].map(mapdata)
    df_final = df_forecast.groupby(['Month','Day']).sum()[['Number_Calls','Need_Workers']]
    df_final['Team01-Number_Calls'] = round(df_final['Number_Calls']*0.38,0).astype('int64')
    df_final['Team01-Need_Workers'] = round(df_final['Need_Workers']*0.38,0).astype('int64')
    df_final['Team02-Number_Calls'] = round(df_final['Number_Calls']*0.25,0).astype('int64')
    df_final['Team02-Need_Workers'] = round(df_final['Need_Workers']*0.25,0).astype('int64')
    df_final['Team03-Number_Calls'] = round(df_final['Number_Calls']*0.17,0).astype('int64')
    df_final['Team03-Need_Workers'] = round(df_final['Need_Workers']*0.17,0).astype('int64')
    df_final['Team04-Number_Calls'] = round(df_final['Number_Calls']-df_final['Team03-Number_Calls']-df_final['Team02-Number_Calls']-df_final['Team01-Number_Calls'],0).astype('int64')
    df_final['Team04-Need_Workers'] = round(df_final['Need_Workers']-df_final['Team03-Need_Workers']-df_final['Team02-Need_Workers']-df_final['Team01-Need_Workers'],0).astype('int64')
    df_final = df_final.reset_index()
    return(df_final)
