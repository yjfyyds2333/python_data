# 📊 YouTube美国视频数据分析仪表盘
基于 Streamlit 构建的交互式数据分析可视化项目，对 YouTube 美国热门视频数据进行多维度分析与展示。

## ✨ 项目简介
本项目通过 **Pandas** 对 YouTube 美国视频数据集（`USvideos.csv`）进行清洗与分析，结合 **Matplotlib** 实现数据可视化，最终使用 **Streamlit** 快速搭建交互式Web仪表盘，支持在线访问与实时数据查看。

**核心解决**：数据可视化展示、中文乱码适配、云端一键部署，适合作为数据分析入门实战项目。

---

## 🚀 在线演示
项目已部署至 Streamlit Cloud，直接访问即可使用：
> 替换为你的 Streamlit 应用链接
https://xxx.streamlit.app/

---

## 🎯 核心功能
1. **数据概览**：展示数据集基础信息、数据规模、字段说明
2. **统计分析**：视频播放量、点赞量、评论量等核心指标统计
3. **可视化图表**：
   - 分类数据分布柱状图
   - 核心指标趋势图
   - 互动数据关联分析
4. **交互式操作**：支持动态筛选、图表自适应展示
5. **云端适配**：完美解决 Matplotlib 中文乱码问题，跨环境稳定运行

---

## 🛠️ 技术栈
- **前端框架**：Streamlit（快速构建Web数据应用）
- **数据处理**：Pandas（数据清洗、分析、统计）
- **可视化**：Matplotlib（图表绘制）
- **部署平台**：Streamlit Cloud（免费云端部署）
- **版本控制**：Git + GitHub

---

## 📦 项目文件结构
```
python数据分析表盘/
├── app.py              # 项目主程序（Streamlit 入口文件）
├── USvideos.csv        # YouTube 美国视频原始数据集
├── requirements.txt    # 项目依赖库声明
└── README.md           # 项目说明文档
```

---

## 🔧 本地运行教程
### 1. 环境准备
确保已安装 Python 3.8+

### 2. 克隆/下载项目
```bash
# 进入项目文件夹
cd "你的项目路径"
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 启动应用
```bash
streamlit run app.py
```

### 5. 访问应用
浏览器自动打开：`http://localhost:8501`

---

## ☁️ 云端部署（Streamlit Cloud）
1. 将项目上传至 **GitHub** 仓库
2. 访问 [share.streamlit.io](https://share.streamlit.io/)，使用 GitHub 登录
3. 新建应用：选择仓库 → 分支 → 主文件路径（`app.py`）
4. 点击 Deploy，等待部署完成即可生成公开访问链接

---

## 📝 依赖文件（requirements.txt）
```txt
streamlit
pandas
matplotlib
```

---

## ⚠️ 重要说明
1. **中文显示**：已适配 Streamlit 云端环境，使用服务器自带中文字体，无乱码问题
2. **文件限制**：GitHub 禁止上传 >100MB 文件，本项目已优化文件大小
3. **更新维护**：修改代码后推送至 GitHub，Streamlit 会自动重新部署

---

## 📄 许可证
本项目仅供学习交流使用，数据集来源于公开数据源。

---

