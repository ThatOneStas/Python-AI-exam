from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callback import MenuCallback

def lose_btn():
    return InlineKeyboardButton(text="🏳️ Здатись", callback_data=MenuCallback(action="lose").pack())

def pause_btn():
    return InlineKeyboardButton(text="⏸ Зупинити та продовжити пізніше", callback_data=MenuCallback(action="pause").pack())

def pvp_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [lose_btn()]
    ])

def pve_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [lose_btn()],
        [pause_btn()]
    ])