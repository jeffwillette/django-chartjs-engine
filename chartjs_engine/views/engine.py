"""
Charting engine which takes the input and routes it to the proper Chart sublcass.
"""
from .line import LineChart
from .bar import BarChart
from .pie_doughnut import PieDoughnutChart
from .base import Chart



class ChartEngine(object):
	"""An engine to make all of the charts necessary"""

	def __init__(self, **kwargs):
		"""take in chart options and decide what kind of chart to make"""
		charts = {
			'line': LineChart,
			'bar': BarChart,
			'pie': PieDoughnutChart,
			'doughnut': PieDoughnutChart,
		}

		self.chart = charts[kwargs['chart_type']](
			chart_name=kwargs['chart_name'],
			chart_type=kwargs['chart_type'],
			chart_labels=kwargs['chart_labels'],
			# Options is not used but left for possible future use
			options=kwargs['options'],
			datasets=kwargs['datasets'])


	def make_chart(self):
		"""Render the proper chart from the given"""
		return self.chart.to_string()
