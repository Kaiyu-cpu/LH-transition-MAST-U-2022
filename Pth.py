import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('./MAST-U_home.xlsx', index_col='Shot Number')

print(df.columns)

conventional = df.loc[(df['Divertor'].values=='Conventional')]
conventional_600 = df.loc[(df['Loop current [kA]'].values==600)]
conventional_750 = df.loc[(df['Loop current [kA]'].values==750)]
superX = df.loc[(df['Divertor'].values=='SUPER-X')]

colors = ['midnightblue', 'royalblue','orangered']

for div, col in zip([conventional_600,conventional_750,superX],colors):

    plt.figure(1,figsize=(8,5))
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth^rad [MW]'].dropna().values,yerr=div['SDPth [MW]'].dropna().values,fmt='^',color=col)
    plt.errorbar(div['ne E-20.1'].dropna().values,div['Pth^rad [MW].1'].dropna().values,yerr=div['SDPth [MW].2'].dropna().values,fmt='v',color=col,markerfacecolor='none')

    plt.figure(2,figsize=(8,5))
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth [MW]'].dropna().values,yerr=div['SDPth [MW].1'].dropna().values,fmt='^',color=col)
    plt.errorbar(div['ne E-20.1'].dropna().values,div['Pth [MW].1'].dropna().values,yerr=div['SDPth [MW].3'].dropna().values,fmt='v',color=col,markerfacecolor='none')

    plt.figure(3,figsize=(8,5))
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth^rad [MW]'].dropna().values,yerr=div['SDPth [MW]'].dropna().values,fmt='^',color=col)

    plt.figure(4,figsize=(8,5))
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth [MW]'].dropna().values,yerr=div['SDPth [MW].1'].dropna().values,fmt='^',color=col)

plt.figure(1)
plt.ylabel('$P_{th,rad} [MW]$')
plt.xlabel('$n_e [10^{20}m^{-3}]$')
plt.ylim(0,4.5)
plt.xlim(0,2.0)
plt.legend(['LH conventional - 600kA','HL conventional at 600kA','LH conventional - 750kA','HL conventional - 750kA','LH SuperX - 600kA','HL SuperX - 600kA'])
plt.savefig(f'./figures/Pth-rad-LHHL.png')

plt.figure(2)
plt.ylabel('$P_{th} [MW]$')
plt.xlabel('$n_e [10^{20}m^{-3}]$')
plt.ylim(0,4.5)
plt.xlim(0,2.0)
plt.legend(['LH conventional - 600kA','HL conventional at 600kA','LH conventional - 750kA','HL conventional - 750kA','LH SuperX - 600kA','HL SuperX - 600kA'])
plt.savefig(f'./figures/Pth-LHHL.png')

plt.figure(3)
plt.ylabel('$P_{th,rad} [MW]$')
plt.xlabel('$n_e [10^{20}m^{-3}]$')
plt.ylim(0,4.5)
plt.xlim(0,2.0)
plt.legend(['conventional - 600kA','conventional - 750kA','SuperX - 600kA'])
plt.savefig(f'./figures/Pth-rad-LH.png')

plt.figure(4)
plt.ylabel('$P_{th} [MW]$')
plt.xlabel('$n_e [10^{20}m^{-3}]$')
plt.ylim(0,4.5)
plt.xlim(0,2.0)
plt.legend(['conventional - 600kA','conventional - 750kA','SuperX - 600kA'])
plt.savefig(f'./figures/Pth-LH.png')