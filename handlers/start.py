from aiogram import Router, types
from aiogram.filters import Command
from keyboards import main_menu

router = Router()

@router.message(Command("start"))
async def start_handler(msg: types.Message):
    await msg.answer(
        "Вітаю у Chess! Обери дію:",
        reply_markup=main_menu()
    )
