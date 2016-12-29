"""
The line chart class
"""
from .base import Chart
from django.template.loader import render_to_string
import json


class LineChart(Chart):
	"""
	Making the JSON data necessary for line charts.
	DOCS: http://www.chartjs.org/docs/#line-chart-introduction
	"""

	def get_options(self):
		"""Gets the options for the chart"""
		self.options = {
			'scales': {
				'yAxes': [{
					'ticks': {
						'beginAtZero': True
					}
				}]
			}
		}
		return self.options

	def get_data(self):
		"""Populating self.data with self.datasets"""

		# self.data['labels'] already set in the Chart base class
		self.data['datasets'] = []
		self.colors = [self.random_color() for sets in self.datasets]

		for i, name in enumerate(self.datasets):
			self.data['datasets'].append({
				'label': name,
				'fill': False,
				'lineTension': 0.1,
				'borderCapStyle': 'butt',
				'borderDash': [],
				'borderDashOffset': 0.0,
				'borderJoinStyle': 'miter',
				'pointBorderColor': "rgba(75,192,192,1)",
				'pointBackgroundColor': "#fff",
				'pointBorderWidth': 1,
				'pointHoverRadius': 5,
				'pointHoverBackgroundColor': "rgba(75,192,192,1)",
				'pointHoverBorderColor': "rgba(220,220,220,1)",
				'pointHoverBorderWidth': 2,
				'pointRadius': 1,
				'pointHitRadius': 10,
				'spanGaps': False,
				'backgroundColor': self.colors[i][0],
				'borderColor': self.colors[i][1],
				'data': self.datasets[name],
			})
		return self.data

	def make_context(self):
		"""Making the context to be returned to the render functions"""
		self.context = {
			'chart_type': self.chart_type,
			'chart_name': self.chart_name,
			'data': json.dumps(self.data),
			'options': json.dumps(self.options)
		}
		return self.context


	def to_string(self):
		"""Generating the javascript needed for a line chart."""

		self.get_options()
		self.get_data()
		self.make_context()
		return render_to_string('chartjs_engine/chart.html', self.context)
