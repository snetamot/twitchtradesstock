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
import twitch
from google import real_time_price

fig = plt.figure()
fig.patch.set_facecolor('lightsteelblue')
gs = fig.add_gridspec(6, 6)

# Plot where the current stocks up and down
ax1 = fig.add_subplot(gs[0:4, 0:4])
ax1.get_xaxis().set_ticks([])
ax1.get_yaxis().set_ticks([])

#NVDA
ax2 = fig.add_subplot(gs[0, 4:6])
ax2.get_xaxis().set_ticks([])
ax2.get_yaxis().set_ticks([])
ax2.set_facecolor('turquoise')
#MSFT
ax3 = fig.add_subplot(gs[1, 4:6])
ax3.get_xaxis().set_ticks([])
ax3.get_yaxis().set_ticks([])

#AAPL
ax4 = fig.add_subplot(gs[2, 4:6])
ax4.get_xaxis().set_ticks([])
ax4.get_yaxis().set_ticks([])

#GOOGL
ax5 = fig.add_subplot(gs[3, 4:6])
ax5.get_xaxis().set_ticks([])
ax5.get_yaxis().set_ticks([])

#AMZN
ax6 = fig.add_subplot(gs[4, 4:6])
ax6.get_xaxis().set_ticks([])
ax6.get_yaxis().set_ticks([])

#META
ax7 = fig.add_subplot(gs[5, 4:6])
ax7.get_xaxis().set_ticks([])
ax7.get_yaxis().set_ticks([])

#overall account value
ax8 = fig.add_subplot(gs[4, 0:4])
ax8.get_xaxis().set_ticks([])
ax8.get_yaxis().set_ticks([])

#last command executed / total in liquid
ax9 = fig.add_subplot(gs[5, 0:4])
ax9.get_xaxis().set_ticks([])
ax9.get_yaxis().set_ticks([])

stock = ['NVDA', 'MSFT', 'AAPL', 'GOOGL', 'AMZN', 'META']

plt.grid()
plt.show()
