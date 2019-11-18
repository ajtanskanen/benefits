import math
import gym
from gym import spaces, logger, utils, error
from gym.utils import seeding
import numpy as np
import fin_benefits
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
        self.muuta_ansiopv_ylaraja=True
        self.ansiopvraha_kesto400=350/(12*21.5) # lyhennetty 50 pv
        self.ansiopvraha_kesto300=250/(12*21.5)   
        self.toe_vaatimus=1.0 # työssäoloehto väh 12kk   
        self.porrastus=True
        self.muuta_ansiopv_ylaraja=True
        self.muuta_pvhoito=True                  

    def paivahoitomenot(self,hoidossa,tulot,p):
        if self.muuta_pvhoito:
            # kutsutaan alkuperäistä funktiota eri maksuprosentilla
            return super().paivahoitomenot(hoidossa,tulot,p,prosentti1=0.08)
        else:
            return super().paivahoitomenot(hoidossa,tulot,p)
    
    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0):
        if tyoton>0:
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
        else:
            kerroin=0.0

        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha(tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=kerroin)

    # yläraja 80% ansionalenemasta
    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka):
        if self.muuta_ansiopv_ylaraja:
            return min(ansiopaivarahamaara,0.8*max(0,vakiintunutpalkka-tyotaikaisettulot))   
        else:
            return super().ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka)        
     
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.07):
        return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=omavastuuprosentti)
     
    #def tyotulovahennys(self):
    #    max_tyotulovahennys=3000/self.kk_jakaja
    #    ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
    #    ttulopros=np.array([0.120,0.0165,0])
    #    return max_tyotulovahennys,ttulorajat,ttulopros