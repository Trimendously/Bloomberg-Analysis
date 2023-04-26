# US Congress Bills & Stock Price Analysis tool

The goal of this application is to facilitate for anlysis of U.S Congress bills and the price of stocks of companies in the S&P 500

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

Instructions for installing the project.

Install latest version of python from https://www.python.org/downloads/

- make sure to click the box to add python to your path when installing


Make sure that you have a working Bloomberg Terminal subscription and ensure that you are logged in to your account on your local machine.
(This has not been tested on Bloomberg Anywhere)
``` bash
$ git clone https://github.com/Trimendously/Bloomberg-Analysis.git
$ cd Bloomberg-Analysis
$ python -m pip install --index-url=https://bcms.bloomberg.com/pip/simple blpapi
$ python Analysis_GUI.py
```

## Usage
Prompts the user to specfiy a specfic date range with any Saturday/ Sundays and specific federal holidays being excluded.

Collects the companies that are currently in the S&P 500
and for the specified date range finds their average stock price

Logs the bills introduced to the U.S. Congress during this date range

## Contributing
Anyone is welcome to contribute to this project this was just a fun side project I decided to work on as I myself became more familiar with the Bloomberg Terminals

## License
This project is licensed under the MIT License - see the LICENSE file for details.
