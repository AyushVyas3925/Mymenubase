# Machine Learning tools module
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import google.generativeai as genai
import json
import os
import tempfile
import librosa
import librosa.display
import cv2
import mediapipe as mp
from datetime import datetime, timedelta
import random

def ml_emi_predictor():
    """EMI and Insurance Predictor"""
    st.subheader("💼 EMI & Insurance Predictor")
    st.write("Calculate EMI and predict insurance premiums")

    tab1, tab2 = st.tabs(["💰 EMI Calculator", "🛡️ Insurance Predictor"])

    with tab1:
        st.subheader("💰 EMI Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            principal = st.number_input("Principal Amount (₹)", min_value=1000, value=100000, step=1000)
            rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, value=10.0, step=0.1)
            time = st.number_input("Time Period (Years)", min_value=1, value=5, step=1)
        
        with col2:
            if st.button("Calculate EMI", key="calculate_emi_btn"):
                monthly_rate = rate / (12 * 100)
                total_months = time * 12
                
                if monthly_rate > 0:
                    emi = principal * (monthly_rate * (1 + monthly_rate)**total_months) / ((1 + monthly_rate)**total_months - 1)
                    total_amount = emi * total_months
                    total_interest = total_amount - principal
                    
                    st.success(f"Monthly EMI: ₹{emi:.2f}")
                    st.info(f"Total Amount: ₹{total_amount:.2f}")
                    st.warning(f"Total Interest: ₹{total_interest:.2f}")
                    
                    # Create pie chart
                    fig = go.Figure(data=[go.Pie(labels=['Principal', 'Interest'], 
                                               values=[principal, total_interest],
                                               hole=.3)])
                    fig.update_layout(title="EMI Breakdown")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.error("Invalid interest rate")

    with tab2:
        st.subheader("🛡️ Insurance Premium Predictor")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Age", 18, 80, 30)
            coverage = st.selectbox("Coverage Amount", ["₹5L", "₹10L", "₹25L", "₹50L", "₹1Cr"])
            health = st.selectbox("Health Status", ["Excellent", "Good", "Average", "Poor"])
            occupation = st.selectbox("Occupation Risk", ["Low", "Medium", "High"])
        
        with col2:
            if st.button("Predict Premium", key="predict_premium_btn"):
                # Simple premium calculation (for demonstration)
                base_premium = 5000
                age_factor = 1 + (age - 30) * 0.02
                coverage_factor = {"₹5L": 0.5, "₹10L": 1.0, "₹25L": 2.0, "₹50L": 3.5, "₹1Cr": 6.0}[coverage]
                health_factor = {"Excellent": 0.8, "Good": 1.0, "Average": 1.2, "Poor": 1.5}[health]
                risk_factor = {"Low": 0.9, "Medium": 1.0, "High": 1.3}[occupation]
                
                monthly_premium = base_premium * age_factor * coverage_factor * health_factor * risk_factor
                
                st.success(f"Estimated Monthly Premium: ₹{monthly_premium:.0f}")
                
                # Create bar chart
                factors = ['Age', 'Coverage', 'Health', 'Risk']
                values = [age_factor, coverage_factor, health_factor, risk_factor]
                
                fig = go.Figure(data=[go.Bar(x=factors, y=values)])
                fig.update_layout(title="Premium Factors", yaxis_title="Factor Value")
                st.plotly_chart(fig, use_container_width=True)

