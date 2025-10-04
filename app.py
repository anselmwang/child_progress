import streamlit as st
from datetime import datetime, timedelta
from utils.data_handler import DataHandler
from utils.validation import validate_problem_format, validate_continuity
from utils.charts import (
    create_daily_chart, create_weekly_chart, create_monthly_chart,
    get_weekly_summary, detect_chapter_completion
)

# Page configuration
st.set_page_config(
    page_title="儿童学习进度追踪",
    page_icon="📚",
    layout="wide"
)

# Initialize data handler
@st.cache_resource
def get_data_handler():
    return DataHandler()

data_handler = get_data_handler()

# Sidebar navigation
st.sidebar.title("学习进度追踪")
page = st.sidebar.radio(
    "选择页面",
    ["📝 输入进度", "📊 概览页面", "📋 详情页面"]
)

# Input Progress Page
if page == "📝 输入进度":
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
                # Save data
                try:
                    data_handler.update_date_record(
                        date_str, problems_list, exercises_list, notes_input
                    )
                    st.success("✅ 进度已成功更新！")
                    
                    # Show what was saved
                    if problems_list or exercises_list:
                        saved_items = problems_list + exercises_list
                        st.info(f"📝 已保存：{', '.join(saved_items)}")
                    
                except Exception as e:
                    st.error(f"❌ 保存失败：{str(e)}")

# Overview Page
elif page == "📊 概览页面":
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
            st.success(f"本周你完成了{weekly_stats['problems']}道问题和{weekly_stats['exercises']}道练习！🌟")
        
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

# Details Page
elif page == "📋 详情页面":
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

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("💡 **使用提示：**")
st.sidebar.markdown("• Problem格式：15.1")
st.sidebar.markdown("• Exercise格式：15.1.5")
st.sidebar.markdown("• 题目必须连续完成")
st.sidebar.markdown("• 可以任意日期补录数据")
