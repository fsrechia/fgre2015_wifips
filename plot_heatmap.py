import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

dfn = pd.read_csv('for_heatmap.csv')

dfn['robloc'] = dfn.apply(lambda x : str(x['loc_x']) + '_' + str(x['loc_y']), axis=1)
dfgrp = dfn.groupby(['robot_id', 'robloc', 'ssid', 'ssid_loc_x', 'ssid_loc_y', 'loc_x', 'loc_y']).agg({'rssi' : {'rssi_avg' : np.mean, 'rssi_per_95' : lambda x: np.percentile(x, q = 95)}})

dfgrp.reset_index(level=0, inplace=True)
dfgrp.reset_index(level=0, inplace=True)
dfgrp.reset_index(level=0, inplace=True)
dfgrp.reset_index(level=0, inplace=True)
dfgrp.reset_index(level=0, inplace=True)
dfgrp.reset_index(level=0, inplace=True)
dfgrp.reset_index(level=0, inplace=True)

cols = list()

for x in dfgrp.columns:
	if x[1] == '':
		cols.append(x[0])
	else:
		cols.append(x[1])

dfgrp.columns = cols

plt.close('all')

dfp = dfgrp[(dfgrp['robloc']=='4798_402') & (dfgrp['robot_id'] == 'robot5')]

dfp['to_plot'] = dfp['rssi_avg'] - df['rssi_avg'].min()
plt.scatter(dfp['ssid_loc_x'], dfp['ssid_loc_y'], s=dfp['to_plot']*10, c=dfp['to_plot'], cmap=cm.gnuplot)

plt.plot(4798, 402, 'r.', markersize=10)
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('Heat Map (Larger the bubble, greater the strength, red bubble shows location of robot')
plt.savefig('fgre_plot.png', format='png')
plt.savefig('fgre_plot.pdf', format='pdf')