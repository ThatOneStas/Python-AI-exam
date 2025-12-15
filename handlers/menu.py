from aiogram import Router
from aiogram.types import CallbackQuery
from keyboards import (
    MenuCallback,
    play_menu
)

router = Router()

@router.callback_query(MenuCallback.filter())
async def menu_handler(call: CallbackQuery, callback_data: MenuCallback):
    if callback_data.action == "play":
        await call.message.answer(
            "♟ Обери режим:",
            reply_markup=play_menu()
            )
    elif callback_data.action == "stats":
        await call.message.answer("📊 Твоя статистика:")
    elif callback_data.action == "pve":
        await call.message.answer("🔄 Створюємо шахматний стіл...")
    elif callback_data.action == "pvp":
        await call.message.answer("⛔️ Наразі недоступно")

    await call.answer()
