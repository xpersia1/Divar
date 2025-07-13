# 🔍 اسکریپر دیوار مشهد با توضیحات خط‌به‌خط

# کتابخانه‌های استاندارد پایتون
import time  # برای زمان‌سنجی و توقف اجرای کد
import pandas as pd  # تحلیل داده و کار با DataFrame
import numpy as np  # عملیات ریاضی و آماری
import matplotlib.pyplot as plt  # رسم نمودار
import seaborn as sns  # زیباسازی نمودارهای matplotlib

# کتابخانه‌های selenium برای اتوماسیون مرورگر
from selenium import webdriver  # برای کنترل مرورگر کروم
from selenium.webdriver.common.by import By  # برای انتخاب المنت‌ها
from selenium.webdriver.chrome.options import Options  # تنظیمات کروم
from selenium.webdriver.chrome.service import Service  # مدیریت سرویس درایور
from webdriver_manager.chrome import ChromeDriverManager  # دانلود خودکار chromedriver
from selenium.webdriver.common.action_chains import ActionChains  # برای اجرای اسکرول واقعی
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin  # نقطه شروع اسکرول

# کتابخانه‌های جانبی
import re  # برای پردازش متنی و استفاده از regex
import os  # برای ساختن پوشه ذخیره فایل‌ها
import warnings  # برای جلوگیری از نمایش هشدارها
from selenium.common.exceptions import NoSuchElementException  # مدیریت خطای نبود المنت
from selenium_stealth import stealth  # برای جلوگیری از شناسایی توسط سایت دیوار


# 🚫 حذف هشدارهای غیر ضروری

def suppress_warnings():
    warnings.filterwarnings("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning)

suppress_warnings()


# ⚙️ تنظیمات اولیه مرورگر کروم

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # جلوگیری از ارور در برخی سیستم‌ها
    chrome_options.add_argument('--disable-dev-shm-usage')  # برای جلوگیری از محدودیت فضای اشتراکی
    # معرفی User-Agent معتبر برای دور زدن ربات‌دیتکشن
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # غیرفعال کردن تشخیص ربات

    # راه‌اندازی مرورگر کروم با stealth
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_size(1920, 1080)  # تعیین اندازه پنجره مرورگر
    driver.maximize_window()  # تمام‌صفحه کردن مرورگر

    # اطلاعات ساختگی برای مخفی‌کاری بیشتر
    stealth(driver,
            languages=["fa-IR", "fa"],
            vendor="Google Inc.",
            platform="MacIntel",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True)
    return driver


# 💰 تابعی برای تبدیل قیمت به عدد صحیح

def convert_price(price_text):
    try:
        price_text = re.sub(r'[^\d]', '', price_text)  # حذف هر چیزی غیر از عدد
        return int(price_text) if price_text else None
    except:
        return None


# 📜 اسکرول خودکار همراه با استخراج همزمان آگهی‌ها

def scroll_and_collect_ads(driver, pause_time=4, scroll_step=1000, max_tries=40, max_time=90):
    start_time = time.time()
    tries = 0
    last_ad_count = 0
    processed_links = set()  # لینک‌های دیده شده برای حذف تکراری‌ها
    data = []  # لیست نهایی آگهی‌ها

    body = driver.find_element(By.TAG_NAME, 'body')
    actions = ActionChains(driver)

    while tries < max_tries and time.time() - start_time < max_time:
        # اسکرول نرم و تدریجی
        scroll_origin = ScrollOrigin.from_element(body)
        actions.scroll_from_origin(scroll_origin, 0, scroll_step).perform()
        time.sleep(pause_time)

        ads = driver.find_elements(By.CSS_SELECTOR, 'article.unsafe-kt-post-card')
        print(f"\U0001F4CA آگهی‌های موجود در DOM: {len(ads)}")

        for ad in ads:
            try:
                link = ad.find_element(By.CSS_SELECTOR, 'a.unsafe-kt-post-card__action').get_attribute('href')
                if link in processed_links:
                    continue  # تکراری‌ها حذف شوند

                title = ad.find_element(By.CSS_SELECTOR, 'h2.unsafe-kt-post-card__title').text
                price = ad.find_element(By.CSS_SELECTOR, 'div.unsafe-kt-post-card__description').text
                location = ad.find_element(By.CSS_SELECTOR, 'span.unsafe-kt-post-card__bottom-description').text
                price_value = convert_price(price)

                data.append({
                    'عنوان': title,
                    'قیمت': price_value,
                    'محله': location,
                    'لینک': link
                })
                processed_links.add(link)
                print(f"📝 آگهی: {title}, قیمت: {price_value}, محله: {location}")
            except:
                continue

        # توقف در صورت عدم تغییر آگهی
        if len(ads) == last_ad_count:
            tries += 1
        else:
            tries = 0
        last_ad_count = len(ads)

    print(f"✅ اسکرول و جمع‌آوری کامل شد. تعداد آگهی‌ها: {len(data)}")
    return data


# 📥 استخراج اولیه از دیوار

def scrape_divar_mashhad(url, ad_limit=1000):
    driver = setup_driver()
    driver.get(url)
    time.sleep(15)
    print("\U0001F501 شروع اسکرول و جمع‌آوری آگهی‌ها...")
    data = scroll_and_collect_ads(driver)
    driver.quit()
    df = pd.DataFrame(data)
    return df.head(ad_limit)


# 🧹 پاک‌سازی داده‌ها

def clean_data(df):
    if df.empty:
        print("⚠️ دیتافریم خالی است.")
        return df

    print(f"\U0001F4CA آگهی قبل از پاک‌سازی: {len(df)}")
    df = df.dropna(subset=['قیمت'])
    df = df[(df['قیمت'] >= 500_000_000) & (df['قیمت'] <= 200_000_000_000)]
    df['متراژ'] = df['عنوان'].str.extract(r'(\d+)\s*متر').astype(float)
    df['تعداد اتاق'] = df['عنوان'].str.extract(r'(\d+)\s*خوابه').astype(float)
    df['قیمت هر متر'] = df.apply(lambda x: x['قیمت'] / x['متراژ'] if pd.notnull(x['متراژ']) else None, axis=1)

    # حذف داده‌های پرت (outlier)
    if df['قیمت هر متر'].notnull().sum() > 0:
        Q1 = df['قیمت هر متر'].quantile(0.25)
        Q3 = df['قیمت هر متر'].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df['قیمت هر متر'] >= Q1 - 1.5 * IQR) | df['قیمت هر متر'].isnull()]

    return df


