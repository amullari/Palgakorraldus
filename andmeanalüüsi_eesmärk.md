# 1. Andmeanalüüsi eesmärk

Käesoleva andmeanalüüsi eesmärk on luua **personalitöötajatele kasutajasõbralik analüüsivahend**. Töö on seotud uue palgaläbipaistvuse direktiiviga (Direktiiv (EL) 2023/970), mis võeti vastu 2023. aastal ning jõustub 2026. aastal. Direktiiv tugevdab õiguslikku raamistikku õiglasema ja läbipaistvama tasustamise tagamiseks.

**Direktiivi peamised elemendid:**  
- Objektiivsed ja sooneutraalsed kriteeriumid palga määramiseks  
- Palgaajaloo küsimise keeld värbamisel  
- Kohustuslik soolise palgalõhe aruandlus (sõltuvalt ettevõtte suurusest)  
- Töötajate õigus küsida palgaandmeid kategooriate kaupa  
- Järelevalve, sanktsioonid ja riiklikud tugimeetmed  

Selles kontekstis on analüüsi eesmärk muuta töötasude ja hüvede struktuur personalitöötajatele ja juhtidele arusaadavaks, võimaldades võrdlusi kategooriate, tasemete ja soo lõikes. Lõppeesmärk on toetada õiglast ja läbipaistvat palgapoliitikat. Palgaläbipaistvuse suurendamine aitab kasvatada **usalduse**, toetab **õiglaseid tasustamistavasid** ning võimaldab teha **teadlikumaid otsuseid** nii töötajatel kui ka juhtidel.  

# 2. Andmestik
Analüüsi väljatöötamiseks genereerisime tehisandmed 400 töötaja kohta IT-ettevõttes AI abil (ChatGPT). Andmed on aasta 2024 kohta.

Andmed põhinevad lepingute ja palkade tabelitel, nagu kirjeldatud andmemudelis.
Lepingute tabelis on:
- enamus töötajaid on töötanud terve aasta
- on uusi töötajaid, kes alustasid 2024. aastal,
- töötajad, kes lahkusid ettevõttest 2024. aastal.
- töötajad, kelle töötingimused muutusid (amet, kategooria, tasemel muutus)
palkade tabelis
- Töötasu arvutatakse peamiselt täistööajaga, aga ka osalise tööajaga.
- Iga lepingu kohta on üks rida kuus, arvestades lepingu algus- ja lõppkuupäeva.
- Esineb puudumisi, puudumise põhjusi näidisandmestikus välja pole toodud, on ainult puudutud tööpäevade arv. Puudumised on genereeritud realistlikult, arvestades Eesti hooajalisust. 
- palk näidisandmestikus on esitatud 2 osas: põhipalk ja lisatasu
- Palgad on proportsionaalselt arvestatud vastavalt puudmistele ja koormustele.
--> töötajate statistika graafik
# 3. Palgavahemikud
## Mõõdikud Miinimum ja maksimumpalk (*MIN Salary* ja *MAX Salary*)
Lahenduses kasutasime täispalgale ümberarvutatud palgamõõdikuid.
```
MIN Salary = 
MINX (
    Salary_Table,
    DIVIDE (
        (Salary_Table[Base Salary] + Salary_Table[Benefits])
            * RELATED ( Monthly_Workdays[Working Days] ),
        Salary_Table[Actual Working Days]
    )
)
```
## Mõõdik liiga väikeste gruppide määramiseks (*Visibility Determiner*)
Avaldamiseks sobival graafikul, tabelis ei tohi olla gruppe, milles liikmete arv on väiksem kui 3.
```
No of Male = 
COUNTAX(
    filter(Contract_Table,Contract_Table[Gender]="Male"),
    Contract_Table[Employee ID]
    )
```
```
Visibility Determiner = 
VAR Male = CALCULATE(Contract_Table[No of Male], REMOVEFILTERS('Contract_Table'[Gender])) 
VAR Female = CALCULATE(Contract_Table[No of Female], REMOVEFILTERS('Contract_Table'[Gender]))
RETURN
IF(MIN(Male, Female) >= 3, MIN(Male, Female))
```
