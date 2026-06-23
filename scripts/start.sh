#!/bin/bash
# SkillUp Quick Start Script
# This script sets up and runs the complete SkillUp application

set -e

echo "🚀 SkillUp - منصة التدريب المهني الجزائرية"
echo "================================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 إنشاء ملف .env..."
    cp .env.example .env
    echo "✓ تم إنشاء .env (يمكنك تعديله حسب احتياجاتك)"
    echo ""
fi

# Check if we should use Docker
if command -v docker-compose &> /dev/null; then
    echo "🐳 Docker متاح - هل تريد استخدام Docker Compose؟"
    echo "1) نعم، استخدم Docker Compose"
    echo "2) لا، تشغيل محلي بدون Docker"
    read -p "اختر (1 أو 2): " choice
    
    if [ "$choice" = "1" ]; then
        echo ""
        echo "🔨 بناء وتشغيل عبر Docker Compose..."
        docker-compose up --build
        exit 0
    fi
fi

# Local setup
echo ""
echo "🔧 إعداد بيئة محلية..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 غير مثبت. يرجى تثبيت Python 3.9+"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 إنشاء بيئة افتراضية..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "✓ تفعيل البيئة الافتراضية..."
source .venv/bin/activate

# Install requirements
echo "📥 تثبيت التبعيات..."
pip install -q -r requirements.txt

# Seed database with initial data
echo "🌱 إضافة بيانات أولية..."
python scripts/seed_data.py || true

echo ""
echo "================================================"
echo "✅ تم الإعداد بنجاح!"
echo "================================================"
echo ""
echo "🌐 تشغيل الخادم على http://localhost:8000"
echo ""
echo "الصفحات الرئيسية:"
echo "  - الرئيسية:      http://localhost:8000"
echo "  - تسجيل دخول:    http://localhost:8000/login.html"
echo "  - تسجيل جديد:    http://localhost:8000/register.html"
echo "  - API Docs:      http://localhost:8000/docs"
echo ""

# Start the server
echo "🚀 بدء خادم FastAPI..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
