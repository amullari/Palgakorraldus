### Kokkuvõte: Normaliseeritud palga arvutamine analüüsiks

**Miks on normaliseerimist vaja?**  
Töötajate palkade võrdlemisel (nt palgalõhe, osalise ja täistööajaga töötajad, haiguspäevade mõju) ei ole mõistlik kasutada ainult tegelikke kuupalku. Osalise tööajaga või puudumistega töötajate palk näib alati väiksem, mis moonutab võrdlust. Seetõttu kasutatakse **normaliseeritud kuupalka või tunnipalka**, mis näitab, kui suur oleks töötaja palk, kui ta oleks töötanud kõik kuu tööpäevad/tunnid.

**Arvutusloogika:**
- Normaliseeritud kuupalk = \((Palk + Hüved) / Tegelikud tööpäevad) × Kuu tööpäevad\)  
- Normaliseeritud tunnipalk = \((Palk + Hüved) / Tegelikud töötunnid) × Kuu töötunnid\)

**Kasutuskoht:**
- Statistikaamet ja Eurostat kasutavad brutotunnipalga põhist normaliseerimist ametlikus palgalõhe statistikas.
- Ettevõttesisestes analüüsides on normaliseeritud kuupalk või tunnipalk oluline, et eemaldada töökoormuse või puudumiste mõju.

**DAX mõõdik Power BI-s (Normaliseeritud kuupalk):**
```DAX
Normalized Monthly Salary :=
AVERAGEX (
    Salary_Table,
    DIVIDE (
        (Salary_Table[Salary] + Salary_Table[Benefits])
            * RELATED ( Monthly_Workdays[Working Days] ),
        Salary_Table[Actual_Working_Days]
    )
)
```

**Selgitus:**
1. Võetakse iga töötaja palk ja hüved.
2. Jagatakse need tegelike tööpäevadega → saadakse päevapalk.
3. Korrutatakse kuu ettenähtud tööpäevade arvuga → saadakse normaliseeritud kuupalk.
4. Arvutatakse keskmine kõigi töötajate kohta, arvestades valitud filtreid (osakond, sugu, aasta jne).

**Tulemus:**
- Osalise tööajaga või puudunud töötajad saavad palga, mis on skaleeritud täiskuuks.
- Täistööajaga töötajatel jääb normaliseeritud palk samaks kui tegelik palk.
- Võimaldab õiglaselt võrrelda erinevaid töötajagruppe ja arvutada palgalõhet ilma töökoormuse mõjust tingitud moonutusteta.