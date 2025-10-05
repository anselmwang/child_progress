import streamlit as st
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_handler import DataHandler
from utils.charts import (
    create_daily_chart, create_weekly_chart, create_monthly_chart,
    get_achievements
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
    
    # Achievements list
    st.subheader("🏆 成就列表")
    achievements = get_achievements(all_data)
    
    if achievements:
        for achievement in achievements:
            # Format date for display
            date_obj = datetime.strptime(achievement['date'], '%Y-%m-%d')
            formatted_date = date_obj.strftime('%Y年%m月%d日')
            
            # Display achievement with date
            achievement_text = f"{achievement['description']} - {formatted_date}"
            st.success(achievement_text)
    else:
        st.info("还没有完成任何成就，继续学习获得你的第一个成就吧！")
    
    # Charts
    st.subheader("📈 学习趋势图表")
    
    # Daily chart
    st.plotly_chart(create_daily_chart(all_data), use_container_width=True)
    
    # Weekly chart
    st.plotly_chart(create_weekly_chart(all_data), use_container_width=True)
    
    # Monthly chart
    st.plotly_chart(create_monthly_chart(all_data), use_container_width=True)
