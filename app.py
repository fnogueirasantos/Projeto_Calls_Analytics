from h2o_wave import site, ui, Q, main, data, app

from page1 import build_page01
from page2 import build_page02
from page3 import build_page03


@app('/')
async def serve(q: Q):
    route = q.args['#']
    q.page.drop()
    if route == 'dashboards/page01':
        await build_page01(q)
    elif route == 'dashboards/page02':
        await build_page02(q)      
    elif route == 'dashboards/page03':
        await build_page03(q)
    else:
        await build_page01(q)