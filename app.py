import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set page config for an executive feel
st.set_page_config(page_title="HR Attrition Story", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for visual polish
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #60A5FA;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #9CA3AF;
        margin-bottom: 2rem;
    }
    .story-card {
        background-color: #1E293B;
        color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 20px;
    }
    .recommendation-card {
        background-color: #064E3B;
        color: #F8FAFC;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    try:
        fact = pd.read_csv('data/FactEmployeeAttrition.csv')
        dim_emp = pd.read_csv('data/DimEmployee.csv')
        dim_dept = pd.read_csv('data/DimDepartment.csv')
        dim_comp = pd.read_csv('data/DimCompensation.csv')
        dim_sat = pd.read_csv('data/DimSatisfaction.csv')
        
        # Merge for easy plotting
        df = fact.merge(dim_emp, on='EmployeeNumber')
        df = df.merge(dim_dept, on='DepartmentID')
        df = df.merge(dim_comp, on='EmployeeNumber')
        df = df.merge(dim_sat, on='SatisfactionID')
        return df
    except FileNotFoundError:
        return None

df = load_data()

if df is None:
    st.error("Data files not found. Please run the ETL pipeline first.")
    st.stop()

# --- SIDEBAR NAVIGATION ---
st.sidebar.markdown("### 📊 Data Story Navigation")
pages = [
    "1. The Problem",
    "2. Workforce Overview",
    "3. Attrition Drivers",
    "4. High-Risk Segments",
    "5. Operational Insights",
    "6. Business Recommendations"
]
page = st.sidebar.radio("Go to:", pages)

st.sidebar.markdown("---")
st.sidebar.markdown("### ⚙️ Global Filters")
department_filter = st.sidebar.multiselect("Department", options=df['Department'].unique(), default=df['Department'].unique())
gender_filter = st.sidebar.multiselect("Gender", options=df['Gender'].unique(), default=df['Gender'].unique())

filtered_df = df[
    (df['Department'].isin(department_filter)) &
    (df['Gender'].isin(gender_filter))
]

# Color palette for Plotly
custom_colors = px.colors.qualitative.Prism

# --- PAGE 1: THE PROBLEM ---
if page == "1. The Problem":
    st.markdown('<p class="main-header">1. The Business Problem</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Understanding the cost of employee turnover and our baseline metrics.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <strong>The Challenge:</strong> High employee turnover disrupts operations, lowers team morale, and dramatically increases recruitment costs. 
        Currently, HR lacks proactive visibility into <i>why</i> employees are leaving. Our objective is to transition from reactive exit interviews to proactive, data-driven retention strategies.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    total_emp = len(filtered_df)
    attrition_count = filtered_df['AttritionFlag'].sum()
    attrition_rate = (attrition_count / total_emp) * 100 if total_emp > 0 else 0
    
    col1.metric("Total Workforce", f"{total_emp:,}")
    col2.metric("Total Attrition", f"{attrition_count:,}")
    col3.metric("Current Attrition Rate", f"{attrition_rate:.1f}%")
    
    st.markdown("---")
    
    # Baseline Attrition Trend (Simulated via Age as a proxy for this static dataset)
    st.subheader("Attrition Distribution by Department")
    dept_attr = filtered_df.groupby('Department')['AttritionFlag'].mean().reset_index()
    dept_attr['AttritionRate'] = dept_attr['AttritionFlag'] * 100
    fig = px.bar(dept_attr, x='Department', y='AttritionRate', 
                 text_auto='.1f', color='Department', color_discrete_sequence=custom_colors,
                 title="Which departments are losing the most talent?")
    fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Attrition Rate (%)")
    st.plotly_chart(fig, use_container_width=True)


# --- PAGE 2: WORKFORCE OVERVIEW ---
elif page == "2. Workforce Overview":
    st.markdown('<p class="main-header">2. Workforce Overview</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">A demographic snapshot of our current employee base.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        age_dist = filtered_df['AgeGroup'].value_counts().reset_index()
        age_dist.columns = ['Age Group', 'Count']
        fig1 = px.pie(age_dist, names='Age Group', values='Count', hole=0.5, 
                      color_discrete_sequence=custom_colors, title="Workforce by Age Group")
        fig1.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        
    with col2:
        gender_attr = filtered_df.groupby(['Gender', 'Attrition'])['EmployeeNumber'].count().reset_index()
        fig2 = px.bar(gender_attr, x='Gender', y='EmployeeNumber', color='Attrition', barmode='group',
                      color_discrete_sequence=['#2563EB', '#EF4444'], title="Attrition Volume by Gender")
        fig2.update_layout(plot_bgcolor='rgba(0,0,0,0)', yaxis_title="Employee Count")
        st.plotly_chart(fig2, use_container_width=True)
        
    st.subheader("Distribution of Job Roles")
    role_dist = filtered_df['JobRole'].value_counts().reset_index()
    role_dist.columns = ['Job Role', 'Count']
    fig3 = px.bar(role_dist, x='Count', y='Job Role', orientation='h', 
                  color='Job Role', color_discrete_sequence=custom_colors)
    fig3.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)


# --- PAGE 3: ATTRITION DRIVERS ---
elif page == "3. Attrition Drivers":
    st.markdown('<p class="main-header">3. Attrition Drivers</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Identifying the key factors that push employees to leave.</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="story-card">
        <strong>The Overtime Crisis:</strong> Employees who work regular overtime are leaving at vastly higher rates. Burnout is a primary driver of our turnover.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        ot_attr = filtered_df.groupby('OverTime')['AttritionFlag'].mean().reset_index()
        ot_attr['AttritionRate'] = ot_attr['AttritionFlag'] * 100
        fig_ot = px.bar(ot_attr, x='OverTime', y='AttritionRate', text_auto='.1f', 
                        color='OverTime', color_discrete_map={'Yes': '#EF4444', 'No': '#10B981'},
                        title="Attrition Rate by Overtime Status (%)")
        fig_ot.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_ot, use_container_width=True)
        
    with col2:
        sat_attr = filtered_df.groupby('SatisfactionCategory')['AttritionFlag'].mean().reset_index()
        sat_attr['AttritionRate'] = sat_attr['AttritionFlag'] * 100
        fig_sat = px.bar(sat_attr, x='SatisfactionCategory', y='AttritionRate', text_auto='.1f',
                         category_orders={"SatisfactionCategory": ["Low", "Medium", "High"]},
                         color='SatisfactionCategory', color_discrete_map={'Low': '#EF4444', 'Medium': '#F59E0B', 'High': '#10B981'},
                         title="Attrition by Job Satisfaction")
        fig_sat.update_layout(plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
        st.plotly_chart(fig_sat, use_container_width=True)
        
    st.markdown("---")
    st.subheader("The Compensation Factor")
    fig_inc = px.box(filtered_df, x='Attrition', y='MonthlyIncome', color='Attrition', 
                     color_discrete_map={'Yes': '#EF4444', 'No': '#2563EB'},
                     title="Monthly Income Distribution: Retained vs. Departed")
    fig_inc.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_inc, use_container_width=True)


# --- PAGE 4: HIGH-RISK SEGMENTS ---
elif page == "4. High-Risk Segments":
    st.markdown('<p class="main-header">4. High-Risk Employee Segments</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Pinpointing specific employee groups and individuals with the highest flight risk.</p>', unsafe_allow_html=True)

    # Risk segment breakdown
    st.subheader("Workforce by Retention Segment")
    segment_counts = filtered_df[filtered_df['Attrition'] == 'No']['RetentionSegment'].value_counts().reset_index()
    segment_counts.columns = ['Segment', 'Employee Count']
    
    fig_seg = px.pie(segment_counts, names='Segment', values='Employee Count', hole=0.4,
                     color='Segment', color_discrete_map={'Safe': '#10B981', 'At Risk': '#F59E0B', 'Flight Risk': '#EF4444'})
    st.plotly_chart(fig_seg, use_container_width=True)

    st.markdown("---")
    st.subheader("🚨 Critical Flight Risk Employees")
    st.write("These current employees have been flagged by the heuristic model (based on overtime, low satisfaction, and income) as highly likely to leave.")
    
    high_risk = filtered_df[(filtered_df['RetentionSegment'] == 'Flight Risk') & (filtered_df['Attrition'] == 'No')]
    display_cols = ['EmployeeNumber', 'Department', 'JobRole', 'MonthlyIncome', 'OverTime', 'SatisfactionCategory', 'AttritionRiskScore']
    
    st.dataframe(
        high_risk[display_cols].sort_values('AttritionRiskScore', ascending=False).style.background_gradient(subset=['AttritionRiskScore'], cmap='Reds'),
        use_container_width=True, height=400
    )


# --- PAGE 5: OPERATIONAL INSIGHTS ---
elif page == "5. Operational Insights":
    st.markdown('<p class="main-header">5. Operational Insights</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Understanding tenure and role-based operational risks.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="story-card">
        <strong>The Mid-Tenure Slump:</strong> There is a distinct spike in attrition for employees who have been with the company for a few years. We are losing them right as they become highly productive.
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_tenure = px.histogram(filtered_df, x='YearsAtCompany', color='Attrition', barmode='group',
                                  color_discrete_map={'Yes': '#EF4444', 'No': '#E5E7EB'},
                                  title="Attrition Count by Years at Company")
        fig_tenure.update_layout(plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_tenure, use_container_width=True)
        
    with col2:
        role_attr = filtered_df.groupby('JobRole')['AttritionFlag'].mean().reset_index()
        role_attr['RetentionRate'] = (1 - role_attr['AttritionFlag']) * 100
        role_attr = role_attr.sort_values('RetentionRate')
        fig_role = px.bar(role_attr, x='RetentionRate', y='JobRole', orientation='h', 
                          title="Retention Rate by Job Role (%)", color='RetentionRate', color_continuous_scale='RdYlGn')
        fig_role.update_layout(plot_bgcolor='rgba(0,0,0,0)', coloraxis_showscale=False)
        st.plotly_chart(fig_role, use_container_width=True)


# --- PAGE 6: BUSINESS RECOMMENDATIONS ---
elif page == "6. Business Recommendations":
    st.markdown('<p class="main-header">6. Business Recommendations</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Actionable strategies derived from the data to improve workforce retention.</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="recommendation-card">
        <h4>1. Mandate Overtime Monitoring</h4>
        <p><strong>Finding:</strong> Overtime is the strongest predictor of attrition.</p>
        <p><strong>Action:</strong> Implement strict thresholds for consecutive weeks of overtime. Require department head approval for sustained overtime and cross-train teams to distribute workload effectively.</p>
    </div>
    
    <div class="recommendation-card">
        <h4>2. Address the Compensation Gap for Junior Talent</h4>
        <p><strong>Finding:</strong> Entry-level and lower-income bracket employees leave at triple the rate.</p>
        <p><strong>Action:</strong> Conduct an immediate market review for the bottom 33% of earners. Introduce staggered micro-promotions or retention bonuses at the 12-month and 24-month marks.</p>
    </div>
    
    <div class="recommendation-card">
        <h4>3. Combat the Mid-Tenure Slump</h4>
        <p><strong>Finding:</strong> A massive loss of institutional knowledge occurs when employees leave between years 3 and 5.</p>
        <p><strong>Action:</strong> Launch a targeted 'Career Pathing Initiative' at the 2.5-year mark. Force managers to have explicit conversations about lateral mobility and long-term career tracks.</p>
    </div>
    
    <div class="recommendation-card">
        <h4>4. Pulse Surveys over Annual Reviews</h4>
        <p><strong>Finding:</strong> Low environmental and job satisfaction are major red flags.</p>
        <p><strong>Action:</strong> Replace static annual engagement surveys with quarterly, anonymous pulse surveys. Link a portion of management bonuses to their team's average satisfaction scores.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.info("Executive reporting package and raw datasets are available in the project data directory.")
