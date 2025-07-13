import pandas as pd
from bs4 import BeautifulSoup
import re


def extract_text_from_html(html_file, output_excel='output.xlsx', output_csv='output.csv'):
    """
    استخراج متن از تگ‌های HTML با ساختار مشخص و ذخیره در Excel و CSV

    Args:
        html_file (str): مسیر فایل HTML ورودی
        output_excel (str): نام فایل Excel خروجی
        output_csv (str): نام فایل CSV خروجی
    """
    # خواندن فایل HTML
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # استفاده از BeautifulSoup برای تجزیه HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # الگوی regex برای یافتن تگ‌های مورد نظر
    pattern = re.compile(r'class="kt-control-row__title">(.*?)</p>', re.DOTALL)
    matches = pattern.findall(str(soup))

    # تمیز کردن متن‌های استخراج شده
    cleaned_matches = []
    for text in matches:
        # حذف فاصله‌های اضافی و کاراکترهای خاص
        cleaned_text = ' '.join(text.split()).strip()
        cleaned_matches.append(cleaned_text)

    # ایجاد DataFrame از داده‌های استخراج شده
    df = pd.DataFrame(cleaned_matches, columns=['Extracted Text'])

    # ذخیره در فایل Excel (بدون پارامتر encoding)
    df.to_excel(output_excel, index=False)

    # ذخیره در فایل CSV (با encoding)
    df.to_csv(output_csv, index=False, encoding='utf-8-sig')

    print(f"داده‌ها