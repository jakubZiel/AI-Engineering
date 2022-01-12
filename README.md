## Problem biznesowy


“Wygląda na to, że nasze firmy kurierskie czasami nie radzą sobie z dostawami. Gdybyśmy
wiedzieli, ile taka dostawa dla danego zamówienia potrwa – moglibyśmy przekazywać tę
informację klientom."

## Obsługa aplikacji

Aplikację należy wystartować z katalogu przy pomocy skryptu run.sh

`cd microservice`

`bash run.sh`

Skrypt tworzy kalog database w katalogu mongodb, w którym  
przechowywane dane dla testów A / B.

## Obsługa API

Testowanie API jest możliwe przy pod URL przy pomocy Swagger UI:

`http://localhost:8000/docs`

## Endpointy

### POST /ab_test

Wykorzystywany do zbierania danych w ramach testu A/B

url : http://localhost:8000/ab_test?user_id=123

dane : 

{ <br>
  "city": 0, <br>
  "street": 0, <br>
  "purchase_week_day_plus_hour": 0<br>
}

odpowiedź : 

{
  "response": "OK",
  "group": "group_b",
  "prediction" : 2
}

### POST /predict/{model_id}

Wykorzystywany do serwowania predykcji

`url : http://localhost:8000/predict/0`

dane :

{ <br>
  "city": 0, <br>
  "street": 0, <br>
  "purchase_week_day_plus_hour": 0<br>
}

odpowiedź :

{<br>
  "prediction": 2<br>
}

###  GET /models

Sprawdzenie dostępnych modeli

`url :  http://localhost:8000/models`

odpowiedź :

{<br>
  "0": "svm",<br>
  "1": "ml-perceptron"<br>
}

### POST /ab_test_switch

Wyłączenie/Włączenie testu A/B

`url : http://localhost:8000/ab_test_switch?turned_on=true`

odpowiedź : 

{<br>
  "ab_test_state": true,<br>
  "switched?": false<br>
}

## Symulacja testu A/B

w pliku

`/microservice/test_simulation.ipynb`

znajduje się notatnik z krokami potrzebnymi do zasymulowania 
testu A/B. Symulacja kończy się analizą hipotez.