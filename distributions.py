# Boston2018 / Boston2012 are interchangable and you can query any race key you like to make this comparison

import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

df = pd.read_csv('path', low_memory=False)


boston2012 = df.query("racekey == 'Boston_Marathon2012-04-16'")['time'].str.slice(stop=4).to_frame()
boston2018 = df.query("racekey == 'Boston_Marathon2018-04-16'")['time'].str.slice(stop=4).to_frame()
boston2012['time'] = pd.to_timedelta(boston2012['time'].astype(str) + ':00')
boston2018['time'] = pd.to_timedelta(boston2018['time'].astype(str) + ':00')
boston2012_min = pd.to_numeric(boston2012['time'].dt.total_seconds() / 60)
boston2018_min = pd.to_numeric(boston2018['time'].dt.total_seconds() / 60)


graph_data = pd.concat([boston2012_min, boston2018_min], axis=1, keys=['2012', '2018'])

# pd.to_numeric(boston2012['time'].to_list()), pd.to_numeric(boston2018['time'].to_list())

background_color = '#002b36'

print(graph_data.columns)

baa_palette = sns.color_palette([(2/255, 75/255, 142/255), (255/255, 215/255, 0)])
sns.set_palette(baa_palette)
sns.set_style("dark", {'axes.facecolor': '#657b83'})

# sns.kdeplot(data=graph_data, fill=True, alpha=.5)
sns.kdeplot(data=boston2012_min, label='Boston 2012', shade=True, alpha=0.5, color=(0/255, 83/255, 155/255))
sns.kdeplot(data=boston2018_min, label='Boston 2018', shade=True, alpha=0.5, color=(255/255, 184/255, 28/255))

plt.gca().set_facecolor(background_color)
plt.rcParams['text.color'] = 'white'



plt.xlim(120, 480)
plt.xticks([120, 180, 240, 300, 360, 420, 480], ['2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00'])
plt.xlabel('Finishing time')
plt.ylabel('Density of Finishers')
plt.title('Distribution of Fininshing Times for the Boston Marathon')

avg_temp_boston2012 = df.query('racekey == "2012 Boston Marathon"')['avgtemp']
avg_temp_boston2018 = df.query('racekey == "2018 Boston Marathon"')['avgtemp']

plt.legend(title='Year', loc='upper right', labels=['2018: 70.28\xb0F', '2012: 45.25\xb0F'])


plt.show()
