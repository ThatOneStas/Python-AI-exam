from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import MenuCallback

def stats_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📋 Історія матчів", callback_data=MenuCallback(action="stat_games").pack())],
        [InlineKeyboardButton(text="↩️ Назад до головного меню", callback_data=MenuCallback(action="stat_back").pack())]
    ])

def stats_games_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Назад до головного меню", callback_data=MenuCallback(action="stat_back").pack())]
    ])