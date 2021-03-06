from setuptools import find_packages, setup

setup(
  name='daily_checklist',
  version='1.0.0',
  packages=find_packages(),
  include_package_data=True,
  zip_safe=False,
  install_requires=[
    'Flask >= 1.1.0',
    'wheel',
    'bootstrap-flask',
    'pytest'
  ],
)