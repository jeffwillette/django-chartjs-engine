"""
The pie/doughnut chart class
"""
from .base import Chart
from django.template.loader import render_to_string
import json



class PieDoughnutChart(Chart):
	"""
	Making the JSON necessary for a pie or doughnut chart
	DOCS: http://www.chartjs.org/docs/#doughnut-pie-chart-introduction
	"""

	def render_template(self):
		"""Rendering pie or doughnut chart data to a template"""

		self.data = {
			'labels': self.chart_labels,
			'datasets': []
		}

		for i, name in enumerate(self.datasets):

			if len(self.datasets) == 1:
				self.colors = [self.random_color() for d in self.datasets[name]]
			else:
				self.error = "Pie/Doughnut charts support one dataset at this time"
				return self.error

			self.data['datasets'].append({
				# Labels in a pie chart have no function as of now
				'label': name,
				'backgroundColor': [color[0] for color in self.colors],
				'hoverBackGroundColor': [color[1] for color in self.colors],
				'borderWidth': 3,
				# For future support of multiple datasets
				'data': self.datasets[name],
			})

		self.context = {
			'chart_type': self.chart_type,
			'chart_name': self.chart_name,
			'data': json.dumps(self.data),
			'options': json.dumps(self.options)
		}

		return render_to_string('chartjs_engine/chart.html', self.context)