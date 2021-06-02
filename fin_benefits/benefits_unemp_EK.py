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
        #self.muuta_ansiopv_ylaraja=True
        #self.ansiopvraha_kesto400=350/(12*21.5) # lyhennetty 50 pv
        #self.ansiopvraha_kesto300=250/(12*21.5)   
        #self.toe_vaatimus=1.0 # työssäoloehto väh 12kk   
        self.porrastus=False
        self.muuta_ansiopv_ylaraja=False
        self.muuta_pvhoito=False
        self.muuta_toimeentulotuki=True
        self.muuta_asumistuki=True

    def paivahoitomenot(self,hoidossa,tulot,p):
        if self.muuta_pvhoito:
            # kutsutaan alkuperäistä funktiota eri maksuprosentilla
            return super().paivahoitomenot(hoidossa,tulot,p,prosentti1=0.08)
        else:
            return super().paivahoitomenot(hoidossa,tulot,p)
    
    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0,omavastuukerroin=1.0):
        # porrastetaan ansio-osa keston mukaan
        if self.porrastus:
            if kesto>6*25:
                kerroin=0.85
            elif kesto>3*25:
                kerroin=0.95
            else:
                kerroin=1.05
        else:
            kerroin=1.0
            
        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha(tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=kerroin,omavastuukerroin=omavastuukerroin)

    # yläraja 80% ansionalenemasta
    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka):
        if self.muuta_ansiopv_ylaraja:
            return min(ansiopaivarahamaara,0.8*max(0,vakiintunutpalkka-tyotaikaisettulot))   
        else:
            return super().ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka)        
     
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.07):
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
            suojaosa=300*p['aikuisia']
            perusomavastuu=max(0,0.42*(0.8*max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
            if perusomavastuu<10:
                perusomavastuu=0
            
            tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
        
            if debug:
                print('palkka {:.1f} muuttulot {:.1f} perusomavastuu {:.1f} vuokra {:.1f} max_meno {:.1f} tuki {:.1f}'.format(palkkatulot,muuttulot,perusomavastuu,vuokra,max_meno,tuki))
    
            return tuki
        else:
            return super().asumistuki2018(palkkatulot,muuttulot,vuokra,p)
        

    #def tyotulovahennys(self):
    #    max_tyotulovahennys=3000/self.kk_jakaja
    #    ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
    #    ttulopros=np.array([0.120,0.0165,0])
    #    return max_tyotulovahennys,ttulorajat,ttulopros