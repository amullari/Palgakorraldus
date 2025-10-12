# Salary Management Tool (_Palgakorraldus_)

The objective of this data analysis is to create a **user-friendly analysis tool for HR staff**.  
Artificial (dummy) data used for this tool was generated with the help of ChatGPT.


## 📘 Project Overview

This project demonstrates how data analysis can support **pay transparency** and **equitable compensation** in an organization.  
The Power BI report visualizes gender pay gaps, workforce composition, and structural factors influencing salary differences.  
It enables HR professionals to explore salaries by **category, level, and gender**, and to identify key drivers of pay disparities.


## 📊 Power BI Files

- _Palgauuring.pbx_ – Complete Power BI report  
- _Palgauuringu Demo 3.pbx_ – Extract of created charts for presentation purposes  
- _Palgauuring Demo uute andmetega.pbix_ – Demo file created using improved salary data  


## 📁 Documentation

- _Andmelugu.md_ – Data story  
- _Demo kirjeldus.md_ – Description of the demonstration  

Data sources are located in the folder **_Andmemudel_**.  

The folder **_Ülesande analüüs_** contains documentation from the analysis stage, including the interview and analytical notes.  

The folder **_Abimaterjalid_** includes reference and supporting materials created or collected during the project.


## 🧩 Data Model Overview

The data model consists of two core tables — **Contract_table** and **Salary_table** — linked by _ContractID_.  
These tables contain information about:
- Employment contracts and job dimensions (category, level, workload, gender)  
- Monthly salary, benefits, working days  

The structure enables **drill-down analysis** across different organizational groups.  
Data definitions and calculated fields are described in detail in the files within https://github.com/amullari/Palgakorraldus/tree/main/Andmemudel

---

## ⚙️ Usage Instructions

1. Open `.pbix` files with **Power BI Desktop (version 2024 or newer)**.  
2. The report uses synthetic data and can be explored safely without privacy concerns.  


## 🪪 License / Credits

_This project was created as part of a data analysis training exercise using synthetic data._  
_All data was generated for demonstration purposes only and does not represent any real organization or individuals._

