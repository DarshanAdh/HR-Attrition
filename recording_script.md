# Executive Presentation Walkthrough Script
**Target Length:** 3–5 Minutes
**Focus:** Storytelling, DAX Sophistication, Professional Visuals, Executive KPIs, Interactive Analytics, Clean Data Modeling

---

### [0:00 - 0:45] 1. The Hook & The Problem
"Hello everyone, and thank you for your time. Today, I'm presenting an end-to-end Enterprise HR Attrition Analytics solution. 

The core business challenge we face is that employee turnover is reactive and expensive. High attrition disrupts operations and incurs massive recruitment costs. Currently, HR relies on lagging indicators like exit interviews. 

My objective with this project was to transition us from reactive damage control to proactive retention. To achieve this, I engineered a fully interactive, executive-friendly analytics dashboard designed to identify flight risks *before* they leave, powered by clean data modeling and sophisticated DAX measures."

### [0:45 - 1:30] 2. Data Architecture & Clean Modeling
"Before we look at the visuals, I want to emphasize the foundation. High-quality analytics require high-quality data architecture. 

Using Python, I orchestrated an ETL pipeline to extract the raw HR data, clean it, and perform extensive feature engineering—creating custom 'Attrition Risk Scores', Income Bands, and Tenure Categories. 

Crucially, I transformed the flat file into a professional **Star Schema**, centralizing the metrics in a `FactEmployeeAttrition` table and branching out into optimized Dimension tables for Employees, Departments, and Compensation. This clean data modeling approach ensures scalable performance and enables the sophisticated DAX calculations that power our dashboard."

### [1:30 - 2:15] 3. DAX Sophistication & Executive KPIs
"In the BI layer, I authored advanced DAX measures to drive our Executive KPIs. Rather than simple sums, I utilized context-transition functions like `CALCULATE` and `FILTER` to create dynamic, highly responsive metrics. 

For instance, our 'Retention Rate' and 'Departmental Attrition' KPIs dynamically recalculate across any cross-filtered dimension. I also implemented dynamic measure switching, allowing executives to pivot the entire dashboard's context from 'Total Employees' to 'Average Income' without cluttering the UI."

### [2:15 - 3:00] 4. Dashboard Storytelling: Attrition Drivers
"Let's look at the interactive analytics. The dashboard is structured as a narrative. 

When we drill down into the **Attrition Drivers**, the data tells a stark story. The visuals clearly isolate the 'Overtime Crisis': employees working regular overtime are burning out and leaving at nearly triple the baseline rate. 

Furthermore, our Income vs. Attrition scatter analysis proves we are bleeding entry-level talent in the lowest income quartiles, resulting in a negative ROI on junior hiring."

### [3:00 - 3:45] 5. High-Risk Segments & Operational Insights
"But knowing *why* they leave isn't enough; we need to know *who*. 

Using the engineered Risk Score heuristic, the **High-Risk Segments** page isolates current, active employees classified as 'Flight Risks'. This interactive table allows HR Business Partners to immediately intervene with specific individuals.

Operationally, I also identified a 'Mid-Tenure Slump'. Our histogram visualizations show a massive spike in attrition at the 3-to-5-year mark—the exact moment employees reach peak productivity."

### [3:45 - 4:30] 6. Actionable Business Recommendations
"Finally, the dashboard translates these insights into actionable business recommendations:
1. **Mandate Overtime Monitoring:** Implement a 'Burnout Dashboard' and require VP approval for sustained team overtime.
2. **Restructure Junior Compensation:** Introduce staggered micro-promotions at the 12- and 24-month marks to bridge the low-income retention gap.
3. **Launch Career Pathing:** Attack the Mid-Tenure Slump by forcing career mobility check-ins at the 2.5-year mark.

By leveraging clean data models, sophisticated DAX, and professional storytelling, this solution gives HR the exact tools needed to reduce turnover and save the company millions. Thank you, I'd be happy to answer any technical questions."
