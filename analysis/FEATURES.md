# FEATURES.md

## Požymių analizė

Šiame etape buvo apskaičiuoti požymiai visoms `groundtruth/series/` serijoms ir rezultatai išsaugoti faile `analysis/features.csv`.

Kiekvienai serijai buvo apskaičiuota 10 požymių:

1. `baseline_90d` – pirmųjų 90 dienų medianinis peržiūrų lygis.
2. `final_level_90d` – paskutinių 90 dienų medianinis peržiūrų lygis.
3. `level_ratio` – galutinio ir bazinio lygio santykis.
4. `peak_ratio` – didžiausio piko ir bazinio lygio santykis.
5. `days_above_2x_baseline` – dienų skaičius, kai peržiūrų skaičius viršijo du kartus bazinį lygį.
6. `days_peak_to_1.5x` – dienų skaičius nuo didžiausio piko iki grįžimo į 1.5 karto bazinį lygį.
7. `autocorrelation_365d` – autokoreliacija su 365 dienų vėlavimu.
8. `coefficient_variation` – serijos variacijos koeficientas.
9. `log_slope` – logaritmuotos serijos tiesinės tendencijos nuolydis.
10. `peak_count` – aptiktų atskirų pikų skaičius.

---

## Triukšmo mažinimas

Wikipedia dienos peržiūrų duomenys gali būti triukšmingi ir turėti pavienių trumpalaikių šuolių. Todėl prieš skaičiuojant požymius buvo naudojamas 7 dienų slenkantis langas.

7 dienų langas pasirinktas todėl, kad jis atitinka vienos savaitės laikotarpį. Jis sumažina pavienių dienų triukšmo įtaką, tačiau išlaiko trumpesnius pokyčius ir sezoninius svyravimus. Slenkanti mediana yra mažiau jautri labai dideliems pavieniams pikams negu slenkantis vidurkis.

---

#### Medianų pagal klasę lentelė

| Požymis | Breakout | Spike | Seasonal | Stable |
|---|---:|---:|---:|---:|
| `baseline_90d` | 171.00 | 2965.25 | 1231.25 | 530.75 |
| `final_level_90d` | 2837.25 | 1696.25 | 1361.00 | 398.25 |
| `level_ratio` | **8.0789** | 0.7614 | 0.8930 | 0.6984 |
| `peak_ratio` | **52.9003** | 3.5513 | 32.4484 | 2.0346 |
| `days_above_2x_baseline` | **1131.5** | 77.5 | 415.0 | **1.5** |
| `days_peak_to_1.5x` | **0.0** | 21.5 | 52.0 | 13.0 |
| `autocorrelation_365d` | 0.0585 | 0.0750 | **0.6081** | 0.3050 |
| `coefficient_variation` | 0.7399 | 0.3916 | **1.5740** | **0.2263** |
| `log_slope` | **0.000781** | -0.0002 | -0.0000 | -0.0002 |
| `peak_count` | **72.5** | 18.0 | 45.5 | **6.0** |
---

# Požymių analizė

## `baseline_90d`

Bazinis lygis tarp klasių labai skiriasi, tačiau šis skirtumas greičiausiai priklauso nuo konkretaus Wikipedia straipsnio populiarumo, o ne nuo tendencijos tipo.

Pavyzdžiui, `spike` klasės mediana yra didžiausia – 2965.25, tačiau tai nereiškia, kad didelis pradinis peržiūrų skaičius lemia spike.

**Išvada:** šis požymis silpnai skiria tendencijų klases ir neturėtų būti pagrindinis klasifikavimo požymis.

---

## `final_level_90d`

Galutinis lygis taip pat stipriai priklauso nuo konkretaus straipsnio absoliutaus populiarumo.

`breakout` klasės galutinio lygio mediana yra didžiausia – 2837.25, tačiau kitos klasės taip pat gali turėti didelį galutinį peržiūrų skaičių.

**Išvada:** vienas pats šis požymis nėra pakankamai patikimas klasifikavimui.

---

## `level_ratio`

Šis požymis labai aiškiai išskiria `breakout` klasę.

`breakout` klasės mediana yra 8.079, o kitų trijų klasių reikšmės yra mažesnės už 1:

* `spike`: 0.761;
* `seasonal`: 0.893;
* `stable`: 0.698.

Tai rodo, kad breakout serijų galutinis lygis dažniausiai yra daug didesnis už pradinį lygį ir augimas išlieka iki laikotarpio pabaigos.

**Išvada:** vienas stipriausių požymių `breakout` klasei atskirti.

---

## `peak_ratio`

`breakout` klasės didžiausio piko ir bazinio lygio santykio mediana yra 52.900.

Tačiau `seasonal` klasės mediana taip pat yra gana didelė – 32.448. Todėl vien didelis pikas negali patikimai atskirti breakout nuo sezoninio reiškinio.

`spike` ir `stable` klasėse medianos yra daug mažesnės – atitinkamai 3.551 ir 2.034.

**Išvada:** gerai atskiria `stable` ir dalį `spike` serijų nuo didelių pokyčių, tačiau turi būti naudojamas kartu su `level_ratio` ir sezoniškumo požymiais.

---

## `days_above_2x_baseline`

Tai vienas aiškiausiai klases skiriančių požymių.

Medianų rezultatai:

* `breakout`: 1131.5 dienos;
* `seasonal`: 415 dienų;
* `spike`: 77.5 dienos;
* `stable`: 1.5 dienos.

Breakout serijos ilgą laiką išlieka virš dvigubo bazinio lygio. Stable serijos beveik niekada nepasiekia tokio lygio.

**Išvada:** labai stiprus požymis, ypač `breakout` ir `stable` klasėms atskirti.

---

## `days_peak_to_1.5x`

