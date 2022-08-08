import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():

    transition_data = pd.read_excel('../../data/transition_data.xlsx',index_col='Shot Number')
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    for shot in transition_data.index:

        current = transition_data.at[shot,'Ip']
        LH = transition_data.at[shot,'LH']
        HL = transition_data.at[shot,'HL']
        xlim = (transition_data.at[shot,'start'],transition_data.at[shot,'end'])
        powlim = (transition_data.at[shot,'powlimStart'],transition_data.at[shot,'powlimEnd'])
        set = transition_data.at[shot,'SET']
        divertor = transition_data.at[shot,'Divertor']
        
        f,axes = plt.subplots(7, 1, sharex=True, figsize=(16,7), gridspec_kw={'height_ratios': [1,1,1,1,1,1,2]})
        plt.setp(axes, xlim=xlim)

        axes[0].annotate('$I_p [kA]$', xy=(0.005,0.71),xycoords='axes fraction',fontsize=9,color=colors[0])
        axes[1].annotate('$n_e [10^{19}m^{-3}]$', xy=(0.005,0.71),xycoords='axes fraction',fontsize=9,color=colors[0])
        axes[2].annotate(r'$\dfrac{dw}{dt} [MW]$', xy=(0.005,0.21),xycoords='axes fraction',fontsize=9,color=colors[0])
        axes[3].annotate('$T_e [keV]$', xy=(0.005,0.71),xycoords='axes fraction',fontsize=9,color=colors[0])
        axes[4].annotate(r'$D_{\alpha} [V]$', xy=(0.005,0.71),xycoords='axes fraction',fontsize=9,color=colors[0])
        axes[5].annotate('$B_T [T]$', xy=(0.005,0.71),xycoords='axes fraction',fontsize=9,color=colors[0])
        axes[6].annotate('$P_{loss} [MW]$', xy=(0.005,0.47),xycoords='axes fraction',fontsize=9,color=colors[0])
        axes[6].annotate('$P_{OHM} [MW]$', xy=(0.005,0.35),xycoords='axes fraction',fontsize=9,color=colors[1])
        axes[6].annotate('$P_{NBI} [MW]$', xy=(0.005,0.59),xycoords='axes fraction',fontsize=9,color=colors[2])
        axes[6].annotate('$P_{radiation} [MW]$', xy=(0.005,0.71),xycoords='axes fraction',fontsize=9,color=colors[3])


        timeTrace = pd.read_csv(f'../../data/time_trace_data/traces{int(shot)}.csv')
        psol = pd.read_csv(f'../../data/time_trace_data/psol{int(shot)}.csv')

        axes[0].set_title(f'{divertor} configuration - shot #{int(shot)}',fontweight='bold')
        axes[6].set_xlabel('Time [s]')

        axes[0].plot(timeTrace['IpTime'],timeTrace['Ip'])
        axes[0].set_ylim((current)-100,(current)+100)
        axes[1].plot(timeTrace['neCoreTime'],timeTrace['neCore']*1e-20)
        axes[2].plot(psol['t'],psol['pdw_dt']*1e-6)
        axes[3].plot(timeTrace['TeCoreTime'], timeTrace['TeCore']*1e-3)
        axes[4].plot(timeTrace['DalphaSPTime'], timeTrace['DalphaSP'])
        axes[4].set_ylim(0,12)
        axes[5].plot(timeTrace['BtTime'], timeTrace['Bt'],label='Bt [T]')
        axes[5].set_ylim(-0.65,-0.45)
        axes[6].plot(psol['t'],psol['psol']*1e-6)
        axes[6].plot(psol['t'],psol['pohm']*1e-6)
        axes[6].plot(psol['t'],(psol['pss']+psol['psw'])*1e-6)
        axes[6].plot(psol['t'],psol['prad_core']*1e-6)
        axes[6].set_ylim(powlim)

        for ax in axes:
            ax.axvline(LH, color='tab:green', linestyle='--')
            ax.axvline(HL, color='tab:red', linestyle='--')

        f.savefig(f'./figures/timeTrace{int(shot)}_{set}.png')

if __name__ == '__main__':
    main()