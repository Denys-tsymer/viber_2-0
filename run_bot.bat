@echo off
chcp 65001 > nul
title Viber Bot Launcher

echo Running screen scanner (main.py)...
start cmd /k "python main.py & pause"

timeout /t 2 > nul

echo Running Telegram bot (telegram_bot.py)...
start cmd /k "python telegram_bot.py & pause"

echo All components launched.
pause
