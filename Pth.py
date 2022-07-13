from cProfile import label
from turtle import color
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_excel('MAST-U_home.xlsx', index_col='Shot Number')

print(df.columns)

conventional = df.loc[(df['Divertor'].values=='Conventional')]
conventional_600 = df.loc[(df['Loop current [kA]'].values==600)]
conventional_750 = df.loc[(df['Loop current [kA]'].values==750)]
superX = df.loc[(df['Divertor'].values=='SUPER-X')]

for div in [conventional_600,conventional_750,superX]:
    plt.figure(1)
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth [MW]'].dropna().values,yerr=div['SDPth [MW]'].dropna().values,fmt='^')
    plt.errorbar(div['ne E-20.1'].dropna().values,div['Pth [MW].1'].dropna().values,yerr=div['SDPth [MW].2'].dropna().values,fmt='v')

    plt.figure(2)
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth no rad [MW]'].dropna().values,yerr=div['SDPth [MW].1'].dropna().values,fmt='^')
    plt.errorbar(div['ne E-20.1'].dropna().values,div['Pth no rad [MW].1'].dropna().values,yerr=div['SDPth [MW].3'].dropna().values,fmt='v')

    plt.figure(3)
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth [MW]'].dropna().values,yerr=div['SDPth [MW]'].dropna().values,fmt='^')

    plt.figure(4)
    plt.errorbar(div['ne E-20'].dropna().values,div['Pth no rad [MW]'].dropna().values,yerr=div['SDPth [MW].1'].dropna().values,fmt='^')

plt.figure(1)
plt.ylabel('Pth [MW]')
plt.xlabel('ne E-20 []')
plt.legend(['LH conventional - 600kA','LH conventional - 750kA','LH SuperX - 600kA','HL conventional at 600kA','HL conventional - 750kA','HL SuperX - 600kA'])

plt.figure(2)
plt.ylabel('Pth no rad [MW]')
plt.xlabel('ne E-20 []')
plt.legend(['LH conventional - 600kA','LH conventional - 750kA','LH SuperX - 600kA','HL conventional at 600kA','HL conventional - 750kA','HL SuperX - 600kA'])

plt.figure(3)
plt.ylabel('Pth [MW]')
plt.xlabel('ne E-20 []')
plt.legend(['LH conventional - 600kA','LH conventional - 750kA','LH SuperX - 600kA'])

plt.figure(4)
plt.ylabel('Pth no rad [MW]')
plt.xlabel('ne E-20 []')
plt.legend(['LH conventional - 600kA','LH conventional - 750kA','LH SuperX - 600kA'])



plt.show()


