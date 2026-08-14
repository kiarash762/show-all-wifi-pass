# Show All Wi-Fi Passwords (Python Script)

یک اسکریپت ساده و کاربردی به زبان پایتون (Python) برای استخراج و نمایش تمامی شبکه های Wi-Fi ذخیره شده در سیستم‌عامل ویندو به همراه گذرواژه (Password) آن‌ها.

---

## 📋 توضیح کد و نحوه کار

این اسکریپت با استفاده از کتابخانه داخلی `subprocess` دستورات CLI سیستم‌عامل ویندوز (`netsh wlan show profiles`) را اجرا کرده و لیست تمام پروفایل‌های ذخیره‌شده و رمز عبور آن‌ها را استخراج و نمایش می‌دهد.

### سورس کد پایتون (`show wifi pass.py`)

```python
import subprocess

# دریافت تمامی پروفایل‌های وای‌فای ذخیره شده در سیستم
data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

print(f"{'Wi-Fi Name (SSID)':<30} | {'Password':<20}")
print("-" * 55)

for profile in profiles:
    try:
        # استخراج کلید/گذرواژه مربوط به هر پروفایل
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        try:
            print(f"{profile:<30} | {results[0]:<20}")
        except IndexError:
            print(f"{profile:<30} | {'<No Password/Open>':<20}")
    except subprocess.CalledProcessError:
        print(f"{profile:<30} | {'<Error Fetching>':<20}")
```

---

## 🚀 نحوه اجرا

1. **پیشنیازها:** داشتن پایتون 3 نسخه نصب‌شده روی سیستم‌عامل ویندو.
2. **اجرا:** ترمینال یا CMD را در پوشه پروژه باز کرده و دستور زیر را اجرا کنید:

```bash
python "show wifi pass.py"
```

---

## ⚠️ نکات مهم

- **سیستم‌عامل:** این اسکریپت مخصوص سیستم‌عامل **Windows** است زیرا از ابزار `netsh` استفاده می‌کند.
- **دسترسی (Permissions):** برای نمایش رمزهای عبور برخی از پروفایل‌ها، ممکن است نیاز به اجرای ترمینال به صورت **Administrator** باشد.
