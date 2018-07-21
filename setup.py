from setuptools import setup, find_packages

setup(
    name='webcrawler',
    version='0.1',
    description='Webcrawler that gathers links from website',
    url='https://github.com/mmalarz/webcrawler',
    license='LICENSE',
    packaages=find_packages(),
    install_requires=[
        'beautifulsoup4 >= 4.6.0',
        'lxml >= 4.2.0',
        'requests >= 2.18.4',
    ],
    zip_safe=False
)

