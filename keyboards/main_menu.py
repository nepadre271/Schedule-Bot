from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu(is_registered, name=None, group_name=None, is_subscribed=False):
    if is_registered:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✏ Изменения")],
                [KeyboardButton(text="📖 Полное расписание")],
                [KeyboardButton(text=f"Рассылка {'(Включена ✔)' if is_subscribed else '(Выключена  ❌)'}")],
                [ KeyboardButton(text=f"🎓 Имя: {name}"), KeyboardButton(text=f"💼 Группа: {group_name}")]
            ],
            resize_keyboard=True
        )
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔑 Регистрация")]
            ],
            resize_keyboard=True
        )
    return keyboard
