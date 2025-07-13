#!/usr/bin/env python3
"""
اسکریپت اجرای اسکرپر دیوار مشهد
"""

import sys
import os

# اضافه کردن مسیر src به PATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from scraper import main

if __name__ == '__main__':
    print("🚀 شروع اسکرپر دیوار مشهد...")
    main()
    print("✅ اسکرپینگ کامل شد!") 