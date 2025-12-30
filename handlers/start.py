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
        await msg.answer(
            "З поверненням у Chess! Оберіть дію:\n" \
            "\n1) Перейти до розділу ігор," \
            "\n2) Перейти до статистики.",
            reply_markup=main_menu(),
        )
        return

    await msg.answer(
        "Вітаю у Chess! Оберіть дію:\n" \
        "\n1) Перейти до розділу ігор," \
        "\n2) Перейти до статистики.",
        reply_markup=main_menu(),
    )
