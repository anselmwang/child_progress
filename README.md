# 儿童学习进度追踪工具

一个帮助孩子记录和追踪 AOPS（Art of Problem Solving）数学学习进度的 Streamlit 应用。

## 功能特点

- 📝 **日常进度输入**：记录每天完成的题目和学习笔记
- 📊 **可视化统计**：通过图表查看学习进度趋势
- 📋 **历史记录**：完整的学习历史详情
- ✅ **智能验证**：自动验证题目连续性，确保学习路径完整
- 🎉 **激励系统**：每周总结和章节里程碑提醒

## 安装说明

### 前置条件

- Python 3.9 或更高版本
- [uv](https://github.com/astral-sh/uv) 包管理器

### 安装 uv

如果你还没有安装 uv，请先安装：

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 安装项目

1. 克隆或下载此项目到本地：
```bash
git clone <repository-url>
cd child_progress
```

2. 使用 uv 同步依赖（会自动创建虚拟环境并安装所有依赖）：
```bash
uv sync
```

## 运行应用

使用 uv 运行 Streamlit 应用：

```bash
uv run streamlit run app.py
```

应用将在浏览器中自动打开，默认地址为 `http://localhost:8501`

## 使用指南

### 1. 输入进度

- 点击侧边栏的"📝 输入进度"
- 选择日期（或点击"今天"按钮快速选择当前日期）
- 输入完成的题目（逗号分隔），例如：`15.1, 15.2, 15.1.1`
  - **Problem**：一个点的题号（如 15.1）
  - **Exercise**：两个点的题号（如 15.1.1）
- 添加学习笔记（可选）
- 点击"更新进度"保存

### 2. 查看概览

- 点击"📊 概览页面"查看学习统计
- 包含日、周、月三种时间维度的图表
- 显示每周完成情况和章节里程碑

### 3. 浏览历史

- 点击"📋 详情页面"查看所有学习记录
- 按时间顺序显示每天的学习内容

## 数据存储

- 所有数据存储在 `data/progress.jsonl` 文件中
- 自动备份：每次更新时在 `data/backups/` 目录创建备份
- 使用原子写入机制，确保数据安全

## 项目结构

```
child_progress/
├── app.py                    # 主应用入口
├── pyproject.toml            # 项目配置和依赖
├── uv.lock                   # uv 锁文件
├── data/
│   ├── progress.jsonl        # 主数据文件
│   └── backups/              # 自动备份目录
├── pages/
│   ├── 1_input_progress.py   # 输入进度页面
│   ├── 2_overview.py         # 概览页面
│   └── 3_details.py          # 详情页面
└── utils/
    ├── validation.py         # 验证逻辑
    ├── data_handler.py       # 数据处理
    └── charts.py             # 图表生成
```

## 开发说明

### 添加依赖

```bash
uv add <package-name>
```

### 更新依赖

```bash
uv sync --upgrade
```

### 运行开发服务器

```bash
uv run streamlit run app.py
```

## 常见问题

**Q: 如何备份数据？**  
A: 数据会自动备份到 `data/backups/` 目录。你也可以手动复制 `data/progress.jsonl` 文件。

**Q: 题目必须连续吗？**  
A: 是的，系统会验证题目连续性。同一天的题目必须连续，且今天的第一题必须紧接昨天的最后一题。

**Q: 可以修改历史记录吗？**  
A: 可以，选择任意日期即可编辑该日期的记录。

**Q: 支持多个孩子使用吗？**  
A: 当前版本设计为单用户使用。如需支持多个孩子，建议为每个孩子创建独立的数据目录。

## 技术栈

- **框架**: Streamlit
- **图表**: Plotly
- **数据处理**: Pandas
- **包管理**: uv

## 许可证

[添加你的许可证信息]

## 贡献

欢迎提交 Issue 和 Pull Request！
