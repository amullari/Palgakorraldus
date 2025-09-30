# Salary Management Report - Solution Analysis
## Table of Contents
- [Purpose of the Data Analysis](#purpose-of-the-data-analysis)
- [Glossary of Terms](#glossary-of-terms)
- [Data Protection](#data-protection)
- [Data Model](#data-model)
  - [Contract Table](#contract-table)
  - [Salary Table](#salary-table)


## Purpose of the Data Analysis

The objective of this data analysis is to create a **user-friendly analysis tool for HR staff**. The work is aligned with the upcoming Pay Transparency Directive (Directive (EU) 2023/970), adopted in 2023 and entering into force in 2026. The directive strengthens the legal framework for fair and transparent pay.  
**Key elements of the directive:**  
- Objective and gender-neutral criteria for pay setting  
- Prohibition on asking about pay history in recruitment  
- Mandatory gender pay gap reporting (depending on company size)  
- Employee right to request pay data by categories  
- Monitoring, sanctions, and national support measures 

In this context, the analysis aims to make salary and benefits structures understandable to employees and managers, allowing comparisons across categories, levels, and gender. The ultimate goal is to support a fair and transparent compensation policy. Improving pay transparency helps build **trust**, supports **equitable pay practices**, and enables **informed decision-making** for both employees and management.  

## Data model
![andmemudel](images/andmemudel.png)
### Contract Table
Contains Contract data. Data about needed dimensions - position category, position level and contract period. Included detail data to enable data drill down.
Employee ID -FK to employee table, not represented in data model
Contract ID - Primary key
Full Name - Employee full name
Gender - Male/Female
start date - Contract start date
End date - Contract end date, may be empty
Position - Employee position
Category - Position Category
Level - Position level
Workload - percent of full position, between 0 and 1

| Field Name   | Data Type     | Key / Relation               | Description                                                                 |
|--------------|--------------|------------------------------|-----------------------------------------------------------------------------|
| EmployeeID   | Long Integer | FK → Employee.EmployeeID (*) | Link to Employee table (not represented in data model).                     |
| ContractID   | Long Integer | PK                           | Primary key of the contract.                                                |
| FullName     | Text (255)   |                              | Employee’s full name.                                                       |
| Gender       | Text (10)    |                              | Gender: "Male" or "Female".                                                 |
| StartDate    | Date/Time    |                              | Contract start date.                                                        |
| EndDate      | Date/Time    |                              | Contract end date (may be empty/null).                                      |
| Position     | Text (100)   |                              | Employee position.                                                          |
| Category     | Text (100)   |                              | Position category.                                                          |
| Level        | Text (50)    |                              | Position level.                                                             |
| Workload     | Number (Double) |                           | Workload as a fraction of full position (0.0–1.0).                          |


### Salary table 
Contains data of monthly payroll and working days

| Field Name         | Data Type        | Key / Relation                 | Description                                                                 |
|--------------------|-----------------|--------------------------------|-----------------------------------------------------------------------------|
| ContractID         | Long Integer    | FK → Contract.ContractID       | Foreign key to Contract table.                                              |
| PeriodStart        | Date/Time       |                                | First day of the month.                                                     |
| PeriodEnd          | Date/Time       |                                | Last day of the month.                                                      |
| ActualWorkingDays  | Integer         |                                | Number of days worked in the month.                                         |
| Salary             | Decimal         |                                | Base salary amount for the month.                                           |
| Benefit            | Decimal        |                                | Benefits/bonuses paid in the month.                                         |
| MissedDays         | Integer         |                                | Number of missed workdays (vacation, sick leave, etc.).                     |
| FullSalary         | Calculated      |                                | `[Salary] + [Benefit]`.                                                     |




- töötajate/töölepingute andmed
- ettevõtte struktuur
- ?tööturu andmed



### mõõdikud


## Glossary of terms

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

- läbipaistvus

## Data Protection
- The HR department decides on the sharing of outputs.  
- HR staff using the reports may access all detailed data.  
- Final outputs are not produced for groups with fewer than 3 individuals.  
- Data may be presented to an employee regarding their own group only.

### Detailandmed on
....

## Väljundi kirjeldus
- palgavahemikud
- palgalõhe analüüs
- ? võrdlus tööturuga

## LISA. Andmete genereerimise skript ja chatgpt esitatud tingimused
For demonstration we generated data with AI (ChatGPT) for 400 employees in an IT company.
- tables for contract data and salary data as described in data model
- data for year 2024
- workload mainly 1, sometimes 0.5, rarely 0.75.
- women and men salary should have small pay gap within the same job position category 
- the contract table have employees with changed contractual conditions (position, category, level of position) and some employees who have started to work in 2024 and some employees who have left the company in year 2024. End date should be mostly empty
- generate missed days realistically taking estonian seasionality into account and calculate smaller salaries proportionally
- create one row for each contract for each month taking into account contract start date and end date

