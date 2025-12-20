from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import MenuCallback

def stats_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Історія матчів", callback_data=MenuCallback(action="stat_games").pack())],
        [InlineKeyboardButton(text="↩️ Назад", callback_data=MenuCallback(action="stat_back").pack())]
    ])