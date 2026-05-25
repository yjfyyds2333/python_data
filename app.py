import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
from matplotlib.font_manager import FontProperties

dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

# 强制重置matplotlib配置 + 清除字体缓存（解决乱码核心！）
plt.rcdefaults()

# 加载你项目里的 微软雅黑 ttc 字体文件
font = FontProperties(fname="msyh.ttc")

# 全局强制设置字体（覆盖所有环境，不依赖系统）
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [font.get_name()]
plt.rcParams["axes.unicode_minus"] = False  # 修复负号方框


# 数据缓存以及清洗
@st.cache_data
def load_data():
    df = pd.read_csv('USvideos.csv',encoding='utf-8')
    df = df.dropna(subset=['views','category_id','likes','publish_time','title','channel_title'])
    df['publish_time'] = pd.to_datetime(df['publish_time'],errors="coerce")
    df['publish_month'] = df['publish_time'].dt.to_period("M")

    # ========== 为三个进阶分析预处理数据（关键！） ==========
    # 1.标题长度(分析2用)
    df['title_length'] = df['title'].str.len()
    # 2.发布小时(分析1用，0-23点)
    df['publish_hour'] = df['publish_time'].dt.hour
    # 3.发布星期(分析1用,转成中文，方便看)
    weekday_map = {0:'周一',1:'周二',2:'周三',3:'周四',4:'周五',5:'周六',6:'周日'}
    df['publish_weekday'] = df['publish_time'].dt.weekday.map(weekday_map)

    return df 

df = load_data()

# 1.页面标题+概览
st.title("Youtube 热门视频数据分析")
st.subheader("数据概览")

# 计算核心指标
total_videos = len(df)
avg_views = round(df['views'].mean()/10000,1)
max_views = round(df['views'].max()/10000,1)

# 创建3列布局
col1,col2,col3 = st.columns(3)

with col1:
    st.metric(label="总视频数",value=f'{total_videos}条')
with col2:
    st.metric(label="平均播放量(万)",value=f'{avg_views}')
with col3:
    st.metric(label="最大播放量(万)",value=f'{max_views}')


# 2.侧边栏
st.sidebar.header("筛选条件")

min_views = st.sidebar.slider(
    label="最低播放量",
    min_value=0,
    max_value=int(df['views'].max()),
    value=0,
    step=100000
)


all_categotys = df['category_id'].unique().astype(str)
selected_categories = st.sidebar.multiselect(
    label="选择视频分类",
    options=all_categotys,
    default=all_categotys
)

# 联动筛选
filtered = df[
    (df['views'] >= min_views) &
    (df['category_id'].astype(str).isin(selected_categories))
]

st.success(f'当前筛选结果:{len(filtered)}条')

# 3.画表
if len(filtered) == 0:
    st.warning("⚠️ 没有符合条件的数据，请调整筛选条件！")
else:
    # 柱状图
    st.subheader("📊 各视频分类平均播放量")
    cat_views = filtered.groupby('category_id')['views'].mean().sort_values(ascending=False)
    fig1,ax1 = plt.subplots(figsize=(10,4))
    ax1.bar(
        cat_views.index.astype(str),cat_views.values,color='steelblue'
    )
    ax1.set_title("各视频分类平均播放量")
    ax1.set_xlabel("分类ID")
    ax1.set_ylabel("平均播放量")
    st.pyplot(fig=fig1)

    # 散点图
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

    # 折线图
    st.subheader("📈 每日视频平均播放量")
    monthly_counts = df.groupby("publish_month")['views'].count()
    fig3,ax3 = plt.subplots(figsize=(10,4))
    ax3.plot(
        monthly_counts.index.astype(str),monthly_counts.values,
        marker="o",color='green'
    )
    ax3.set_title("每日视频平均播放量趋势")
    ax3.set_xlabel("发布日期")
    ax3.set_ylabel("平均播放量")
    ax3.tick_params(axis='x',rotation=45)
    st.pyplot(fig=fig3)


# ---------------------- 新增：进阶分析模块（三个选题） ----------------------
st.header("🔍 进阶分析模块")

# 先判断数据是否为空，避免报错
if len(filtered) == 0:
    st.warning("⚠️ 没有符合条件的数据，无法进行进阶分析，请调整筛选条件！")
