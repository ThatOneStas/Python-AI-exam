import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import re

from chess import Board, engine

from states.game import GameStates

from utils import (
    answer_board,
    ask_for_move,
    recognize_uk_from_file,
    extract_voice_file,
    convert_ogg_to_wav,
    download_file,
    extract_move_ai,
    extract_move,
)

#  ---
from aiogram.types import BufferedInputFile

router = Router()

# handle text message
@router.message(GameStates.wait_for_move, F.text)
async def handle_text_move(message: Message, state: FSMContext):
    # format text
    text = message.text.lower()
    # check
    move = extract_move(text)
    # error
    if not move:
        await message.answer("❌ Не зміг знайти хід. Напиши, наприклад: 'a2a4'")
        return
    # process move
    await move(message=message, move=text, state=state)
            
# handle voice message
@router.message(GameStates.wait_for_move, F.voice)
async def handle_voice_move(message: Message, state: FSMContext):
    # get voice file
    file = await extract_voice_file(message.voice.file_id)

    # local paths
    path_ogg = "voice.ogg"
    path_wav = "voice.wav"

    await download_file(file.file_path, path_ogg)

    # convertation
    convert_ogg_to_wav(path_ogg, path_wav)

    # getting recognized text
    text = recognize_uk_from_file(path_wav)
    if not text:
        await message.answer("❌ Не зміг розпізнати говір. Спробуй ще раз, або напиши, наприклад: 'a2a4'")

    # extracting move
    move = await extract_move_ai(text)
    if not move:
        await message.answer("❌ Не зміг розпізнати хід. Спробуй ще раз, або напиши, наприклад: 'a2a4'")

    await move(message=message, move=text, state=state)

# move processing logic
async def move(message: Message, move: str, state: FSMContext):
    data = await state.get_data()
    board = Board(data["board_fen"])

    # processing move
    await state.set_state(GameStates.processing_move)
    # get move result
    result = await process_move(move, board)

    # check if move was successful
    if not result["success"]:
        if result["status"] == "wrong_move":
            # keep waiting for user move
            await message.answer("❌ Нелегальний хід, спробуй щось інше")
            await state.set_state(GameStates.wait_for_move)
            return

    # send board with successful move
    await answer_board(message=message, board=board, caption="✅ Твій хід виконаний")

    # check if move result was ordinary or final
    if result["status"] == "checkmate":
        await state.clear()
        # send win message
        await message.answer("🎖 Ти переміг! Вітаю!")
        return
    
    elif result["status"] == "moved":
        await state.set_state(GameStates.wait_for_oponent_move)

    # if 'moved' - game has not ended yet, do bot's move
    result_bot = await stockfish_move(board)

    # give user time to glance board with his move
    await asyncio.sleep(1.5)

    # illusion of bot thinking
    await message.answer("💡 Бот думає над ходом, зачекай")
    await asyncio.sleep(2)

    # send board with bot's move
    await answer_board(message=message, board=board, caption="💥 Бот зробив свій хід")


    # check if an error could occure during bot's move
    if not result_bot["success"]:
        await message.answer("⚠️ Упс, бот помилився..")
        return
    
    if result_bot["status"] == "checkmate":
        await state.clear()
        await message.answer("🤖 Бот переміг, удачі наступного разу")
        return
        

    elif result_bot["status"] == "moved":
        # ask for user move
        await ask_for_move(message=message, pvp=False)
        await state.set_state(GameStates.wait_for_move)
        await state.update_data(board_fen=board.fen())
        return

# --- temporary here
# Process user move
async def process_move(move: str, board: Board):
    # make move
    try:
        board.push_uci(move)
    except ValueError:
        return {
            "success": False,
            "status": "wrong_move"
        }
    # check if user won
    if board.is_checkmate():
        return {
            "success": True,
            "status": "checkmate"
        }
    # return move result
    return {
            "success": True,
            "status": "moved"
        }

# Process stockfish move
async def stockfish_move(board: Board):
    try:
        with engine.SimpleEngine.popen_uci(r"C:\Users\Cтас\source\repos\Python-AI-exam-db\stockfish\stockfish-windows-x86-64-avx2.exe") as sf:
            result = sf.play(board, engine.Limit(time=0.5))
            board.push(result.move)
    except ValueError:
        return {
            "success": False,
            "status": "wrong_move"
        }
    # check if bot won
    if board.is_checkmate():
        return {
            "success": True,
            "status": "checkmate"
        }
    # return move result
    return {
            "success": True,
            "status": "moved"
        }