import asyncio
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

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

from services import (
    game_move,
    game_move_bot
)

from menu import (
    main_menu
)

router = Router()

# handle text message
@router.message(GameStates.wait_for_move, F.text)
async def handle_text_move(message: Message, state: FSMContext):
    # get text
    text = message.text
    # check
    move = extract_move(text)
    # error
    if not move:
        await message.answer("❌ Не зміг знайти хід. Напиши, наприклад: 'a2a4'")
        return
    # process move
    await process_move(message=message, move=move, state=state)
            
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
    move = extract_move_ai(text)
    if not move:
        await message.answer("❌ Не зміг розпізнати хід. Спробуй ще раз, або напиши, наприклад: 'a2a4'")

    await process_move(message=message, move=move, state=state)

# move processing logic
async def process_move(message: Message, move: str, state: FSMContext):
    # processing move
    await state.set_state(GameStates.processing_move)
    tg_id = str(message.from_user.id)
    # get move result
    result = await game_move(tg_id, move)
    # check if move was successful
    if not result["success"]:
        if result["status"] == "illegal_move":
            # keep waiting for user move
            await message.answer("❌ Нелегальний хід, спробуй щось інше")
            await state.set_state(GameStates.wait_for_move)
            return

    # send board with successful move
    await answer_board(message=message, board=Board(result["fen"]), caption=f"✅ Твій хід виконаний - {move}")

    # check if move result was ordinary or final
    if result["status"] == "checkmate":
        await state.clear()
        # send win message
        await message.answer(text="🎖 Ти переміг! Вітаю!\n\nТи повернувся у головне меню, перевірим статистику? 📈",
                             reply_markup=main_menu())
        return
    
    # check if move result was ordinary or final
    elif result["status"] == "stalemate":
        await state.clear()
        # send draw message
        await message.answer(text="👾 Нічия, удачі наступного разу\n\nТи повернувся у головне меню, бажаєш отримати інший результат? 🗡",
                             reply_markup=main_menu())
        return
    
    elif result["status"] == "moved":
        await state.set_state(GameStates.wait_for_oponent_move)

    # if 'moved' - game has not ended yet, do bot's move
    result_bot = await game_move_bot(tg_id)

    # give user time to glance board with his move
    await asyncio.sleep(1.5)

    # illusion of bot thinking
    await message.answer("💡 Бот думає над ходом, зачекай...")
    await asyncio.sleep(2)

    # check if an error could occure during bot's move
    if not result_bot["success"]:
        await state.clear()
        await message.answer(text="⚠️ Упс, бот зламався..\n\nСпробуй створити нову гру, якщо помилка залишиться - сконтактуйтесь з нами!",
                             reply_markup=main_menu())
        return

    # send board with bot's move
    await answer_board(message=message, board=Board(result_bot["fen"]), caption="💥 Бот зробив свій хід")
    
    if result_bot["status"] == "checkmate":
        await state.clear()
        await message.answer(text="🤖 Бот переміг, удачі наступного разу!\n\nТи повернувся у головне меню, спробуєш взяти реванш? ⚔️",
                             reply_markup=main_menu())
        return
    
    elif result_bot["status"] == "stalemate":
        await state.clear()
        # send draw message
        await message.answer(text="👾 Нічия, удачі наступного разу\n\nТи повернувся у головне меню, бажаєш отримати інший результат? 🗡",
                             reply_markup=main_menu())
        return
        
    elif result_bot["status"] == "moved":
        # ask for user move
        await ask_for_move(message=message, pvp=False)
        await state.set_state(GameStates.wait_for_move)
        return