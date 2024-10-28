from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import DIRECTIONS, GROUPS

def get_directions_keyboard():
    buttons = [InlineKeyboardButton(text=direction, callback_data=f"direction:{direction}") for direction in DIRECTIONS]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])
    return keyboard

def get_groups_keyboard(direction):
    buttons = [InlineKeyboardButton(text=group, callback_data=f"group:{group}") for group in GROUPS.get(direction, [])]
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])
    return keyboard
