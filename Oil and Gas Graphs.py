import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from pylab import savefig


sns.set(style="whitegrid")
sns.palplot(sns.color_palette("coolwarm", 7))


df= pd.read_csv('/Users/asuth/Desktop/Oil and Gas Correlation/Oil1.csv')

print(df.head())
CNQ_mean= df['CNQ'].mean()
CNQ_std= df['CNQ'].std()
CNQ_norm= (df['CNQ'] - CNQ_mean )/ CNQ_std
print(CNQ_norm.head())

CVX_mean= df['CVX'].mean()
CVX_std= df['CVX'].std()
CVX_norm= (df['CVX']- CVX_mean)/ CVX_std
print(CVX_norm.head())


Brent_mean= df['Brent'].mean()
Brent_std= df['Brent'].std()
Brent_norm= (df['Brent'] - Brent_mean)/ Brent_std
print(Brent_norm.head())

DowOG_mean= df['DowOG'].mean()
DowOG_std= df['DowOG'].std()
DowOG_norm= (df['DowOG'] - DowOG_mean)/ DowOG_std
print(DowOG_norm.head())


DJI1_mean= df['DJI'].mean()
DJI1_std= df['DJI'].std()
DJI1_norm= (df['DJI']- DJI1_mean)/ DJI1_std
print(DJI1_norm.head())

WTI_mean= df['WTI'].mean()
WTI_std= df['WTI'].std()
WTI_norm= (df['WTI']- WTI_mean)/ WTI_std
print(WTI_norm.head())
Tot_data= pd.DataFrame([CNQ_norm, CVX_norm, WTI_norm, DJI1_norm, DowOG_norm, Brent_norm]).T
print(Tot_data.head())

Graph1= pd.DataFrame([CNQ_norm, CVX_norm, WTI_norm]).T
Graph2= pd.DataFrame([CNQ_norm, WTI_norm]).T
Graph3= pd.DataFrame([CNQ_norm, Brent_norm, DJI1_norm]).T

Dates= df['D1']

print(Dates.head())


sns.lineplot(data=Graph1, palette='tab10', linewidth=2.5)
sns.lineplot(data=Graph2, palette='tab10', linewidth=2.5)

TotCorr = Tot_data.corr()
print(TotCorr.head())
TMax= TotCorr.max()
TMin= TotCorr.min()
midpoint= (TMax - TMin)/2
ax= sns.heatmap(TotCorr, vmin=-1, vmax=1, center=0, square=True)
figure= ax.get_figure()
figure.savefig('corr_fig.png')
