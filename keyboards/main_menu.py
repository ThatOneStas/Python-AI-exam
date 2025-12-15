from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import MenuCallback

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="♟ Грати", callback_data=MenuCallback(action="play").pack())],
        [InlineKeyboardButton(text="📊 Статистика", callback_data=MenuCallback(action="stats").pack())]
    ])

