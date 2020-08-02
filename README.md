# IRR calculator for transactions from Avanza

This an internal rate of return (IRR) calculator for instruments traded on Avanza using a .csv file that you can download from your account on Avanza. 

## Getting Started

1. You first have to download your transactions in a .csv file from your Avanza account. Replace the transactions.csv file with your downloaded transactions

2. configure conf.yaml according to which instruments you want to calculate IRR for. You will need to supply quantity of instruments you currently hold and the price of them. You also need to supply a regex to identify the instrument.

3. run main.py using python

### Prerequisites

You will need the following python libraries:

```
pip3 install pandas
pip3 install scipy
pip3 install pyyaml
```
