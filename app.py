from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List

# Import Tic-Tac-Toe Brains
from tic_tac_toe import TicTacToe
from strategy_ttt import Strategy as TTTStrategy

# Import Connect Four Brains
from connect_four import ConnectFour
from strategy_c4 import Strategy as C4Strategy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def serve_homepage():
    return FileResponse("index.html")

# --- TIC-TAC-TOE SECTION ---
class TTTGameState(BaseModel):
    board: List[str]
    ai_letter: str
    strategy: str

@app.post("/get_ttt_move")
def get_ttt_move(state: TTTGameState):
    game = TicTacToe()
    game.board = state.board
    
    for i in range(9):
        if game.board[i] != ' ':
            game.check_winner(i, game.board[i])
            if game.current_winner:
                return {"error": "Game already over"}

    strategy_map = {
        "random": TTTStrategy.random_strategy,
        "sankalp_2": TTTStrategy.sankalp_2,
        "minimax": TTTStrategy.get_move
    }
    
    ai_function = strategy_map.get(state.strategy, TTTStrategy.random_strategy)
    move = ai_function(game, state.ai_letter)
    return {"move": move}


# --- CONNECT FOUR SECTION ---
class C4GameState(BaseModel):
    board: List[List[str]]
    ai_letter: str
    strategy: str

@app.post("/get_c4_move")
def get_c4_move(state: C4GameState):
    game = ConnectFour()
    game.board = state.board
    
    for letter in ['X', 'O']:
        if game.check_winner(letter):
            return {"error": "Game already over"}

    strategy_map = {
        "random": C4Strategy.random_strategy,
        "minimax": C4Strategy.get_move,
        "alphabeta": C4Strategy.best_move_cpu
    }
    
    ai_function = strategy_map.get(state.strategy, C4Strategy.best_move_cpu)
    move_col = ai_function(game, state.ai_letter)
    return {"move": move_col}