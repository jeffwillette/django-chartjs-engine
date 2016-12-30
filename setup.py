from setuptools import setup

setup(name='django-chartjs-engine',
      version='0.0.3',
      description='Django app to build chartjs javascript charts',
      url='https://github.com/deltaskelta/django-chartjs_engine',
      author='Jeff Willette',
      author_email='jrwillette88@gmail.com',
      keywords = ['django', 'chartjs', 'javascript', 'charts'],
      packages = ['chartjs_engine'],
      include_package_data = True,
)

# The command to upload: python setup.py sdist upload -r pypi