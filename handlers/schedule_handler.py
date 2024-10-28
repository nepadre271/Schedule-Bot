from aiogram import Router, types
from datetime import datetime
import json
from utils.db import get_student

def is_even_week_def():
    today = datetime.today()
    week_number = today.isocalendar()[1]
    return week_number % 2 != 0

def get_schedule(group, day, is_even_week):
    with open('services/scheduler/data/schedule.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    schedule = data.get(group, {}).get(day, "Расписание не найдено")
    final_schedule = []
    for item in schedule:
        if isinstance(item, list):
            final_schedule.append(item[0] if is_even_week else item[1])
        else:
            final_schedule.append(item)
    return final_schedule

def schedule_of_the_day(group):
    days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    day = days_of_week[datetime.today().weekday()]
    is_even_week = is_even_week_def()
    schedule = get_schedule(group, day, is_even_week)
    return schedule

def schedule_full(group):
    days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    is_even_week = is_even_week_def()
    full_schedule = []
    for day in days_of_week:
        day_schedule = get_schedule(group, day, is_even_week)
        full_schedule.append(f"{day.capitalize()}:\n" + "\n".join(day_schedule))
    return full_schedule

def register_schedule_handler(router: Router):
    @router.message(lambda message: message.text.startswith("📖 Полное расписание"))
    async def send_full_schedule(message: types.Message):
        user_id = message.from_user.id
        student = get_student(user_id)
        if student:
            group = student[3]
            full_schedule = schedule_full(group)
            await message.answer(f"Полное расписание для группы {group}:\n\n" + "\n\n".join(full_schedule))
        else:
            await message.answer("Вы не зарегистрированы в системе. Пожалуйста, сначала пройдите регистрацию.")
