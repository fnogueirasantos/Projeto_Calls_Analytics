from h2o_wave import ui

global_nav = [
    ui.nav_group('Menu', items=[
        ui.nav_item(name='#dashboards/page01', label='Dashboard'),
        ui.nav_item(name='#dashboards/page02', label='Comparisons'),
        ui.nav_item(name='#dashboards/page03', label='Predictions')
    ]),
]
