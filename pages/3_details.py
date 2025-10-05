import streamlit as st
import sys
import os
import pandas as pd

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
    
    # Prepare data for table
    table_data = []
    for record in all_data_sorted:
        problems = record.get('problems', [])
        exercises = record.get('exercises', [])
        alcumus = record.get('alcumus', [])
        notes = record.get('notes', '').strip()
        
        # Build details string
        details_parts = []
        if problems:
            details_parts.append(f"Problems: {', '.join(problems)}")
        if exercises:
            details_parts.append(f"Exercises: {', '.join(exercises)}")
        if alcumus:
            details_parts.append(f"Alcumus: {', '.join(alcumus)}")
        
        details = " | ".join(details_parts) if details_parts else ""
        
        table_data.append({
            '日期': record['date'],
            'Problem数量': len(problems),
            'Exercise数量': len(exercises),
            'Alcumus数量': len(alcumus),
            'Note': notes if notes else "",
            'Details': details
        })
    
    # Create and display DataFrame
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
