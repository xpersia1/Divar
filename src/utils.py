import re
import os
import pandas as pd
from typing import Optional, Dict, Any

def convert_price(price_text: str) -> Optional[int]:
    """
    تبدیل متن قیمت به عدد صحیح
    
    Args:
        price_text: متن قیمت (مثل "2,500,000,000 تومان")
    
    Returns:
        عدد قیمت یا None در صورت خطا
    """
    try:
        price_text = re.sub(r'[^\d]', '', price_text)
        return int(price_text) if price_text else None
    except:
        return None

def create_directories(*paths: str) -> None:
    """
    ایجاد پوشه‌های مورد نیاز
    
    Args:
        *paths: مسیرهای پوشه‌ها
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)

def save_dataframe(df: pd.DataFrame, filepath: str, **kwargs) -> None:
    """
    ذخیره DataFrame در فایل
    
    Args:
        df: DataFrame برای ذخیره
        filepath: مسیر فایل
        **kwargs: پارامترهای اضافی برای ذخیره
    """
    if df.empty:
        print("⚠️ DataFrame خالی است.")
        return
    
    # ایجاد پوشه اگر وجود نداشته باشد
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if filepath.endswith('.csv'):
        df.to_csv(filepath, index=False, encoding='utf-8-sig', **kwargs)
    elif filepath.endswith('.xlsx'):
        df.to_excel(filepath, index=False, engine='openpyxl', **kwargs)
    else:
        raise ValueError("فرمت فایل پشتیبانی نمی‌شود. از .csv یا .xlsx استفاده کنید.")
    
    print(f"✅ داده‌ها در {filepath} ذخیره شدند.")

def clean_text(text: str) -> str:
    """
    پاک‌سازی متن از کاراکترهای خاص
    
    Args:
        text: متن ورودی
    
    Returns:
        متن پاک‌سازی شده
    """
    return re.sub(r'[*_`]', '', text)

def format_price(price: int) -> str:
    """
    فرمت کردن قیمت با کاما
    
    Args:
        price: قیمت عددی
    
    Returns:
        قیمت فرمت شده
    """
    return f"{price:,} تومان" 