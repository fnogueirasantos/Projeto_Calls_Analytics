from h2o_wave import  ui, Q, app, main, data
import pandas as pd
import data_operator as do
from plotly import io as pio
import plotly.express as px
import numpy as np
from common import global_nav

async def build_page01(q: Q):  
    q.page['meta'] = ui.meta_card(box='', layouts=[
        ui.layout(
            #breakpoint='xs',
            #min_width='800px',
            zones=[
                ui.zone('header', size='65px'),
                ui.zone('title',direction=ui.ZoneDirection.ROW, size='0%'),
                ui.zone('body', size='1200px', zones=[
                    ui.zone('top', direction=ui.ZoneDirection.ROW, size='35%'),
                    ui.zone('middle', direction=ui.ZoneDirection.ROW, size='35%'),
                    ui.zone('bottom', direction=ui.ZoneDirection.ROW, size='20%'),
                ]),
                ui.zone('footer', size='80px'),
            ]
        )      
    ], 
    theme='oceanic'
    )

    q.page['header'] = ui.header_card(
        box = 'header',
        title = 'Web App - Dashboard / Support Calls Analysis',
	    subtitle = 'Enterprise: 2WP ERP, version 1.0',
	    icon = 'ExploreData',
        nav=global_nav
    )


    if not q.client.initialized:
        q.client.filtro = 'Team'
        q.client.initialized = True
 
    elif (q.args.filtro is not None):
        q.client.filtro = q.args.filtro 
    else:
        q.client.filtro = 'Team'

    df = aggregated_data(q)
    df['% of Totally'] = round(100 * df['Call_Id_count'] / df['Call_Id_count'].sum(),2)
    df['% of Totally']  = df['% of Totally'] .astype('string')
    df['% of Totally']  = df['% of Totally']  + '%'
    df.rename(columns={'Call_Id_count':'Quantity'}, inplace=True)
    # Barplot  
    q.page['bar_plot'] = ui.plot_card(box=ui.box('top', order=3, width='700px'),
											    title = f'Totally Call By {q.client.filtro}',
											    data = data(fields = df.columns.tolist(), rows = df.values.tolist()),
											    plot = ui.plot(
                                                marks = [ui.mark(type = 'interval',
														x = f'={q.client.filtro}',
														y = '=Quantity',                                                     
														#color = f'={q.client.filtro}'
                                                        )],
             )
    )
    
    # Prepara dados
    df = do.importa_dados()
    df_filtro_plot = df.groupby(['Call_Date',q.client.filtro,'Month','Year']).sum(['Call_Id_count']).sort_values(by='Call_Date')
    df_filtro_plot = df_filtro_plot.reset_index()
    mapdata = {1:'01',2:'02',3:'03',4:'04',5:'05',6:'06',7:'07',8:'08',9:'09',10:'10',11:'11',12:'12'}
    df_filtro_plot['Month'] = df_filtro_plot['Month'].map(mapdata)
    df_filtro_plot['Mes_Ano'] =  df_filtro_plot['Month']  + '/' + df_filtro_plot['Year'].astype("string")
    df_filtro_plot['Mes_Ano'] = pd.to_datetime(df_filtro_plot['Mes_Ano'], format='%m/%Y')
    df_filtro_plot = df_filtro_plot.groupby(['Mes_Ano',q.client.filtro,'Month']).sum(['Call_Id_count']).sort_values(by='Mes_Ano')
    df_filtro_plot = df_filtro_plot.reset_index()
    df_filtro_plot = df_filtro_plot[[q.client.filtro,'Mes_Ano','Call_Id_count']]
    # Grafico de linhas
    fig = px.line(df_filtro_plot, x="Mes_Ano", y="Call_Id_count", color=f'{q.client.filtro}',
               markers=True)
    fig.update_layout(
        titlefont = {'family': 'Arial',
                                    'size': 22,
                                    'color': '#7f7f7f'},
        title=f'Calls For Months -  by {q.client.filtro}',
                    yaxis={'title':''},
                    xaxis={'title': ''},
                    paper_bgcolor = 'rgb(243, 243, 243)',
                    plot_bgcolor = 'rgb(243, 243, 243)'
    )
        
    config = {
        'scrollZoom': True,
        'showLink': False,
        'displayModeBar': False
    }

    html = pio.to_html(fig, validate=False, include_plotlyjs='cdn', config=config)
    q.page['plot_line'] = ui.frame_card(box=ui.box('top', order=4, width='900px'), title='', content=html)

    # Combobox
    q.page['combo_box'] = ui.form_card(box=ui.box('top', order=2,width='200px'), items=[
        ui.dropdown( 
            name='filtro', 
            label=' Select Variable',
            choices=[
                ui.choice(name='Team', label='Team'),
                ui.choice(name='Category', label='Category'),
                ui.choice(name='Module', label='Module'),
                ui.choice(name='Channel_Origin', label='Channel'),
                ui.choice(name='Day_week', label='Day Week'), 
            ],
            trigger=True,
            value=q.client.filtro
        ),
    ])

    df = aggregated_data(q)
    valor_card = df['Call_Id_count'].sum()
    df_media = media_por_dia()
    media = int(round(df_media['Call_Id_count'].mean(),0))
    median = int(round(df_media['Call_Id_count'].median(),0))
    df_media['media_movel7'] = df_media['Call_Id_count'].rolling(7).mean()
    df_media['media_movel7'] = df_media['media_movel7'].replace(np.nan,0)
    media_movel7d = df_media.tail(1)
    media_movel7d = int(media_movel7d['media_movel7'].sum())

    df_media['media_movel30'] = df_media['Call_Id_count'].rolling(30).mean()
    df_media['media_movel30'] = df_media['media_movel30'].replace(np.nan,0)
    media_movel30d = df_media.tail(1)
    media_movel30d = int(media_movel30d['media_movel30'].sum())

    df_media['media_movel90'] = df_media['Call_Id_count'].rolling(90).mean()
    df_media['media_movel90'] = df_media['media_movel90'].replace(np.nan,0)
    media_movel90d = df_media.tail(1)
    media_movel90d = int(media_movel90d['media_movel90'].sum())

    # Card Resumo
    q.page['card_resumo'] = ui.tall_stats_card(
        box=ui.box('top', order=1, width='200px'),
        items=[
            ui.stat(label='Tottaly Number of Calls', value=f'{valor_card}'),
            ui.stat(label='Average Call For Day', value=f'{media}'),
            ui.stat(label='Median Call For Day',  value=f'{median}'),
            ui.stat(label='Movel Average 7 Days', value=f'{media_movel7d}'),
            ui.stat(label='Movel Average 30 Days', value=f'{media_movel30d}'),
            ui.stat(label='Movel Average 90 Days',  value=f'{media_movel90d}')
        ]
    )

    df = do.dados_boxplot()
    df = df.reset_index()
    df = df[[q.client.filtro,'Wait_Time_sum']]
    df = do.trata_outliers_tme(df, 'Wait_Time_sum')
    lista = list(df[q.client.filtro].unique())
    df_final = []
    for x in lista:
        df_prep = round(df[(df[q.client.filtro]==x)].describe().T,2)
        df_prep[q.client.filtro] = f'{x}'
        df_final.append(df_prep)
    df_final = pd.concat(df_final).reset_index()
    df_final.dropna(inplace=True)
    df_final.drop(columns=['index'],inplace=True)
    df_final.drop_duplicates(inplace=True)
    label = {'count':'Quantity', 'mean':'Average', 'std':'std', 'min':'low', 
             '25%':'q1', '50%':'q2', '75%':'q3', 'max':'high'}
    df_final.rename(columns=label, inplace=True)
    #Boxplot 1
    q.page['box_plot1'] = ui.plot_card(
        box=ui.box('middle', order=1, width='600px'),
        title=f'Box plot Time of Wait - By {q.client.filtro}',
        data=data(fields = df_final.columns.tolist(), rows = df_final.values.tolist()),
        plot=ui.plot([ui.mark(
            type='schema',
            x=f'={q.client.filtro}',
            y1='=low',  # min
            y_q1='=q1',  # lower quartile
            y_q2='=q2',  # median
            y_q3='=q3',  # upper quartile
            y2='=high',  # max
            #color = f'{q.client.filtro}'
        )])
    )

    df = do.dados_boxplot()
    df = df.reset_index()
    df = df[[q.client.filtro,'Time_Resolution_sum']]
    df = do.trata_outliers_tme(df, 'Time_Resolution_sum')
    lista = list(df[q.client.filtro].unique())
    df_final = []
    for x in lista:
        df_prep = round(df[(df[q.client.filtro]==x)].describe().T,2)
        df_prep[q.client.filtro] = f'{x}'
        df_final.append(df_prep)
    df_final = pd.concat(df_final).reset_index()
    df_final.dropna(inplace=True)
    df_final.drop(columns=['index'],inplace=True)
    df_final.drop_duplicates(inplace=True)
    label = {'count':'Quantity', 'mean':'Média', 'std':'std', 'min':'low', 
             '25%':'q1', '50%':'q2', '75%':'q3', 'max':'high'}
    df_final.rename(columns=label, inplace=True)
    #Boxplot 2
    q.page['box_plot2'] = ui.plot_card(
        box=ui.box('middle', order=2, width='600px'),
        title=f'Box plot Time of Resolution - By {q.client.filtro}',
        data=data(fields = df_final.columns.tolist(), rows = df_final.values.tolist()),
        plot=ui.plot([ui.mark(
            type='schema',
            x=f'={q.client.filtro}',
            y1='=low',  # min
            y_q1='=q1',  # lower quartile
            y_q2='=q2',  # median
            y_q3='=q3',  # upper quartile
            y2='=high',  # max
            #color = f'={q.client.filtro}'
        )])
    )

    df = do.dados_stack_bar()
    df = df.groupby([q.client.filtro,'Priority']).count()
    df = df[['Call_Id']].reset_index()
    df = df.groupby([q.client.filtro,'Priority']).sum().reset_index()
    df.rename(columns={'Call_Id':'Calls'}, inplace=True)
    # Stackbar
    q.page.add('stack_plot', ui.plot_card(
    box=ui.box('middle', order=3 ),
    title=f'Calls Priority By {q.client.filtro}',
    data=data(fields = df.columns.tolist(), rows = df.values.tolist()),
    plot=ui.plot([ui.mark(type='interval', y='=Priority', x='=Calls', 
                          color=f'={q.client.filtro}',stack='auto', x_min=0)])
))

    await q.page.save()

def aggregated_data(q):
    df = do.importa_dados()
    df = df.groupby(f'{q.client.filtro}').sum(['Call_Id_count'])
    df = df['Call_Id_count']
    df = df.reset_index()
    return df

def media_por_dia():
    df = do.importa_dados()
    df = df.groupby(['Call_Date']).sum()
    df = df['Call_Id_count']
    df = df.reset_index()
    return df