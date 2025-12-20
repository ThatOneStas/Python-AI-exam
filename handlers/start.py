from aiogram import Router, types
from aiogram.filters import Command
from keyboards import main_menu

from services import (
    create_user
)

router = Router()

@router.message(Command("start"))
async def start_handler(msg: types.Message):

    tg_id = str(msg.from_user.id)

    user = await create_user(tg_id)

    if not user:
        await msg.answer("❌ Помилка створення користувача")
        return

    await msg.answer(
        "Вітаю у Chess! Обери дію:",
        reply_markup=main_menu(),
    )
