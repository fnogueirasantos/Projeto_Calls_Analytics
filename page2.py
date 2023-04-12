from h2o_wave import  ui, Q, app, main, data
import data_operator as do
import plotly.graph_objs as go
from plotly import io as pio
from plotly import tools

from common import global_nav


async def build_page02(q: Q):  
    q.page['meta'] = ui.meta_card(box='', layouts=[
        ui.layout(
            #breakpoint='xl',
            #min_width='800px',
            zones=[
                ui.zone('header', size='65px'),
                ui.zone('title',direction=ui.ZoneDirection.ROW, size='0%'),
                ui.zone('body', size='1200px', zones=[
                    ui.zone('top', direction=ui.ZoneDirection.ROW, size='12%'),
                    ui.zone('middle', direction=ui.ZoneDirection.ROW, size='30%'),
                    ui.zone('bottom', direction=ui.ZoneDirection.ROW, size='15%'),
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
        q.client.combo1 = 'All'
        q.client.combo2 = 'Call_Id'
        q.client.initialized = True
    elif (q.args.combo1 is not None) and (q.args.combo1 is not None):
        q.client.combo1 = q.args.combo1
        q.client.combo2 = q.args.combo2
    else:
        q.client.combo1 = 'All'
        q.client.combo2 = 'Call_Id'


    # Heatmap
    df = do.importa_dados_pag2()
    label={14:'14:00', 8:'08:00', 10:'10:00', 12:'12:00', 13:'13:00', 9:'09:00', 11:'11:00', 
           18:'18:00', 16:'16:00', 17:'17:00', 15:'15:00'}
    df['Hour'] = df['Hour'].map(label)
    df['Time_Resolution'] = df['Time_Resolution']/60
    df['Wait_Time'] = df['Wait_Time']/60

    if q.client.combo1 == 'All' and q.client.combo2 == 'Call_Id':
        df_filtro = df.groupby(['Call_Date','Day_week','Hour','Team'])[q.client.combo2].agg('count').reset_index()
        df_filtro = df_filtro.groupby(['Call_Date','Day_week','Hour','Team'])[q.client.combo2].agg('mean').reset_index()
        df_filtro1 = df_filtro.query('Team == "Team-01"')
        df_filtro2 = df_filtro.query('Team == "Team-02"')
        df_filtro3 = df_filtro.query('Team == "Team-03"')
        df_filtro4 = df_filtro.query('Team == "Team-04"')
    elif q.client.combo1 == 'All' and q.client.combo2 != 'Call_Id':
        df_filtro = df.groupby(['Call_Date','Day_week','Hour','Team'])[q.client.combo2].agg('mean').reset_index()
        df_filtro1 = df_filtro.query('Team == "Team-01"')
        df_filtro2 = df_filtro.query('Team == "Team-02"')
        df_filtro3 = df_filtro.query('Team == "Team-03"')
        df_filtro4 = df_filtro.query('Team == "Team-04"')
    elif q.client.combo1 != 'All' and q.client.combo2 == 'Call_Id':
        df_filtro = df.groupby(['Call_Date','Day_week','Hour','Team','Channel_Origin'])[q.client.combo2].agg('count').reset_index()
        df_filtro = df_filtro.groupby(['Call_Date','Day_week','Hour','Team','Channel_Origin'])[q.client.combo2].agg('mean').reset_index()
        df_filtro1 = df_filtro.query(f'Team == "Team-01" & Channel_Origin =="{q.client.combo1}"')
        df_filtro2 = df_filtro.query(f'Team == "Team-02" & Channel_Origin =="{q.client.combo1}"')
        df_filtro3 = df_filtro.query(f'Team == "Team-03" & Channel_Origin =="{q.client.combo1}"')
        df_filtro4 = df_filtro.query(f'Team == "Team-04" & Channel_Origin =="{q.client.combo1}"')
    else:
        df_filtro = df.groupby(['Call_Date','Day_week','Hour','Team','Channel_Origin'])[q.client.combo2].agg('mean').reset_index()
        df_filtro1 = df_filtro.query(f'Team == "Team-01" & Channel_Origin =="{q.client.combo1}"')
        df_filtro2 = df_filtro.query(f'Team == "Team-02" & Channel_Origin =="{q.client.combo1}"')
        df_filtro3 = df_filtro.query(f'Team == "Team-03" & Channel_Origin =="{q.client.combo1}"')
        df_filtro4 = df_filtro.query(f'Team == "Team-04" & Channel_Origin =="{q.client.combo1}"')

    #Grafico
    trace1 = go.Heatmap(
        x=df_filtro1['Day_week'],
        y=df_filtro1['Hour'],
        z=round(df_filtro1[q.client.combo2],0),
        colorscale='YlOrRd',
        zmin = 0, zmax = df_filtro1[q.client.combo2].mean()
    )
    trace2 = go.Heatmap(
        x=df_filtro2['Day_week'],
        y=df_filtro2['Hour'],
        z=round(df_filtro1[q.client.combo2],0),
        colorscale='YlOrRd',
        zmin = 0, zmax = df_filtro1[q.client.combo2].mean() 
    )
    trace3 = go.Heatmap(
        x=df_filtro3['Day_week'],
        y=df_filtro3['Hour'],
        z=round(df_filtro1[q.client.combo2],0),
        colorscale='YlOrRd',
        zmin = 0, zmax = df_filtro1[q.client.combo2].mean() 
    )
    trace4 = go.Heatmap(
        x=df_filtro4['Day_week'],
        y=df_filtro4['Hour'],
        z=round(df_filtro1[q.client.combo2],0),
        colorscale='YlOrRd',
        zmin = 0, zmax = df_filtro1[q.client.combo2].mean()
    )
    fig = tools.make_subplots(rows=1, cols=4,
        subplot_titles=('Team-01','Team-02','Team-03','Team-04'),
        shared_yaxes = False,
    )
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 2)
    fig.append_trace(trace3, 1, 3)
    fig.append_trace(trace4, 1, 4)

    fig['layout'].update(
        title=f'Heatmap of Avarage Calls By Channel {q.client.combo1} and aggregated BY {q.client.combo2}'
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True)
        
    config = {
        'scrollZoom': False,
        'showLink': False,
        'displayModeBar': False
    }

    html = pio.to_html(fig, validate=False, include_plotlyjs='cdn', config=config)
    q.page['heat_map'] = ui.frame_card(box=ui.box('middle', order=3, width='1800px',height='750px'), title='', content=html)

    #Combobox 1
    q.page['combo_box'] = ui.form_card(box=ui.box('top', order=1, width='250px',height='120px'), items=[
        ui.dropdown( 
            name='combo1', 
            label='Channel:',
            choices=[
                ui.choice(name='All', label='All'),
                ui.choice(name='Chat Blip', label='Chat Blip'),
                ui.choice(name='whatsapp', label='whatsapp'),
                ui.choice(name='Telefone', label='Telefone'),
                ui.choice(name='E-mail', label='E-mail'),
                ui.choice(name='Rede Social', label='Rede Social')

            ],
            trigger=True,
            value=q.client.combo1
        ),
    ])

    #Combobox 2
    q.page['combobox2'] = ui.form_card(box=ui.box('top', order=2, width='250px',height='120px'), items=[
        ui.dropdown( 
            name='combo2', 
            label='Numerical Variable:',
            choices=[
                ui.choice(name='Call_Id', label='Number of Calls'),
                ui.choice(name='Time_Resolution', label='Resolution Time (Minutes)'),
                ui.choice(name='Wait_Time', label='Wait Time (Minutes')
            ],
            trigger=True,
            value=q.client.combo2
        ),
    ])

    await q.page.save()

