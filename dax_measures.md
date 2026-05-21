# HR Attrition Analytics - Advanced DAX Measures

This document contains the DAX measures requested for the Power BI implementation of the Star Schema data model. 

## 1. Core KPIs

```dax
Total Employees = 
// Row Context: Iterates over FactEmployeeAttrition
// Filter Context: Evaluates based on active visual filters
DISTINCTCOUNT(FactEmployeeAttrition[EmployeeNumber])
```

```dax
Attrition Count = 
CALCULATE(
    [Total Employees],
    FactEmployeeAttrition[Attrition] = "Yes"
)
```

```dax
Attrition Rate = 
// Safely divides Attrition Count by Total Employees to prevent divide by zero errors
DIVIDE(
    [Attrition Count],
    [Total Employees],
    0
)
```

## 2. Advanced Metrics

```dax
Avg Monthly Income = 
AVERAGE(DimCompensation[MonthlyIncome])
```

```dax
Avg Years at Company = 
AVERAGE(FactEmployeeAttrition[YearsAtCompany])
```

```dax
Overtime Employees % = 
VAR OvertimeCount = CALCULATE([Total Employees], FactEmployeeAttrition[OverTime] = "Yes")
RETURN
DIVIDE(OvertimeCount, [Total Employees], 0)
```

## 3. Risk & Retention Analysis

```dax
High Risk Employees = 
CALCULATE(
    [Total Employees],
    FactEmployeeAttrition[RetentionSegment] = "Flight Risk"
)
```

```dax
Employee Retention Rate = 
1 - [Attrition Rate]
```

```dax
Satisfaction Score = 
// Computes an average satisfaction level from the dimension
AVERAGE(DimSatisfaction[AvgSatisfaction])
```

## 4. Time Intelligence & Dynamic Measures

```dax
Department Attrition % = 
// Calculates the specific department's attrition against ALL departments
VAR DeptAttrition = [Attrition Count]
VAR AllAttrition = CALCULATE([Attrition Count], ALL(DimDepartment))
RETURN
DIVIDE(DeptAttrition, AllAttrition, 0)
```

```dax
Running Attrition Trend = 
// Requires a DimDate table linked to an exit date (if available). 
// Assuming a hypothetical 'ExitDate' in FactEmployeeAttrition
CALCULATE(
    [Attrition Count],
    FILTER(
        ALL(DimDate),
        DimDate[Date] <= MAX(DimDate[Date])
    )
)
```

```dax
Dynamic KPI Measure = 
// Allows the user to select which KPI they want to view on the dashboard
VAR SelectedKPI = SELECTEDVALUE('KPI_Selection'[KPI_Name], "Total Employees")
RETURN
SWITCH(SelectedKPI,
    "Total Employees", [Total Employees],
    "Attrition Count", [Attrition Count],
    "Attrition Rate", FORMAT([Attrition Rate], "Percent"),
    "Avg Monthly Income", FORMAT([Avg Monthly Income], "Currency"),
    BLANK()
)
```

## Business Relevance
- **Context Transition**: The use of `CALCULATE` effectively transitions row context to filter context, allowing for accurate aggregations over segments like Overtime or Retention Segments.
- **`ALL` function**: Useful for stripping away filters (e.g., in `Department Attrition %`) to find the ratio of a part to the whole.
- **Dynamic KPIs**: Provide a more executive-friendly, clean dashboard interface where multiple metrics can share a single visualization block.
