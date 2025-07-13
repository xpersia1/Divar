import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# مسیری که دادی
data_path = '/Users/x/Divar/src/data/raw/divar_mashhad_cleaned.csv'
output_folder = '/Users/x/Divar/src/data/analysis'
os.makedirs(output_folder, exist_ok=True)

# ---------------------------------------------------
# 1️⃣ Load Data
df = pd.read_csv(data_path)
print("✅ داده‌ها بارگذاری شدند")

# ---------------------------------------------------
# 2️⃣ Descriptive Statistics
desc_stats = df.describe(include='all')
desc_stats.to_csv(os.path.join(output_folder, 'descriptive_stats.csv'), encoding='utf-8-sig')
print("✅ آمار توصیفی ذخیره شد")

# ---------------------------------------------------
# 3️⃣ میانگین قیمت هر متر در هر محله
region_avg = df.groupby('محله')['قیمت هر متر'].mean().sort_values()
region_avg.to_csv(os.path.join(output_folder, 'region_avg_price.csv'), encoding='utf-8-sig')
print("✅ میانگین قیمت هر متر در هر محله ذخیره شد")

# 📌 Plot 1: Average price per meter by region
plt.figure(figsize=(12, 8))
region_avg.plot(kind='barh', color='teal')
plt.title('Average Price per Meter by Region')
plt.xlabel('Price per Meter (Toman)')
plt.ylabel('Region')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot1_avg_price_per_region.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 📌 Plot 2: Histogram of Price per Meter
plt.figure(figsize=(10, 6))
sns.histplot(df['قیمت هر متر'].dropna(), bins=40, color='orange', kde=True)
plt.title('Distribution of Price per Meter')
plt.xlabel('Price per Meter (Toman)')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot2_hist_price_per_meter.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 📌 Plot 3: Boxplot Price per Meter by Region
plt.figure(figsize=(14, 8))
top_regions = df['محله'].value_counts().index[:10]
sns.boxplot(data=df[df['محله'].isin(top_regions)], x='قیمت هر متر', y='محله')
plt.title('Price per Meter by Region (Top 10)')
plt.xlabel('Price per Meter (Toman)')
plt.ylabel('Region')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot3_boxplot_price_per_region.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 📌 Plot 4: Scatter plot of Total Price vs Area
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='متراژ', y='قیمت', alpha=0.6)
plt.title('Total Price vs Area')
plt.xlabel('Area (m²)')
plt.ylabel('Total Price (Toman)')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot4_scatter_totalprice_area.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 📌 Plot 5: Scatter plot of Price per Meter vs Area
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='متراژ', y='قیمت هر متر', alpha=0.6, color='green')
plt.title('Price per Meter vs Area')
plt.xlabel('Area (m²)')
plt.ylabel('Price per Meter (Toman)')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot5_scatter_pricepermeter_area.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 📌 Plot 6: Count of Listings per Region
plt.figure(figsize=(12, 8))
listing_counts = df['محله'].value_counts().sort_values(ascending=True)
listing_counts.plot(kind='barh', color='purple')
plt.title('Number of Listings by Region')
plt.xlabel('Number of Listings')
plt.ylabel('Region')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot6_count_listings_region.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 📌 Plot 7: Count of Listings by Room Count
plt.figure(figsize=(8, 6))
sns.countplot(x='تعداد اتاق', data=df, color='skyblue')
plt.title('Distribution of Room Counts')
plt.xlabel('Number of Rooms')
plt.ylabel('Count')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot7_count_room_numbers.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 📌 Plot 8: Average Price per Meter by Room Count
room_avg = df.groupby('تعداد اتاق')['قیمت هر متر'].mean().sort_index()
plt.figure(figsize=(8, 6))
room_avg.plot(kind='bar', color='coral')
plt.title('Average Price per Meter by Number of Rooms')
plt.xlabel('Number of Rooms')
plt.ylabel('Average Price per Meter (Toman)')
plt.tight_layout()
plt.savefig(os.path.join(output_folder, 'plot8_avg_pricepermeter_rooms.png'), dpi=300)
plt.close()

# ---------------------------------------------------
# 9️⃣ ارزش خرید
df['ارزش خرید'] = df['قیمت هر متر'] / df['محله'].map(region_avg)
best_houses = df.sort_values('ارزش خرید', ascending=True).head(20)
best_houses.to_csv(os.path.join(output_folder, 'best_value_houses.csv'), index=False, encoding='utf-8-sig')
print("✅ بهترین خانه‌های با ارزش خرید بالا ذخیره شدند")

# ---------------------------------------------------
print("🎯 همه تحلیل‌ها و نمودارها با موفقیت ذخیره شدند ✅")
