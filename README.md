# 🧠 محلل المشاعر | Sentiment Analyzer

تطبيق ويب لتحليل مشاعر النصوص بأكثر من 20 لغة باستخدام Claude AI و Flask.

---

## 📁 هيكل المشروع

```
sentiment_project/
├── app.py                 ← السيرفر الخلفي (Flask)
├── requirements.txt       ← المكتبات المطلوبة
├── Procfile               ← للنشر على Render/Railway
├── .env.example           ← نموذج إعدادات البيئة
├── .gitignore             ← ملفات يجب استثناؤها من Git
├── README.md              ← هذا الملف
└── templates/
    └── index.html         ← الواجهة الأمامية
```

---

## 🚀 التشغيل المحلي

### 1. استنسخ المشروع
```bash
git clone https://github.com/username/sentiment-analyzer.git
cd sentiment-analyzer
```

### 2. أنشئ بيئة افتراضية
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. ثبّت المكتبات
```bash
pip install -r requirements.txt
```

### 4. أعدّ مفتاح API
```bash
cp .env.example .env
```
افتح ملف `.env` وأضف مفتاحك من https://console.anthropic.com/settings/keys:
```
ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXX
```

### 5. شغّل السيرفر
```bash
python app.py
```
افتح المتصفح على: **http://localhost:5000**

---

## ☁️ النشر على Render (مجاني)

### 1. ارفع المشروع على GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/sentiment-analyzer.git
git push -u origin main
```
> ⚠️ تأكد أن `.env` موجود في `.gitignore` ولم يُرفع!

### 2. أنشئ حساباً على Render
- اذهب إلى: https://render.com
- سجّل دخول بحساب GitHub

### 3. أنشئ Web Service جديد
- New → Web Service
- اختر repository المشروع
- الإعدادات:
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn app:app`
  - **Environment:** Python 3

### 4. أضف متغيرات البيئة
في لوحة Render → Environment → Add:
```
ANTHROPIC_API_KEY = sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXX
```

### 5. انشر! 🎉
سيعطيك Render رابطاً مثل: `https://sentiment-analyzer.onrender.com`

---

## 🔒 أمان API Key

| ✅ آمن | ❌ خطر |
|--------|--------|
| متغير بيئة `.env` | في الكود مباشرة |
| Environment Variables في Render | في ملف HTML |
| Backend فقط يرى المفتاح | في Git/GitHub |

---

## 🛠️ التقنيات المستخدمة

- **Backend:** Python, Flask, Anthropic SDK
- **Frontend:** HTML, CSS, JavaScript
- **AI Model:** Claude claude-sonnet-4-20250514
- **Deployment:** Render / Railway / Heroku
- **NLP Task:** Multilingual Sentiment Analysis

---

## 📊 API Endpoints

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/` | الصفحة الرئيسية |
| POST | `/api/analyze` | تحليل النص |
| GET | `/api/health` | فحص حالة السيرفر |

### مثال على طلب API:
```bash
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "المنتج رائع!", "text_lang": "ar", "response_lang": "Arabic"}'
```

---

## 👨‍💻 المطوّر

مشروع تعليمي في إطار تعلم **Data Science & NLP**
