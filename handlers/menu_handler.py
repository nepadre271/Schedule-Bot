from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from utils.db import get_student, add_or_update_student
from keyboards.main_menu import get_main_menu
from keyboards.groups_kb import get_directions_keyboard, get_groups_keyboard
from states.data_edit import EditState
from .schedule_handler import schedule_of_the_day  # Импортируем функцию

def register_menu_handler(router: Router):
    @router.message(lambda message: message.text.startswith("✏ Изменения"))
    async def send_daily_schedule(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        student = get_student(user_id)
        if student:
            group = student[3]
            await message.answer(f"Расписание на сегодня для группы {group}:\n" + "\n".join(schedule_of_the_day(group)))
        else:
            await message.answer("Вы не зарегистрированы в системе. Пожалуйста, сначала пройдите регистрацию.")
        
    @router.message(lambda message: message.text.startswith("🎓 Имя"))
    async def change_name(message: types.Message, state: FSMContext):
        await message.answer("Введите новое имя:")
        await state.set_state(EditState.waiting_for_name)

    @router.message(EditState.waiting_for_name)
    async def update_name(message: types.Message, state: FSMContext):
        new_name = message.text
        user_id = message.from_user.id
        student = get_student(user_id)
        if student:
            _, group_name, _ = student[2], student[3], student[4]
            add_or_update_student(user_id, new_name, group_name)
            await message.answer(f"Имя успешно изменено на {new_name}!", reply_markup=get_main_menu(True, new_name, group_name))
        await state.clear()

    @router.message(lambda message: message.text.startswith("💼 Группа"))
    async def change_group(message: types.Message, state: FSMContext):
        await message.answer("Выберите ваше направление.", reply_markup=get_directions_keyboard())
        await state.set_state(EditState.waiting_for_direction)

    @router.callback_query(EditState.waiting_for_direction)
    async def process_direction(callback_query: types.CallbackQuery, state: FSMContext):
        direction = callback_query.data.split(":")[1]
        await state.update_data(direction=direction)
        await callback_query.message.edit_text("Теперь выберите вашу учебную группу.", reply_markup=get_groups_keyboard(direction))
        await state.set_state(EditState.waiting_for_group)

    @router.callback_query(EditState.waiting_for_group)
    async def update_group(callback_query: types.CallbackQuery, state: FSMContext):
        new_group = callback_query.data.split(":")[1]
        user_id = callback_query.from_user.id
        student = get_student(user_id)
        if student:
            name = student[2]
            add_or_update_student(user_id, name, new_group)
            await callback_query.message.delete()
            await callback_query.message.answer(f"Группа успешно изменена на {new_group}!", reply_markup=get_main_menu(True, name, new_group))
        await state.clear()
