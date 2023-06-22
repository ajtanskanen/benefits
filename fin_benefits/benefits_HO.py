import math
import gym
from gym import spaces, logger, utils, error
from gym.utils import seeding
import numpy as np
from .benefits import Benefits
import random

class BenefitsEK(Benefits):
    """
    Description:
        Changes to unemployment benefits in the EK model

    Source:
        AT

    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        #self.ansiopvraha_kesto400=350/(12*21.5) # lyhennetty 50 pv
        #self.ansiopvraha_kesto300=250/(12*21.5)   
        #self.toe_vaatimus=1.0 # työssäoloehto väh 12kk   
        self.porrastus=True
        self.muuta_ansiopv_ylaraja=True
        self.muuta_pvhoito=True
        self.muuta_toimeentulotuki=True
        self.muuta_asumistuki=True
        self.year=2023
        self.set_year(self.year)
        
    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_EK()

    def setup_EK(self):
        self.asumistuki=self.asumistuki2022
        self.paivahoitomenot=self.paivahoitomenot2022

    #def paivahoitomenot(self,hoidossa,tulot,p):
    #    if self.muuta_pvhoito:
    #        # kutsutaan alkuperäistä funktiota eri maksuprosentilla
    #        return super().paivahoitomenot(hoidossa,tulot,p,prosentti1=0.08)
    #    else:
    #        return super().paivahoitomenot(hoidossa,tulot,p)

    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0,omavastuukerroin=1.0,alku=''):
        # porrastetaan ansio-osa keston mukaan
        # 2 kk -> 80%
        # 34 vko -> 75%
        if self.porrastus:
            if kesto>6*25:
                kerroin=0.75
            elif kesto>3*25:
                kerroin=0.80
            else:
                kerroin=1.00
        else:
            kerroin=1.00
            
        p['suojaosa_aseta_taso']=0

        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha(tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=kerroin,omavastuukerroin=omavastuukerroin,alku=alku)

    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.05):
        if self.muuta_toimeentulotuki:
            return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=omavastuuprosentti)
        else:
            return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0)
     
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
            suojaosa=0
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
        

        
    def asumistuki2022(self,palkkatulot,muuttulot,vuokra,p):
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
        suojaosa=0
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

    def asumistuki2023(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,p: dict) -> float:
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
        max_menot=np.array([[582, 563, 447, 394],[843, 808, 652, 574],[1_072, 1_019, 828, 734],[1_253, 1_188, 981, 875]])
        max_lisa=np.array([156, 148, 134, 129])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.7 
        suojaosa=0
        perusomavastuu=max(0,0.50*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(667+111*p['aikuisia']+246*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
        #if p['aikuisia']==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and p['lapsia']==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<15:
            tuki=0
    
        return tuki    

    def lapsilisa2023(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 68.3
            
        return lapsilisat