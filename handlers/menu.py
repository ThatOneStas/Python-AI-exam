from aiogram import Router
from aiogram.types import CallbackQuery, BufferedInputFile
from keyboards import (
    MenuCallback,
    play_menu
)

from chess import Board

from utils import (
    render_board
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
        # testing sending board photo
        board = Board()
        await call.message.answer_photo(
            render_board(board=board),
            caption="Твій хід ♟"
        )
    elif callback_data.action == "pvp":
        await call.message.answer("⛔️ Наразі недоступно")

    await call.answer()
