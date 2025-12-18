from handlers import (
    menu,
    start,
    move,
    ignore
)

def setup_routers(dp):
    dp.include_router(menu.router),
    dp.include_router(start.router),
    dp.include_router(move.router),        
    dp.include_router(ignore.router), 