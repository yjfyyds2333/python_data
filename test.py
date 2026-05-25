import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import streamlit as st

matplotlib.rcParams["font.family"] = "SimHei"
matplotlib.rcParams["axes.unicode_minus"] = False

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)


st.title("Youtube热门数据分析")

# 缓存加载数据 + 清洗数据(避免每次刷新都读文件)
@st.cache_data

def load_data():
    df = pd.read_csv("USvideos.csv",encoding='utf-8')
    df = df.dropna(subset=['views','category_id','likes','publish_time'])
    df['publish_time'] = pd.to_datetime(df["publish_time"],errors="coerce")
    df["publish_month"] = df["publish_time"].dt.to_period("M")
    return df

# 加载数据
df = load_data()

# ---------------------- 1. 标题 + 数据概览 ----------------------
st.title("Youtube热门视频数据分析仪表盘")
st.subheader("数据概览")

# 计算3个关键指标
total_videos = len(df)
avg_views = round(df["views"].mean()/10000,1)
max_views = round(df["views"].max()/10000,1)

# 用st.metric显示指标(3个并排展示)
col1,col2,col3 = st.columns(3)
with col1:
    st.metric(label="总视频数",value=f'{total_videos}条')
with col2:
    st.metric(label="平均观看量",value=f'{avg_views}条')
with col3:
    st.metric(label="最高观看量",value=f'{max_views}条')


# ---------------------- 2. 侧边栏筛选器 ----------------------
st.sidebar.header('筛选条件')

# 最低观看量滑块
min_views = st.sidebar.slider(
    label="最低观看量",
    min_value=0,
    max_value=int(df["views"].max()),
    value=0,
    step=100000
)

# 视频分类多选框(让用户选择要看哪些分类)
# 先获取所有分类ID,转换成字符串方便显示
all_categotys = df['category_id'].unique().astype(str)
selected_categories = st.sidebar.multiselect(
    label="选择视频分类",
    options = all_categotys,
    default=all_categotys # 默认全选
)

# 核心筛选逻辑:同时过滤观看量和分类
filtered = df[
    (df['views'] >= min_views) & 
    (df["category_id"].astype(str).isin(selected_categories))
]

# 显示筛选后的结果
st.success(f'当前筛选结果:{len(filtered)}条视频数据')


# ---------------------- 3. 三张联动图表 ----------------------
# 先判断筛选后有没有数据，避免报错
if len(filtered) == 0:
    st.warning("⚠️ 没有符合条件的数据，请调整筛选条件！")
else:
    # ①图表1:各分类平均观看量柱状图
    st.subheader("📊 各视频分类平均观看量")
    cat_views = filtered.groupby('category_id')['views'].mean().sort_values(ascending=False)
    fig1,ax1 = plt.subplots(figsize=(10,4))
    ax1.bar(
        cat_views.index.astype(str),cat_views.values,color='steelblue'
    )
    ax1.set_title("各分类平均观看量")
    ax1.set_xlabel("分类ID")
    ax1.set_ylabel("平均观看量")
    st.pyplot(fig=fig1)

    # ②图表2：观看量vs点赞数 散点图
    st.subheader("🎯 观看量与点赞数相关性")
    fig2,ax2 = plt.subplots(figsize=(10,4))
    ax2.scatter(
        filtered['views'],filtered['likes'],alpha=0.3,color='orange'
    )
    corr = filtered["views"].corr(filtered["likes"])
    ax2.set_title(f"观看量vs点赞数 | 相关系数:{corr:.2f}")
    ax2.set_xlabel("观看量")
    ax2.set_ylabel("观看量")
    st.pyplot(fig=fig2)

    # ③图表3： 月度视频发布趋势折线图(解决了Period报错！)
    st.subheader("📈 月度视频发布趋势")
    monthly_counts = filtered.groupby('publish_month')['video_id'].count()
    fig3,ax3 = plt.subplots(figsize=(10,4))
    ax3.plot(
        monthly_counts.index.astype(str),
        monthly_counts.values,
        marker="o",color="green"
    )
    ax3.set_title("月度视频发布数量趋势")
    ax3.set_xlabel("发布月份")
    ax3.set_ylabel("视频数量")
    ax3.tick_params(axis="x",rotation=45) # 旋转x轴标签，避免重叠
    st.pyplot(fig=fig3)

    # ---------------------- 4. 数据表格（筛选后原始数据） ----------------------
    st.subheader("📄 筛选后原始数据预览（前20条）")
    # 只显示前20条，避免页面太卡
    st.dataframe(filtered.head(20),use_container_width=True)
    