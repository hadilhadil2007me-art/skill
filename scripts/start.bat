@echo off
REM SkillUp Quick Start Script for Windows
REM This script sets up and runs the complete SkillUp application

setlocal enabledelayedexpansion

echo.
echo 🚀 SkillUp - منصة التدريب المهني الجزائرية
echo ================================================
echo.

REM Check if .env file exists
if not exist .env (
    echo 📝 إنشاء ملف .env...
    copy .env.example .env
    echo ✓ تم إنشاء .env (يمكنك تعديله حسب احتياجاتك)
    echo.
)

REM Check if Docker is available
where docker-compose >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo 🐳 Docker متاح - هل تريد استخدام Docker Compose؟
    echo 1) نعم، استخدم Docker Compose
    echo 2) لا، تشغيل محلي بدون Docker
    set /p choice="اختر (1 أو 2): "
    
    if "!choice!"=="1" (
        echo.
        echo 🔨 بناء وتشغيل عبر Docker Compose...
        docker-compose up --build
        exit /b 0
    )
)

echo.
echo 🔧 إعداد بيئة محلية...
echo.

REM Check if Python is installed
python --version >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ❌ Python غير مثبت. يرجى تثبيت Python 3.9+
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist .venv (
    echo 📦 إنشاء بيئة افتراضية...
    python -m venv .venv
)

REM Activate virtual environment
echo ✓ تفعيل البيئة الافتراضية...
call .venv\Scripts\activate.bat

REM Install requirements
echo 📥 تثبيت التبعيات...
pip install -q -r requirements.txt

REM Seed database with initial data
echo 🌱 إضافة بيانات أولية...
python scripts\seed_data.py || (echo ⚠️ تحذير: فشل إضافة البيانات الأولية)

echo.
echo ================================================
echo ✅ تم الإعداد بنجاح!
echo ================================================
echo.
echo 🌐 تشغيل الخادم على http://localhost:8000
echo.
echo الصفحات الرئيسية:
echo   - الرئيسية:      http://localhost:8000
echo   - تسجيل دخول:    http://localhost:8000/login.html
echo   - تسجيل جديد:    http://localhost:8000/register.html
echo   - API Docs:      http://localhost:8000/docs
echo.

REM Start the server
echo 🚀 بدء خادم FastAPI...
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause
