#!/usr/bin/env python3


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('waitTime.csv',parse_dates=[0], index_col=[0])
for l in df.columns:
  fig, ax = plt.subplots()
  df[[l]].plot()
  fig.
