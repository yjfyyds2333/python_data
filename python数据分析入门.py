import pandas as pd
import os 
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams["font.family"] = "SimHei" # 支持中文显示
matplotlib.rcParams["axes.unicode_minus"] = False

# 切换目录
dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(dir)

# 读取CSV
df = pd.read_csv('USvideos.csv',encoding='utf-8')
# 清除缺失值，避免后续计算报错
df.dropna(subset=["views","likes","comment_count","category_id","publish_time"])
# 处理时间数据,折线图必用
df["publish_time"] = pd.to_datetime(df['publish_time'])

# 用df.info()和df.describe()查看数据
print('df.info()数据如下:')
print(df.info())
print('\ndf.describe()数据如下:')
print(df.describe())

# 找出观看量最高的10个视频，打印出标题和观看量.
max_views_10 = df.sort_values('views',ascending=False).head(10)[['title','views']]
print('\n观看量最高的10个视频(降序)')
print(max_views_10)


# 1.==============各分类平均观看量柱状图================
category_views = df.groupby('category_id')['views'].mean().sort_values(ascending=False)
# 创建画布并绘制柱状图
plt.figure(figsize=(12, 5))  # 设置画布大小（宽12，高5）
plt.bar(
    x=category_views.index.astype(str),  # X轴：分类ID（转为字符串，避免被当成连续值）
    height=category_views.values,        # Y轴：每个分类的平均观看量
    color="steelblue"               # 柱子颜色，比默认颜色更美观
)

# 图表美化与标注
plt.title("Youtube各分类平均观看量",fontsize=14) # 标题，字号稍大
plt.xlabel("视频分类ID",fontsize=12)
plt.ylabel("平均观看量",fontsize=12)
plt.tight_layout() # 自动调整布局，防止标签被截断

# 保存图片并显示图表
plt.savefig("bar_chart.png",dpi=300)  # 保存成图片,dpi=300提升图片清晰度
plt.show()



# 2.==============画观看量分布直方图（用 log 坐标）================
plt.figure(figsize=(10,5))

plt.hist(
    df["views"],
    bins=50,
    log=True,
    color='orange',
    edgecolor = 'black'
)

plt.title("Youtube观看量分布直方图(用log坐标表示)",fontsize=14)
plt.xlabel("观看量",fontsize=12)
plt.ylabel("视频数量(Log)",fontsize=12)
plt.tight_layout()
plt.show()


# 3.==============画观看量vs点赞数的散点图================
plt.figure(figsize=(10,5))
cor = df['views'].corr(df["likes"])

plt.scatter(
    df['views'],df['likes'],alpha=0.3,color='blue'
)

plt.title(f'Youtube视频观看量vs点赞数的散点图(相关系数：{cor:.2f})',fontsize=14)
plt.xlabel('观看量',fontsize=12)
plt.ylabel('点赞数',fontsize=12)
plt.tight_layout()
plt.show()


# 4.==============画每月发布视频数量折线图（需要先把发布时间转成月份）================
plt.figure(figsize=(10,5))
df["publish_month"] = df["publish_time"].dt.to_period("M")
monthly_counts = df.groupby("publish_month")['video_id'].count()

plt.plot(
    monthly_counts.index.astype(str),monthly_counts.values,
    marker="o",color="green",linewidth=2
)
plt.title("YouTube每日视频发布数量趋势", fontsize=14)
plt.xlabel("发布日期(月份)", fontsize=12)
plt.ylabel("视频数量", fontsize=12)
plt.xticks(rotation=45)  # 旋转日期标签，避免重叠
plt.grid(alpha=0.3)  # 加网格线，方便读取数值
plt.tight_layout()
plt.show()




 