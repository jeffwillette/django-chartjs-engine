from mock import patch
from django.test import TestCase, Client
from django.template.loader import render_to_string
from .views.engine import *

# Create your tests here.
class ChartTests(TestCase):
	"""Tests for the blog views"""

	def setUp(self):
		"""Making tests for the charting app. Uses another chartjs app installed to virtualenv"""
		self.chart = Chart(
			chart_type='line',
			chart_name='this',
			options={'options': 'options'},
			chart_labels=['the', 'labels'],
			datasets={'data': (1, 2), 'data2': (3, 4)})

	def test_chart_class(self):
		"""Testing that the chart class instantiates"""
		self.assertEqual(self.chart.chart_type, 'line')

	def test_random_color(self):
		"""Testing that the random color generator returns a tuple of length 2"""
		colors = self.chart.random_color()
		self.assertEqual(len(colors), 2)

	def test_make_js(self):
		"""
		Testing that the exception is raised when I call the Chart class make_js
		method
		"""
		with self.assertRaises(Exception):
			self.chart.render_template()

	def test_exception_when_kwargs_missing(self):
		"""Testing that there is an exception rasied when all kwargs not present"""
		with self.assertRaises(Exception):
			chart = Chart()



class LineChartTests(TestCase):
	"""Tests for the different chart class types"""

	def setUp(self):
		"""Setting up what needs to be done for the line charts"""
		self.chart = LineChart(
			chart_type='line',
			chart_name='the_chart',
			options={'options': 'options'},
			chart_labels=['the', 'labels'],
			datasets={'data': (1, 2), 'data2': (3, 4)})

	@patch('chartjs_engine.views.line.render_to_string')
	def test_render_template_method(self, mock_rts):
		"""Testing that everything has rendered correctly 'rts' is render_to_string"""
		chart = self.chart.render_template()
		mock_rts.assert_called()



class BarChartTests(TestCase):
	"""Testing the bar chart class"""

	def setUp(self):
		"""Setting up the options for a bar chart"""
		self.chart = BarChart(
			chart_type='bar',
			chart_name='the_chart',
			options={'options': 'options'},
			chart_labels=['the', 'labels'],
			datasets={'data': (1, 2), 'data2': (3, 4)})

		self.single_dataset_chart = BarChart(
			chart_type='bar',
			chart_name='the_chart',
			options={'options': 'options'},
			chart_labels=['the', 'labels'],
			datasets={'data': (1, 2)})

	@patch('chartjs_engine.views.bar.render_to_string')
	def test_render_template_method(self, mock_rts):
		"""Testing rendering the bar chart to a template"""
		chart = self.chart.render_template()
		mock_rts.assert_called()

	def test_one_color_if_multiple_datasets(self):
		"""
		Testing that there will be one color per dataset when multiple datasets
		are present
		"""
		chart = self.chart.render_template()
		for ds in self.chart.data['datasets']:
			self.assertEqual(ds['backgroundColor'][0], ds['backgroundColor'][1])
			self.assertEqual(ds['borderColor'][0], ds['borderColor'][1])

	def test_multiple_colors_if_one_dataset(self):
		"""Testing that there will be multiple colors if there is only one dataset"""
		chart = self.single_dataset_chart.render_template()
		for ds in self.single_dataset_chart.data['datasets']:
			self.assertNotEqual(ds['backgroundColor'][0], ds['backgroundColor'][1])
			self.assertNotEqual(ds['borderColor'][0], ds['borderColor'][1])



class PieDoughnutChartTests(TestCase):
	"""Testing that Pie and Doughnut Charts render correctly"""

	def setUp(self):
		"""Setting up multiple and single datasets"""
		self.chart = PieDoughnutChart(
			chart_type='pie',
			chart_name='the_chart',
			options={'options': 'options'},
			chart_labels=['the', 'labels'],
			datasets={'data': (1, 2), 'data2': (3, 4)})

		self.doughnut_chart = PieDoughnutChart(
			chart_type='doughnut',
			chart_name='the_chart',
			options={'options': 'options'},
			chart_labels=['the', 'labels'],
			datasets={'data': (1, 2)})

		self.single_dataset_chart = PieDoughnutChart(
			chart_type='pie',
			chart_name='the_chart',
			options={'options': 'options'},
			chart_labels=['the', 'labels'],
			datasets={'data': (1, 2)})

	@patch('chartjs_engine.views.pie_doughnut.render_to_string')
	def test_one_dataset_returns_chart(self, mock_rts):
		"""Testing that one dataset will return a chart"""
		chart = self.single_dataset_chart.render_template()
		mock_rts.assert_called()

	@patch('chartjs_engine.views.pie_doughnut.render_to_string')
	def test_doughnut_chart_returns_chart(self, mock_rts):
		"""Testing that passing in settings for doughnut chart returns a chart"""
		chart = self.doughnut_chart.render_template()
		mock_rts.assert_called()

	def test_two_dataset_returns_error_as_string(self):
		"""Testing that two datasets will return an error as a string."""
		chart = self.chart.render_template()
		self.assertEqual(chart, self.chart.error)



class ChartEngineTests(TestCase):
	"""Testing that the chart engine works with proper input"""

	def setUp(self):
		"""Setting up the data that will be plugged into the charts."""

		self.chart_setup = {
			'chart_name': 'testchart',
			'chart_type': 'line',
			'chart_labels': ['the', 'labels'],
			'options': 'options',
			'datasets': {
				'data1': [1, 2],
				'data2': [3, 4],
			}
		}

	def test_make_line_chart(self):
		"""Testing that the engine delivers the charts as expected"""
		self.engine = ChartEngine(**self.chart_setup)
		self.assertIn('line', self.engine.make_chart())

	def test_make_bar_chart(self):
		"""Testing that the engine delivers charts with "bar" as the title"""
		self.chart_setup['chart_type'] = 'bar'
		self.engine = ChartEngine(**self.chart_setup)
		self.assertIn('bar', self.engine.make_chart())

	def test_make_pie_chart(self):
		"""Testing that the engine delivers charts with pie as the type"""
		self.chart_setup['chart_type'] = 'pie'
		self.chart_setup['datasets'] = {'data1': [1, 2]}
		self.engine = ChartEngine(**self.chart_setup)
		self.assertIn('pie', self.engine.make_chart())

	def test_make_doughnut_chart(self):
		"""Testing that the engine delivers charts with dughnut as the type"""
		self.chart_setup['chart_type'] = 'doughnut'
		self.chart_setup['datasets'] = {'data1': [1, 2]}
		self.engine = ChartEngine(**self.chart_setup)
		self.assertIn('doughnut', self.engine.make_chart())
