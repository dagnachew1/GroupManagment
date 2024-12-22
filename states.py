from aiogram.fsm.state import State, StatesGroup

class VerificationStates(StatesGroup):
    waiting_verification = State()
