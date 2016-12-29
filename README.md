## Chartjs_engine

`chartjs_engine` aims to provide a django app that will produce [chartjs](http://www.chartjs.org/)
charts by instantiating a chart engine.

## Install

```
pip install django-chartjs-engine
```

## Add to installed apps

settings.py

```
INSTALLED_APPS = [
    ...
    'chartjs_engine',
]
```

## Pass data to the Engine

## TODO:

1. make the chart render both responses and to string based on function call (how is this going to work?)
2. make sure everything works on local jrwillete before pushing
3. split up functions of the chart classes (make other files like bar.py)
