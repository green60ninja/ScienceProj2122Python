import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('values.csv')
# df.plot()
df.plot(kind='scatter', x='Longitude', y='Latitude')
plt.show()