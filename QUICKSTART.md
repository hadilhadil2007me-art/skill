# SkillUp Full Stack - Quick Start Guide

**SkillUp** منصة جزائرية متكاملة (Full Stack) لربط الشباب بالمهنيين والحرفيين للتدريب الميداني.

## 🎯 ما يجب أن تعرفه

هذا مشروع **Full Stack كامل** يتضمن:

✅ **Backend API** - FastAPI مع JWT و Role-Based Access Control  
✅ **Frontend Web** - HTML/CSS/JavaScript مع دعم اللغة العربية (RTL)  
✅ **Database** - PostgreSQL مع Alembic Migrations  
✅ **Docker** - جاهز للتطوير والإنتاج  
✅ **Authentication** - تسجيل وتسجيل دخول آمن  

---

## 🚀 البدء السريع (3 خطوات فقط)

### الخيار 1: استخدام Docker (الأسهل)

```bash
cd /path/to/skillup

# تحقق من وجود .env (سيتم إنشاؤه تلقائياً)
# شغّل التطبيق:
docker-compose up --build

# انتظر رسالة: "Application startup complete"
# ثم اذهب إلى: http://localhost:8000
```

### الخيار 2: تشغيل محلي بدون Docker

```bash
cd /path/to/skillup

# 1. أنشئ بيئة افتراضية
python -m venv .venv

# 2. فعّلها
# على Windows:
.venv\Scripts\activate
# على Linux/Mac:
source .venv/bin/activate

# 3. ثبّت التبعيات
pip install -r requirements.txt

# 4. أضف بيانات أولية (اختياري)
python scripts/seed_data.py

# 5. شغّل التطبيق
uvicorn app.main:app --reload --port 8000
```

### الخيار 3: استخدام سكريبت البدء السريع

**على Windows:**
```bash
.\scripts\start.bat
```

**على Linux/Mac:**
```bash
bash scripts/start.sh
```

---

## 🔗 الوصول للتطبيق

بعد التشغيل، يمكنك الوصول إلى:

| الصفحة | الرابط |
|------|--------|
| **الرئيسية** | http://localhost:8000 |
| **تسجيل دخول** | http://localhost:8000/login.html |
| **تسجيل جديد** | http://localhost:8000/register.html |
| **لوحة التحكم** | http://localhost:8000/dashboard.html |
| **API Docs** | http://localhost:8000/docs |
| **ReDoc** | http://localhost:8000/redoc |

---

## 👤 حسابات اختبار

### حساب المسؤول (ينشأ تلقائياً)

```
البريد: admin@skillup.dz
كلمة المرور: admin_secure_password_99
```

### حسابات تجريبية (يمكن إنشاؤها عبر seed_data.py)

**متدرب تجريبي:**
```
البريد: youcef@skillup.dz
كلمة المرور: Demo@2025
الدور: متدرب (يبحث عن تدريب)
```

**مدرب تجريبي:**
```
البريد: fatima@skillup.dz
كلمة المرور: Demo@2025
الدور: مدرب (يقدم تدريب)
```

---

## 🧪 اختبار التطبيق

### 1. اختبار المصادقة (Authentication)

```bash
# تسجيل مستخدم جديد
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "محمد احمد",
    "password": "Test@1234",
    "phone": "0661234567",
    "role": "trainee"
  }'

# تسجيل دخول
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Test@1234"
```

### 2. اختبار المهارات (Skills)

```bash
# الحصول على قائمة المهارات
curl http://localhost:8000/api/v1/skills

# إضافة مهارة جديدة (يحتاج مسؤول)
curl -X POST http://localhost:8000/api/v1/skills \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "name": "الإلكترونيات",
    "description": "تدريب في الإلكترونيات والدوائر الكهربائية"
  }'
```

### 3. اختبار ملفات المدربين (Trainer Profiles)

```bash
# الحصول على قائمة المدربين
curl http://localhost:8000/api/v1/trainers

# إنشاء ملف مدرب (يحتاج تسجيل دخول مدرب)
curl -X POST http://localhost:8000/api/v1/trainers/me \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "skill_id": 1,
    "city": "الجزائر العاصمة",
    "experience_years": 5,
    "bio": "مدرب متخصص في الكهرباء"
  }'
```

### 4. اختبار طلبات التدريب (Training Requests)

```bash
# إرسال طلب تدريب (من متدرب)
curl -X POST http://localhost:8000/api/v1/requests \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "trainer_id": "TRAINER_UUID",
    "message": "أتطلع للتدريب معك"
  }'

# قبول/رفض طلب (من مدرب)
curl -X PATCH http://localhost:8000/api/v1/requests/REQUEST_UUID \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "status": "accepted"
  }'
```

---

## 📊 بنية المشروع

