"""
The bar chart class
"""
from .base import Chart
from django.template.loader import render_to_string
import json


class BarChart(Chart):
	"""
	Making the JSON data necessary for a bar chart
	DOCS: http://www.chartjs.org/docs/#bar-chart-introduction
	"""

	def render_template(self):
		"""Rendering bar chart data to a template"""

		self.options = {
			'scales': {
				'yAxes': [{
					'ticks': {
						'beginAtZero': True
					}
				}]
			}
		}

		self.data = {
			'labels': self.chart_labels,
			'datasets': []
		}

		for i, name in enumerate(self.datasets):

			if len(self.datasets) == 1:
				# If there is one dataset, each label will have a different color
				self.colors = [self.random_color() for d in self.datasets[name]]
			else:
				# If there is more than one dataset, each dataset will have its own
				# color which stays the same throughout the chart.
				self.rand_color = self.random_color()
				self.colors = [self.rand_color for d in self.datasets[name]]

			self.data['datasets'].append({
				'label': name,
				'backgroundColor': [color[0] for color in self.colors],
				'borderColor': [color[1] for color in self.colors],
				'borderWidth': 3,
				'data': self.datasets[name],
			})

		self.context = {
			'chart_type': self.chart_type,
			'chart_name': self.chart_name,
			'data': json.dumps(self.data),
			'options': json.dumps(self.options)
		}

		return render_to_string('chartjs_engine/chart.html', self.context)