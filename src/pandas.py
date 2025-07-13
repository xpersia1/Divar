import pandas as pd

# بارگذاری داده‌ها
df = pd.read_csv('../data/raw/divar_mashhad_cleaned.csv')

# محاسبه میانگین قیمت هر متر در هر محله
region_avg = df.groupby('محله')['قیمت هر متر'].mean()

# اضافه کردن ستون ارزش خرید
df['ارزش خرید'] = df['قیمت هر متر'] / df['محله'].map(region_avg)

# مرتب‌سازی بر اساس ارزش خرید (کمترین قیمت نسبت به منطقه)
best_houses = df.sort_values('ارزش خرید', ascending=True).head(20)

# ذخیره نتایج
best_houses.to_csv('../data/raw/best_value_houses.csv', index=False, encoding='utf-8-sig')

print("✅ بهترین خانه‌های با ارزش خرید بالا ذخیره شدند.")
