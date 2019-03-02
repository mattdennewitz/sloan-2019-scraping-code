# SSAC 19 Scraping w/ Python 3

Hello! Happy to have you following along. The session deck will be available
after the presentation, so please feel free to poke around here while I talk.

## Installation

First, clone this repository

```shell
$ git clone git@github.com:mattdennewitz/sloan-2019-scraping-code.git
```

Enter the repository

```shell
$ cd sloan-2019-scraping-code
```

Create a virtual environment for this project, then activate

```shell
$ python3 -m venv .
$ source bin/activate
```

Finally, install its requirements

```shell
$ pip install -r requirements.txt
```

This will install `requests-html` and `requests`.

## Usage

With your environment still activated, you may run any of the
Python scripts to pull data. These scripts will overwrite the
CSV files included in the repo.

Running the BP scraper:

```shell
$ python p_bpro.py
```

Once you've run a scraper, view its relevant CSV output file to see the results.
