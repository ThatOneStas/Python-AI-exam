import asyncio
from aiogram.types import Message
from chess import Board
from typing import Literal

from .board_render import render_board

from keyboards import (
    pvp_menu,
    pve_menu
)

async def answer_board(message: Message, board: Board, caption: str):
    await message.answer_photo(
        render_board(board),
        caption=caption
    )

async def ask_for_move(message: Message, pvp: bool):
    await message.answer(text="♟ Твоя черга:",
                        reply_markup=pvp_menu() if pvp else pve_menu()
                    )