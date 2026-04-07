@echo off
title Expense Tracker
echo.
echo [1/2] Starting Server...
echo.

:: فتح المتصفح تلقائياً على رابط البرنامج
start "" http://127.0.0.1:8000

:: تشغيل السيرفر باستخدام البايثون والمكتبات اللي جوه الـ venv
cd backend
..\venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000

pause