else:
    # ============== 分析1：什么时间发布视频最容易上热门？ ==============
    st.subheader("⏰ 发布时间与观看量分析")
    st.write("分析不同发布时段的平均观看量，找出最优发布时间")

    # 1. 按小时统计平均观看量
    hour_views = filtered.groupby('publish_hour')['views'].mean().sort_values()
    fig_hour, ax_hour = plt.subplots(figsize=(10,4))
    ax_hour.bar(hour_views.index, hour_views.values, color='purple')
    ax_hour.set_title("各发布小时的平均观看量")
    ax_hour.set_xlabel("发布小时（0-23点）")
    ax_hour.set_ylabel("平均观看量")
    st.pyplot(fig=fig_hour)

    # 2. 按星期统计平均观看量
    weekday_views = filtered.groupby('publish_weekday')['views'].mean()
    # 强制按周一到周日排序，避免乱序
    weekday_order = ['周一','周二','周三','周四','周五','周六','周日']
    weekday_views = weekday_views.reindex(weekday_order)

    fig_weekday, ax_weekday = plt.subplots(figsize=(10,4))
    ax_weekday.bar(weekday_views.index, weekday_views.values, color='teal')
    ax_weekday.set_title("各发布星期的平均观看量")
    ax_weekday.set_xlabel("发布星期")
    ax_weekday.set_ylabel("平均观看量")
    st.pyplot(fig=fig_weekday)

    # 自动给结论
    best_hour = hour_views.idxmax()
    best_weekday = weekday_views.idxmax()
    st.info(f"💡 分析结论：当前筛选条件下，**{best_weekday}的{best_hour}点**发布的视频平均观看量最高，更容易上热门！")


    # ============== 分析2：标题长度和观看量有关系吗？ ==============
    st.subheader("📝 标题长度与观看量相关性分析")
    st.write("计算标题字符数与观看量的相关系数，判断两者是否有关联")

    # 计算相关系数（核心）
    corr_title = filtered['title_length'].corr(filtered['views'])

    # 画散点图
    fig_title, ax_title = plt.subplots(figsize=(10,4))
    ax_title.scatter(filtered['title_length'], filtered['views'], alpha=0.3, color='brown')
    ax_title.set_title(f"标题长度 vs 观看量 | 相关系数: {corr_title:.2f}")
    ax_title.set_xlabel("标题长度（字符数）")
    ax_title.set_ylabel("观看量")
    st.pyplot(fig=fig_title)

    # 自动解读相关系数
    if abs(corr_title) < 0.1:
        st.info("💡 分析结论：标题长度和观看量几乎没有相关性，标题长短不影响视频热度~")
    elif abs(corr_title) < 0.3:
        st.info("💡 分析结论：标题长度和观看量的相关性很弱，对视频热度影响不大")
    elif abs(corr_title) < 0.5:
        st.info("💡 分析结论：标题长度和观看量存在弱相关性，有一定影响")
    else:
        st.info("💡 分析结论：标题长度和观看量存在较强相关性，标题长度对视频热度影响明显！")


    # ============== 分析3：哪些频道是"热门制造机"？ ==============
    st.subheader("🏆 热门频道TOP10（上热门次数最多）")
    st.write("统计每个频道发布的热门视频数量，找出发布热门视频最多的频道")

    # 统计每个频道的视频数量，取前10
    channel_counts = filtered.groupby('channel_title')['video_id'].count().sort_values(ascending=False).head(10)

    # 画横向柱状图（频道名字不会重叠）
    fig_channel, ax_channel = plt.subplots(figsize=(10,5))
    # 反转数据，让第一名在最上面
    ax_channel.barh(channel_counts.index[::-1], channel_counts.values[::-1], color='darkred')
    ax_channel.set_title("上热门次数最多的TOP10频道")
    ax_channel.set_xlabel("上热门视频数量")
    st.pyplot(fig=fig_channel)

    # 自动给结论
    top_channel = channel_counts.index[0]
    top_count = channel_counts.iloc[0]
    st.info(f"💡 分析结论：当前筛选条件下，**{top_channel}**是热门制造机，共发布了{top_count}条热门视频！")


    # 4.筛选后原始数据表格模块
    st.subheader("📄 筛选后原始数据预览(前20条)")
    st.dataframe(filtered.head(20),use_container_width=True)