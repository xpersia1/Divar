# تنظیمات پروژه اسکرپر دیوار مشهد

# تنظیمات Selenium
CHROME_OPTIONS = {
    '--no-sandbox': True,
    '--disable-dev-shm-usage': True,
    '--disable-blink-features': 'AutomationControlled'
}

# تنظیمات اسکرپینگ
SCRAPING_CONFIG = {
    'pause_time': 4,
    'scroll_step': 1000,
    'max_tries': 40,
    'max_time': 90,
    'ad_limit': 1000
}

# تنظیمات فیلتر قیمت
PRICE_FILTERS = {
    'min_price': 500_000_000,  # 500 میلیون تومان
    'max_price': 200_000_000_000  # 200 میلیارد تومان
}

# تنظیمات مسیرها
PATHS = {
    'raw_data': 'data/raw',
    'processed_data': 'data/processed',
    'plots': 'data/plots'
}

# تنظیمات تلگرام
TELEGRAM_CONFIG = {
    'token': '8152891768:AAE1zL57parZHZwH0J7djv-e38HliNjaJgk',
    'password': 'secret123'
}

# URL های هدف
URLS = {
    'divar_mashhad': 'https://divar.ir/s/mashhad/buy-apartment'
} 