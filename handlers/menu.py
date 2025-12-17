from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.game import GameStates

from keyboards import (
    MenuCallback,
    play_menu
)

from chess import Board

from utils import (
    answer_board
)

router = Router()

@router.callback_query(MenuCallback.filter())
async def menu_handler(call: CallbackQuery, callback_data: MenuCallback, state: FSMContext):
    if callback_data.action == "play":
        await call.message.answer(
            "♟ Обери режим:",
            reply_markup=play_menu()
        )
    elif callback_data.action == "stats":
        await call.message.answer("📊 Твоя статистика:")
    elif callback_data.action == "pve":

        await call.message.answer("🔄 Створюємо шахматний стіл...")

        board = Board()
        await answer_board(message=call.message, board=board, caption="♟ Твій хід:")

        await state.set_state(GameStates.wait_for_move)
        await state.update_data(board_fen=board.fen())
    elif callback_data.action == "pvp":
        await call.message.answer("⛔️ Наразі недоступно")

    await call.answer()
