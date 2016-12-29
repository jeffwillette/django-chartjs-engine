## Chartjs_engine

`chartjs_engine` aims to provide a django app that will produce [chartjs](http://www.chartjs.org/)
charts by instantiating a chart engine.

## Install

```
pip install django-chartjs-engine
```

## Add to installed apps

settings.py

```python
INSTALLED_APPS = [
    ...
    'chartjs_engine',
]
```

## Pass data to the Engine