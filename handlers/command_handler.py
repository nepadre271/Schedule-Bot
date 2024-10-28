from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from utils.db import get_student, update_subscription_status, get_all_students
from keyboards.main_menu import get_main_menu
from config import bot, CHANNEL_ID

def register_command_handlers(router: Router):
    #Обработчик команды /start
    @router.message(Command("start"))
    async def send_welcome(message: types.Message):
        user_id = message.from_user.id
        student = get_student(user_id)
        if student:
            name, group_name, is_subscribed = student[2], student[3], student[4]
            await message.answer(f"Привет, {name} из группы {group_name}!", reply_markup=get_main_menu(True, name, group_name, is_subscribed))
        else:
            await message.answer("Привет! Нажмите кнопку ниже, чтобы зарегистрироваться.", reply_markup=get_main_menu(False))

    @router.message(lambda message: message.text.startswith("Рассылка"))
    async def toggle_subscription(message: types.Message):
        user_id = message.from_user.id
        student = get_student(user_id)
        if student:
            is_subscribed = not student[4]
            update_subscription_status(user_id, is_subscribed)
            await message.answer(f"Рассылка {'включена' if is_subscribed else 'выключена'}.", reply_markup=get_main_menu(True, student[2], student[3], is_subscribed))

    #Обработчик команды /send
    @router.message(Command("send"))
    async def send_message_to_channel(message: Message):
        msg = message.text.split("/send ", 1)[1] if "/send " in message.text else None
        if msg:
            # Отправка сообщения в канал
            await bot.send_message(CHANNEL_ID, msg)
            # Отправка сообщения всем зарегистрированным пользователям в личку
            students = get_all_students()
            unique_errors = set()
            for student in students:
                user_id = student[1]
                try:
                    await bot.send_message(user_id, msg)
                except Exception as e:
                    unique_errors.add(str(e))
            if unique_errors:
                print("Не удалось отправить сообщения по следующим причинам:")
                for error in unique_errors:
                    print(f"- {error}")
            await message.answer("Сообщение отправлено в канал и всем зарегистрированным пользователям!")
        else:
            await message.answer("Пожалуйста, укажите сообщение для отправки.")