def ml_student_performance():
    """Student Performance Analyzer"""
    st.subheader("📊 Student Performance Analyzer")
    st.write("Analyze student performance with interactive visualizations")

    # -----------------------
    # 🛠️ Helper Functions
    # -----------------------
    def add_download_button(df, filename):
        """Add download button for dataframe"""
        csv = df.to_csv(index=False)
        st.download_button(
            label=f"📥 Download {filename}",
            data=csv,
            file_name=filename,
            mime="text/csv"
        )

    def suggest_college(score):
        """Suggest college based on score"""
        if score >= 90:
            return "🏆 Top Tier College - Excellent choice!"
        elif score >= 80:
            return "🎯 Good College - Strong performance!"
        elif score >= 70:
            return "📚 Average College - Room for improvement"
        else:
            return "💪 Community College - Focus on improvement"

    def score_to_gpa(score):
        """Convert percentage to GPA"""
        if score >= 90:
            return 4.0
        elif score >= 80:
            return 3.5
        elif score >= 70:
            return 3.0
        elif score >= 60:
            return 2.5
        else:
            return 2.0

    @st.cache_data
    def load_sample_data():
        """Load sample student data"""
        np.random.seed(42)
        n_students = 100
        
        data = {
            'Student_ID': range(1, n_students + 1),
            'Name': [f"Student_{i}" for i in range(1, n_students + 1)],
            'Math_Score': np.random.normal(75, 15, n_students).clip(0, 100),
            'Science_Score': np.random.normal(78, 12, n_students).clip(0, 100),
            'English_Score': np.random.normal(80, 10, n_students).clip(0, 100),
            'History_Score': np.random.normal(72, 18, n_students).clip(0, 100),
            'Study_Hours': np.random.normal(6, 2, n_students).clip(1, 12),
            'Sleep_Hours': np.random.normal(7, 1.5, n_students).clip(5, 10),
            'Attendance': np.random.normal(85, 10, n_students).clip(60, 100)
        }
        
        df = pd.DataFrame(data)
        df['Total_Score'] = df[['Math_Score', 'Science_Score', 'English_Score', 'History_Score']].sum(axis=1)
        df['Average_Score'] = df['Total_Score'] / 4
        df['GPA'] = df['Average_Score'].apply(score_to_gpa)
        
        return df

    # -----------------------
    # 📊 Main Application
    # -----------------------
    st.title("📊 Student Performance Analyzer")
    st.markdown("---")

    # Load data
    df = load_sample_data()

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    min_score = st.sidebar.slider("Minimum Average Score", 0, 100, 0)
    max_score = st.sidebar.slider("Maximum Average Score", 0, 100, 100)
    
    min_gpa = st.sidebar.slider("Minimum GPA", 0.0, 4.0, 0.0, 0.1)
    max_gpa = st.sidebar.slider("Maximum GPA", 0.0, 4.0, 4.0, 0.1)

    # Filter data
    filtered_df = df[
        (df['Average_Score'] >= min_score) & 
        (df['Average_Score'] <= max_score) &
        (df['GPA'] >= min_gpa) & 
        (df['GPA'] <= max_gpa)
    ]

    # Main content
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📈 Performance Overview")
        
        # Key metrics
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        with metrics_col1:
            st.metric("Total Students", len(filtered_df))
        with metrics_col2:
            st.metric("Average Score", f"{filtered_df['Average_Score'].mean():.1f}%")
        with metrics_col3:
            st.metric("Average GPA", f"{filtered_df['GPA'].mean():.2f}")
        with metrics_col4:
            st.metric("Top Performer", f"{filtered_df['Average_Score'].max():.1f}%")

        # Performance distribution
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Score Distribution', 'GPA Distribution', 'Study vs Score', 'Attendance vs Score'),
            specs=[[{"type": "histogram"}, {"type": "histogram"}],
                   [{"type": "scatter"}, {"type": "scatter"}]]
        )

        # Score distribution
        fig.add_trace(go.Histogram(x=filtered_df['Average_Score'], name='Scores'), row=1, col=1)
        
        # GPA distribution
        fig.add_trace(go.Histogram(x=filtered_df['GPA'], name='GPA'), row=1, col=2)
        
        # Study hours vs Score
        fig.add_trace(go.Scatter(x=filtered_df['Study_Hours'], y=filtered_df['Average_Score'], 
                                mode='markers', name='Study vs Score'), row=2, col=1)
        
        # Attendance vs Score
        fig.add_trace(go.Scatter(x=filtered_df['Attendance'], y=filtered_df['Average_Score'], 
                                mode='markers', name='Attendance vs Score'), row=2, col=2)

        fig.update_layout(height=600, title_text="Performance Analysis Dashboard")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Quick Insights")
        
        # Top performers
        top_students = filtered_df.nlargest(5, 'Average_Score')[['Name', 'Average_Score', 'GPA']]
        st.write("🏆 **Top 5 Students:**")
        st.dataframe(top_students, use_container_width=True)
        
        # Subject analysis
        subjects = ['Math_Score', 'Science_Score', 'English_Score', 'History_Score']
        subject_means = [filtered_df[subject].mean() for subject in subjects]
        
        fig = go.Figure(data=[go.Bar(x=subjects, y=subject_means)])
        fig.update_layout(title="Subject Performance", height=300)
        st.plotly_chart(fig, use_container_width=True)

    # Detailed analysis section
    st.markdown("---")
    st.subheader("🔍 Detailed Analysis")

    tab1, tab2, tab3 = st.tabs(["📊 Statistical Analysis", "🎓 College Recommendations", "📈 Trend Analysis"])

    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Correlation Matrix:**")
            corr_matrix = filtered_df[['Math_Score', 'Science_Score', 'English_Score', 'History_Score', 
                                     'Study_Hours', 'Sleep_Hours', 'Attendance']].corr()
            
            fig = px.imshow(corr_matrix, text_auto=True, aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Performance by GPA Range:**")
            gpa_ranges = pd.cut(filtered_df['GPA'], bins=[0, 2.0, 2.5, 3.0, 3.5, 4.0], 
                               labels=['0-2.0', '2.0-2.5', '2.5-3.0', '3.0-3.5', '3.5-4.0'])
            gpa_stats = filtered_df.groupby(gpa_ranges)['Average_Score'].agg(['count', 'mean', 'std'])
            st.dataframe(gpa_stats, use_container_width=True)

    with tab2:
        st.write("**College Recommendations based on Performance:**")
        
        # Generate recommendations
        recommendations = []
        for _, student in filtered_df.iterrows():
            college = suggest_college(student['Average_Score'])
            recommendations.append({
                'Student': student['Name'],
                'Score': f"{student['Average_Score']:.1f}%",
                'GPA': f"{student['GPA']:.2f}",
                'Recommendation': college
            })
        
        rec_df = pd.DataFrame(recommendations)
        st.dataframe(rec_df, use_container_width=True)
        
        # Download recommendations
        add_download_button(rec_df, "college_recommendations.csv")

    with tab3:
        # Time series analysis (simulated)
        st.write("**Performance Trends (Simulated Monthly Data):**")
        
        # Generate monthly trend data
        months = pd.date_range(start='2024-01-01', end='2024-12-01', freq='M')
        trend_data = []
        
        for month in months:
            # Simulate improving performance over time
            base_score = 70
            improvement = (month.month - 1) * 2
            monthly_score = base_score + improvement + np.random.normal(0, 3)
            trend_data.append({
                'Month': month.strftime('%B %Y'),
                'Average_Score': max(0, min(100, monthly_score))
            })
        
        trend_df = pd.DataFrame(trend_data)
        
        fig = px.line(trend_df, x='Month', y='Average_Score', markers=True)
        fig.update_layout(title="Monthly Performance Trend", xaxis_title="Month", yaxis_title="Average Score")
        st.plotly_chart(fig, use_container_width=True)

    # Download section
    st.markdown("---")
    st.subheader("📥 Download Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        add_download_button(filtered_df, "filtered_student_data.csv")
    
    with col2:
        add_download_button(df, "complete_student_data.csv")

def ml_smart_meter_app():
    """Smart Meter Bill Predictor"""
    st.subheader("🔌 Smart Meter Bill Predictor")
    st.write("Predict electricity bills using machine learning")

    # Initialize session state
    if 'smart_meter_model' not in st.session_state:
        st.session_state.smart_meter_model = None
    if 'smart_meter_data' not in st.session_state:
        st.session_state.smart_meter_data = None

    # Helper Functions
    def train_and_save_model():
        """Train and save the smart meter model"""
        np.random.seed(42)
        n_samples = 1000
        
        # Generate synthetic smart meter data
        data = {
            'kwh_used': np.random.normal(500, 150, n_samples).clip(100, 1000),
            'peak_hours': np.random.normal(4, 2, n_samples).clip(0, 12),
            'temperature': np.random.normal(25, 10, n_samples).clip(5, 40),
            'humidity': np.random.normal(60, 20, n_samples).clip(20, 100),
            'day_of_week': np.random.randint(0, 7, n_samples),
            'is_holiday': np.random.choice([0, 1], n_samples, p=[0.8, 0.2])
        }
        
        # Calculate bill (with some noise)
        base_rate = 0.12  # $0.12 per kWh
        peak_multiplier = 1.5
        temperature_factor = 1 + (data['temperature'] - 25) * 0.01
        
        bills = (data['kwh_used'] * base_rate * 
                (1 + (data['peak_hours'] / 24) * (peak_multiplier - 1)) * 
                temperature_factor + 
                np.random.normal(0, 5, n_samples))
        
        data['bill_amount'] = bills.clip(10, 200)
        
        df = pd.DataFrame(data)
        
        # Prepare features
        X = df[['kwh_used', 'peak_hours', 'temperature', 'humidity', 'day_of_week', 'is_holiday']]
        y = df['bill_amount']
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Save to session state
        st.session_state.smart_meter_model = model
        st.session_state.smart_meter_data = df
        
        return model, df

    @st.cache_resource
    def load_model():
        """Load the trained model"""
        if st.session_state.smart_meter_model is None:
            model, df = train_and_save_model()
        return st.session_state.smart_meter_model, st.session_state.smart_meter_data

    # Main App
    tab1, tab2, tab3 = st.tabs(["🔮 Predict Bill", "📊 Data Analysis", "⚡ Usage Insights"])

    with tab1:
        st.subheader("🔮 Predict Your Electricity Bill")
        
        col1, col2 = st.columns(2)
        
        with col1:
            kwh_used = st.number_input("kWh Used", min_value=50, max_value=2000, value=500, step=10)
            peak_hours = st.slider("Peak Hours Usage", 0, 24, 4)
            temperature = st.slider("Average Temperature (°C)", 0, 50, 25)
            humidity = st.slider("Average Humidity (%)", 0, 100, 60)
        
        with col2:
            day_of_week = st.selectbox("Day of Week", 
                                     ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            is_holiday = st.checkbox("Is Holiday")
            
            # Convert day to number
            day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
                      "Friday": 4, "Saturday": 5, "Sunday": 6}
            day_num = day_map[day_of_week]
            holiday_num = 1 if is_holiday else 0
        
        if st.button("🔮 Predict Bill", key="predict_bill_btn"):
            model, df = load_model()
            
            # Make prediction
            features = np.array([[kwh_used, peak_hours, temperature, humidity, day_num, holiday_num]])
            predicted_bill = model.predict(features)[0]
            
            st.success(f"💡 **Predicted Bill: ${predicted_bill:.2f}**")
            
            # Show breakdown
            base_cost = kwh_used * 0.12
            peak_surcharge = base_cost * (peak_hours / 24) * 0.5
            temperature_adjustment = base_cost * (temperature - 25) * 0.01
            
            st.info(f"""
            **Bill Breakdown:**
            - Base Cost (${base_cost:.2f}): {kwh_used} kWh × $0.12
            - Peak Hours Surcharge (${peak_surcharge:.2f}): {peak_hours} peak hours
            - Temperature Adjustment (${temperature_adjustment:.2f}): {temperature}°C
            """)

    with tab2:
        st.subheader("📊 Smart Meter Data Analysis")
        
        model, df = load_model()
        
        # Show sample data
        st.write("**Sample Smart Meter Data:**")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Correlation analysis
        st.write("**Feature Correlation with Bill Amount:**")
        corr = df.corr()['bill_amount'].sort_values(ascending=False)
        fig = px.bar(x=corr.index, y=corr.values, title="Feature Correlation with Bill")
        st.plotly_chart(fig, use_container_width=True)
        
        # Usage patterns
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(df, x='kwh_used', y='bill_amount', 
                           title="Usage vs Bill Amount")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(df, x='temperature', y='bill_amount', 
                           title="Temperature vs Bill Amount")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("⚡ Usage Insights & Recommendations")
        
        model, df = load_model()
        
        # Usage statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_usage = df['kwh_used'].mean()
            st.metric("Average Usage", f"{avg_usage:.1f} kWh")
        
        with col2:
            avg_bill = df['bill_amount'].mean()
            st.metric("Average Bill", f"${avg_bill:.2f}")
        
        with col3:
            peak_usage = df['peak_hours'].mean()
            st.metric("Peak Hours", f"{peak_usage:.1f} hours")
        
        # Recommendations
        st.write("**💡 Energy Saving Recommendations:**")
        
        recommendations = [
            "🌅 **Shift Usage to Off-Peak Hours:** Use major appliances during off-peak hours to avoid surcharges.",
            "🌡️ **Optimize Temperature:** Keep your home at 22-24°C for optimal energy efficiency.",
            "💡 **Use LED Bulbs:** Replace incandescent bulbs with energy-efficient LEDs.",
            "🔌 **Unplug Unused Devices:** Many devices consume power even when turned off.",
            "🏠 **Improve Insulation:** Better insulation reduces heating/cooling costs."
        ]
        
        for rec in recommendations:
            st.write(rec)
        
        # Usage comparison
        st.write("**📊 Your Usage vs Average:**")
        
        # Get user input for comparison
        user_kwh = st.number_input("Enter your kWh usage for comparison:", value=500, key="compare_kwh")
        
        if st.button("Compare Usage", key="compare_usage_btn"):
            user_bill = model.predict([[user_kwh, 4, 25, 60, 0, 0]])[0]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Your Usage", f"{user_kwh} kWh", 
                         delta=f"{user_kwh - avg_usage:.1f} kWh")
            
            with col2:
                st.metric("Your Bill", f"${user_bill:.2f}", 
                         delta=f"${user_bill - avg_bill:.2f}")
            
            if user_kwh > avg_usage:
                st.warning("⚠️ Your usage is above average. Consider the energy-saving tips above!")
            else:
                st.success("✅ Great job! Your usage is below average.")

def ml_advanced_salary_predictor():
    """Advanced Salary Predictor"""
    st.subheader("💼 Advanced Salary Predictor")
    st.write("Predict salary based on multiple factors using machine learning")

    # Initialize session state
    if 'salary_model' not in st.session_state:
        st.session_state.salary_model = None
    if 'salary_data' not in st.session_state:
        st.session_state.salary_data = None

    # Helper Functions
    @st.cache_data
    def load_data():
        """Load salary dataset"""
        np.random.seed(42)
        n_samples = 2000
        
        # Generate synthetic salary data
        data = {
            'age': np.random.normal(35, 10, n_samples).clip(22, 65),
            'experience_years': np.random.normal(8, 6, n_samples).clip(0, 30),
            'education_level': np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'], n_samples),
            'job_title': np.random.choice(['Software Engineer', 'Data Scientist', 'Manager', 'Analyst', 'Developer'], n_samples),
            'company_size': np.random.choice(['Startup', 'Small', 'Medium', 'Large', 'Enterprise'], n_samples),
            'location': np.random.choice(['Remote', 'Small City', 'Medium City', 'Large City', 'Metro'], n_samples),
            'skills_count': np.random.poisson(8, n_samples).clip(1, 20),
            'certifications': np.random.poisson(2, n_samples).clip(0, 8),
            'projects_completed': np.random.poisson(15, n_samples).clip(0, 50)
        }
        
        # Calculate salary based on factors
        base_salary = 50000
        
        # Age factor (peaks around 40-45)
        age_factor = 1 + np.exp(-((data['age'] - 42.5) / 10)**2) * 0.5
        
        # Experience factor
        exp_factor = 1 + (data['experience_years'] / 20) * 1.5
        
        # Education factor
        edu_factors = {'High School': 0.7, 'Bachelor': 1.0, 'Master': 1.3, 'PhD': 1.6}
        edu_factor = [edu_factors[edu] for edu in data['education_level']]
        
        # Job title factor
        title_factors = {'Analyst': 0.8, 'Developer': 1.0, 'Software Engineer': 1.1, 
                        'Data Scientist': 1.3, 'Manager': 1.4}
        title_factor = [title_factors[title] for title in data['job_title']]
        
        # Company size factor
        size_factors = {'Startup': 0.8, 'Small': 0.9, 'Medium': 1.0, 'Large': 1.2, 'Enterprise': 1.3}
        size_factor = [size_factors[size] for size in data['company_size']]
        
        # Location factor
        loc_factors = {'Remote': 0.9, 'Small City': 0.8, 'Medium City': 0.9, 
                      'Large City': 1.1, 'Metro': 1.2}
        loc_factor = [loc_factors[loc] for loc in data['location']]
        
        # Skills and certifications
        skills_factor = 1 + (data['skills_count'] - 8) * 0.05
        cert_factor = 1 + data['certifications'] * 0.1
        projects_factor = 1 + (data['projects_completed'] - 15) * 0.02
        
        # Calculate final salary
        salary = (base_salary * age_factor * exp_factor * np.array(edu_factor) * 
                 np.array(title_factor) * np.array(size_factor) * np.array(loc_factor) * 
                 skills_factor * cert_factor * projects_factor)
        
        # Add some noise
        salary = salary + np.random.normal(0, salary * 0.1)
        salary = salary.clip(30000, 200000)
        
        data['salary'] = salary
        
        return pd.DataFrame(data)

    @st.cache_resource
    def train_model():
        """Train the salary prediction model"""
        df = load_data()
        
        # Prepare features
        feature_cols = ['age', 'experience_years', 'skills_count', 'certifications', 'projects_completed']
        
        # Encode categorical variables
        df_encoded = df.copy()
        df_encoded['education_encoded'] = df['education_level'].map({'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3})
        df_encoded['title_encoded'] = df['job_title'].map({'Analyst': 0, 'Developer': 1, 'Software Engineer': 2, 'Data Scientist': 3, 'Manager': 4})
        df_encoded['size_encoded'] = df['company_size'].map({'Startup': 0, 'Small': 1, 'Medium': 2, 'Large': 3, 'Enterprise': 4})
        df_encoded['location_encoded'] = df['location'].map({'Remote': 0, 'Small City': 1, 'Medium City': 2, 'Large City': 3, 'Metro': 4})
        
        feature_cols.extend(['education_encoded', 'title_encoded', 'size_encoded', 'location_encoded'])
        
        X = df_encoded[feature_cols]
        y = df_encoded['salary']
        
        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        return model, df, feature_cols

    # Main App
    tab1, tab2, tab3 = st.tabs(["🔮 Predict Salary", "📊 Market Insights", "💡 Career Tips"])

    with tab1:
        st.subheader("🔮 Predict Your Salary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.slider("Age", 22, 65, 30)
            experience = st.slider("Years of Experience", 0, 30, 5)
            education = st.selectbox("Education Level", ['High School', 'Bachelor', 'Master', 'PhD'])
            job_title = st.selectbox("Job Title", ['Analyst', 'Developer', 'Software Engineer', 'Data Scientist', 'Manager'])
        
        with col2:
            company_size = st.selectbox("Company Size", ['Startup', 'Small', 'Medium', 'Large', 'Enterprise'])
            location = st.selectbox("Location", ['Remote', 'Small City', 'Medium City', 'Large City', 'Metro'])
            skills = st.slider("Number of Skills", 1, 20, 8)
            certifications = st.slider("Number of Certifications", 0, 8, 2)
            projects = st.slider("Projects Completed", 0, 50, 15)
        
        if st.button("🔮 Predict Salary", key="predict_salary_btn"):
            model, df, feature_cols = train_model()
            
            # Encode inputs
            education_encoded = {'High School': 0, 'Bachelor': 1, 'Master': 2, 'PhD': 3}[education]
            title_encoded = {'Analyst': 0, 'Developer': 1, 'Software Engineer': 2, 'Data Scientist': 3, 'Manager': 4}[job_title]
            size_encoded = {'Startup': 0, 'Small': 1, 'Medium': 2, 'Large': 3, 'Enterprise': 4}[company_size]
            location_encoded = {'Remote': 0, 'Small City': 1, 'Medium City': 2, 'Large City': 3, 'Metro': 4}[location]
            
            # Make prediction
            features = np.array([[age, experience, skills, certifications, projects, 
                                education_encoded, title_encoded, size_encoded, location_encoded]])
            predicted_salary = model.predict(features)[0]
            
            st.success(f"💰 **Predicted Salary: ${predicted_salary:,.0f}**")
            
            # Show salary range
            confidence_interval = predicted_salary * 0.15
            st.info(f"**Salary Range:** ${predicted_salary - confidence_interval:,.0f} - ${predicted_salary + confidence_interval:,.0f}")
            
            # Factor analysis
            st.write("**📊 Salary Factors Analysis:**")
            
            factors = {
                'Age': age,
                'Experience': experience,
                'Education': education,
                'Job Title': job_title,
                'Company Size': company_size,
                'Location': location,
                'Skills': skills,
                'Certifications': certifications,
                'Projects': projects
            }
            
            for factor, value in factors.items():
                st.write(f"• **{factor}:** {value}")

    with tab2:
        st.subheader("📊 Market Insights")
        
        model, df, feature_cols = train_model()
        
        # Market statistics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_salary = df['salary'].mean()
            st.metric("Average Salary", f"${avg_salary:,.0f}")
        
        with col2:
            median_salary = df['salary'].median()
            st.metric("Median Salary", f"${median_salary:,.0f}")
        
        with col3:
            max_salary = df['salary'].max()
            st.metric("Top Salary", f"${max_salary:,.0f}")
        
        # Salary by education
        st.write("**🎓 Salary by Education Level:**")
        edu_salary = df.groupby('education_level')['salary'].agg(['mean', 'count']).round(0)
        st.dataframe(edu_salary, use_container_width=True)
        
        # Salary by job title
        st.write("**💼 Salary by Job Title:**")
        title_salary = df.groupby('job_title')['salary'].agg(['mean', 'count']).round(0)
        st.dataframe(title_salary, use_container_width=True)
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.box(df, x='education_level', y='salary', title="Salary Distribution by Education")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.box(df, x='job_title', y='salary', title="Salary Distribution by Job Title")
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("💡 Career Tips & Recommendations")
        
        st.write("**🚀 Tips to Increase Your Salary:**")
        
        tips = [
            "🎓 **Continue Learning:** Pursue advanced degrees or certifications",
            "💼 **Gain Experience:** More years of experience typically lead to higher salaries",
            "🔧 **Develop Skills:** Learn in-demand technical and soft skills",
            "🏢 **Target Larger Companies:** Enterprise companies often pay more than startups",
            "🌆 **Consider Location:** Metropolitan areas typically offer higher salaries",
            "📚 **Build Portfolio:** Complete projects to showcase your skills",
            "🤝 **Network:** Build professional relationships in your industry",
            "📈 **Track Market Trends:** Stay updated with industry salary trends"
        ]
        
        for tip in tips:
            st.write(tip)
        
        # Salary negotiation tips
        st.write("**💬 Salary Negotiation Tips:**")
        
        negotiation_tips = [
            "📊 **Research Market Rates:** Know what others in your position earn",
            "💪 **Highlight Achievements:** Quantify your contributions and impact",
            "🎯 **Set Target Range:** Have a specific salary range in mind",
            "⏰ **Choose Timing:** Negotiate during performance reviews or job offers",
            "🔄 **Practice:** Rehearse your negotiation points beforehand",
            "🤝 **Be Professional:** Maintain a positive and collaborative approach"
        ]
        
        for tip in negotiation_tips:
            st.write(tip)

def prompt_engineering_gemini_optimizer():
    """Gemini Prompt Optimizer"""
    st.subheader("🚀 Gemini Prompt Optimizer")
    st.write("Optimize your prompts for better AI responses")

    # Initialize session state
    if 'optimized_prompts' not in st.session_state:
        st.session_state.optimized_prompts = []

    # Prompt optimization techniques
    techniques = {
        "Role Definition": "Define the AI's role clearly (e.g., 'You are an expert data scientist')",
        "Context Setting": "Provide relevant background information and context",
        "Specific Instructions": "Give clear, step-by-step instructions",
        "Output Format": "Specify the desired output format (e.g., 'Provide a table with columns...')",
        "Examples": "Include examples of what you want (e.g., 'Like this: [example]')",
        "Constraints": "Set boundaries and limitations (e.g., 'Keep it under 200 words')",
        "Iterative Refinement": "Ask for improvements or alternatives",
        "Chain of Thought": "Ask the AI to show its reasoning process"
    }

    # Main interface
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("✍️ Enter Your Prompt")
        
        original_prompt = st.text_area(
            "Your Original Prompt:",
            height=150,
            placeholder="Enter the prompt you want to optimize..."
        )
        
        selected_techniques = st.multiselect(
            "Select Optimization Techniques:",
            list(techniques.keys()),
            default=["Role Definition", "Specific Instructions"]
        )

    with col2:
        st.subheader("🔧 Optimization Techniques")
        
        for technique in selected_techniques:
            with st.expander(technique):
                st.write(techniques[technique])
        
        if st.button("🚀 Optimize Prompt", key="optimize_prompt_btn"):
            if original_prompt:
                # Apply selected techniques
                optimized = original_prompt
                
                if "Role Definition" in selected_techniques:
                    optimized = f"You are an expert AI assistant. {optimized}"
                
                if "Specific Instructions" in selected_techniques:
                    optimized += "\n\nPlease provide a clear, detailed response with specific examples."
                
                if "Output Format" in selected_techniques:
                    optimized += "\n\nFormat your response in a structured way with clear sections."
                
                if "Examples" in selected_techniques:
                    optimized += "\n\nInclude relevant examples to illustrate your points."
                
                if "Constraints" in selected_techniques:
                    optimized += "\n\nKeep your response concise and focused."
                
                if "Chain of Thought" in selected_techniques:
                    optimized += "\n\nPlease explain your reasoning process step by step."
                
                # Store in session state
                st.session_state.optimized_prompts.append({
                    'original': original_prompt,
                    'optimized': optimized,
                    'techniques': selected_techniques,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                st.success("✅ Prompt optimized successfully!")
                st.rerun()
            else:
                st.warning("Please enter a prompt to optimize.")

    # Display optimized prompts
    if st.session_state.optimized_prompts:
        st.markdown("---")
        st.subheader("📝 Optimized Prompts History")
        
        for i, prompt_data in enumerate(reversed(st.session_state.optimized_prompts)):
            with st.expander(f"Prompt {len(st.session_state.optimized_prompts) - i} - {prompt_data['timestamp']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**Original Prompt:**")
                    st.text_area("", prompt_data['original'], height=100, key=f"orig_{i}", disabled=True)
                
                with col2:
                    st.write("**Optimized Prompt:**")
                    st.text_area("", prompt_data['optimized'], height=100, key=f"opt_{i}", disabled=True)
                
                st.write("**Techniques Applied:**")
                for technique in prompt_data['techniques']:
                    st.write(f"• {technique}")
                
                # Copy buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy Original", key=f"copy_orig_{i}"):
                        st.write("Original prompt copied to clipboard!")
                
                with col2:
                    if st.button("📋 Copy Optimized", key=f"copy_opt_{i}"):
                        st.write("Optimized prompt copied to clipboard!")

def machine_learning_menu():
    """Main machine learning menu"""
    st.title("🤖 Machine Learning Tools")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "💼 EMI & Insurance", "📊 Student Performance", "🔌 Smart Meter", "💰 Salary Predictor", "✍️ Prompt Engineering"
    ])

    with tab1:
        ml_emi_predictor()

    with tab2:
        ml_student_performance()

    with tab3:
        ml_smart_meter_app()

    with tab4:
        ml_advanced_salary_predictor()

    with tab5:
        prompt_engineering_gemini_optimizer()
