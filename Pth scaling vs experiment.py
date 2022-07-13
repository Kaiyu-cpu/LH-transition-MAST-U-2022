#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 10:59:16 2022

@author: hukaiyu
"""


from cProfile import label
from turtle import color
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def Bout(Bt,Ip):
    A=1.45
    a=0.65
    mu0=4*np.pi*10**-7
    Btout=Bt*A/(A+1)
    Bpout=(mu0*Ip/(2*np.pi*a))*(1+A**-1)
    Bout=np.sqrt(Btout**2+Bpout**2)
    return Bout
def scaling(Bout,n):
    F=1
    gamma=1
    s=22
    Zeff=2
    Pth=0.072*Bout**0.7*n**0.7*s**0.9*(Zeff/2)*0.7*F**gamma
    return Pth
    
df = pd.read_excel('MAST-U_home.xlsx', index_col='Shot Number')

print(df.columns)

conventional = df.loc[(df['Divertor'].values=='Conventional')]
conventional_600 = df.loc[(df['Loop current [kA]'].values==600)]
conventional_750 = df.loc[(df['Loop current [kA]'].values==750)]
superX = df.loc[(df['Divertor'].values=='SUPER-X')]

Pth_for_sup=[]
for i in range (0,3):
    Pth_for_sup.append(scaling(Bout(df['BT at magnetic axis [T]'].values[i],df['Loop current [kA]'].values[i]*1000),df['ne E-20'].values[i]))

Pth_for_con=[]
for i in range (3,6):
    Pth_for_con.append(scaling(Bout(df['BT at magnetic axis [T]'].values[i],df['Loop current [kA]'].values[i]*1000),df['ne E-20'].values[i]))

Pth_bac_sup=[]
for i in range (0,3):
    Pth_bac_sup.append(scaling(Bout(df['BT at magnetic axis [T]'].values[i],df['Loop current [kA]'].values[i]*1000),df['ne E-20.1'].values[i]))

Pth_bac_con=[]
for i in range (3,6):
    Pth_bac_con.append(scaling(Bout(df['BT at magnetic axis [T]'].values[i],df['Loop current [kA]'].values[i]*1000),df['ne E-20.1'].values[i]))    
    
plt.figure(1)
plt.errorbar(Pth_for_sup,df['Pth no rad [MW]'].values[0:3],yerr=df['SDPth [MW]'].values[0:3],fmt='^',label='superX')
plt.errorbar(Pth_for_con,df['Pth no rad [MW]'].values[3:6],yerr=df['SDPth [MW]'].values[3:6],fmt='^',label='conventional')
y=[0,1,2,3,4]
plt.plot(y,y,label='scaling=experimental data')
plt.legend()
plt.xlabel('scaling prediction Pth (MW)')
plt.ylabel('Pth (MW)')
plt.show()



plt.figure(1)
plt.errorbar(Pth_for_sup,df['Pth no rad [MW]'].values[0:3],yerr=df['SDPth [MW]'].values[0:3],fmt='^',label='superX LH')
plt.errorbar(Pth_bac_sup[1:],df['Pth no rad [MW].1'].values[1:3],yerr=df['SDPth [MW].1'].values[1:3],fmt='v',label='superX HL')
plt.errorbar(Pth_for_con,df['Pth no rad [MW]'].values[3:6],yerr=df['SDPth [MW]'].values[3:6],fmt='^',label='conventional LH')
plt.errorbar(Pth_bac_con[:2],df['Pth no rad [MW].1'].values[3:5],yerr=df['SDPth [MW].1'].values[3:5],fmt='v',label='conventional HL')
y=[0,1,2,3,4]
plt.plot(y,y,label='scaling=experimental data')
plt.legend()
plt.xlabel('scaling prediction Pth (MW)')
plt.ylabel('Pth (MW)')

