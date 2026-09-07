# Baseline klasifikatoriaus rezultatai

## Bendras tikslumas

**Accuracy: 0.7656 (76.56%)**


## Painiavos matrica

Eilutės rodo tikrą klasę, o stulpeliai – klasifikatoriaus prognozę.

| Actual \ Predicted | breakout | spike | seasonal | stable |
| breakout           | 15       | 0     | 0        | 1      |
| spike              | 0        | 11    | 2        | 3      |
| seasonal           | 1        | 5     | 9        | 1      |
| stable             | 0        | 0     | 2        | 14     |

## Precision ir Recall pagal klasę

| Class    | Precision | Recall |
| breakout | 0.938     | 0.938  |
| spike    | 0.688     | 0.688  | 
| seasonal | 0.692     | 0.562  | 
| stable   | 0.737     | 0.875  |

## Klaidingai suklasifikuoti atvejai

Iš viso klaidingai suklasifikuota **15** atvejų.

| Tema              | klasė    | Algoritmo klasė | Kodėl taisyklė suklydo
| ChatGPT           | breakout | stable          | Tikras augimas prasidėjo nuo 2022 m., todėl pirmųjų 90 dienų baseline nėra tikras pradinis 2021 m. lygis. Kadangi serija prasideda vėliau, peak_ratio ir level_ratio taisyklės gali neteisingai parodyti stabilumą.
| Formula One       | seasonal | spike           | Tema turi metinį pasikartojantį sezoninį modelį, tačiau 365 dienų autokoreliacija nepasiekė pasirinktos 0.5 ribos. Todėl dideli sezoniniai pikai buvo interpretuoti kaip paprasti spike.
| Summer            | seasonal | stable          | Sezoninis pakilimas vyksta tik tam tikru metų laiku ir nėra pakankamai panašus visomis likusiomis dienomis. Dėl to 365 dienų autokoreliacija buvo per maža.
| Derivative        | stable   | seasonal        | Stabilioje serijoje gali būti natūralus metinis pasikartojimas, pavyzdžiui, susijęs su mokslo metais ar studijomis. Aukšta 365 dienų autokoreliacija savaime nereiškia, kad serija turi pakankamai stiprų sezoninį piką.
| Logarithm         | stable   | seasonal        | Panašiai kaip Derivative, nedideli pasikartojantys metiniai svyravimai padidino autokoreliaciją, nors pagal bendrą grafiką serija išliko stabili.
| Google            | spike    | stable          | Dideli pikai egzistuoja, tačiau 7 dienų medianos išlyginimas sumažino trumpalaikio piko aukštį. Po išlyginimo peak_ratio galėjo nukristi žemiau 3× ribos.
| Pizza             | spike    | stable          | Serijoje buvo keli dideli trumpalaikiai pikai, tačiau dėl 7 dienų išlyginimo jų aukštis sumažėjo. Todėl taisyklė galėjo nepasiekti 3× peak_ratio ribos.
| Vilnius           | spike    | stable          | Trumpi labai aukšti pikai po išlyginimo tapo mažesni, todėl klasifikatorius neaptiko pakankamai didelio piko ir priskyrė stable.
| Literature        | spike    | seasonal        | Keli dideli pikai ir panašūs svyravimai skirtingais metais sukūrė didesnę 365 dienų autokoreliaciją. Algoritmas supainiojo atsitiktinius ar su akademiniu kalendoriumi susijusius pikus su tikru sezoniniu modeliu.
| Easter            | seasonal | spike           | Velykų data kiekvienais metais keičiasi. Todėl pikai nėra tiksliai 365 dienų atstumu ir paprasta 365 dienų autokoreliacija blogai aptinka tokį sezoninį modelį.
| Raspberry Pi      | spike    | seasonal        | Serijoje gali būti metinių ar pasikartojančių svyravimų, kurie padidino autokoreliaciją, nors pagrindinis klasifikavimo požymis buvo konkretus trumpalaikis spike.
| League of Legends | seasonal | spike           | Metiniai pikai nėra pakankamai tiksliai išsidėstę kas 365 dienas, todėl autokoreliacija nepasiekė nustatytos ribos. Algoritmas matė didelius pikus, bet neatpažino jų pasikartojimo.
| Black Friday      | seasonal | breakout        | Sezoninis pikas yra labai didelis ir paskutinės 90 dienų patenka arti aktyvaus sezono. Dėl to final_level / baseline galėjo viršyti 1.5 ir algoritmas klaidingai interpretavo sezoninį pakilimą kaip naują ilgalaikį baseline.
| Easter Bunny      | seasonal | spike           | Kaip ir Easter, Velykų data keičiasi kiekvienais metais. Todėl 365 dienų autokoreliacija nėra patikimas būdas aptikti šį sezoninį modelį.
| Carnival          | seasonal | spike           | Kaip ir Easter, Velykų data keičiasi kiekvienais metais. Todėl 365 dienų autokoreliacija nėra patikimas būdas aptikti šį sezoninį modelį.


## Išvada

Šis klasifikatorius naudoja paprastas rankiniu būdu nustatytas taisykles. Jo paskirtis nėra pasiekti maksimalų tikslumą, bet sukurti bazinius rezultatus, su kuriais vėliau bus lyginami sudėtingesni modeliai.