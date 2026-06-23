# SkillUp Backend (FastAPI)

وصف المشروع:
SkillUp هو منصة جزائرية تربط الشباب بالحرفيين والمهنيين لاكتساب خبرة عملية وتدريب ميداني.

Automation scripts (run locally)

1) Push repository to GitHub (set `GITHUB_REPO` first):

```bash
export GITHUB_REPO="https://github.com/yourusername/skillup.git"
./scripts/push_to_github.sh
```

2) Set GitHub secrets using `gh` CLI (login with `gh auth login` first):

```bash
export DOCKERHUB_USERNAME="your_dockerhub_username"
export DOCKERHUB_TOKEN="your_dockerhub_token"
# optional:
export RENDER_API_KEY="<render api key>"
export RENDER_SERVICE_ID="<render service id>"
./scripts/setup_github_secrets.sh
```

3) Trigger a Render deploy manually (if you have `RENDER_API_KEY` and `RENDER_SERVICE_ID`):

```bash
export RENDER_API_KEY="..."
export RENDER_SERVICE_ID="..."
./scripts/trigger_render.sh
```

Notes:
- `gh` CLI is required for `./scripts/setup_github_secrets.sh`.
- `jq` is recommended for `./scripts/trigger_render.sh` output formatting.

التقنيات المستخدمة:
- Python + FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic (migrations)
- JWT Authentication
- Docker + docker-compose

الملفات والمجلدات الأساسية:
- `app/` : كود التطبيق الرئيسي (models, schemas, routes, services, auth, core, database)
- `alembic/` : إعدادات وملفات الهجرة
- `Dockerfile`, `docker-compose.yml` : تشغيل الحاويات
- `requirements.txt` : تبعيات Python

النماذج الأساسية في قاعدة البيانات:
- `User` (admin, trainer, trainee)
- `Skill`
- `TrainerProfile`
- `TrainingRequest`
- `Review`

المزايا المدعومة:
- تسجيل دخول وتسجيل مستخدمين
- مصادقة JWT
- صلاحيات دورية (Role-based)
- CRUD للمهارات
- CRUD لملف المدرب
- إنشاء وادارة طلبات التدريب
- التقييمات والمراجعات
- توثيق OpenAPI (Swagger)

إعداد سريع (باستخدام Docker)

1) نسخ المثال للبيئة:

```bash
cp .env.example .env
```

2) تشغيل الحاويات (وسيقوم `web` بالانتظار لحين جاهزية قاعدة البيانات):

```bash
docker-compose up --build
```

3) الوصول إلى API:
- توثيق Swagger: http://localhost:8000/docs
- واجهة الحالة: http://localhost:8000/

تشغيل محلي بدون Docker

1) أنشئ بيئة افتراضية وثبت التبعيات:

```bash
python -m venv .venv
source .venv/bin/activate   # أو on Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

2) إعداد متغيرات البيئة: أنشئ `.env` بمحتوى مماثل لـ `.env.example`.

3) تشغيل السيرفر:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

قاعدة البيانات والهجرات (Alembic)

1) إعداد `.env` لربط قاعدة البيانات التي تريدها (Postgres أو SQLite). مثال Postgres:

```text
DATABASE_URL=postgresql://postgres:postgres_password@db:5432/skillup
```

2) إذا استخدمت Docker، شغّل الحاويات أولاً ثم نفّذ الهجرات داخل حاوية `web`:

```bash
docker compose exec web alembic upgrade head
```

3) إذا تعمل محليًا (بدون Docker) وتريد تشغيل الهجرات مباشرة من جهازك:

```bash
# بعد تفعيل .venv وتعديل .env
alembic upgrade head
```

ملاحظة عن الوضع الحالي للتشغيل السريع

لراحة العرض المحلي قمت مؤقتًا بجعل `DATABASE_URL` الافتراضي في المشروع يشير إلى SQLite (`sqlite:///./skillup.db`) حتى يعمل التطبيق فورًا دون إعداد Postgres أو Docker. هذا مناسب للاختبار المحلي وتطوير الواجهات. قبل نشر الإنتاج، استبدل `DATABASE_URL` بقاعدة Postgres مناسبة وشغّل:

```bash
alembic upgrade head
```

زراعة المستخدم الإداري

يمكنك ضبط `FIRST_SUPERUSER_EMAIL` و `FIRST_SUPERUSER_PASSWORD` في `.env`؛ التطبيق سيحاول زراعته تلقائياً عند التشغيل إذا لم يوجد.

نقل البيانات من SQLite إلى Postgres

إذا بدأت محلياً على SQLite ثم قررت الانتقال إلى Postgres لاحقًا، اصدر بياناتك أو اكتب سكربت لنقل الجداول — Alembic لن ينقل البيانات تلقائياً بين محركات قواعد البيانات.

جعل الموقع متاحًا عبر الإنترنت (مباشر)

خيار سريع (تجريبي) — استخدام `ngrok` لفتح نفق من جهازك المحلي:

1) حمّل ngrok وسجّل دخولك: https://ngrok.com/
2) شغل السيرفر محليًا (كما في الأعلى).
3) افتح نفق HTTP إلى المنفذ 8000:

