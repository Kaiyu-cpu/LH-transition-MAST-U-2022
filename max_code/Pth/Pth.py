import matplotlib.pyplot as plt
import pandas as pd

def main():

    transition_data = pd.read_excel('../../data/transition_data.xlsx',index_col='Shot Number')

    f1,axes1 = plt.subplots(1,2)
    f2,axes2 = plt.subplots(1,2)

    conventional = transition_data.loc[(transition_data['Divertor'].values=='Conventional')]
    conventional_600 = conventional.loc[(conventional['Ip'].values==600)]
    conventional_750 = conventional.loc[(conventional['Ip'].values==750)]
    superX = transition_data.loc[(transition_data['Divertor'].values=='SUPER-X')]

    colors = ['midnightblue', 'royalblue','orangered']

    for div,col in zip([conventional_600,conventional_750,superX],colors):

        axes1[0].errorbar(div['ne_LH'].dropna().values,div['Pth_LH'].dropna().values,yerr=div['Pth_LH_SD'].dropna().values,fmt='^',color=col)
        axes1[0].errorbar(div['ne_HL'].dropna().values,div['Pth_HL'].dropna().values,yerr=div['Pth_HL_SD'].dropna().values,fmt='v',color=col,markerfacecolor='none')

        axes2[0].errorbar(div['ne_LH'].dropna().values,div['Pth_LH_rad'].dropna().values,yerr=div['Pth_LH_SD_rad'].dropna().values,fmt='^',color=col)
        axes2[0].errorbar(div['ne_HL'].dropna().values,div['Pth_HL_rad'].dropna().values,yerr=div['Pth_HL_SD_rad'].dropna().values,fmt='v',color=col,markerfacecolor='none')

        axes1[1].errorbar(div['ne_LH'].dropna().values,div['Pth_LH'].dropna().values,yerr=div['Pth_LH_SD'].dropna().values,fmt='^',color=col)

        axes2[1].errorbar(div['ne_LH'].dropna().values,div['Pth_LH_rad'].dropna().values,yerr=div['Pth_LH_SD_rad'].dropna().values,fmt='^',color=col)


    f1.savefig('./figures/Pth.png')
    f2.savefig('./figures/Pth_rad.png')


if __name__ == '__main__':
    main()
     