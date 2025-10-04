import streamlit as st
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_handler import DataHandler
from utils.charts import (
    create_daily_chart, create_weekly_chart, create_monthly_chart,
    get_weekly_summary, detect_chapter_completion
)

# Page configuration
st.set_page_config(
    page_title="概览页面 - 儿童学习进度追踪",
    page_icon="📊",
    layout="wide"
)


# Initialize data handler
@st.cache_resource
def get_data_handler():
    return DataHandler()


data_handler = get_data_handler()

# Main content
st.title("📊 学习进度概览")

# Load all data
all_data = data_handler.load_all_data()

if not all_data:
    st.info("还没有学习记录，请先去输入进度页面添加数据。")
else:
    # Missing dates warning
    st.subheader("📅 最近记录检查")
    
    # Check for missing dates in the last 14 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=13)
    
    existing_dates = {record['date'] for record in all_data}
    missing_dates = []
    
    current_date = start_date
    while current_date <= end_date:
        if current_date.strftime('%Y-%m-%d') not in existing_dates:
            missing_dates.append(current_date)
        current_date += timedelta(days=1)
    
    if missing_dates:
        missing_str = ", ".join([d.strftime('%m月%d日') for d in missing_dates])
        st.warning(f"⚠️ 缺失记录：{missing_str}")
    else:
        st.success("✅ 最近14天记录完整！")
    
    # Weekly summary and motivation
    st.subheader("🌟 本周成就")
    weekly_stats = get_weekly_summary(all_data)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Problem", weekly_stats['problems'])
    with col2:
        st.metric("Exercise", weekly_stats['exercises'])
    with col3:
        st.metric("总计", weekly_stats['total'])
    
    if weekly_stats['total'] > 0:
        problem_count = weekly_stats['problems']
        exercise_count = weekly_stats['exercises']
        st.success(f"本周你完成了{problem_count}道问题和{exercise_count}道练习！🌟")
    
    # Chapter completion milestones
    completed_chapters = detect_chapter_completion(all_data)
    if completed_chapters:
        st.subheader("🎉 里程碑成就")
        for achievement in completed_chapters:
            st.success(achievement)
    
    # Charts
    st.subheader("📈 学习趋势图表")
    
    # Daily chart
    st.plotly_chart(create_daily_chart(all_data), use_container_width=True)
    
    # Weekly chart
    st.plotly_chart(create_weekly_chart(all_data), use_container_width=True)
    
    # Monthly chart
    st.plotly_chart(create_monthly_chart(all_data), use_container_width=True)
