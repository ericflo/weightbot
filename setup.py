from setuptools import setup, find_packages
 
VERSION = '0.1'
 
LONG_DESCRIPTION = """
This module is an unofficial API into WeightBot_.  Right now it's very simple
because WeightBot_ is simple.

Here's an example of how you can use it::

    from weightbot import WeightBot
    from pprint import pprint
    
    wb = WeightBot('me@example.com', 'my_password')
    data = wb.get_data()
    
    pprint(data)

And then running that program might result in::

    [{'date': datetime.date(2009, 8, 6), 'kilograms': 91.2, 'pounds': 201.1},
     {'date': datetime.date(2009, 8, 7), 'kilograms': 90.1, 'pounds': 198.7},
     {'date': datetime.date(2009, 8, 8), 'kilograms': 90.0, 'pounds': 198.5},
     {'date': datetime.date(2009, 8, 9), 'kilograms': 89.8, 'pounds': 198.0},]


You could also get at the raw csv file by doing ``wb.get_csv_data``.

Hope you enjoy it!

.. _WeightBot: http://tapbots.com/weightbot
"""
 
setup(
    name='weightbot',
    version=VERSION,
    description="An unofficial API into WeightBot.com",
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Web Environment",
    ],
    keywords='weight,weightbot,api',
    author='Eric Florenzano',
    author_email='floguy@gmail.com',
    url='http://github.com/ericflo/weightbot/tree/master',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['setuptools'],
)