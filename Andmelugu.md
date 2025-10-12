# Salary Management Report - Data Story

## Table of Contents
- [Purpose of the Data Analysis](#purpose-of-the-data-analysis)
- [Glossary of Terms](#glossary-of-terms)
- [Data Protection](#data-protection)
- [Data Model](#data-model)
  - [Contract Table](#contract-table)
  - [Salary Table](#salary-table)
  - [Monthly Workdays Table](#monthly-workdays-table)
- [Measures](#measures)
- [Generation of Dummy data](#generation-of-dummy-data)
- [Description of output](#description-of-output)

## Purpose of the Data Analysis

The objective of this data analysis is to create a **user-friendly analysis tool for HR staff**. This involves making salary and benefits structures understandable to employees and managers, allowing comparisons across categories, levels, and gender. The aim is to support a fair and transparent salary policy.

Improving pay transparency helps build **trust**, supports **equitable pay practices**, and enables informed decision-making for both employees and management.

## Glossary of Terms

**Base Salary** – the employee’s monthly base salary (excluding allowances or bonuses).  

**Benefit** or **Variable pay** – the variable salary paid to an employee (e.g. bonus, overtime allowance).  

**Monthly Salary** – the employee’s total monthly pay, including base salary and allowances.  

**Full-Time Monthly Salary** or **Monthly salary**  – the monthly salary of a full-time employee.  

**Average Salary** – the average monthly salary of a full-time employee over the selected period.  

**Group Average Salary** – the average salary of employees within a group (e.g. department, job category).  

**Group Median** – the median of employees’ monthly salaries within a group, representing the typical pay level (not affected by exceptionally high or low salaries).  

**Salary Range** – the minimum and maximum values of average monthly salaries within a group.  

**Gender Pay Gap** – the difference between men’s and women’s average salaries, expressed as a percentage of men’s average salary. 

**Category** – a group of job positions that share similar functions or job family within the organization.Each category may include multiple job titles at different levels of seniority.

**Level** – indicates the seniority or experience of a position within a category.

## Data Protection
- The HR department decides on the sharing of outputs.  
- HR staff using the reports may access all detailed data.  
- Final outputs are not produced for groups with fewer than 3 individuals.  
- Data may be presented to an employee regarding their own group only.

## Data Model
![Data Model](Ülesande%20Analüüs/images/andmemudel.png)
### Contract Table

Contains detailed employment contract data, including key dimensions such as gender, position category, and position level. The table also includes workload information, contract dates, and employee identifiers to enable filtering and drill-down analysis across different organizational groups. Workload values are used in salary normalization and comparison calculations to ensure fair analysis across full- and part-time positions.

#### Fields

| Field Name | Data Type | Key / Relation | Description |
|-------------|------------|----------------|--------------|
| **ContractID** | Long Integer | **PK** | Primary key of the contract record. Unique contract number. |
| **EmployeeID** | Long Integer | **FK → Employee.EmployeeID** | Unique identifier of the employee. Links to the Employee table. |
| **FullName** | Text |  | Employee’s full name (first name and surname). |
| **Gender** | Text |  | Gender of the employee: “Male” or “Female”. |
| **StartDate** | Date |  | Contract start date. |
| **EndDate** | Date |  | Contract end date (can be empty/null if the contract is active). |
| **Position** | Text |  | Specific job role or title in the organization. |
| **Category** | Text |  | Group of job positions sharing similar functions or belonging to the same job family. Each category may include multiple job titles at different seniority levels. |
| **CategoryCode** | Text |  | ISCO-08 four-digit job classification code for the position category. |
| **Level** | Text |  | Indicates the seniority or experience level of the position within a category. |
| **Workload** | Number (Real) |  | Workload as a fraction of a full-time position (0.0–1.0). |

---

#### Calculated Columns

| Field Name | Calculation Type | Description |
|-------------|------------------|--------------|
| **No of Levels by Category** | Derived | Calculates how many distinct levels exist within each category. |
| **Category and Level** | Derived | Combines category and level into one value, used when a category has more than one level. |
| **LevelText** | Derived | Displays the level as a text value without the numeric prefix (e.g., “Senior” instead of “03-Senior”). |

---

### Salary Table

Contains detailed monthly payroll and working time data for each employee.  
The table provides information about base salary, benefits, working days, and missed days.  
It serves as the basis for salary analysis, and comparison of salary levels across employee groups.

#### Fields

| Field Name         | Data Type      | Key / Relation                  | Description                                                                 |
|--------------------|---------------|---------------------------------|-----------------------------------------------------------------------------|
| ContractID         | Long Integer  | FK → Contract.ContractID        | Foreign key to Contract table.                                              |
| PeriodStart        | Date          |                                 | First day of the month.                                                     |
| PeriodEnd          | Date          | FK → Monthly Workdays.Month     | Last day of the month.                                                      |
| ActualWorkingDays  | Integer       |                                 | Number of days worked in the month.                                         |
| Salary             | Decimal       |                                 | Base salary amount for the month.                                           |
| Benefit            | Decimal       |                                 | Benefits/bonuses paid in the month.                                         |
| MissedDays         | Integer       |                                 | Number of missed workdays (vacation, sick leave, etc.).                     |
---
#### Calculated Columns

| Field Name   | Description                            |
|--------------|----------------------------------------|
| FullSalary   | Calculated as `[Salary] + [Benefit]`.  |
| Hourly Salary | Average hourly salary for a full-time employee over the selected period.       |
---

### Monthly Workdays Table 
Contains number of working days and working hours for each month

#### Fields

| Field Name         | Data Type        | Key / Relation                 | Description                                                                 |
|--------------------|-----------------|--------------------------------|-----------------------------------------------------------------------------|
| Month              | Date    | PK       | Last day of the month                                              |
| Working days        | integer       |                      | Number of working days per month for a full time employee                |
| Hours          | integer       |                           | Number of working hours per month for a full time employee                                                      |
---
### Measures

The measures are divided into two main categories:

- **General Measures** – count-based or status measures used for monitoring workforce structure and contract activity.  
- **Analytical Measures** – salary-based or calculated measures used for analyzing pay levels, pay gaps, and distribution patterns.

The separation into *General* and *Analytical* measures helps maintain clarity between **structural metrics** (headcounts, contract activity) and **quantitative pay analysis metrics** (salary levels, distribution, and equity).

#### General Measures

| Measure Name        | Description                                                                                                   |
|----------------------|---------------------------------------------------------------------------------------------------------------|
| **ActiveEmployees**      | Employees with active contracts. Evaluates whether the current date is between contract start and end dates. |
| **No of Employees**      | Total number of employees in the company (based on unique Employee IDs).                                   |
| **Ended Contracts**      | Contracts that have an end date within the selected month and year.                                       |
| **StartedContracts**     | Contracts that have a start date within the selected month and year.                                      |
| **No of Males**          | Number of male employees based on Employee ID.                                                            |
| **No of Females**        | Number of female employees based on Employee ID.                                                          |
| **No of Contracts**      | Number of contracts based on Contract ID.                                                                 |
| **VisibilityDeterminer** | Calculates the smaller of the counts of males and females; if the smaller count is less than 3, the measure returns blank to protect confidentiality. |

---

#### Analytical Measures

| Measure Name           | Description                                                                                                   |
|-------------------------|---------------------------------------------------------------------------------------------------------------|
| **AVG BaseSalary**          | Average monthly base salary of full-time employees over the selected period.                               |
| **AVG Benefits**            | Average monthly variable salary elements such as bonuses or allowances.                                    |
| **AVG Salary**              | Average total monthly salary (base salary + benefits) of full-time employees.                              |
| **AVG Salary Female**       | Average total monthly salary for female employees.                                                        |
| **AVG Salary Male**         | Average total monthly salary for male employees.                                                          |
| **AVG HourlySalary**        | Average hourly salary of a full-time employee based on monthly working days.                              |
| **AVG CalculatedSalary**    | Average salary adjusted for actual working and missed days (includes workload correction).                 |
| **MAX Salary**              | Maximum value of average full-time monthly salaries within the selected period.                            |
| **MedianSalary**            | Median monthly salary value of full-time employees over the selected period.                              |
| **MIN Salary**              | Minimum value of average full-time monthly salaries within the selected period.                            |
| **SalaryGap**               | Difference between men’s and women’s average salaries, expressed as a percentage of men’s average salary. |
| **Salary Range**            | The minimum and maximum values of average monthly salaries within a group.                                |
| **SalaryDifference**        | Salary range calculated as (MAX Salary – MIN Salary).                                                     |

---

##### Calculation Notes

- All average and median salary measures are based on **full-time equivalent (FTE)** values and take **workload** into account.  
- The time filters (month, year, or period) are applied consistently across all measures to ensure comparability.  
- **SalaryGap** is calculated dynamically per filter context, allowing analysis by category, level, or other dimensions.  
- **VisibilityDeterminer** supports privacy compliance by suppressing values in groups with fewer than 3 employees of either gender.  

## Description of Output
- Salary range table by category and Level
- Salary gap analysis graphs and/or tables
- Drill down to source data

## Generation of Dummy Data
For demonstration we generated data with AI (ChatGPT) for 400 employees in an IT company.
- tables for contract data and salary data as described in data model
- data for year 2024
- workload mainly 1, sometimes 0.5, rarely 0.75.
- women and men salary should have small pay gap within the same job position category 
- the contract table have employees with changed contractual conditions (position, category, level of position) and some employees who have started to work in 2024 and some employees who have left the company in year 2024. End date should be mostly empty
- generate missed days realistically taking estonian seasionality into account and calculate smaller salaries proportionally
- create one row for each contract for each month taking into account contract start date and end date, actual working days

![Employee statistics](/images/Employee_statistics.png)

## Results
The description of the result is in progress...