import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy.optimize import curve_fit
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Tmall AI BI", page_icon="📊", layout="wide")

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    margin-bottom: 2rem;
    text-align: center;
    color: white;
}
.metric-card {
    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
    padding: 1rem;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
.insight-box {
    background: #e8f4f8;
    padding: 1rem;
    border-radius: 12px;
    border-left: 5px solid #667eea;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv('tmall_sales_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

def sigmoid_curve(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

def fit_sigmoid(df, spend_col, incremental_col):
    mask = (df[spend_col] > 0) & (df[incremental_col] > 0)
    x_data = df.loc[mask, spend_col].values
    y_data = df.loc[mask, incremental_col].values
    if len(x_data) < 10:
        return None, None, None, None
    try:
        popt, _ = curve_fit(sigmoid_curve, x_data, y_data, 
                           p0=[max(y_data), 0.00005, np.median(x_data)], maxfev=5000)
        x_smooth = np.linspace(0, max(x_data), 100)
        y_smooth = sigmoid_curve(x_smooth, *popt)
        return popt, x_smooth, y_smooth, (x_data, y_data)
    except:
        return None, None, None, None

with st.sidebar:
    st.markdown("### 📊 Tmall AI BI")
    st.markdown("---")
    # 修复1: 为 radio 添加非空 label，然后隐藏它
    page = st.radio(
        label="选择功能页面",
        options=["📈 AI 销量预测", "💰 营销预算优化", "📊 活动效果复盘", "📋 综合数据看板"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption(f"📅 数据: {df['date'].min().date()} 至 {df['date'].max().date()}")

st.markdown("""
<div class="main-header">
    <h1>📊 Tmall AI BI 智能决策系统</h1>
    <p>基于 Baseline + Incremental 框架 | 数据驱动的电商决策</p>
</div>
""", unsafe_allow_html=True)

# ==================== 销量预测 ====================
if page == "📈 AI 销量预测":
    st.markdown("### 🎯 AI 销量预测助手")
    col1, col2 = st.columns(2)
    with col1:
        rtb_input = st.number_input("🎯 RTB 广告预算", 0, 150000, 50000, step=5000)
        promo_input = st.number_input("🏷️ 促销活动费用", 0, 100000, 30000, step=5000)
        live_input = st.number_input("📹 直播带货投入", 0, 60000, 20000, step=5000)
        forecast_days = st.slider("📆 预测天数", 7, 30, 14)
    with col2:
        if st.button("🚀 开始预测", type="primary", use_container_width=True):
            base_avg = df['base_sales'].tail(30).mean()
            rtb_inc = sigmoid_curve(rtb_input, 600, 0.000045, 50000)
            promo_inc = sigmoid_curve(promo_input, 450, 0.00008, 35000)
            live_inc = max(live_input * 0.008 - 20, 0)
            total_inc = rtb_inc + promo_inc + live_inc
            daily_forecast = base_avg + total_inc
            st.metric("📊 预测日销量", f"{daily_forecast:.0f} 件", delta=f"+{total_inc:.0f}")
            st.metric("📅 未来总销量", f"{daily_forecast * forecast_days:.0f} 件")
            inc_df = pd.DataFrame({'渠道': ['RTB', '促销', '直播'], '增量': [rtb_inc, promo_inc, live_inc]})
            st.bar_chart(inc_df.set_index('渠道'))
            future_dates = pd.date_range(df['date'].max() + timedelta(days=1), periods=forecast_days)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'].tail(60), y=df['final_sales'].tail(60),
                                    mode='lines', name='历史销量', line=dict(color='#667eea', width=2)))
            fig.add_trace(go.Scatter(x=future_dates, y=[daily_forecast] * forecast_days,
                                    mode='lines+markers', name='预测销量',
                                    line=dict(color='#f093fb', width=2, dash='dash')))
            fig.update_layout(height=400, xaxis_title="日期", yaxis_title="销量")
            # 修复2: 使用 width='stretch'
            st.plotly_chart(fig, use_container_width=True)

# ==================== 预算优化 ====================
elif page == "💰 营销预算优化":
    st.markdown("### 💰 营销预算优化师")
    tab1, tab2 = st.tabs(["📱 RTB 广告", "🏷️ 促销活动"])
    with tab1:
        result = fit_sigmoid(df, 'rtb_spend', 'incremental_rtb')
        if result[0] is not None:
            popt, x_smooth, y_smooth, raw_data = result
            L, k, x0 = popt
            col1, col2, col3 = st.columns(3)
            col1.metric("🎯 效率最高点", f"{x0:,.0f} 元")
            col2.metric("📈 饱和上限", f"{L:.0f} 件/天")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=raw_data[0], y=raw_data[1], mode='markers', name='实际数据', marker=dict(color='#667eea')))
            fig.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines', name='S曲线拟合', line=dict(color='#f093fb', width=3)))
            inflection_y = sigmoid_curve(x0, *popt)
            fig.add_trace(go.Scatter(x=[x0], y=[inflection_y], mode='markers', name='拐点', marker=dict(color='red', size=12)))
            fig.update_layout(height=450, xaxis_title="投资金额(元)", yaxis_title="增量销量(件)")
            st.plotly_chart(fig, use_container_width=True)

# ==================== 活动复盘 ====================
elif page == "📊 活动效果复盘":
    st.markdown("### 📊 活动效果复盘报告")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("📅 开始日期", df['date'].min() + timedelta(days=100))
    with col2:
        end_date = st.date_input("📅 结束日期", start_date + timedelta(days=30))
    if st.button("📈 生成报告", type="primary", use_container_width=True):
        mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
        campaign = df[mask]
        if len(campaign) > 0:
            total = campaign['final_sales'].sum()
            base = campaign['base_sales'].sum()
            inc = total - base
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("总销量", f"{total:,.0f}")
            col_b.metric("增量销量", f"{inc:,.0f}")
            col_c.metric("活动天数", f"{len(campaign)}")
            fig = go.Figure(go.Waterfall(
                measure=["absolute", "relative", "relative", "relative"],
                x=["基准销量", "RTB", "促销", "直播"],
                y=[base, campaign['incremental_rtb'].sum(), campaign['incremental_promo'].sum(), campaign['incremental_live'].sum()]
            ))
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)

