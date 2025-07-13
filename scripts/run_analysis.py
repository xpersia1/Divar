#!/usr/bin/env python3
"""
اسکریپت اجرای تحلیل داده
"""

import sys
import os

# اضافه کردن مسیر src به PATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# تغییر مسیر کاری به src
os.chdir(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pandas

if __name__ == '__main__':
    print("📊 شروع تحلیل داده‌ها...")
    # اجرای کد pandas.py
    exec(open('pandas.py').read())
    print("✅ تحلیل داده‌ها کامل شد!") 