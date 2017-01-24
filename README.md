# decentralized-mortgage-market
After cloning the repository initialize dispersy by running

`git submodule update --init --recursive`

Install the dependencies with

`pip install tftpy nose coverage decorator cryptography faker twisted m2crypto netifaces enum34 mock`

Run the market using market.py

  usage: market.py [-h] [--headless] [--bank {abn,ing,rabo,moneyou}]
                   [--scenario {bank,borrower,investor}]

  optional arguments:
    -h, --help            show this help message and exit
    --headless            Run the market in headless mode
    --bank {abn,ing,rabo,moneyou}
                          Run the market as a bank.
    --scenario {bank,borrower,investor}
                          Select a scenario to enable
                          
Generate the API docs by running `make html` in the docs directory.



Travis CI build status: [![Build Status](https://travis-ci.org/Jumba/decentralized-mortgage-market.svg?branch=master)](https://travis-ci.org/Jumba/decentralized-mortgage-market)


Jenkins build status: [![Build Status](https://jenkins.tribler.org/job/pers/job/bep_market_v3/badge/icon)](https://jenkins.tribler.org/job/pers/job/bep_market_v3/)
