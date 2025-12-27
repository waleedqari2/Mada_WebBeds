```markdown
# Hotel Scraper (dotwconnect) — Setup & Run

ملخص
- مشروع لاستخراج أسعار الغرف من صفحات `dotwconnect` (hotel-details).
- يتضمن API (FastAPI) وملفات مساعدة لاستخدام Selenium (Chrome).

الخطوات السريعة (محلي)

1. إنشاء بيئة افتراضية وتثبيت المتطلبات
```bash
python -m venv .venv
# على Windows: .venv\Scripts\activate
# على macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
```

2. إعداد المتغيّرات (انسخ المثال وحرّر القيم إذا لزم)
```bash
cp .env.example .env
# ثم افتح .env وعدّل القيم مثل CHROMEDRIVER_PATH أو HEADLESS
```

ملاحظات عن ChromeDriver
- خياران:
  1. تعيين CHROMEDRIVER_PATH في `.env` لمسار chromedriver المثبت محليًا.
  2. عدم تعيين PATH واستخدام webdriver-manager (المكوّن `selenium_client.py` يدعم هذا تلقائيًا).

3. تشغيل الـ API (تطوّري)
```bash
# اجعل start.sh قابلاً للتنفيذ أولاً
chmod +x start.sh
./start.sh
# أو تشغيل مباشرة:
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

4. خطوات ما بعد التشغيل
- افتح http://127.0.0.1:8000/docs لاستعراض واجهات الـ API.
- ارفع ملف الكوكيز عبر endpoint `/cookies` (إن وُجد في مشروعك) أو ضع `cookies.json` في المسار المشار إليه بـ `COOKIE_FILE` داخل `.env`.
- جرّب endpoint البحث (search) كما صمّمته سابقًا.

نُصُح مهمة قبل التشغيل الكامل
- تأكّد أن الكوكيز صالحة لعرض الأسعار (جلسة مسجّلة).
- جرّب سكربت `scraping/selenium_client.py` على رابط واحد للتحقّق من XPATHs.
- حدّث ChromeDriver ليتوافق مع نسخة متصفح Chrome لديك (أو اسمح لـ webdriver-manager بتحميله تلقائيًا).

ملفات مهمة في هذا commit
- requirements.txt
- .env.example
- start.sh
- scraping/selenium_client.py

إذا أردت أكمّل الآن:
- (الآتي) أضيف Logging + retries + فحص صلاحية الكوكيز، أو
- أبدأ بإنشاء Dockerfile لتشغيل موثوق (Chromium + chromedriver + uvicorn).

أعلمني أي خيار تريده أبدأ به بعد ذلك.
```