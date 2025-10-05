import streamlit as st
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.data_handler import DataHandler
from utils.validation import (
    validate_problem_format, validate_continuity, extract_alcumus_timestamps
)

# Page configuration
st.set_page_config(
    page_title="输入进度 - 儿童学习进度追踪",
    page_icon="📝",
    layout="wide"
)

# Initialize data handler
@st.cache_resource
def get_data_handler():
    return DataHandler()

data_handler = get_data_handler()

# Main content
st.title("📝 输入今日学习进度")

# Date selection with "Today" button
col1, col2 = st.columns([3, 1])
with col1:
    selected_date = st.date_input(
        "选择日期",
        value=datetime.today(),
        max_value=datetime.today()
    )
with col2:
    if st.button("今天", type="primary"):
        selected_date = datetime.today().date()
        st.rerun()

date_str = selected_date.strftime('%Y-%m-%d')

# Show current book
st.info("**当前书籍：** Introduction to Algebra")

# Load existing data for this date
existing_data = data_handler.get_data_by_date(date_str)
existing_problems_str = ", ".join(existing_data.get('problems', []))
existing_exercises_str = ", ".join(existing_data.get('exercises', []))
existing_notes = existing_data.get('notes', '')

# Combine problems and exercises for display
existing_items = []
if existing_problems_str:
    existing_items.append(existing_problems_str)
if existing_exercises_str:
    existing_items.append(existing_exercises_str)
existing_combined = ", ".join(existing_items)

# Input fields
st.subheader("AOPS 题目")
problems_input = st.text_input(
    "输入完成的题目（逗号分隔）",
    value=existing_combined,
    placeholder="例如：15.1, 15.2, 15.1.1, 15.1.2",
    help="Problem格式：X.Y（如15.1）；Exercise格式：X.Y.Z（如15.1.1）"
)

st.subheader("Alcumus 题目")
existing_alcumus = existing_data.get('alcumus', [])
existing_alcumus_str = "\n".join(existing_alcumus) if existing_alcumus else ""
alcumus_input = st.text_area(
    "粘贴 Alcumus 题目历史",
    value=existing_alcumus_str,
    placeholder="从 AOPS 网站复制粘贴 Alcumus 题目历史（包含时间戳）",
    help="粘贴包含时间戳的文本，系统会自动提取时间戳",
    height=150
)

# Show extracted timestamps preview
if alcumus_input.strip():
    preview_timestamps = extract_alcumus_timestamps(alcumus_input)
    if preview_timestamps:
        st.info(f"📋 检测到 {len(preview_timestamps)} 个时间戳：")
        # Display timestamps in a compact format
        timestamp_display = ", ".join(preview_timestamps[:10])
        if len(preview_timestamps) > 10:
            timestamp_display += f" ... (还有 {len(preview_timestamps) - 10} 个)"
        st.caption(timestamp_display)
    else:
        st.warning("⚠️ 未检测到有效的时间戳格式 (YYYY-MM-DD HH:MM:SS)")

st.subheader("学习笔记")
notes_input = st.text_area(
    "记录今天的其他学习活动",
    value=existing_notes,
    placeholder="今天还做了什么其他学习活动？",
    height=100
)

# Validation and update
if st.button("更新进度", type="primary"):
    # Validate format
    is_valid, error_msg, problems_list, exercises_list = validate_problem_format(problems_input)
    
    if not is_valid:
        st.error(f"❌ {error_msg}")
    else:
        # Get previous day's data for continuity check
        previous_date = selected_date - timedelta(days=1)
        previous_date_str = previous_date.strftime('%Y-%m-%d')
        prev_problems, prev_exercises = data_handler.get_latest_problems_and_exercises(date_str)
        
        # Validate continuity
        continuity_valid, continuity_error = validate_continuity(
            problems_list, exercises_list, prev_problems, prev_exercises
        )
        
        if not continuity_valid:
            st.error(f"❌ {continuity_error}")
        else:
            # Extract Alcumus timestamps
            alcumus_timestamps = extract_alcumus_timestamps(alcumus_input)
            
            # Save data
            try:
                data_handler.update_date_record(
                    date_str, problems_list, exercises_list, notes_input,
                    alcumus=alcumus_timestamps
                )
                st.success("✅ 进度已成功更新！")
                
                # Show what was saved
                saved_info = []
                if problems_list or exercises_list:
                    saved_items = problems_list + exercises_list
                    saved_info.append(f"AOPS: {', '.join(saved_items)}")
                if alcumus_timestamps:
                    saved_info.append(f"Alcumus: {len(alcumus_timestamps)}道题")
                
                if saved_info:
                    st.info(f"📝 已保存：{' | '.join(saved_info)}")
                
            except Exception as e:
                st.error(f"❌ 保存失败：{str(e)}")

# Sidebar tips
st.sidebar.markdown("---")
st.sidebar.markdown("💡 **使用提示：**")
st.sidebar.markdown("• Problem格式：15.1")
st.sidebar.markdown("• Exercise格式：15.1.5")
st.sidebar.markdown("• 题目必须连续完成")
st.sidebar.markdown("• 可以任意日期补录数据")
