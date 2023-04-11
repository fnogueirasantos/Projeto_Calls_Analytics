from h2o_wave import  ui, Q, app, main, data
import data_operator as do
from common import global_nav


async def build_page03(q: Q): 
    q.page['meta'] = ui.meta_card(box='', layouts=[
        ui.layout(
            breakpoint='xl',
            min_width='800px',
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
        q.client.select1 = 'Janeiro'
        q.client.select2 = 'All'
        q.client.initialized = True
    elif (q.args.select1 is not None) and (q.args.select2 is not None):
        q.client.select1 = q.args.select1
        q.client.select2 = q.args.select2
    else:
        q.client.select1 = 'Janeiro'
        q.client.select2 = 'All' 
    
    #Tabela
    df = do.forecast_pag3()
    df = df.query(f'Month == "{q.client.select1}"')
    if q.client.select2 == 'Team-01':
        df = df[['Month','Day','Team01-Number_Calls','Team01-Need_Workers']]
    elif q.client.select2 == 'Team-02':
        df = df[['Month','Day','Team02-Number_Calls','Team02-Need_Workers']]
    elif q.client.select2 == 'Team-03':
        df = df[['Month','Day','Team03-Number_Calls','Team03-Need_Workers']]
    elif q.client.select2 == 'Team-04':
        df = df[['Month','Day','Team04-Number_Calls','Team04-Need_Workers']]
    else:
        pass
    q.page['table_view'] = ui.form_card(
        box=ui.box('middle', order=1, width='1800px',height='600px'),
        items=[
            ui.text_xl(f"Forecasts of Calls for {q.client.select1} 2023 - {q.client.select2}"),
            ui.table(
            name='aggregated_data_table',
            columns=[ui.table_column(name=col, label=col, min_width='150px') for col in df.columns.values],
            rows=[
                    ui.table_row(
                        name=str(i),
                        cells=[str(df[col].values[i]) for col in df.columns.values]
                    ) for i in range(len(df))
                ],
                downloadable=True,
                groupable=False,
                height='600px'
            )
        ]
    )

    #Combobox2
    q.page['combo_box'] = ui.form_card(box=ui.box('top', order=1, width='250px', height='100px'), items=[
        ui.dropdown( 
            name='select1', 
            label='Select Month:',
            choices=[
                ui.choice(name='Janeiro', label='Janeiro'),
                ui.choice(name='Fevereiro', label='Fevereiro'),
                ui.choice(name='Março', label='Março'),
                ui.choice(name='Abril', label='Abril'),
                ui.choice(name='Maio', label='Maio'),
                ui.choice(name='Junho', label='Junho'),
                ui.choice(name='Julho', label='Julho'),
                ui.choice(name='Agosto', label='Agosto'),
                ui.choice(name='Setembro', label='Setembro'),
                ui.choice(name='Outubro', label='Outubro'),
                ui.choice(name='Novembro', label='Novembro'),
                ui.choice(name='Dezembro', label='Dezembro'),
            ],
            trigger=True,
            value=q.client.select1
        ),
    ])

    #Combobox2
    q.page['combo_box2'] = ui.form_card(box=ui.box('top', order=2, width='250px', height='100px'), items=[
        ui.dropdown( 
            name='select2', 
            label='Team:',
            choices=[
                ui.choice(name='All', label='All'),
                ui.choice(name='Team-01', label='Team-01'),
                ui.choice(name='Team-02', label='Team-02'),
                ui.choice(name='Team-03', label='Team-03'),
                ui.choice(name='Team-04', label='Team-04')

            ],
            trigger=True,
            value=q.client.select2
        ),
    ])

    await q.page.save()