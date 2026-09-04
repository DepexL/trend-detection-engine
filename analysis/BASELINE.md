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

| Tema              | klasė    | Algoritmo klasė | Kodėl taisyklė suklydo |
| ChatGPT           | breakout | stable          |  |
| Formula One       | seasonal | spike           |  |
| Summer            | seasonal | stable          |  |
| Derivative        | stable   | seasonal        | |
| Logarithm         | stable   | seasonal        | |
| Google            | spike    | stable          ||
| Pizza             | spike    | stable          |  |
| Vilnius           | spike    | stable          |  |
| Literature        | spike    | seasonal        |  |
| Easter            | seasonal | spike           |  |
| Raspberry Pi      | spike    | seasonal        |  |
| League of Legends | seasonal | spike           |  |
| Black Friday      | seasonal | breakout        |  |
| Easter Bunny      | seasonal | spike           |  |
| Carnival          | seasonal | spike           |  |


## Išvada

Šis klasifikatorius naudoja paprastas rankiniu būdu nustatytas taisykles. Jo paskirtis nėra pasiekti maksimalų tikslumą, bet sukurti bazinius rezultatus, su kuriais vėliau bus lyginami sudėtingesni modeliai.