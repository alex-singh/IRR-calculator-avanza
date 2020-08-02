import pandas
import datetime
import math
from scipy.optimize import fsolve
import yaml

CONSIDER_COMMISSIONS = True

def main():
    with open("conf.yaml", 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    df = pandas.read_csv('transactions.csv', sep=';', header=0, decimal=',',
                converters={'amount':convertToFloat, 'quote':convertToFloat, 'commission':convertToFloat, 'date':convertToDate},
                names=['date', 'account', 'transactionType', 'description', 'qty', 'quote', 'amount', 'commission', 'curr', 'isin'])

    print('******** IRR of positions ********\n')
    for pos in conf.get('positions'):
        print_position(pos, df)
    print('\n************************')

def print_position(pos, df):
    ts = df[(df.description.str.match(pos.get('regex'))) & (df.amount.notna())]
    irr = calc_irr(ts, pos.get('quantity') * pos.get('price', 0), irr_to_date(pos, ts))
    print(pos.get('name') + ':',  str(round(100 * irr, 2)) + '%', special_greeting(irr))

def irr_to_date(pos, ts):
    if pos.get('quantity') == 0:
        return ts['date'].max()
    else:
        return datetime.date.today()

def special_greeting(irr):
    if irr > 0.20:
        return " ---- Great job Mr. Buffett"
    if irr < -0.4:
        return " ---- Ouch... that's gonna hurt your overall portfolio performance"
    return ""

def calc_irr(transactions, market_price, to_date):
    def target(r):
        return present_value(r, transactions, to_date) - market_price

    return fsolve(target, 0)[0]

def present_value(r, transactions, to_date):
    pv = 0
    for i, t in transactions.iterrows():
        pv += t.amount * capitalization_factor(r, t.date, to_date)
        if CONSIDER_COMMISSIONS & (not math.isnan(t.commission)):
            pv += -t.commission * capitalization_factor(r, t.date, to_date)
    return -pv

def capitalization_factor(r, t0, t1):
    dt = (t1 - t0).days / 360
    return math.exp(dt*r)


def convertToFloat(s):
    return float(s.replace(',','.')) if s != '-' else float('nan') 

def convertToDate(s):
    return datetime.date.fromisoformat(s)

if __name__ == "__main__":
    main()