import math
import gym
from gym import spaces, logger, utils, error
from gym.utils import seeding
import numpy as np
from .benefits import Benefits
import random

class BenefitsUC(Benefits):
    """
    Description:
        Universal Credit a la Asmo Maanselkä
        Only for year 2022, for now

    Source:
        Antti Tanskanen, 9.5.2023

    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.ansiopvraha_kesto400=350/(12*21.5) # lyhennetty 50 pv
        #self.ansiopvraha_kesto300=250/(12*21.5)   
        #self.toe_vaatimus=1.0 # työssäoloehto väh 12kk   
        #self.porrastus=True
        self.muuta_ansiopv_ylaraja=True
        self.muuta_pvhoito=True
        self.muuta_toimeentulotuki=True
        self.muuta_asumistuki=True
        self.year=2022
        print('Universal Credit')
        self.set_year(self.year)
        
    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_UC()

    def setup_UC(self):
        self.asumistuki=self.asumistukiUC2022
        self.paivahoitomenot=self.paivahoitomenot2022

    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.50):
        #if kesto<=0.25:
        #    return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.5)
        #else:

        # first version
        return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,0,muutmenot,p,omavastuuprosentti=1.0)
     
    def asumistuki2018(self,palkkatulot,muuttulot,vuokra,p,debug=False):
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        # e/kk    IIII kuntaryhmä,
        # e/kk
        # 1    508    492    411    362
        # 2    735    706    600    527
        # 3    937    890    761    675
        # 4    1095    1038    901    804
        # + lisähenkilöä kohden, e/kk
        # 
        # 137    130    123    118
        # enimmaismenot kuntaryhmittain kun hloita 1-4
        
        if self.muuta_asumistuki:
            max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
            max_lisa=np.array([137, 130, 123, 118])
            # kuntaryhma=3

            max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

            prosentti=0.7 # vastaa 70 %
            suojaosa=300*p['aikuisia']
            #perusomavastuu=max(0,0.42*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
            #perusomavastuu=max(0,0.5*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(500+100*p['aikuisia']+275*p['lapsia'])))
            perusomavastuu=max(0,0.5*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
            if perusomavastuu<10:
                perusomavastuu=0
            
            tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
        
            if debug:
                print('palkka {:.1f} muuttulot {:.1f} perusomavastuu {:.1f} vuokra {:.1f} max_meno {:.1f} tuki {:.1f}'.format(palkkatulot,muuttulot,perusomavastuu,vuokra,max_meno,tuki))
    
            return tuki
        else:
            return super().asumistuki2018(palkkatulot,muuttulot,vuokra,p)
     
    def asumistuki2021(self,palkkatulot,muuttulot,vuokra,p,debug=False):
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        # e/kk    IIII kuntaryhmä,
        # e/kk
        # 1    508    492    411    362
        # 2    735    706    600    527
        # 3    937    890    761    675
        # 4    1095    1038    901    804
        # + lisähenkilöä kohden, e/kk
        # 
        # 137    130    123    118
        # enimmaismenot kuntaryhmittain kun hloita 1-4
        
        if self.muuta_asumistuki:
            max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
            max_lisa=np.array([137, 130, 123, 118])
            # kuntaryhma=3

            max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

            prosentti=0.7 # vastaa 70 %
            suojaosa=300*p['aikuisia']
            #perusomavastuu=max(0,0.42*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
            #perusomavastuu=max(0,0.5*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(500+100*p['aikuisia']+275*p['lapsia'])))
            perusomavastuu=max(0,0.5*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
            if perusomavastuu<10:
                perusomavastuu=0
            
            tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
        
            if debug:
                print('palkka {:.1f} muuttulot {:.1f} perusomavastuu {:.1f} vuokra {:.1f} max_meno {:.1f} tuki {:.1f}'.format(palkkatulot,muuttulot,perusomavastuu,vuokra,max_meno,tuki))
    
            return tuki
        else:
            return super().asumistuki2018(palkkatulot,muuttulot,vuokra,p)
        

    def asumistukiUC2022(self,palkkatulot,muuttulot,vuokra,p):
        # Universal Credit

        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        # e/kk    IIII kuntaryhmä,
        # e/kk
        # 1    508    492    411    362
        # 2    735    706    600    527
        # 3    937    890    761    675
        # 4    1095    1038    901    804
        # + lisähenkilöä kohden, e/kk
        # 
        # 137    130    123    118
        # enimmaismenot kuntaryhmittain kun hloita 1-4
        max_menot=np.array([[537, 520, 413, 364],[778, 746, 602, 530],[990, 941, 764, 678],[1157, 1097, 906, 808]])
        max_lisa=np.array([144, 137, 124, 119])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.7 # vastaa 80 %
        suojaosa=300*p['aikuisia']
        perusomavastuu=max(0,0.5*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(619+103*p['aikuisia']+228*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
        if p['aikuisia']==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and p['lapsia']==0:
            perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<15:
            tuki=0
    
        return tuki
