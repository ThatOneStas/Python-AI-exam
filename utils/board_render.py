from aiogram.types import BufferedInputFile
from chess import Board, svg
import cairosvg

def render_board(board: Board) -> BufferedInputFile:
    wrapper = svg.board(board)
    bytes = wrapper.encode("utf-8")
    png = BufferedInputFile(cairosvg.svg2png(bytes), filename="Board.png")
    return png
