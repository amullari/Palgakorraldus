genereeri andmed

- 400 töötajaga IT-ettevõtte jaoks

# Tabelid
## employee_table: väjad - Employee_id, full_name,gender
## contract_table: väljad - Employee_id, contract_id, start_date, end_date (mainly empty), position, position_category, Position_level,workload=percent from full position (mainly 1, sometimes 0.5, rarely 0.75 or other)
tingimused - lepingud peavad kehtima aastal 2024, üks lepingu rida kajastab komplekti nendest andmetest.
andmetes võiks esineda tööd alustanud töötajaid, tööd lõpetanud töötajaid ja muutunud lepingutingimustega (ametikohaga, kategooriaga, ametikoha tasemega) töötajaid 
salary_table: väljad - employee_id, contract_id, Period_end_Date(arvestuskuu viimane kuupäev),salary,benefits,illness_vacation_compensation,actual_working_days,missed_days
tingmused: töötaja saab palka igas kuus, välja arvatud puhkused ja puudumised.
Palk on ühe lepingu rea korral igas kuus ühesugune, kuid puudumiste korral proportsionaalne kuus töötatud päevade arvuga
lisatasu võib olla juhuslik. Tuleks genereerida andmed 2024 aasta kohta.
andmete loomise eesmärk on kasutada neid demonstratsiooniks töötajate keskmise kuupalga ja palgavahemike analüüsiks kuupalkade alusel. Andmetes võiks esineda väike erinevus naiste ja meeste palkades sama ametikategooria lõikes