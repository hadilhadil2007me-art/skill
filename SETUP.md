# SkillUp - Complete Setup Guide

SkillUp هي منصة جزائرية كاملة (Full Stack) لربط الشباب بالمهنيين والحرفيين للتدريب الميداني.

## المميزات الرئيسية

✅ **Backend API متكامل** - FastAPI مع JWT Authentication و Role-Based Access  
✅ **Frontend كامل** - HTML/CSS/JavaScript مع واجهة عربية RTL  
✅ **قاعدة بيانات** - PostgreSQL مع SQLAlchemy و Alembic Migrations  
✅ **Docker Support** - Docker Compose للتطوير والإنتاج  
✅ **API Documentation** - Swagger/OpenAPI للتوثيق التفاعلي  

---

## البدء السريع (بدون Docker)

### 1. تثبيت المتطلبات

```bash
# أنشئ بيئة افتراضية
python -m venv .venv

# تفعيل البيئة الافتراضية
# على Windows:
.venv\Scripts\activate
# على Linux/Mac:
source .venv/bin/activate

# ثبت التبعيات
pip install -r requirements.txt
```

### 2. إعداد متغيرات البيئة

```bash
# انسخ ملف المثال (إن لم يكن موجوداً):
# انسخ .env.example إلى .env أو تجاهل (البرنامج سيستخدم القيم الافتراضية)
```

### 3. تشغيل التطبيق

```bash
# تأكد من أنك في المجلد الجذر:
cd /path/to/skillup

# شغّل الخادم:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. الوصول للتطبيق

- **الواجهة الأمامية**: http://localhost:8000
- **توثيق API (Swagger)**: http://localhost:8000/docs
- **توثيق API (ReDoc)**: http://localhost:8000/redoc

---

## البدء باستخدام Docker

### المتطلبات

- Docker و Docker Compose مثبتة

### خطوات التشغيل

```bash
# 1. اذهب إلى مجلد المشروع
cd /path/to/skillup

# 2. اِبدأ الخدمات
docker-compose up --build

# يسينتظر التطبيق تجاهز قاعدة البيانات تلقائياً ثم يبدأ
```

### الوصول للتطبيق

- **التطبيق**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **قاعدة البيانات**: localhost:5432 (PostgreSQL)

### الإيقاف

```bash
# أوقف جميع الخدمات:
docker-compose down

# أوقف مع حذف البيانات:
docker-compose down -v
```

---

## إضافة بيانات أولية (Seeds)

### إنشاء مهارات افتراضية

قم بتشغيل هذا السكريبت لإضافة مهارات افتراضية:

```bash
python -m scripts.seed_skills
```

أو استخدم API مباشرة:

```bash
curl -X POST http://localhost:8000/api/v1/skills \
  -H "Content-Type: application/json" \
  -d '{"name": "الكهرباء", "description": "تدريب في مجال الكهرباء"}' \
  -H "Authorization: Bearer <YOUR_ADMIN_TOKEN>"
