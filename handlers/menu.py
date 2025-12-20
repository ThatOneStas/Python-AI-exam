from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from states.game import GameStates
from datetime import datetime

from keyboards import (
    MenuCallback,
    play_menu,
    main_menu,
    stats_menu
)

from chess import Board

from utils import (
    answer_board,
    ask_for_move
)

from services import (
    get_user,
    get_user_games,
    create_game,
    get_user_active_game,
    surrender
)

router = Router()

FORMAT_PATTERN = "%Y-%m-%dT%H:%M"

@router.callback_query(MenuCallback.filter())
async def menu_handler(call: CallbackQuery, callback_data: MenuCallback, state: FSMContext):
    if callback_data.action == "play":
        await call.message.answer(
            "♟ Обери режим:",
            reply_markup=play_menu()
        )

    elif callback_data.action == "stats":

        tg_id = str(call.from_user.id)

        user = await get_user(tg_id)
        
        if not user:
            await call.message.answer("❌ Не вдалось отримати користувача")
            return

        await call.message.answer(
            text="📊 Твоя статистика:\n" \
            "\n🤖 PVE:\n" \
            f"- перемог: {user['pve_wins']}\n" \
            f"- нічиї: {user['pve_draws']}\n" \
            f"- програші: {user['pve_defeats']}\n" \
            "\n🌐 PVP:\n" \
            f"- перемог: {user['pvp_wins']}\n" \
            f"- нічиї: {user['pvp_draws']}\n" \
            f"- програші: {user['pvp_defeats']}",
            reply_markup=stats_menu()
        )

    elif callback_data.action == "stat_back":
        await call.message.answer(text="✅ Повернуто назад",
                                  reply_markup=main_menu())
    
    elif callback_data.action == "stat_games":

        tg_id = str(call.from_user.id)

        games = await get_user_games(tg_id)
        history = "\n\n🕳 Схоже ти ще не грав.."

        games = games["games"]

        if games != []:
            history = ""
            for i in range(len(games)):
                winner: str | None = games[i]['winner_color']
                created_at = datetime.fromisoformat(games[i]['created_at']).strftime(FORMAT_PATTERN)
                finished_at = datetime.fromisoformat(games[i]['finished_at']).strftime(FORMAT_PATTERN) if games[i]['finished_at'] else None
                
                history += f"\n\n{i+1}) Тривалість: {created_at} - {datetime.strptime(finished_at, FORMAT_PATTERN) if finished_at else '(гра продовжується)'},\n" \
                           f"     переможець: {winner.capitalize() + (' - ⚪️' if winner == 'white' else ' - ⚫️') if winner else '(гра не завершена)'}"

        await call.message.answer(
            text="📊 Твоя історія матчів:" \
            f"{history}",
            reply_markup=stats_menu())

    elif callback_data.action == "pve":

        tg_id = str(call.from_user.id)

        game = await create_game(tg_id)

        if not game:
            await call.message.answer("🔄 Завантажуємо існуючий стіл...")
            game = await get_user_active_game(tg_id)
        else:
            await call.message.answer("🔄 Створюємо шахматний стіл...")

        board = Board(game["fen"])
        if board:
            await answer_board(message=call.message,
                               board=board,
                               caption="✅ Стіл завантажено!\n\n" \
                               "Виконуй ходи у текстовому форматі: a1a2 / a1 a2\n" \
                               "Або ж у такомуж форматі, голосом! 🎤")

        await ask_for_move(message=call.message, pvp=False)

        await state.set_state(GameStates.wait_for_move)
        await state.update_data(board_fen=board.fen())

    elif callback_data.action == "pvp":
        await call.message.answer("⛔️ Наразі недоступно",
                                  reply_markup=play_menu()
                                )

    elif callback_data.action == "surrender":
        tg_id = str(call.from_user.id)

        result = await surrender(tg_id)

        if not result:
            await call.message.answer(
                "⚠️ Щось пішло не так, скоріш за все - немає активної гри",
                reply_markup=main_menu()
            )
        finished_at = datetime.fromisoformat(result['finished_at']).strftime(FORMAT_PATTERN)
        await call.message.answer(
            "🏳️ Ти здався, жаль..\n\n" \
            f"Перемога: {result['winner_color']}" \
            f"Гра завершилась о: {finished_at}",
            reply_markup=main_menu()
        )
        await state.clear()
    
    elif callback_data.action == "pause":
        await call.message.answer("▶️ Партія на паузі та збережена!",
                                  reply_markup=main_menu()
                                )
        await state.set_state(GameStates.idle)

    await call.answer()
