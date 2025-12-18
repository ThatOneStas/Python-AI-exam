from aiogram import Router
from aiogram.types import Message

from states import GameStates

router = Router()

@router.message(GameStates.wait_for_oponent_move)
async def ignore_as_oponent_move(message: Message):
    await message.answer("⏳ Зачекай, хід опонента...")

@router.message(GameStates.processing_move)
async def ignore_as_processing(message: Message):
    await message.answer("⏳ Зачекай, обробляю твій хід...")

@router.message(GameStates.in_queue)
async def ignore_as_queue(message: Message):
    await message.answer("⏳ Зачекай, знаходжу суперника...")