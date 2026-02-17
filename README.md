# Salary Management Tool (_Palgakorraldus_)

The objective of this data analysis is to create a **user-friendly analysis tool for HR staff**. Artificial (dummy) data used for this tool was generated with the help of ChatGPT.

## 📘 Project Overview

This project demonstrates how data analysis can support **pay transparency** and **equitable compensation** in an organization.  
The Power BI report visualizes gender pay gaps, workforce composition, and structural factors influencing salary differences.  
It enables HR professionals to explore salaries by **category, level, and gender**, and to identify key drivers of pay disparities.

---

## 📸 Key Visualizations

Below are selected views from the Power BI report illustrating the main analytical perspectives:
### Salary Ranges

Visual overview of salary dispersion across job categories and levels. Wide ranges and outliers highlight potential inconsistencies in role grading and compensation practices. Used to quickly identify areas that require deeper investigation.
![Salary Ranges](/images/salary-ranges.png)

### Salary Range Cross Table

Compact tabular view of salary ranges by category and level. Provides precise numerical comparison where visual overview is not sufficient.
![Salary Range Cross Table](/images/cross-table.png)

### Gender Pay Gap by Category

Bar chart showing gender pay gap across job families and levels. Categories are sorted by decreasing pay gap to highlight the most critical areas. Pay gaps above 5% are flagged as potential risk indicators. Supporting lines show average male and female salaries for context.
![Gender Pay Gap By Category](/images/salary-gap.png)

### Male vs Female Salaries by Position

Scatter plot comparing average male and female salaries per job position. Point size reflects the number of employees. Positions above the diagonal indicate higher male salaries, positions below indicate higher female salaries. Used to detect structural imbalance at role level.

Scatter Plot is connected with interactive table showing employee-level salary details. Clicking any chart filters the table accordingly. Supports root-cause analysis behind observed pay gaps and anomalies.

   ![Male vs Female Salaries by Position](/images/scatter-plot.png)

## 📊 Power BI Files

- _Palgauuring.pbx_ – Complete Power BI report  
- _Palgauuringu Demo 3.pbx_ – Extract of created charts for presentation purposes  
- _Palgauuring Demo uute andmetega.pbix_ – Demo file created using improved salary data  

---

## 📁 Documentation

- _Andmelugu.md_ – Data story  
- _Demo kirjeldus.md_ – Description of the demonstration  

Data sources are located in the folder **_Andmemudel_**.  

The folder **_Ülesande analüüs_** contains documentation from the analysis stage, including the interview and analytical notes.  

The folder **_Abimaterjalid_** includes reference and supporting materials created or collected during the project.

---

## 🧩 Data Model Overview

The data model consists of two core tables — **Contract_table** and **Salary_table** — linked by _ContractID_.  
These tables contain information about:
- Employment contracts and job dimensions (category, level, workload, gender)  
- Monthly salary, benefits, working days  

The structure enables **drill-down analysis** across different organizational groups.  
Data definitions and calculated fields are described in detail in the files within [**_Andmemudel_**](#andmemudel)

---

## ⚙️ Usage Instructions

1. Open `.pbix` files with **Power BI Desktop (version 2024 or newer)**.  
2. The report uses synthetic data and can be explored safely without privacy concerns.  

---

## 🪪 License / Credits

_This project was created as part of a data analysis training exercise using synthetic data._  
_All data was generated for demonstration purposes only and does not represent any real organization or individuals._

---
