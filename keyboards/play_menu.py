from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import MenuCallback

def play_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Грати  Оффлайн", callback_data=MenuCallback(action="pve").pack())],
        [InlineKeyboardButton(text="🌐 Грати  Онлайн (недоступно)", callback_data=MenuCallback(action="pvp").pack())]
    ])