# ==================== 数据看板 ====================
else:
    st.markdown("### 📋 综合数据看板")
    time_range = st.selectbox("时间范围", ["最近30天", "最近90天", "全部数据"], label_visibility="collapsed")
    if time_range == "最近30天":
        plot_df = df.tail(30)
    elif time_range == "最近90天":
        plot_df = df.tail(90)
    else:
        plot_df = df
    fig = make_subplots(rows=2, cols=2,
                        subplot_titles=("销量趋势", "渠道增量", "投资分布", "销量分布"))
    fig.add_trace(go.Scatter(x=plot_df['date'], y=plot_df['final_sales'], mode='lines', name='总销量'), row=1, col=1)
    fig.add_trace(go.Bar(x=plot_df['date'], y=plot_df['incremental_rtb'], name='RTB'), row=1, col=2)
    fig.add_trace(go.Bar(x=plot_df['date'], y=plot_df['incremental_promo'], name='促销'), row=1, col=2)
    total_rtb = plot_df['rtb_spend'].sum()
    total_promo = plot_df['promotion_spend'].sum()
    total_live = plot_df['livestreaming_spend'].sum()
    fig.add_trace(go.Pie(labels=['RTB', '促销', '直播'], values=[total_rtb, total_promo, total_live]), row=2, col=1)
    fig.add_trace(go.Histogram(x=plot_df['final_sales'], nbinsx=30), row=2, col=2)
    fig.update_layout(height=600, showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("<p style='text-align:center;color:gray'>🚀 Baseline + Incremental 框架 | AI 驱动决策</p>", unsafe_allow_html=True)
