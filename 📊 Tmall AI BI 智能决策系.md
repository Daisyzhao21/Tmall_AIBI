# 📊 Tmall AI BI 智能决策系统

<p align="center">
  <img src="https://img.icons8.com/color/96/000000/tmall.png" alt="Tmall AI BI" width="100">
</p>

<p align="center">
  <strong>基于 Baseline + Incremental 框架的电商智能决策系统</strong><br>
  为天猫商家提供 AI 驱动的销量预测、预算优化和活动复盘服务
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg">
  <img src="https://img.shields.io/badge/Streamlit-1.58.0-red.svg">
  <img src="https://img.shields.io/badge/Plotly-6.8.0-green.svg">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
</p>

---

## ✨ 核心功能

| 功能模块 | 说明 | 业务价值 |
|---------|------|----------|
| 📈 **AI 销量预测** | 输入营销预算，智能预测未来销量 | 科学制定销售目标 |
| 💰 **营销预算优化** | S曲线分析，找到投资效率最高点 | 提升 ROI，避免预算浪费 |
| 📊 **活动效果复盘** | 瀑布图量化各渠道贡献 | 优化营销策略 |
| 📋 **综合数据看板** | 全局监控销售趋势和渠道表现 | 实时掌握经营状况 |

---

## 🎯 解决的问题

| 问题 | 解决方案 |
|------|----------|
| ❌ 主观预测 | ✅ 数据驱动的科学决策 |
| ❌ 预算盲目 | ✅ S曲线找到投资效率拐点 |
| ❌ 归因模糊 | ✅ 瀑布图量化各渠道贡献 |
| ❌ 信息滞后 | ✅ 实时看板监控销售趋势 |

---

## 🚀 在线体验

🌐 **公网链接**：`https://tmallaibi-xxxx.streamlit.app`

> 无需安装，手机电脑都能用，打开即用！

---

## 📁 项目结构

```
Tmall_AIBI/
├── app.py                 # Streamlit 主应用
├── generate_data.py       # 模拟数据生成脚本
├── tmall_sales_data.csv   # 销售数据 (可替换为真实数据)
├── requirements.txt       # Python 依赖
└── README.md              # 项目文档
```

---

## 🔧 技术架构

```
┌─────────────────────────────────────────────────────┐
│                   Streamlit 前端                      │
├─────────────────────────────────────────────────────┤
│              Plotly 数据可视化                        │
├─────────────────────────────────────────────────────┤
│              Pandas / NumPy 数据处理                  │
├─────────────────────────────────────────────────────┤
│           Scipy S曲线拟合 (Logistic)                  │
├─────────────────────────────────────────────────────┤
│              CSV 数据存储 (可升级为数据库)             │
└─────────────────────────────────────────────────────┘
```

### 核心技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Streamlit | 1.58.0 | Web 应用框架 |
| Plotly | 6.8.0 | 交互式数据可视化 |
| Pandas | 2.3.3 | 数据处理与分析 |
| NumPy | 2.2.6 | 数值计算 |
| Scipy | 1.15.3 | S曲线拟合优化 |

---

## 📊 算法模型

### Baseline + Incremental 框架

```
总销量 = 基准销量 + 增量销量

基准销量 = 趋势 + 季节性 + 随机波动
增量销量 = f(RTB) + f(促销) + f(直播)
```

### S 曲线 (Logistic) 公式

```
Incremental = L / (1 + e^(-k * (Investment - x0)))
```

**参数说明：**
- **L**: 饱和上限 - 理论最大增量
- **k**: 增长速度 - 响应速度
- **x0**: 拐点 - 效率最高点

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- pip 或 conda

### 本地安装

```bash
# 1. 克隆项目
git clone https://github.com/Daisyzhao21/Tmall_AIBI.git
cd Tmall_AIBI

# 2. 创建虚拟环境 (推荐)
conda create -n Tmall_AI_BI python=3.10 -y
conda activate Tmall_AI_BI

# 3. 安装依赖
pip install -r requirements.txt

# 4. 生成模拟数据
python generate_data.py

# 5. 运行应用
streamlit run app.py
```

### 使用说明

1. **销量预测**：输入 RTB/促销/直播预算 → 点击预测 → 查看结果
2. **预算优化**：查看 S 曲线 → 找到效率最高点 → 调整预算
3. **活动复盘**：选择日期范围 → 生成报告 → 查看渠道贡献
4. **数据看板**：切换时间范围 → 监控销售趋势

---

## 📈 性能指标

| 指标 | 数值 |
|------|------|
| 数据加载 | < 1 秒 |
| 预测计算 | < 0.5 秒 |
| 图表渲染 | < 1 秒 |
| 支持数据量 | 10 万+ 行 |

---

## 🔌 接入真实数据

### 准备数据文件

CSV 文件需包含以下列：

| 列名 | 类型 | 说明 |
|------|------|------|
| date | date | 日期 |
| base_sales | int | 基准销量 |
| rtb_spend | int | RTB 投入 |
| promotion_spend | int | 促销投入 |
| livestreaming_spend | int | 直播投入 |
| final_sales | int | 实际销量 |

### 替换数据

```bash
# 替换默认数据文件
cp your_data.csv tmall_sales_data.csv

# 重启应用
streamlit run app.py
```

---

## ☁️ 云端部署

### Streamlit Cloud 部署

1. 推送代码到 GitHub
2. 访问 [share.streamlit.io](https://share.streamlit.io)
3. 选择仓库 `Daisyzhao21/Tmall_AIBI`
4. 点击 Deploy

部署完成后获得公网链接，永久在线！

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 许可证

MIT License

---

## 📧 联系方式

- **项目作者**: Daisy Zhao
- **GitHub**: [@Daisyzhao21](https://github.com/Daisyzhao21)
- **项目链接**: [https://github.com/Daisyzhao21/Tmall_AIBI](https://github.com/Daisyzhao21/Tmall_AIBI)

---

## 🙏 致谢

- [Streamlit](https://streamlit.io/) - Web 应用框架
- [Plotly](https://plotly.com/) - 数据可视化库
- [Scipy](https://scipy.org/) - 科学计算工具
- [Pandas](https://pandas.pydata.org/) - 数据处理利器

---

<p align="center">
  📊 Tmall AI BI System | Data-Driven Decision Making
</p>
