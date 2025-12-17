import asyncio
from aiogram.types import Message
from chess import Board

from .board_render import render_board

async def answer_board(message: Message, board: Board, caption: str):
    await message.answer_photo(
        render_board(board),
        caption=caption
    )