```bash
ngrok http 8000
```

4) سيعطيك ngrok عنوانًا عامًّا مثل `https://abcd-12-34-56.ngrok.io` — أرسل هذا الرابط لأي شخص ليصل إلى موقعك (مؤقت).

نشر سريع عبر Render (مثال)

1) ادفع المستودع إلى GitHub.
2) في Render، اختر "New Web Service" ثم "Connect a repository".
3) اختر بناء من Dockerfile أو ارفع `render.yaml` الموجود في المشروع.
4) أضف متغيرات البيئة (`DATABASE_URL`, `SECRET_KEY`, `FIRST_SUPERUSER_EMAIL`, `FIRST_SUPERUSER_PASSWORD`) ضمن إعدادات الخدمة.
5) بعد النشر، شغّل الهجرات عبر لوحة Render أو قم بإضافة خطوة بدء (build command) لتشغيل `./run_migrations.sh` قبل بدء الخادم.

خيار الإنتاج — نشر دائم

- Render / Railway: ربط المستودع (GitHub) وسيقوم النظام بإنشاء حاوية وتشغيل التطبيق تلقائياً. استخدم `Dockerfile` الموجود أو إعداد `Python` مع أمر تشغيل `uvicorn app.main:app`.
- يمكنك أيضًا بناء صورة Docker ودفعها إلى Docker Hub ثم نشرها إلى أي مزود سحابي.

نصيحة أمان

لا تعرض بيئة التطوير (قيم `.env` حاملة لمفاتيح أو كلمات مرور) مباشرة للعامة. استخدم متغيّرات بيئة آمنة في خدمة النشر واختر `SECRET_KEY` قويًا.

قاعدة البيانات والهجرات (Alembic)

1) تهيئة (عند الحاجة) وتطبيق الهجرات:

```bash
alembic upgrade head
```

ملاحظة: المشروع يحتوي على استدعاء تلقائي لإنشاء الجداول (`Base.metadata.create_all`) عند تشغيل التطبيق كبديل مؤقت إن لم تُشغّل الهجرات.

إنشاء/تهيئة مستخدم المدير (Superuser)

يمكنك تعيين `FIRST_SUPERUSER_EMAIL` و `FIRST_SUPERUSER_PASSWORD` في `.env`؛ التطبيق سيقوم بزراعته تلقائياً عند بداية التشغيل إذا لم يكن موجودا.

نظرة عامة على المصادقة

- تسجيل مستخدم: POST `/api/v1/auth/register` مع بيانات `UserCreate`.
- تسجيل دخول: POST `/api/v1/auth/login` باستخدام `application/x-www-form-urlencoded` (OAuth2 password grant).
- الرأس للاستخدام: `Authorization: Bearer <access_token>`

نماذج طلبات سريعة (curl)

1) تسجيل:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" -H "Content-Type: application/json" -d '{"email":"user@example.com","full_name":"User Name","password":"secret123","role":"trainee"}'
```

2) تسجيل دخول:

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" -F "username=user@example.com" -F "password=secret123"
```

3) طلب محمي:

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/users/me
```

نصائح وأفضل ممارسات

- لا تستخدم مفاتيح `SECRET_KEY` الواردة في المثال في بيئة الإنتاج؛ استعمل قيمة قوية عشوائية.
- في الإنتاج قم بتقييد `CORS` بدلاً من `allow_origins=["*"]`.
- شغّل Alembic لإدارة تغييرات المخطط بدل `create_all` في البيئات الحية.

المزيد من المساعدة

أريد أن أساعدك بتشغيل الحاويات أو تنفيذ الهجرات الآن — هل تريد أن أشغّل `docker-compose up` هنا، أم تفضل تعليمات محلية؟

---

النشر من GitHub إلى Render (خطوات عملية)

1) ادفع المستودع إلى GitHub:

```bash
git remote add origin https://github.com/yourusername/skillup.git
git branch -M main
git push -u origin main
```

2) في Render: اختر "New Web Service" → "Connect a repository" → حدّد المستودع.

3) أضف متغيرات البيئة في Render (Settings → Environment):
- `DATABASE_URL` (Postgres)
- `SECRET_KEY` (سري قوي)
- `FIRST_SUPERUSER_EMAIL` و `FIRST_SUPERUSER_PASSWORD`

4) (اختياري) إعداد نشر آلي عبر GitHub Actions وDocker Hub:
- أضف أسرار GitHub repository: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`.
- إذا أردت أن يطلب GitHub نشرًا لدى Render بعد بناء الصورة، أضف أيضًا `RENDER_API_KEY` و `RENDER_SERVICE_ID` كأسرار/متغيرات بيئة.

بعد الخطوات أعلاه، كل دفعة إلى `main` ستبني صورة Docker وتدفعها إلى Docker Hub، ويمكن أن تطلب نشرًا في Render (إن أعددت الأسرار). بهذه الطريقة، إذا أعطيت أي شخص رابط المستودع على GitHub ثم ربطته بـ Render، سيعمل الموقع ويمكن للمستخدمين إنشاء حسابات عبر صفحات الواجهة.
