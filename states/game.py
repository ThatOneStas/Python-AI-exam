from aiogram.fsm.state import StatesGroup, State

class GameStates(StatesGroup):
    # default
    idle = State()
    # chess-related
    started = State()
    processing_move = State()
    wait_for_move = State()
    wait_for_oponent_move = State()
    # for matchmaking
    in_queue = State()