Šis požymis parodo, kaip greitai serija po didžiausio piko grįžta prie žemesnio lygio.

`breakout` klasės mediana yra 0 dienų. Tai reiškia, kad breakout serijose po didžiausio piko dažnai neįvyksta grįžimas iki 1.5 karto bazinio lygio.

Kitų klasių reikšmės yra:

* `spike`: 21.5;
* `seasonal`: 52;
* `stable`: 13.

**Išvada:** labai naudingas požymis `breakout` atskyrimui, tačiau vienas pats aiškiai neatskiria `spike`, `seasonal` ir `stable`.

---

## `autocorrelation_365d`

Šis požymis aiškiausiai išskiria `seasonal` klasę.

`seasonal` klasės mediana yra 0.608, kai:

* `breakout`: 0.059;
* `spike`: 0.075;
* `stable`: 0.305.

Didelė 365 dienų autokoreliacija rodo, kad serijos elgesys yra panašus tuo pačiu metu skirtingais metais.

**Išvada:** vienas svarbiausių požymių sezoninėms tendencijoms aptikti.

---

## `coefficient_variation`

Variacijos koeficientas rodo santykinį serijos kintamumą.

`stable` klasė turi mažiausią medianą – 0.226.

Didžiausią medianą turi `seasonal` klasė – 1.574, nes sezoninės serijos reguliariai turi didelius pakilimus ir kritimus.

`spike` ir `breakout` klasės yra tarp šių reikšmių.

**Išvada:** naudingas požymis, ypač `stable` klasės atskyrimui ir kartu su autokoreliacija sezoninėms serijoms aptikti.

---

## `log_slope`

Šis požymis labai aiškiai išskiria `breakout` klasę.

`breakout` klasės medianinis nuolydis yra teigiamas:

`0.000781`

Visų kitų klasių medianinis nuolydis yra neigiamas:

* `spike`: -0.000166;
* `seasonal`: -0.000039;
* `stable`: -0.000194.

Tai rodo, kad breakout serijos turi aiškią ilgalaikę augimo tendenciją.

**Išvada:** vienas stipriausių požymių breakout tendencijoms atpažinti.

---

## `peak_count`

Pikų skaičius tarp klasių taip pat skiriasi:

* `breakout`: 72.5;
* `seasonal`: 45.5;
* `spike`: 18;
* `stable`: 6.

Tačiau didesnis pikų skaičius nebūtinai reiškia konkretų tendencijos tipą. Breakout ir seasonal serijos gali turėti daug pikų dėl ilgalaikio aktyvumo arba pasikartojančių sezoninių pokyčių.

**Išvada:** naudingas papildomas požymis, tačiau vienas pats neturėtų būti naudojamas klasifikavimui.

---

# Kurie požymiai geriausiai skiria klases?

Pagal medianų skirtumus stipriausi požymiai yra:

### Breakout

* `level_ratio`;
* `days_above_2x_baseline`;
* `days_peak_to_1.5x`;
* `log_slope`;
* `peak_count`.

Breakout serijoms būdingas ilgalaikis padidėjimas, daug dienų virš bazinio lygio ir teigiama ilgalaikė tendencija.

### Spike

Spike klasei vienas atskiras požymis nėra toks aiškus kaip breakout ar seasonal atveju.

Spike geriausiai turėtų būti atpažįstamas pagal kelių požymių kombinaciją:

* santykinai trumpą laiką virš 2x bazinio lygio;
* grįžimą po piko;
* neigiamą arba mažą ilgalaikį `log_slope`;
* mažesnį `level_ratio` negu breakout.

### Seasonal

Svarbiausi požymiai:

* `autocorrelation_365d`;
* `coefficient_variation`;
* `peak_ratio`;
* `peak_count`.

Didelė 365 dienų autokoreliacija yra aiškiausias signalas, kad pokyčiai kartojasi kasmet.

### Stable

Svarbiausi požymiai:

* `days_above_2x_baseline`;
* `coefficient_variation`;
* `peak_ratio`;
* `peak_count`.

Stable serijos turi mažą santykinį kintamumą ir labai mažai dienų, kai peržiūrų skaičius gerokai viršija bazinį lygį.

---

# Galutinė požymių atranka

Pagal medianų skirtumus į tendencijų klasifikavimo variklį pirmiausia verta įtraukti:

1. `level_ratio`;
2. `days_above_2x_baseline`;
3. `days_peak_to_1.5x`;
4. `autocorrelation_365d`;
5. `coefficient_variation`;
6. `log_slope`;
7. `peak_ratio`;
8. `peak_count`.

`baseline_90d` ir `final_level_90d` yra naudingi kaip kontekstiniai požymiai, tačiau absoliutūs peržiūrų skaičiai patys savaime patikimai neskiria klasių.

---

# Išvada

Rezultatai rodo, kad skirtingos tendencijų klasės turi aiškius skirtingus požymių rinkinius.

`breakout` geriausiai atpažįstamas pagal ilgalaikį lygio augimą ir didelį `level_ratio`.

`spike` būdingas laikinas pakilimas be ilgalaikio lygio padidėjimo.

`seasonal` aiškiausiai atpažįstamas pagal didelę 365 dienų autokoreliaciją.

`stable` klasė turi mažiausią kintamumą ir beveik neturi dienų, kai reikšmė ilgą laiką būtų daugiau negu du kartus didesnė už bazinį lygį.

Todėl klasifikatorius turėtų naudoti kelių požymių kombinaciją, o ne remtis vien didžiausiu piku. Didelis pikas gali reikšti tiek breakout, tiek seasonal, tiek spike, todėl svarbu vertinti, ar pokytis išlieka, ar grįžta į ankstesnį lygį ir ar pasikartoja kasmet.
