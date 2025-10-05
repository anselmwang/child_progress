import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
from typing import List, Dict, Any

def prepare_chart_data(all_data: List[Dict[str, Any]]) -> pd.DataFrame:
    """Prepare data for chart visualization."""
    chart_data = []
    
    for record in all_data:
        date = record['date']
        problems_count = len(record.get('problems', []))
        exercises_count = len(record.get('exercises', []))
        alcumus_count = len(record.get('alcumus', []))
        total_count = problems_count + exercises_count + alcumus_count
        
        chart_data.append({
            'date': datetime.strptime(date, '%Y-%m-%d'),
            'problems': problems_count,
            'exercises': exercises_count,
            'alcumus': alcumus_count,
            'total': total_count
        })
    
    return pd.DataFrame(chart_data)

def create_daily_chart(all_data: List[Dict[str, Any]]) -> go.Figure:
    """Create daily aggregated chart."""
    df = prepare_chart_data(all_data)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="暂无数据",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        fig.update_layout(title="每日学习进度")
        return fig
    
    fig = go.Figure()
    
    # Add traces for each type
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['problems'],
        mode='lines+markers',
        name='Problem',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['exercises'],
        mode='lines+markers',
        name='Exercise',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['alcumus'],
        mode='lines+markers',
        name='Alcumus',
        line=dict(color='#9467bd', width=2),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['total'],
        mode='lines+markers',
        name='总计',
        line=dict(color='#2ca02c', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="每日学习进度",
        xaxis_title="日期",
        yaxis_title="题目数量",
        hovermode='x unified',
        showlegend=True,
        xaxis=dict(tickformat='%Y-%m-%d')
    )
    
    return fig

