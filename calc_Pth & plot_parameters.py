#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 20:37:19 2022

@author: kc1457

Read me: This code is used to calculate Pth and plot the power breakdown and the general parameters.
         Please make sure you also have calc_pohm.py,calc_w_dot.py,calc_ne_bar.py and read_efit.py in the directory.
         Each cell has different function. Please run cell by cell.
"""

import pyuda
#from mast.mast_client import ListType
import matplotlib.pyplot as plt
from mastu_exhaust_analysis.calc_pohm import calc_pohm
from mastu_exhaust_analysis.calc_w_dot import calc_w_dot
from mastu_exhaust_analysis.calc_ne_bar import calc_ne_bar
#from mastu_exhaust_analysis.calc_psol import calc_psol
from scipy.interpolate import interp1d
import numpy as np

def Sum (a,b):
    return a.data+b.data

def single_plot(shot,t,p,label,LH,HL,Range):
    plt.figure(figsize=(15,6))
    for i in range (len(p)):
        if label[i]=='Ploss':
            plt.plot(t[i],p[i],linewidth=3)
        else:
            plt.plot(t[i],p[i])
    plt.xlabel('t (s)')
    plt.legend(label,loc='best')
    plt.title(shot)
    plt.axvline(LH,linestyle='--',color='g')
    plt.axvline(HL,linestyle='--',color='r')
    plt.xlim(Range)
    plt.show()

#%% load data
   
client=pyuda.Client()

SWP_1 = client.get('/XNB/SW/BEAMPOWER',45154) # south west beam power
SWP_2 = client.get('/XNB/SW/BEAMPOWER',45312) # south west beam power
SWP_3 = client.get('/XNB/SW/BEAMPOWER',45352) # south west beam power

SSP_1 = client.get('/XNB/SS/BEAMPOWER',45154) # south south beam power
SSP_2 = client.get('/XNB/SS/BEAMPOWER',45312) # south south beam power
#SSP_2 = client.get('/XNB/SS/BEAMPOWER',45352) # south south beam power

Pnbi_1 = Sum(SWP_1,SSP_2)*1000000 #convert unit into W
Pnbi_2 = Sum(SWP_2,SSP_2)*1000000
Pnbi_3 = SWP_3.data*1000000
Pnbi_1_time = SWP_1.time.data
Pnbi_2_time = SWP_2.time.data  
Pnbi_3_time = SWP_3.time.data
#Pnbi_3 = Sum(SWP_3,SSP_3)

Prad_1 = client.get('/abm/core/prad',45154) # radiation power
Prad_2 = client.get('/abm/core/prad',45312) # radiation power
Prad_3 = client.get('/abm/core/prad',45352) # radiation power

dW_1 = calc_w_dot(45154) # gradient of plasma stored energy
dW_2 = calc_w_dot(45312) # gradient of plasma stored energy
dW_3 = calc_w_dot(45352) # gradient of plasma stored energy

Poh_1 = calc_pohm(45154) # ohmic heating
Poh_2 = calc_pohm(45312) # ohmic heating
Poh_3 = calc_pohm(45352) # ohmic heating

ne_1 = calc_ne_bar(45154) # line averaged electron density
ne_2 = calc_ne_bar(45312) # line averaged electron density
ne_3 = calc_ne_bar(45352) # line averaged electron densityg
#%% Calculate Pth (linear interpolation is used)
fPnbi_1 = interp1d(Pnbi_1_time,Pnbi_1)
fPnbi_2 = interp1d(Pnbi_2_time,Pnbi_2)
fPnbi_3 = interp1d(Pnbi_3_time,Pnbi_3)
Pin_1 = []
Pin_2 = []
Pin_3 = []
Pin_1_time = []
Pin_2_time = []
Pin_3_time = []

for i in range (len(Poh_1['t'])):
     Pin_1.append(float(fPnbi_1(Poh_1['t'][i])) + Poh_1['pohm'][i])
     Pin_1_time.append(Poh_1['t'][i])
     
for i in range (len(Poh_2['t'])):
     Pin_2.append(float(fPnbi_2(Poh_2['t'][i])) + Poh_2['pohm'][i])
     Pin_2_time.append(Poh_2['t'][i])

for i in range (len(Poh_3['t'])):
     Pin_3.append(float(fPnbi_3(Poh_3['t'][i])) + Poh_3['pohm'][i])
     Pin_3_time.append(Poh_3['t'][i])

fPin_1 = interp1d(Pin_1_time,Pin_1)
fPin_2 = interp1d(Pin_2_time,Pin_2)
fPin_3 = interp1d(Pin_3_time,Pin_3)
fPrad_1 = interp1d(Prad_1.time.data,Prad_1.data)
fPrad_2 = interp1d(Prad_2.time.data,Prad_2.data)
fPrad_3 = interp1d(Prad_3.time.data,Prad_3.data)
PL_1 = []
PL_2 = []
PL_3 = []
PL_1_time = []
PL_2_time = []
PL_3_time = []

for i in range (len(dW_1['t'])):
     PL_1.append(float(fPin_1(dW_1['t'][i])) - dW_1['data'][i] - fPrad_1(dW_1['t'][i]))
     PL_1_time.append(dW_1['t'][i])
     
for i in range (len(dW_2['t'])):
     PL_2.append(float(fPin_2(dW_2['t'][i])) - dW_2['data'][i] - fPrad_2(dW_1['t'][i]))
     PL_2_time.append(dW_2['t'][i])
     
for i in range (len(dW_3['t'])):
     PL_3.append(float(fPin_3(dW_3['t'][i])) - dW_3['data'][i] - fPrad_3(dW_1['t'][i]))
     PL_3_time.append(dW_3['t'][i])
     
#%% shot 45154 power breakdown plot
shot=45154
LH=0.848
HL=0.8501
time=[PL_1_time,dW_1['t'],Poh_1['t'],Pnbi_1_time,Prad_1.time.data]
parameters=[PL_1,dW_1['data'],Poh_1['pohm'],Pnbi_1,Prad_1.data]
labels=['Ploss','dW/dt','Poh','Pnbi','Prad_core']
Range=np.array([0.8,0.9])
single_plot(shot, time, parameters, labels,LH,HL,Range)
     

#%% shot 45312  power breakdown plot
shot=45312
LH=0.714
HL=0.7318
time=[PL_2_time,dW_2['t'],Poh_2['t'],Pnbi_2_time,Prad_2.time.data]
parameters=[PL_2,dW_2['data'],Poh_2['pohm'],Pnbi_2,Prad_2.data]
labels=['Ploss','dW/dt','Poh','Pnbi','Prad_core']
Range=np.array([0.66,0.76])
single_plot(shot, time, parameters, labels,LH,HL,Range)

#%% shot 45352  power breakdown plot
shot=45312
LH=0.482
HL=0.6107
time=[PL_3_time,dW_3['t'],Poh_3['t'],Pnbi_3_time,Prad_3.time.data]
parameters=[PL_3,dW_3['data'],Poh_3['pohm'],Pnbi_3,Prad_3.data]
labels=['Ploss','dW/dt','Poh','Pnbi','Prad_core']
Range=np.array([0.2,0.9])
single_plot(shot, time, parameters, labels,LH,HL,Range)
#%% plot of PL against t
plt.title('#45154 with Prad')
plt.plot(PL_1_time,PL_1,'x')
plt.ylabel('PL (J)')
plt.xlabel('t (s)')
plt.show()  
plt.title('#45312 with Prad')
plt.plot(PL_2_time,PL_2,'x')
plt.ylabel('PL (J)')
plt.xlabel('t (s)')
plt.show()  
plt.title('#45352 with Prad')
plt.plot(PL_3_time,PL_3,'x')
plt.ylabel('PL (J)')
plt.xlabel('t (s)')
plt.show()    
     
#%% show the value of Pth^rad
fPL_1 = interp1d(PL_1_time,PL_1)
fPL_2 = interp1d(PL_2_time,PL_2)
fPL_3 = interp1d(PL_3_time,PL_3)
print('Pth with Prad for #45154 is', fPL_1(0.848))
print('Pth with Prad for #45312 is', fPL_2(0.714))
print('Pth with Prad for #45352 is', fPL_2(0.482))
     
#%% plot of PL  aganist ne
plt.title('PL vs ne with Prad')
fne_1 = interp1d(ne_1['t'],ne_1['data'])
fne_2 = interp1d(ne_2['t'],ne_2['data'])
fne_3 = interp1d(ne_3['t'],ne_3['data'])
ne = np.array([fne_1(0.848),fne_2(0.714),fne_3(0.482)])
Pth = np.array([fPL_1(0.848)/1e6,fPL_2(0.714)/1e6,fPL_3(0.482)/1e6])
plt.plot(ne,Pth,'x')
plt.ylabel('threshold power (MW)')
plt.xlabel('line averaged electron density')
plt.errorbar(ne,Pth,yerr=0.1*Pth,xerr=0.01*ne,fmt='none')
print('Pth with Prad for #45154 is', fPL_1(0.848)/1e6)
print('Pth with Prad for #45312 is', fPL_2(0.714)/1e6)
print('Pth with Prad for #45352 is', fPL_2(0.482)/1e6)
     
#%% Load other parameters    
p_I_1 = client.get('AMC/PLASMA_CURRENT',45154) #plasma current
p_I_data_1 = p_I_1.data
p_I_time_1 = p_I_1.time.data
p_I_2 = client.get('AMC/PLASMA_CURRENT',45312) #plasma current
p_I_data_2 = p_I_2.data
p_I_time_2 = p_I_2.time.data
p_I_3 = client.get('AMC/PLASMA_CURRENT',45352) #plasma current
p_I_data_3 = p_I_3.data
p_I_time_3 = p_I_3.time.data

D_a_1 = client.get('xim/da/hu10/osp',45154) #D-alpha upper outer strike point
D_a_data_1 = D_a_1.data
D_a_time_1 = D_a_1.time.data
D_a_2 = client.get('xim/da/hu10/osp',45312) #D-alpha upper outer strike point
D_a_data_2 = D_a_2.data
D_a_time_2 = D_a_2.time.data
D_a_3 = client.get('xim/da/hu10/osp',45352) #D-alpha upper outer strike point
D_a_data_3 = D_a_3.data
D_a_time_3 = D_a_3.time.data

W_1 = client.get('epm/output/globalParameters/plasmaEnergy',45154) #plama stored energy
W_data_1 = W_1.data
W_time_1 = W_1.time.data
W_2 = client.get('epm/output/globalParameters/plasmaEnergy',45312) #plama stored energy
W_data_2 = W_2.data
W_time_2 = W_2.time.data
W_3 = client.get('epm/output/globalParameters/plasmaEnergy',45352) #plama stored energy
W_data_3 = W_3.data
W_time_3 = W_3.time.data

T_e_core_1 = client.get('ayc/t_e_core',45154) #electron core temperature
T_e_core_data_1 = T_e_core_1.data
T_e_core_time_1 = T_e_core_1.time.data
T_e_core_2 = client.get('ayc/t_e_core',45312) #electron core temperature
T_e_core_data_2 = T_e_core_2.data
T_e_core_time_2 = T_e_core_2.time.data
T_e_core_3 = client.get('ayc/t_e_core',45352) #electron core temperature
T_e_core_data_3 = T_e_core_3.data
T_e_core_time_3 = T_e_core_3.time.data

B_1 = client.get('EPM/OUTPUT/GLOBALPARAMETERS/BPHIRMAG',45154)
B_2 = client.get('EPM/OUTPUT/GLOBALPARAMETERS/BPHIRMAG',45312)
B_3 = client.get('EPM/OUTPUT/GLOBALPARAMETERS/BPHIRMAG',45352)


#%% Plot general parameters for shot 45154
fig,axes = plt.subplots(nrows=7,ncols=1,sharex='col',sharey='row',figsize=(15,10))
fig.suptitle ('45154')

ax0 = axes[0]
ax0.plot(p_I_time_1,p_I_data_1,label='Ip')
ax0.legend(loc='left')
ax0.set_xlim([0.8,0.9])
#ax0.set_ylim([500,700])
ax0.axvline(0.848,linestyle='--',color='g')
ax0.axvline(0.8501,linestyle='--',color='r')

ax1 = axes[1]
ax1.plot(ne_1['t'],ne_1['data'],label='ne')
ax1.legend(loc='left')
#ax1.set_ylim([500,700])
ax1.axvline(0.848,linestyle='--',color='g')
ax1.axvline(0.8501,linestyle='--',color='r')

ax2 = axes[2]
ax2.plot(W_time_1,W_data_1,label='W')
ax2.legend(loc='left')
#ax2.set_ylim([500,700])
ax2.axvline(0.848,linestyle='--',color='g')
ax2.axvline(0.8501,linestyle='--',color='r')

ax3 = axes[3]
ax3.plot(T_e_core_time_1,T_e_core_data_1,label='Te_core')
ax3.legend(loc='left')
ax3.set_ylim([0,1200])
ax3.axvline(0.848,linestyle='--',color='g')
ax3.axvline(0.8501,linestyle='--',color='r')

ax4 = axes[4]
ax4.plot(D_a_time_1,D_a_data_1,label='Da')
ax4.legend(loc='left')
#ax4.set_ylim([500,700])
ax4.axvline(0.848,linestyle='--',color='g')
ax4.axvline(0.8501,linestyle='--',color='r')

ax5 = axes[5]
ax5.plot(B_1.time.data,B_1.data,label='Bt')
ax5.legend(loc='left')
#ax5.set_ylim([500,700])
ax5.axvline(0.848,linestyle='--',color='g')
ax5.axvline(0.8501,linestyle='--',color='r')

ax6 = axes[6]
ax6.plot(Poh_1['t'],Poh_1['pohm'],label='Poh')
ax6.plot(Pnbi_1_time,Pnbi_1,label='Pnbi')
ax6.plot(PL_1_time,PL_1,label='Ploss')
ax6.legend(loc='left')
ax6.set_ylim([-1e6,2e6])
ax6.axvline(0.848,linestyle='--',color='g')
ax6.axvline(0.8501,linestyle='--',color='r')
ax6.set_xlabel('t (s)')

#%% Plot general parameters for shot 45312
fig,axes = plt.subplots(nrows=7,ncols=1,sharex='col',sharey='row',figsize=(15,10))
fig.suptitle ('45312')

ax0 = axes[0]
ax0.plot(p_I_time_2,p_I_data_2,label='Ip')
ax0.legend(loc='left')
ax0.set_xlim([0.7,0.75])
ax0.set_ylim([500,700])
ax0.axvline(0.714,linestyle='--',color='g')
ax0.axvline(0.7318,linestyle='--',color='r')

ax1 = axes[1]
ax1.plot(ne_2['t'],ne_2['data'],label='ne')
ax1.legend(loc='left')
#ax1.set_ylim([500,700])
ax1.axvline(0.714,linestyle='--',color='g')
ax1.axvline(0.7318,linestyle='--',color='r')

ax2 = axes[2]
ax2.plot(W_time_2,W_data_2,label='W')
ax2.legend(loc='left')
#ax2.set_ylim([500,700])
ax2.axvline(0.714,linestyle='--',color='g')
ax2.axvline(0.7318,linestyle='--',color='r')

ax3 = axes[3]
ax3.plot(T_e_core_time_2,T_e_core_data_2,label='Te_core')
ax3.legend(loc='left')
ax3.set_ylim([0,1000])
ax3.axvline(0.714,linestyle='--',color='g')
ax3.axvline(0.7318,linestyle='--',color='r')

ax4 = axes[4]
ax4.plot(D_a_time_2,D_a_data_2,label='Da')
ax4.legend(loc='left')
#ax4.set_ylim([500,700])
ax4.axvline(0.714,linestyle='--',color='g')
ax4.axvline(0.7318,linestyle='--',color='r')

ax5 = axes[5]
ax5.plot(B_2.time.data,B_2.data,label='Bt')
ax5.legend(loc='left')
#ax5.set_ylim([500,700])
ax5.axvline(0.714,linestyle='--',color='g')
ax5.axvline(0.7318,linestyle='--',color='r')

ax6 = axes[6]
ax6.plot(Poh_2['t'],Poh_2['pohm'],label='Poh')
ax6.plot(Pnbi_2_time,Pnbi_2,label='Pnbi')
ax6.plot(PL_2_time,PL_2,label='Ploss')
ax6.legend(loc='left')
ax6.set_ylim([0,5e6])
ax6.axvline(0.714,linestyle='--',color='g')
ax6.axvline(0.7318,linestyle='--',color='r')
ax6.set_xlabel('t (s)')

#%% Plot general parameters for shot 45352
fig,axes = plt.subplots(nrows=7,ncols=1,sharex='col',sharey='row',figsize=(15,10))
fig.suptitle ('45352')

ax0 = axes[0]
ax0.plot(p_I_time_3,p_I_data_3,label='Ip')
ax0.legend(loc='left')
ax0.set_xlim([0.4,0.7])
ax0.set_ylim([500,700])
ax0.axvline(0.482,linestyle='--',color='g')
ax0.axvline(0.6107,linestyle='--',color='r')

ax1 = axes[1]
ax1.plot(ne_3['t'],ne_3['data'],label='ne')
ax1.legend(loc='left')
#ax1.set_ylim([500,700])
ax1.axvline(0.482,linestyle='--',color='g')
ax1.axvline(0.6107,linestyle='--',color='r')

ax2 = axes[2]
ax2.plot(W_time_3,W_data_3,label='W')
ax2.legend(loc='left')
#ax2.set_ylim([500,700])
ax2.axvline(0.482,linestyle='--',color='g')
ax2.axvline(0.6107,linestyle='--',color='r')

ax3 = axes[3]
ax3.plot(T_e_core_time_3,T_e_core_data_3,label='Te_core')
ax3.legend(loc='left')
ax3.set_ylim([0,1200])
ax3.axvline(0.482,linestyle='--',color='g')
ax3.axvline(0.6107,linestyle='--',color='r')

ax4 = axes[4]
ax4.plot(D_a_time_3,D_a_data_3,label='Da')
ax4.legend(loc='left')
#ax4.set_ylim([500,700])
ax4.axvline(0.482,linestyle='--',color='g')
ax4.axvline(0.6107,linestyle='--',color='r')

ax5 = axes[5]
ax5.plot(B_3.time.data,B_3.data,label='Bt')
ax5.legend(loc='left')
#ax5.set_ylim([500,700])
ax5.axvline(0.482,linestyle='--',color='g')
ax5.axvline(0.6107,linestyle='--',color='r')

ax6 = axes[6]
ax6.plot(Poh_3['t'],Poh_3['pohm'],label='Poh')
ax6.plot(Pnbi_3_time,Pnbi_3,label='Pnbi')
ax6.plot(PL_3_time,PL_3,label='Ploss')
ax6.legend(loc='left')
ax6.set_ylim([0,2e6])
ax6.axvline(0.482,linestyle='--',color='g')
ax6.axvline(0.6107,linestyle='--',color='r')
ax6.set_xlabel('t (s)')
