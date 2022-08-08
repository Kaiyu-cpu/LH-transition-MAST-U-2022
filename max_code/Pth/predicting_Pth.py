import pandas as pd
from scipy import interpolate

def main():

    transition_data = pd.read_excel('../../data/transition_data.xlsx',index_col='Shot Number')

    for shot in transition_data.index:

        LH = transition_data.at[shot,'LH']
        HL = transition_data.at[shot,'HL']

        psol = pd.read_csv(f'../../data/time_trace_data/psol{int(shot)}.csv',index_col='t')
        ne_bar = pd.read_csv(f'../../data/time_trace_data/ne_bar{int(shot)}.csv',index_col='t')

        pth = interpolate.interp1d(psol.index,psol.psol.values)
        pth_rad = interpolate.interp1d(psol.index,psol.prad_core.values)
        ne = interpolate.interp1d(ne_bar.index,ne_bar.data.values)

        for t,mode in zip([LH,HL],['LH','HL']):
            transition_data.at[shot,'Pth_'+mode] = (pth(t) + pth_rad(t))*1e-6
            transition_data.at[shot,'Pth_'+mode+'_rad'] = (pth(t))*1e-6
            transition_data.at[shot,'ne_'+mode] = ne(t)

    writer = pd.ExcelWriter('../../data/transition_data.xlsx',engine='xlsxwriter')
    transition_data.to_excel(writer,sheet_name='MAST-U_transitions',index=True)  

    writer.save()

if __name__ == '__main__':
    main()
