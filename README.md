# API example

## Installation

1. `git clone` this repo and `cd` into the project's top level folder
2. create a Python3 virtual environment and activate it

`virtualenv -p python3.7 venv`

`source venv/bin/activate`

(This was developed and tested with Python 3.7 on a MacBook Air running OS 10.15 Catalina.)

3. install dependencies

`pip install -r requirements.txt`

## Running locally

In the top level directory and with the virtualenv active:

`python api.py`

Sample usage:
```
$ curl -L localhost:5000/students
{
  "studentIds": [
    "Mohamed2",
    "Izaiah_Schroeder",
    "Morris5",
    "Julia.Effertz",
    "Thalia.Gleichner9",
    "Misael65",
    "Marion.Zieme51",
    "Gregg_Grimes64",
    "Camden_Lynch35",
    "Gilda.Stokes52",
    "Elton.Boyer94",
    "Karolann_Sanford",
    "Ernie_Macejkovic74",
    "Zane_Grady77",
    "Colin_Volkman",
    "Verlie.Stamm57",
    "Lawson_Denesik",
    "Bettie_Herman7",
    "Erick11",
    "Ramon.Beier"
  ]
}
```

## Running the tests

In the top level directory and with the virtualenv active:

`python -m pytest`

Test coverage data:

`coverage run -m pytest && coverage report`

output:

```
Name              Stmts   Miss  Cover
-------------------------------------
src/services.py      41      0   100%
src/views.py         25      0   100%
-------------------------------------
TOTAL                66      0   100%
```