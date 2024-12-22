from aiogram import Router
from . import commands, service_messages, welcome

def get_handlers_router() -> Router:
    router = Router()
    
    # Include all handler routers
    router.include_router(commands.router)
    router.include_router(service_messages.router)
    router.include_router(welcome.router)
    
    return router
