from handlers import (
    menu,
    start,
)

def setup_routers(dp):
    dp.include_router(menu.router),
    dp.include_router(start.router),

