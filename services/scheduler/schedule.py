import pandas as pd
import json
import os

# Путь к файлу JSON
output_path = 'data/schedule.json'

# Проверка существования файла JSON
if os.path.exists(output_path):
    print(f"{output_path} уже существует. Расписание не будет перезаписано.")
else:
    # Чтение CSV файла с указанием разделителя
    df = pd.read_csv('data/schedule.csv', delimiter=';', header=0)

    # Дни недели
    days_of_week = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]

    # Инициализация расписания
    schedule = {}

    # Перебор групп (начиная с третьей колонки)
    groups = df.columns[2:]
    groups = [col for col in groups if not col.startswith('Unnamed:')]

    for group in groups:
        group_schedule = {day: [] for day in days_of_week}
        current_day = None

        # Перебор строк DataFrame
        for index, row in df.iterrows():
            # Если в первой колонке указан день недели, устанавливаем текущий день
            if pd.notna(row.iloc[0]) and row.iloc[0].strip().lower() in days_of_week:
                current_day = row.iloc[0].strip().lower()
            
            # Если текущий день установлен и есть данные для группы
            if current_day and pd.notna(row[group]):
                # Получаем номер пары
                pair_number = row.iloc[1]  # Номер пары из второй колонки
                
                if pd.isna(pair_number):  # Проверяем, является ли pair_number NaN
                    # Получаем последний предмет, добавленный в расписание на текущий день
                    last_subject = group_schedule[current_day][-1] if group_schedule[current_day] else ""
                    # Объединяем последний предмет с текущим значением row[group]
                    num = last_subject.split()[0]
                    combined_subject = [last_subject, f"{num} {row[group].replace('\n', ' ')}".strip()]
                    # Заменяем последнее значение в расписании
                    if group_schedule[current_day]:
                        group_schedule[current_day][-1] = combined_subject
                else:
                    # Формируем строку с номером пары и предметом
                    subject_with_pair = f"{str(pair_number).split('.')[0]}: {row[group].replace('\n', ' ')}"
                    # Добавляем пару в расписание для текущего дня этой группы
                    group_schedule[current_day].append(subject_with_pair)
                
        # Сохраняем расписание группы в общий словарь
        schedule[group] = group_schedule

    # Сохранение расписания в JSON файл в папку data
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=4)
    print(f"{output_path} успешно создан.")