```
skillup/
├── app/                       # كود التطبيق الرئيسي
│   ├── main.py               # نقطة الدخول الرئيسية
│   ├── auth/                 # مصادقة JWT
│   ├── core/                 # إعدادات الأمان
│   ├── database/             # اتصال قاعدة البيانات
│   ├── models/               # نماذج SQLAlchemy
│   │   ├── user.py
│   │   ├── skill.py
│   │   ├── trainer_profile.py
│   │   ├── training_request.py
│   │   └── review.py
│   ├── routes/               # نقاط نهاية API
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── skills.py
│   │   ├── trainer_profiles.py
│   │   ├── training_requests.py
│   │   └── reviews.py
│   ├── schemas/              # Pydantic Schemas
│   └── services/             # منطق العمل
│
├── frontend/                 # الواجهة الأمامية
│   ├── index.html           # الصفحة الرئيسية
│   ├── login.html           # تسجيل الدخول
│   ├── register.html        # التسجيل الجديد
│   ├── dashboard.html       # لوحة التحكم
│   ├── api.js               # عميل API
│   ├── app.js               # سكريبتات عامة
│   ├── style.css            # الأنماط الرئيسية
│   └── pages.css            # أنماط الصفحات
│
├── scripts/                  # سكريبتات مساعدة
│   ├── seed_data.py         # إضافة بيانات أولية
│   ├── start.sh             # سكريبت بدء Linux/Mac
│   └── start.bat            # سكريبت بدء Windows
│
├── Dockerfile               # صورة Docker
├── docker-compose.yml       # تكوين Docker Compose
├── requirements.txt         # تبعيات Python
└── .env                    # متغيرات البيئة
```

---

## 🔧 استكشاف الأخطاء الشائعة

### ❌ المشكلة: "Connection refused" للقاعدة

**✅ الحل:**
```bash
# تأكد من تشغيل PostgreSQL
docker-compose ps

# أعد التشغيل:
docker-compose restart db

# أو شغّل من جديد:
docker-compose down -v && docker-compose up --build
```

### ❌ المشكلة: المنفذ 8000 قيد الاستخدام

**✅ الحل:**
```bash
# استخدم منفذ مختلف:
uvicorn app.main:app --reload --port 8001

# أو أغلق العملية القديمة
# على Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### ❌ المشكلة: "ModuleNotFoundError" عند البدء

**✅ الحل:**
```bash
# تأكد من تفعيل البيئة الافتراضية:
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# أعد تثبيت التبعيات:
pip install -r requirements.txt
```

### ❌ المشكلة: الواجهة الأمامية لا تحمل

**✅ الحل:**
1. تحقق من أن الخادم يعمل بشكل صحيح
2. امسح ذاكرة التخزين المؤقت: `Ctrl+Shift+Delete`
3. جرّب متصفح مختلف
4. تحقق من وحدة تحكم المتصفح للأخطاء: `F12`

---

## 🎓 الخطوات التالية

### بعد التشغيل الناجح:

1. **استكشف الواجهة الأمامية**
   - تصفح الصفحة الرئيسية
   - جرّب تسجيل حساب جديد
   - تسجيل الدخول واختبر لوحة التحكم

2. **اختبر API**
   - انتقل إلى http://localhost:8000/docs
   - جرّب المحاولات المختلفة
   - أضف مهارات جديدة

3. **أضف بيانات حقيقية**
   - أنشئ عدة حسابات اختبار
   - أنشئ ملفات مدربين
   - ابدأ طلبات التدريب

4. **خصص التطبيق**
   - عدّل الألوان والنصوص في `style.css`
   - أضف مهارات جزائرية أكثر
   - أضف ميزات جديدة

---

## 📚 موارد إضافية

- **SETUP.md**: دليل شامل للإعداد والنشر
- **README.md**: معلومات المشروع الكاملة
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **FastAPI**: https://fastapi.tiangolo.com
- **SQLAlchemy**: https://docs.sqlalchemy.org

---

## 🚀 النشر للإنتاج

### على Render.com:

```bash
# 1. ادفع الكود إلى GitHub
git add .
git commit -m "SkillUp Full Stack"
git push origin main

# 2. انشئ خدمة جديدة على Render
# - اختر "Web Service"
# - ربط مستودع GitHub
# - اختر Python كبيئة التشغيل
# - أضف متغيرات البيئة

# 3. التطبيق سيُنشر تلقائياً
```

### على Heroku:

```bash
# 1. ثبّت Heroku CLI
# 2. سجّل دخول:
heroku login

# 3. أنشئ تطبيق:
heroku create skillup-app

# 4. أضف متغيرات البيئة:
heroku config:set SECRET_KEY="your-secret-key"
heroku config:set DATABASE_URL="postgresql://..."

# 5. ادفع الكود:
git push heroku main
```

---

## ✅ قائمة التحقق

- [ ] تم تثبيت Python 3.9+
- [ ] تم إنشاء بيئة افتراضية
- [ ] تم تثبيت التبعيات
- [ ] تم إنشاء ملف .env
- [ ] يعمل الخادم بدون أخطاء
- [ ] يمكن الوصول للواجهة الأمامية
- [ ] يمكن تسجيل حساب جديد
- [ ] يمكن تسجيل الدخول
- [ ] يظهر API Docs بشكل صحيح
- [ ] تم إضافة بيانات أولية

---

## 🤝 المساهمة والدعم

- وجدت مشكلة؟ أنشئ issue على GitHub
- هل لديك فكرة؟ أنشئ pull request
- تحتاج مساعدة؟ تحقق من التوثيق أولاً

---

**🎉 مبروك! لديك الآن منصة تدريب جزائرية متكاملة وجاهزة للاستخدام!**

ابدأ الآن:
```bash
docker-compose up --build
# أو
uvicorn app.main:app --reload
```

ثم اذهب إلى: **http://localhost:8000** 🚀
