from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='acs-data-collection',
    version='1.0.0',
    packages=find_packages(where='admin/library'),
    package_dir={'': 'admin/library'},
    description='ACS Data Collection Service - Professional data collection from marketplaces to ClickHouse',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='AbovyansConsultingServices',
    author_email='abovyan.mg@gmail.com',
    url='https://github.com/abovyanmg/data-collection-service',
    install_requires=[
        'requests',
        'clickhouse-connect',
        'pandas',
        'python-dateutil',
        'transliterate',
        'chardet'
    ],
    python_requires='>=3.7',
)