def create_weekly_chart(all_data: List[Dict[str, Any]]) -> go.Figure:
    """Create weekly aggregated chart."""
    df = prepare_chart_data(all_data)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="暂无数据",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        fig.update_layout(title="每周学习进度")
        return fig
    
    # Group by week and use week-ending date (Sunday)
    df['week'] = df['date'].dt.to_period('W').dt.end_time
    weekly_df = df.groupby('week').agg({
        'problems': 'sum',
        'exercises': 'sum',
        'alcumus': 'sum',
        'total': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['problems'],
        mode='lines+markers',
        name='Problem',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['exercises'],
        mode='lines+markers',
        name='Exercise',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['alcumus'],
        mode='lines+markers',
        name='Alcumus',
        line=dict(color='#9467bd', width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=weekly_df['week'],
        y=weekly_df['total'],
        mode='lines+markers',
        name='总计',
        line=dict(color='#2ca02c', width=2),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="每周学习进度",
        xaxis_title="周",
        yaxis_title="题目数量",
        hovermode='x unified',
        showlegend=True,
        xaxis=dict(tickformat='%Y-%m-%d')
    )
    
    return fig

def create_monthly_chart(all_data: List[Dict[str, Any]]) -> go.Figure:
    """Create monthly aggregated chart."""
    df = prepare_chart_data(all_data)
    
    if df.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="暂无数据",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=20)
        )
        fig.update_layout(title="每月学习进度")
        return fig
    
    # Group by month
    df['month'] = df['date'].dt.to_period('M').dt.start_time
    monthly_df = df.groupby('month').agg({
        'problems': 'sum',
        'exercises': 'sum',
        'alcumus': 'sum',
        'total': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_df['month'],
        y=monthly_df['problems'],
        mode='lines+markers',
        name='Problem',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_df['month'],
        y=monthly_df['exercises'],
        mode='lines+markers',
        name='Exercise',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_df['month'],
        y=monthly_df['alcumus'],
        mode='lines+markers',
        name='Alcumus',
        line=dict(color='#9467bd', width=2),
        marker=dict(size=10)
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_df['month'],
        y=monthly_df['total'],
        mode='lines+markers',
        name='总计',
        line=dict(color='#2ca02c', width=2),
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        title="每月学习进度",
        xaxis_title="月份",
        yaxis_title="题目数量",
        hovermode='x unified',
        showlegend=True,
        xaxis=dict(tickformat='%Y-%m')
    )
    
    return fig

def get_weekly_summary(all_data: List[Dict[str, Any]]) -> Dict[str, int]:
    """Get current week's summary statistics."""
    now = datetime.now()
    week_start = now - timedelta(days=now.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    
    this_week_data = []
    for record in all_data:
        record_date = datetime.strptime(record['date'], '%Y-%m-%d')
        if record_date >= week_start:
            this_week_data.append(record)
    
    total_problems = sum(len(record.get('problems', []))
                        for record in this_week_data)
    total_exercises = sum(len(record.get('exercises', []))
                         for record in this_week_data)
    
    return {
        'problems': total_problems,
        'exercises': total_exercises,
        'total': total_problems + total_exercises
    }


def get_achievements(all_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Get all achievements (chapter completions and milestones) sorted by completion date (newest first)."""
    if not all_data:
        return []
    
    from utils.validation import parse_problem_number
    
    achievements = []
    
    # Prepare data sorted by date
    sorted_data = sorted(all_data, key=lambda x: x['date'])
    
    # Track chapter completion
    chapter_last_dates = {}  # chapter_num -> last_date_seen
    total_problems_by_date = {}  # date -> cumulative_count
    
    cumulative_count = 0
    
    for record in sorted_data:
        date = record['date']
        all_items = (record.get('problems', []) + 
                     record.get('exercises', []) + 
                     record.get('alcumus', []))
        
        # Update cumulative count
        cumulative_count += len(all_items)
        total_problems_by_date[date] = cumulative_count
        
        # Track chapters seen on this date
        for item in all_items:
            parsed = parse_problem_number(item)
            if parsed:
                chapter_num = parsed[0]
                chapter_last_dates[chapter_num] = date
    
    # Detect chapter completions
    # When we see a new chapter, the previous chapter is considered complete
    sorted_chapters = sorted(chapter_last_dates.keys())
    for i in range(len(sorted_chapters) - 1):
        current_chapter = sorted_chapters[i]
        next_chapter = sorted_chapters[i + 1]
        
        # If chapters are consecutive, mark current as completed
        if next_chapter == current_chapter + 1:
            completion_date = chapter_last_dates[current_chapter]
            achievements.append({
                'type': 'chapter_completion',
                'description': f'📚 第{current_chapter}章完成！',
                'date': completion_date,
                'chapter': current_chapter
            })
    
    # Detect milestone achievements (every 100 problems)
    milestone_dates = {}  # milestone -> date_achieved
    
    for date, count in total_problems_by_date.items():
        milestone = (count // 100) * 100
        if milestone >= 100 and milestone not in milestone_dates:
            milestone_dates[milestone] = date
    
    # Add milestone achievements
    for milestone, date in milestone_dates.items():
        achievements.append({
            'type': 'milestone',
            'description': f'🎯 完成{milestone}道题目！',
            'date': date,
            'milestone': milestone
        })
    
    # Sort by date (newest first), then by type for same dates
    achievements.sort(key=lambda x: (x['date'], x['type']), reverse=True)
    
    return achievements

def detect_chapter_completion(all_data: List[Dict[str, Any]]) -> List[str]:
    """Detect completed chapters from the data."""
    if not all_data:
        return []
    
    # Get all problems and exercises
    all_problems = []
    all_exercises = []
    
    for record in all_data:
        all_problems.extend(record.get('problems', []))
        all_exercises.extend(record.get('exercises', []))
    
    completed_chapters = []
    
    # Simple heuristic: if we see chapter X followed by chapter X+1 problems
    # we assume chapter X is completed
    from utils.validation import parse_problem_number
    
    chapters_seen = set()
    for prob in all_problems + all_exercises:
        parsed = parse_problem_number(prob)
        if parsed:
            chapters_seen.add(parsed[0])
    
    sorted_chapters = sorted(chapters_seen)
    for i in range(len(sorted_chapters) - 1):
        current_chapter = sorted_chapters[i]
        next_chapter = sorted_chapters[i + 1]
        if next_chapter == current_chapter + 1:
            completed_chapters.append(f"第{current_chapter}章完成！🎉")
    
    return completed_chapters
