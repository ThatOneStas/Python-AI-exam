from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.game import GameStates

from keyboards import (
    MenuCallback,
    play_menu,
    main_menu
)

from chess import Board

from utils import (
    answer_board,
    ask_for_move
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

        # try loading table from memory (temporary, will be switched to api logic)
        try:
            data = await state.get_data()
            board = Board(data["board_fen"])
            if board:
                await answer_board(message=call.message, board=board, caption="✅ Стіл завантажено та знятий з паузи!")
        except Exception:
            board = Board()
            await answer_board(message=call.message, board=board, caption="✅ Стіл створено!")

        await ask_for_move(message=call.message, pvp=False)

        await state.set_state(GameStates.wait_for_move)
        await state.update_data(board_fen=board.fen())

    elif callback_data.action == "pvp":
        await call.message.answer("⛔️ Наразі недоступно",
                                  reply_markup=play_menu()
                                )

    elif callback_data.action == "lose":
        await call.message.answer("🏳️ Ти здався, жаль..",
                                  reply_markup=main_menu()
                                )
        await state.clear()
    
    elif callback_data.action == "pause":
        await call.message.answer("▶️ Партія на паузі та збережена!",
                                  reply_markup=main_menu()
                                )
        await state.set_state(GameStates.idle)

    await call.answer()
