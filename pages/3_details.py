import streamlit as st
from datetime import datetime
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_handler import DataHandler

# Page configuration
st.set_page_config(
    page_title="详情页面 - 儿童学习进度追踪",
    page_icon="📋",
    layout="wide"
)

# Initialize data handler
@st.cache_resource
def get_data_handler():
    return DataHandler()

data_handler = get_data_handler()

# Main content
st.title("📋 学习进度详情")

# Load all data
all_data = data_handler.load_all_data()

if not all_data:
    st.info("还没有学习记录，请先去输入进度页面添加数据。")
else:
    st.subheader(f"总计 {len(all_data)} 天的学习记录")
    
    # Sort by date (newest first)
    all_data_sorted = sorted(all_data, key=lambda x: x['date'], reverse=True)
    
    # Display records
    for record in all_data_sorted:
        date_obj = datetime.strptime(record['date'], '%Y-%m-%d')
        date_display = date_obj.strftime('%Y年%m月%d日 (%A)')
        
        with st.expander(f"📅 {date_display}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**📚 AOPS 题目：**")
                problems = record.get('problems', [])
                exercises = record.get('exercises', [])
                
                if problems:
                    st.write(f"Problems: {', '.join(problems)}")
                if exercises:
                    st.write(f"Exercises: {', '.join(exercises)}")
                
                if not problems and not exercises:
                    st.write("当天没有完成AOPS题目")
            
            with col2:
                st.write("**📝 学习笔记：**")
                notes = record.get('notes', '').strip()
                if notes:
                    st.write(notes)
                else:
                    st.write("无笔记")
