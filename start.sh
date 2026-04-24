#!/bin/bash
set -e

echo "=== Установка Stockfish 18 ==="
mkdir -p temp
cd temp

# Скачиваем архив с бинарником
wget -q https://github.com/official-stockfish/Stockfish/releases/download/sf_18/stockfish-ubuntu-x86-64-bmi2.tar
tar -xf stockfish-ubuntu-x86-64-bmi2.tar

# Ищем бинарник внутри папки stockfish
if [ -f "stockfish/stockfish-ubuntu-x86-64-bmi2" ]; then
    cp stockfish/stockfish-ubuntu-x86-64-bmi2 ../engine
else
    echo "Ошибка: бинарник не найден!"
    exit 1
fi

cd ..
rm -rf temp
chmod +x ./engine

echo "=== Запуск движка ==="
exec gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT engine:app
