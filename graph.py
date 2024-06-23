# Want to make a candlestick graph that tracks
# the current stocks in inventory and the overall value of
# the account

from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.animation as animation
from matplotlib.gridspec import GridSpec
import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import math


fig = plt.figure()
fig.patch.set_facecolor('gray')
gs = fig.add_gridspec(6, 6)
ax1 = fig.add_subplot(gs[0:4, 0:4])
ax2 = fig.add_subplot(gs[0, 4:6])
ax3 = fig.add_subplot(gs[1, 4:6])
ax4 = fig.add_subplot(gs[2, 4:6])
ax5 = fig.add_subplot(gs[3, 4:6])
ax6 = fig.add_subplot(gs[4, 4:6])
ax7 = fig.add_subplot(gs[5, 4:6])
ax8 = fig.add_subplot(gs[4, 0:4])
ax9 = fig.add_subplot(gs[5, 0:4])

stock = ['AAPL', 'AMZN', 'NVDA', 'MSFT', 'META', 'GOOGL', 'GME']



plt.show()