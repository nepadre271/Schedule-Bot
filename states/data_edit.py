from aiogram.fsm.state import StatesGroup, State

class EditState(StatesGroup):
    waiting_for_name = State()
    waiting_for_direction = State()
    waiting_for_group = State()
