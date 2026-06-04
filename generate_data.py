import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("🚀 开始生成 Tmall 电商模拟数据...")
print("=" * 50)

# 生成日期范围
dates = pd.date_range(start='2024-01-01', end='2025-12-31', freq='D')
n_days = len(dates)
print(f"📅 日期范围: {dates[0].date()} 到 {dates[-1].date()}，共 {n_days} 天")

np.random.seed(42)

# 基准销量
trend = np.linspace(80, 180, n_days)
weekday_seasonal = np.zeros(n_days)
month_seasonal = np.zeros(n_days)

for i, date in enumerate(dates):
    if date.weekday() == 5:
        weekday_seasonal[i] = 30
    elif date.weekday() == 6:
        weekday_seasonal[i] = 20
    else:
        weekday_seasonal[i] = 5
    
    if date.month == 6:
        month_seasonal[i] = 50
    elif date.month == 11:
        month_seasonal[i] = 80

base_sales = trend + weekday_seasonal + month_seasonal + np.random.normal(0, 10, n_days)
base_sales = np.maximum(base_sales, 30).astype(int)

# 营销投资
rtb_spend = np.random.uniform(0, 120000, n_days).astype(int)
promotion_spend = np.random.uniform(0, 90000, n_days).astype(int)
livestreaming_spend = np.random.uniform(0, 50000, n_days).astype(int)

# S曲线函数
def sigmoid_response(spend, L, k, x0):
    return L / (1 + np.exp(-k * (spend - x0)))

# 增量计算
incremental_rtb = sigmoid_response(rtb_spend, 600, 0.000045, 50000).astype(int)
incremental_promo = sigmoid_response(promotion_spend, 450, 0.00008, 35000).astype(int)
incremental_live = np.maximum((livestreaming_spend * 0.008 - 20), 0).astype(int)

# 总销量
final_sales = base_sales + incremental_rtb + incremental_promo + incremental_live

# 保存数据
df = pd.DataFrame({
    'date': dates,
    'base_sales': base_sales,
    'rtb_spend': rtb_spend,
    'promotion_spend': promotion_spend,
    'livestreaming_spend': livestreaming_spend,
    'incremental_rtb': incremental_rtb,
    'incremental_promo': incremental_promo,
    'incremental_live': incremental_live,
    'final_sales': final_sales
})

df.to_csv('tmall_sales_data.csv', index=False)
print(f"\n✅ 数据生成完成！")
print(f"📊 数据形状: {df.shape}")
print(f"📈 销量范围: {df['final_sales'].min()} - {df['final_sales'].max()}")
print(f"\n📋 前5行预览:")
print(df.head())
