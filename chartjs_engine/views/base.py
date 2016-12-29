"""
The base chart class that all the chart type cublcasses inherits from

TODO:

1. Construct the data in JSON and make it accpet all types of charts.
2. Move [chartjs] markup splitting to the model so chart engine can be agnostic,
   and just take chart settings as input
3. split each chart type class into smaller methods
"""
import random



class Chart(object):
	"""A base class for charts, init will store all the data needed for subclasses"""

	def __init__(self, chart_type=None, chart_name=None, options=None, \
		chart_labels=None, datasets=None):
		"""
		Setting all of the settings that will be needed in the charts subclasses
		"""
		self.chart_type = chart_type
		# datasets will be put into self.data in each charts get_data method
		self.datasets = datasets
		self.chart_name = chart_name
		self.options = options
		self.data = {'labels': chart_labels,}
		# Figure out how to access the kwargs as a list and make sure none of them
		# are None. Raise exception if they are and test.
		if not all([self.chart_type, self.chart_name, self.data['labels'], \
			self.datasets]):
			raise Exception(
				"Chart class needs to have all keyword arguments specified")


	def random_color(self):
		"""Generates a random javascript valid rgba color for each set in datasets
		return: tuple of javascript rgba color strings."""

		red, green, blue = random.randint(0, 255), \
			random.randint(0, 255), random.randint(0, 150)

		return ("rgba(%s, %s, %s, .4)" % (red, green, blue), \
			"rgba(%s, %s, %s, 1)" % (red, green, blue))


	def to_string(self):
		"""
		This method is meant to be overridden in the child chart type classes
		"""
		raise Exception("to_string method has not been overridden")


'''
class RadarChart(Chart):
	"""
	Making the JSON data necessary for a radar chart
	DOCS: http://www.chartjs.org/docs/#radar-chart-introduction
	"""
	pass


class PolarAreaChart(Chart):
	"""
	Making JSON data necessary for a polar area chart
	DOCS: http://www.chartjs.org/docs/#polar-area-chart-introduction"""
	pass


class BubbleChart(Chart):
	"""
	Making the JSON necessary for a bubble chart
	DOCS: http://www.chartjs.org/docs/#bubble-chart-introduction
	"""
	pass
'''