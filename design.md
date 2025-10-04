我想要做一个网站，是帮助孩子记录学习进度的。

每天，孩子输入两种学习进度
- 一个是aops学习进度，孩子输入今天做的题目，用逗号分隔
    - 逗号之间是题号
        - 如果题号中只有一个“."，属于problem，例子15.1
        - 如果题号中有两个"."，属于exercise，例子15.1.5
- 一个是”笔记“文本框，孩子可以简单的输入今天做的其他事情

然后有一个overview page
- 画出三张曲线图，每张曲线图上面有三条曲线
    - problem数量的变化
    - exercise数量的变化
    - problem + exercise数量的变化
- 三张曲线图分别是，范围都是从最早有数据开始到最晚有数据
    - aggregate by day
    - aggregate by week
    - aggregate by month

一个detail page
- 就是简单平铺直叙的列出每一天的进度
    - aops做了的题目
    - 还有”笔记“