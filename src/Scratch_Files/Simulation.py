import json
import pandas as pd


df = pd.read_csv('wk2.csv')
df['implied_prob'] = df['Moneyline']
