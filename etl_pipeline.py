import pandas as pd
import numpy as np
import os

def load_data(file_path):
    """Loads the dataset and performs initial inspection."""
    print(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    print(f"Dataset shape: {df.shape}")
    return df

def clean_data(df):
    """Handles nulls, duplicates, and standardizes data."""
    print("Cleaning data...")
    # Drop duplicates if any
    df = df.drop_duplicates()
    
    # Check for nulls (HR dataset usually doesn't have nulls, but good practice)
    if df.isnull().sum().sum() > 0:
        df = df.fillna(method='ffill')
    
    # Drop columns that add no value (standard HR dataset columns)
    cols_to_drop = ['EmployeeCount', 'Over18', 'StandardHours']
    df = df.drop(columns=[col for col in cols_to_drop if col in df.columns], errors='ignore')
    
    return df

def feature_engineering(df):
    """Engineers business features for advanced analytics."""
    print("Engineering features...")
    
    # 1. Age Groups
    bins_age = [17, 25, 35, 45, 100]
    labels_age = ['18-25', '26-35', '36-45', '46+']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins_age, labels=labels_age)
    
    # 2. Income Bands
    quantiles = df['MonthlyIncome'].quantile([0.33, 0.66]).to_dict()
    def income_band(income):
        if income <= quantiles[0.33]: return 'Low Income'
        elif income <= quantiles[0.66]: return 'Medium Income'
        else: return 'High Income'
    df['IncomeBand'] = df['MonthlyIncome'].apply(income_band)
    
    # 3. Tenure Categories
    bins_tenure = [-1, 2, 7, 50]
    labels_tenure = ['New Employee', 'Mid Tenure', 'Long Tenure']
    df['TenureCategory'] = pd.cut(df['YearsAtCompany'], bins=bins_tenure, labels=labels_tenure)
    
    # 4. Satisfaction Categories (Avg of environment, job, relationship)
    df['AvgSatisfaction'] = df[['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction']].mean(axis=1)
    df['SatisfactionCategory'] = pd.cut(df['AvgSatisfaction'], bins=[0, 2, 3, 5], labels=['Low', 'Medium', 'High'])
    
    # 5. Overtime Risk Indicator
    df['OvertimeRisk'] = np.where(df['OverTime'] == 'Yes', 'High Risk', 'Low Risk')
    
    # 6. Attrition Flag (Numeric for aggregations)
    df['AttritionFlag'] = np.where(df['Attrition'] == 'Yes', 1, 0)
    
    # 7. Attrition Risk Score (Heuristic based on Low Satisfaction, High Overtime, Low Income)
    def calculate_risk(row):
        score = 0
        if row['OverTime'] == 'Yes': score += 3
        if row['SatisfactionCategory'] == 'Low': score += 3
        if row['IncomeBand'] == 'Low Income': score += 2
        if row['AgeGroup'] == '18-25': score += 1
        if row['YearsSinceLastPromotion'] > 3: score += 1
        return score
        
    df['AttritionRiskScore'] = df.apply(calculate_risk, axis=1)
    
    # Retention Segments based on Risk Score
    df['RetentionSegment'] = pd.cut(df['AttritionRiskScore'], bins=[-1, 3, 6, 15], labels=['Safe', 'At Risk', 'Flight Risk'])
    
    return df

def generate_star_schema(df, output_dir):
    """Generates the Fact and Dimension tables and exports them."""
    print("Generating Star Schema...")
    os.makedirs(output_dir, exist_ok=True)
    
    # Create surrogate keys
    # Department Dimension
    dim_dept = df[['Department', 'JobRole']].drop_duplicates().reset_index(drop=True)
    dim_dept['DepartmentID'] = dim_dept.index + 1
    
    # Merge back to get DepartmentID
    df = df.merge(dim_dept, on=['Department', 'JobRole'], how='left')
    
    # Satisfaction Dimension
    satisfaction_cols = ['EnvironmentSatisfaction', 'JobSatisfaction', 'RelationshipSatisfaction', 'WorkLifeBalance', 'SatisfactionCategory', 'AvgSatisfaction']
    dim_satisfaction = df[satisfaction_cols].drop_duplicates().reset_index(drop=True)
    dim_satisfaction['SatisfactionID'] = dim_satisfaction.index + 1
    df = df.merge(dim_satisfaction, on=satisfaction_cols, how='left')
    
    # Dimension: Employee
    emp_cols = ['EmployeeNumber', 'Age', 'AgeGroup', 'Gender', 'MaritalStatus', 'Education', 'EducationField', 'DistanceFromHome']
    dim_employee = df[emp_cols].drop_duplicates()
    
    # Dimension: Compensation
    comp_cols = ['EmployeeNumber', 'MonthlyIncome', 'IncomeBand', 'DailyRate', 'HourlyRate', 'MonthlyRate', 'PercentSalaryHike', 'StockOptionLevel']
    dim_compensation = df[comp_cols].drop_duplicates()
    
    # Fact: Attrition
    fact_cols = ['EmployeeNumber', 'DepartmentID', 'SatisfactionID', 'Attrition', 'AttritionFlag', 'OverTime', 'OvertimeRisk', 
                 'YearsAtCompany', 'TenureCategory', 'TotalWorkingYears', 'YearsInCurrentRole', 'YearsSinceLastPromotion', 
                 'YearsWithCurrManager', 'NumCompaniesWorked', 'TrainingTimesLastYear', 'PerformanceRating', 
                 'BusinessTravel', 'JobLevel', 'JobInvolvement', 'AttritionRiskScore', 'RetentionSegment']
    fact_attrition = df[fact_cols]
    
    # Exporting
    dim_dept.to_csv(f"{output_dir}/DimDepartment.csv", index=False)
    dim_satisfaction.to_csv(f"{output_dir}/DimSatisfaction.csv", index=False)
    dim_employee.to_csv(f"{output_dir}/DimEmployee.csv", index=False)
    dim_compensation.to_csv(f"{output_dir}/DimCompensation.csv", index=False)
    fact_attrition.to_csv(f"{output_dir}/FactEmployeeAttrition.csv", index=False)
    
    print("ETL complete. Star schema saved to", output_dir)

def run_pipeline():
    file_path = '/Users/darshanadhikari/Desktop/hr attrition project/HR-Employee-Attrition.csv'
    output_dir = 'data'
    
    df = load_data(file_path)
    df = clean_data(df)
    df = feature_engineering(df)
    generate_star_schema(df, output_dir)

if __name__ == "__main__":
    run_pipeline()
