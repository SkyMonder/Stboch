import os, chess, chess.engine
from fastapi import FastAPI, HTTPException

app = FastAPI()
engine = None

def init_engine():
    global engine
    # Ищем бинарник (он может называться engine, stockfish, berserk_engine, clover_engine)
    binary = "./engine"
    if not os.path.exists(binary):
        for name in ["./stockfish", "./berserk_engine", "./berserk", "./clover_engine", "./clover"]:
            if os.path.exists(name):
                binary = name
                break
    print(f"Loading engine from {binary}")
    engine = chess.engine.SimpleEngine.popen_uci(binary)
    # Только поддерживаемые опции
    engine.configure({
        "Skill Level": 20,
        "Hash": 128,
        "Threads": 1,
        "Move Overhead": 50,
    })
    # Если движок поддерживает Contempt (не для Stockfish), пробуем добавить, но не падаем
    try:
        if "berserk" in binary.lower():
            engine.configure({"Contempt": 15})
        elif "clover" in binary.lower():
            engine.configure({"Contempt": -15})
    except:
        pass  # Игнорируем, если опция не поддерживается

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
