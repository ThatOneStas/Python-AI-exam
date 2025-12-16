from aiogram.fsm.state import StatesGroup, State

class GameStates(StatesGroup):
    started = State()
    processing_move = State()
    wait_for_move = State()
    wait_for_oponent_move = State()
