import os, chess, chess.engine, traceback
from fastapi import FastAPI, HTTPException

app = FastAPI()
engine = None

def init_engine():
    global engine
    engine = chess.engine.SimpleEngine.popen_uci("./engine")
    engine.configure({
        "Skill Level": 20,
        "Hash": 384,
        "Threads": 2,
        "Move Overhead": 50,
    })

@app.on_event("startup")
async def startup():
    init_engine()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/get_move")
async def get_move(data: dict):
    try:
        fen = data.get("fen")
        move_time = data.get("move_time", 1.0)
        board = chess.Board(fen)
        result = engine.play(board, chess.engine.Limit(time=move_time))
        return {"move": result.move.uci() if result.move else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
