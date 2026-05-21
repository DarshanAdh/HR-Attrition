# Executive Dashboard Walkthrough Script
**Target Length:** 3–5 Minutes (~650 words)
**Focus:** Executive Storytelling, Interactive Analytics, Data Modeling, DAX, and KPIs.

*(Note: Read at a comfortable, professional pace. Click through the left sidebar navigation as you speak.)*

---

### [0:00] Intro & Tab 1: The Problem
*(Screen: Start on "1. The Problem")*

"Hello everyone, and thank you for your time. Today I'm walking you through an end-to-end Enterprise HR Analytics solution. 

The core business challenge we face is that employee turnover is reactive and incredibly expensive. We needed a way to transition from lagging indicators—like exit interviews—to proactive, data-driven retention strategies. 

To build this, I orchestrated a complete ETL pipeline using Python to extract our raw HR data, clean it, and perform extensive feature engineering. I then transformed that data into a professional **Star Schema**—centralizing metrics into a Fact table surrounded by optimized Dimension tables. This clean modeling is what powers the dashboard you see here.

Looking at our first tab, **The Problem**, we immediately see our executive KPIs: a Total Workforce of 1,470 and a baseline attrition rate of 16.1%. Using sophisticated DAX-style context transitions, these KPIs are dynamic—if we filter the dashboard, the metrics instantly recalculate."

---

### [1:00] Tab 2: Workforce Overview
*(Screen: Click to "2. Workforce Overview")*

"Moving to the **Workforce Overview**, we get a demographic snapshot of our current employee base. 

Because of the clean dimensional modeling I mentioned earlier, we can seamlessly slice our data by custom categories I engineered, such as 'Age Groups'. The visuals here show our workforce distribution and exactly where our attrition volume is coming from, split by gender and job role. Notice how the interactive Plotly visuals allow executives to hover and drill down into specific data points without writing any code."

---

### [1:45] Tab 3: Attrition Drivers
*(Screen: Click to "3. Attrition Drivers")*

"Knowing *that* people leave isn't enough; we need to know *why*. On the **Attrition Drivers** tab, the data tells a stark story. 

The first major driver is what I call the 'Overtime Crisis.' As you can see in the bar chart, employees working regular overtime are burning out and leaving at vastly higher rates. 

Below that, our Income vs. Attrition box plot proves we are bleeding entry-level talent in the lowest income quartiles. We are losing these junior employees before they even reach optimal productivity, resulting in a massively negative ROI on hiring."

---

### [2:30] Tab 4: High-Risk Segments
*(Screen: Click to "4. High-Risk Segments")*

"But we need to know exactly *who* is at risk right now. 

In my ETL pipeline, I engineered a custom 'Attrition Risk Score' heuristic based on a combination of overtime, low satisfaction, and income brackets. 

Here on the **High-Risk Segments** tab, we isolate our current, active employees. The table at the bottom highlights critical 'Flight Risk' employees using dynamic gradient styling. This isn't historical data—this is a targeted action list that HR Business Partners can use today to intervene with specific individuals before they hand in their notice."

---

### [3:15] Tab 5: Operational Insights
*(Screen: Click to "5. Operational Insights")*

"Operationally, we also have systemic issues to address. 

If we look at the **Operational Insights** tab, the histogram reveals a 'Mid-Tenure Slump.' There is a pronounced spike in attrition when employees hit the 3-to-5-year mark with the company. This means we are losing our talent exactly at the moment they acquire deep institutional knowledge and reach peak productivity."

---

### [4:00] Tab 6: Business Recommendations
*(Screen: Click to "6. Business Recommendations")*

"Finally, an analytics project is only as good as the actions it drives. On the final tab, I've translated these insights into four concrete **Business Recommendations**:

1. **Mandate Overtime Monitoring:** We need to implement strict thresholds for consecutive weeks of overtime to prevent burnout.
2. **Address the Junior Comp Gap:** We must review market rates for the bottom 33% of earners and introduce staggered micro-promotions.
3. **Combat the Mid-Tenure Slump:** We should force career-pathing check-ins at the 2.5-year mark to provide lateral mobility.
4. **Pulse Surveys:** We need to transition from annual reviews to quarterly pulse surveys to catch satisfaction drops early.

By leveraging a robust data pipeline, clean dimensional modeling, and interactive storytelling, this solution gives HR the exact tools needed to reduce turnover and save millions. Thank you, I'd be happy to answer any questions."