# 📊 تحلیل و ذخیره نمودار

def analyze_data(df):
    if df.empty:
        print("⚠️ دیتافریم خالی است.")
        return

    print(f"💰 مجموع قیمت: {df['قیمت'].sum():,.0f} تومان")
    print(f"میانگین قیمت هر متر: {df['قیمت هر متر'].mean():,.0f}")

    # رسم نمودار هیستوگرام
    plt.figure(figsize=(10, 6))
    sns.histplot(df['قیمت هر متر'].dropna(), bins=30, kde=True)
    plt.title('توزیع قیمت هر متر')
    plt.savefig('data/plots/price_distribution.png')

    # رسم باکس‌پلات
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df['قیمت هر متر'].dropna())
    plt.title('باکس‌پلات قیمت هر متر')
    plt.savefig('data/plots/price_boxplot.png')

    # پراکندگی قیمت بر اساس متراژ و تعداد اتاق
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='متراژ', y='قیمت', hue='تعداد اتاق', size='تعداد اتاق', data=df)
    plt.title('پراکندگی قیمت نسبت به متراژ')
    plt.savefig('data/plots/price_vs_area.png')


# 🚀 اجرای همه مراحل

def main():
    url = 'https://divar.ir/s/mashhad/buy-apartment'
    print("🚀 شروع استخراج داده‌ها...")
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/plots', exist_ok=True)

    df = scrape_divar_mashhad(url)
    print("🧹 پاک‌سازی داده‌ها...")
    df_cleaned = clean_data(df)

    print("📈 تحلیل داده‌ها...")
    analyze_data(df_cleaned)

    if not df_cleaned.empty:
        df_cleaned.to_csv('data/raw/divar_mashhad_cleaned.csv', index=False, encoding='utf-8-sig')
        df_cleaned.to_excel('data/raw/divar_mashhad_cleaned.xlsx', index=False, engine='openpyxl')
        print("📁 داده‌ها ذخیره شدند.")
    else:
        print("⚠️ هیچ داده‌ای برای ذخیره وجود ندارد.")


# شروع اجرای برنامه
if __name__ == '__main__':
    main()
