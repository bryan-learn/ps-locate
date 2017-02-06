from setuptools import setup, find_packages

setup(
    name='pslocate',
    version='0.2.1',
    url='https://github.com/bryan-learn/ps-locate',
    author='Bryan Learn',
    author_email='blearn@psc.edu',
    include_package_data=True,
    platforms='any',
    scripts=['ps_locate'],
    packages=find_packages(),
    data_files = [('', ['geolocate/GeoLite2-City.mmdb']), ('',['log/ps_locate.log'])],
)
