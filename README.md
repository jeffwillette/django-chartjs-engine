[![Build Status](https://travis-ci.org/deltaskelta/django-chartjs-engine.svg?branch=master)](https://travis-ci.org/deltaskelta/django-chartjs-engine)

[![Coverage Status](https://coveralls.io/repos/github/deltaskelta/django-chartjs-engine/badge.svg?branch=master)](https://coveralls.io/github/deltaskelta/django-chartjs-engine?branch=master)

## Chartjs_engine

`chartjs_engine` aims to provide a django app that will produce [chartjs](http://www.chartjs.org/)
charts by instantiating a chart engine which renders the chart to a string of html and `<script>`
tags. This can be useful for making charts in whatever kind of pre-existing views you already
have.

If you have a blog app, you could write a model method that scans for custom chart markup and
then inserts the html.

If you wish to create a chart based on django querysets, outside API calls, or anything else, just gather your data in a django view and pass it to the chart engine which can then be returned like
a regular view.

## Install

```python
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

## Method 1: Pass data to the Engine And Return Chart as Response

```python
from django.http import HttpResponse
from chartjs_engine.views.engine import Engine


def chart_view(request):
    """construct data form a source and send it to the chart engine"""

    chart_setup = {
		'chart_name': 'testchart',
		'chart_type': 'line',
		'chart_labels': ['the', 'labels'],
		'options': 'options',
		'datasets': {
			'data1': [1, 2],
			'data2': [3, 4],
		}
    }

    engine = ChartEngine(**chart_setup)
    chart = engine.make_chart()
    return HttpResponse(chart)
```

## Method 2: Creating Custom Markup on a Database Object

If you have a database object which is returned in a response (like a blog post) you can make some
custom markup which can be substituted for chart html when the view is loaded.

#### Example:

##### settings.py
```python
CHARTJS_REGEX = re.compile(r'(\[chartjs\].*?\[/chartjs\])', re.DOTALL)
```

The above regular expression will capture everything in between and including `[chartjs]` and `[/chartjs]` tags in the database.

##### models.py
```python
class BlogPost(models.Model):
	"""A model that has everything needed for a blogpost"""

	# All of the model fields would be here
	...

	def insert_chart(self):
		"""
		Finds the chartjs data by regex in a post and calls the function to
		replace markup with chart javascript in the post.
		"""
		chart_data = {}
		# re.DOTALL makes "." accept all characters. chart_data var is list of matches.
		pattern = settings.CHARTJS_REGEX
		#Finding all the chartjs markup and iterating to parse each one
		markup_data = re.findall(pattern, self.post)
		for data in markup_data:
			# Regex captures the "[chartsjs]" tags, omitting them...
			data = data.split('\r\n')[1:-1]
			# name and type are in list as "name: the-name" so split/strip whitespace
			chart_data['chart_name'] = data[0].split(':')[1].strip()
			chart_data['chart_type'] = data[1].split(':')[1].strip()

			# Split label by item delimited by "," stripped of whitespace.
			chart_data['chart_labels'] = [item.strip() for item in \
				data[2].split(':')[1].split(',')]

			chart_data['datasets'] = {}
			# data[3:] is going to be chart data so split/strip and convert to json.
			for data_set in data[3:]:
				# split by ':', then [0] index will be the dataset title
				d = data_set.split(':')
				chart_data['datasets'][d[0]] = [item.strip() for item in \
					d[1].split(',')]

			# Left for future use, this may cause errors with chart specific
			# options in views if changed
			chart_data['options'] = 'options'

			# Instantiate the ChartEngine and make the chart
			engine = ChartEngine(**chart_data)
			# replace 1 match in the post with the chart javascript
			self.post = re.sub(pattern, engine.make_chart(), self.post, count=1)
```