```

---

## حسابات الاختبار التلقائية

عند بدء التطبيق، سيتم إنشاء حساب مسؤول تلقائياً:

**البريد الإلكتروني**: `admin@skillup.dz`  
**كلمة المرور**: `admin_secure_password_99` (يمكن تغييرها من `.env`)

### اختبار تسجيل الدخول

1. اذهب إلى http://localhost:8000/login.html
2. استخدم بيانات المسؤول أعلاه
3. أو استخدم بيانات التجربة (Demo):
   - **متدرب تجريبي**: `youcef@skillup.dz` / `Demo@2025`
   - **مدرب تجريبي**: `fatima@skillup.dz` / `Demo@2025`

---

## هيكل المشروع

```
skillup/
├── app/                      # كود التطبيق الرئيسي
│   ├── main.py              # نقطة دخول FastAPI
│   ├── auth/                # مصادقة JWT و Role-based access
│   ├── core/                # إعدادات الأمان والتكوين
│   ├── database/            # اتصال قاعدة البيانات
│   ├── models/              # نماذج SQLAlchemy
│   ├── routes/              # مسارات API
│   ├── schemas/             # Pydantic schemas للتحقق
│   └── services/            # منطق العمل
│
├── alembic/                 # إدارة الهجرات
│
├── assets/                  # موارد إضافية
├── scripts/                 # سكريبتات المساعدة
│
├── frontend/                # الواجهة الأمامية (HTML/JS)
│   ├── index.html          # الصفحة الرئيسية
│   ├── login.html          # صفحة تسجيل الدخول
│   ├── register.html       # صفحة التسجيل
│   ├── dashboard.html      # لوحة التحكم
│   ├── api.js              # عميل API
│   ├── app.js              # جافا سكريبت عام
│   ├── style.css           # أنماط CSS
│   └── pages.css           # أنماط الصفحات
│
├── Dockerfile              # صورة Docker
├── docker-compose.yml      # تكوين Docker Compose
├── requirements.txt        # التبعيات Python
└── .env                    # متغيرات البيئة
```

---

## نقاط النهاية الرئيسية للـ API

### المصادقة
- `POST /api/v1/auth/register` - تسجيل مستخدم جديد
- `POST /api/v1/auth/login` - تسجيل دخول (إرجاع JWT)
- `GET /api/v1/users/me` - الحصول على بيانات المستخدم الحالي

### المهارات
- `GET /api/v1/skills` - قائمة جميع المهارات
- `POST /api/v1/skills` - إضافة مهارة جديدة (للمسؤولين فقط)
- `GET /api/v1/skills/{skill_id}` - تفاصيل مهارة
- `PUT /api/v1/skills/{skill_id}` - تحديث مهارة (للمسؤولين فقط)
- `DELETE /api/v1/skills/{skill_id}` - حذف مهارة (للمسؤولين فقط)

### ملفات المدربين
- `GET /api/v1/trainers` - قائمة جميع المدربين
- `GET /api/v1/trainers/me` - ملفي كمدرب
- `POST /api/v1/trainers/me` - إنشاء ملف مدرب
- `PUT /api/v1/trainers/me` - تحديث ملف مدرب
- `GET /api/v1/trainers/{trainer_id}` - تفاصيل مدرب

### طلبات التدريب
- `POST /api/v1/requests` - إرسال طلب تدريب (للمتدربين)
- `GET /api/v1/requests` - قائمة الطلبات الخاصة بي
- `PATCH /api/v1/requests/{request_id}` - قبول/رفض طلب (للمدربين)

### التقييمات
- `POST /api/v1/reviews` - كتابة تقييم (للمتدربين)
- `GET /api/v1/reviews/trainer/{trainer_id}` - تقييمات المدرب

---

## استكشاف الأخطاء

### المشكلة: "Connection refused" عند الاتصال بقاعدة البيانات

**الحل**:
```bash
# تأكد من تشغيل PostgreSQL محلياً أو عبر Docker
docker-compose ps

# أعد تشغيل الخدمات:
docker-compose restart db
```

### المشكلة: المنفذ 8000 قيد الاستخدام

**الحل**:
```bash
# استخدم منفذ مختلف:
uvicorn app.main:app --reload --port 8001

# أو بـ Docker:
# عدّل docker-compose.yml وغيّر المنفذ
```

### المشكلة: خطأ JWT Invalid Token

**الحل**:
- تأكد من أن `SECRET_KEY` في `.env` ثابت
- امسح ملفات تخزين مؤقت المتصفح والـ localStorage
- جرّب تسجيل الدخول مرة أخرى

---

## الخطوات التالية

1. **إضافة المزيد من المهارات** عبر لوحة API
2. **إنشاء عدد من الحسابات التجريبية** للاختبار
3. **تخصيص القوائم والنصوص** حسب احتياجاتك
4. **نشر على Render أو Heroku** لبيئة الإنتاج
5. **إضافة المزيد من الميزات** مثل الإشعارات والدفع

---

## الدعم والمساعدة

- **التوثيق الكاملة**: http://localhost:8000/docs
- **الملفات الأساسية**:
  - `app/main.py` - معالج التطبيق الرئيسي
  - `app/routes/` - نقاط نهاية API
  - `app/models/` - نماذج قاعدة البيانات

---

**هل أنت جاهز؟ ابدأ الآن! 🚀**

```bash
# البدء السريع:
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

أو استخدم Docker:

```bash
docker-compose up --build
```

ثم اذهب إلى http://localhost:8000 🎉
