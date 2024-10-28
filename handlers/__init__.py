from .command_handler import register_command_handlers
from .new_member_handler import register_new_member_handler
from .menu_handler import register_menu_handler
from .schedule_handler import register_schedule_handler

def setup_handlers(router):
    register_command_handlers(router)
    register_new_member_handler(router)
    register_menu_handler(router)
    register_schedule_handler(router)
