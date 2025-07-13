#!/usr/bin/env python3
"""
اسکریپت اجرای ربات تلگرام
"""

import sys
import os

# اضافه کردن مسیر src به PATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# تغییر مسیر کاری به src
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'src'))

import Telegram

if __name__ == '__main__':
    print("🤖 راه‌اندازی ربات تلگرام...")
    print("📱 ربات آماده است. در تلگرام رمز عبور را وارد کنید: secret123")
    print("🔗 سپس دستور /start را بفرستید")
    # ربات در Telegram.py اجرا می‌شود 