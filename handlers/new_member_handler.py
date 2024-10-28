from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from utils.db import add_or_update_student
from keyboards.main_menu import get_main_menu
from keyboards.groups_kb import get_directions_keyboard, get_groups_keyboard

class Registration(StatesGroup):
    waiting_for_name = State()
    waiting_for_direction = State()
    waiting_for_group = State()

def register_new_member_handler(router: Router):
    @router.message(lambda message: message.text == "🔑 Регистрация")
    async def start_registration(message: types.Message, state: FSMContext):
        await message.answer("Пожалуйста, напишите своё имя.")
        await state.set_state(Registration.waiting_for_name)

    @router.message(Registration.waiting_for_name)
    async def process_name(message: types.Message, state: FSMContext):
        await state.update_data(name=message.text)
        await message.answer("Спасибо! Теперь выберите ваше направление.", reply_markup=get_directions_keyboard())
        await state.set_state(Registration.waiting_for_direction)

    @router.callback_query(Registration.waiting_for_direction)
    async def process_direction(callback_query: types.CallbackQuery, state: FSMContext):
        direction = callback_query.data.split(":")[1]
        await state.update_data(direction=direction)
        await callback_query.message.edit_text("Спасибо! Теперь выберите вашу учебную группу.", reply_markup=get_groups_keyboard(direction))
        await state.set_state(Registration.waiting_for_group)

    @router.callback_query(Registration.waiting_for_group)
    async def process_group(callback_query: types.CallbackQuery, state: FSMContext):
        group_name = callback_query.data.split(":")[1]
        user_data = await state.get_data()
        name = user_data['name']
        add_or_update_student(callback_query.from_user.id, name, group_name)
        await callback_query.message.edit_text(f"Спасибо, {name}! Вы зарегистрированы в группе {group_name}.", reply_markup=get_main_menu(True, name, group_name))
        await state.clear()
