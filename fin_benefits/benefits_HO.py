import math
import gym
from gym import spaces, logger, utils, error
from gym.utils import seeding
import numpy as np
from .benefits import Benefits
import random

class BenefitsHO(Benefits):
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
        self.year=2023
        self.set_year(self.year)

        print('Hallitusohjelma 2023 BENEFITS')

    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_HO()

    def setup_HO(self):
        self.asumistuki=self.asumistuki2023
        self.tyotulovahennys=self.tyotulovahennys2023
        self.valtionvero_asteikko=self.valtionvero_asteikko_2023
        self.lapsilisa=self.lapsilisa2023
        self.veroparam=self.veroparam2023

    def veroparam2023(self):
        '''
        Päivitetty 6.5.2023
        '''
        super().veroparam2023()
        self.tyottomyysvakuutusmaksu=0.0150 - 0.002 # vastaa VM:n arviota rakenteellisesta maksun muutoksesta 

    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0,omavastuukerroin=1.0,alku=''):
        # porrastetaan ansio-osa keston mukaan
        # 2 kk -> 80%
        # 34 vko -> 75%
        if self.porrastus:
            if kesto>34/52*12*21.5:
                kerroin=0.75
            elif kesto>2*21.5:
                kerroin=0.80
            else:
                kerroin=1.00 # =1-2/3/21.5
        else:
            if kesto<3*21.5:
                kerroin=1.00 # =1-2/3/21.5
            else:
                kerroin=1.00 # =1-2/3/21.5
            
        p2=p.copy()

        p2['tyottomyysturva_suojaosa_taso']=0
        p2['ansiopvrahan_suojaosa']=0
        p2['ansiopvraha_lapsikorotus']=0

        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha(tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p2,ansiokerroin=kerroin,omavastuukerroin=omavastuukerroin,alku=alku)

    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,aikuisia,lapsia,kuntaryhma,p,omavastuuprosentti=0.05):
        return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,aikuisia,lapsia,kuntaryhma,p,omavastuuprosentti=omavastuuprosentti)

    def asumistuki2023(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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
        max_menot=np.array([[563, 563, 447, 394],[808, 808, 652, 574],[1_019, 1_019, 828, 734],[1_188, 1_188, 981, 875]])
        max_lisa=np.array([148, 148, 134, 129])

        # kuntaryhma=3
        max_menot[:,0]=max_menot[:,1]
        max_lisa[0]=max_lisa[1]

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.7 # vastaa 80 %
        suojaosa=0 #p['asumistuki_suojaosa']*p['aikuisia']
        lapsiparam=246 # FIXME 270?
        perusomavastuu=max(0,0.50*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(667+111*aikuisia+lapsiparam*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if p['aikuisia']==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and p['lapsia']==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<30:
            tuki=0
    
        return tuki    

    def valtionvero_asteikko_2023(self):
        rajat=np.array([0,19_900,29_700,49_000,150_000])/self.kk_jakaja
        pros=(1-100/20000)*np.maximum(0,np.array([0.1264,0.19,0.3025,0.34,0.44+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.44+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros

    def lapsilisa2023(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69]) + 2.0
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 68.3 + 10.0
            
        return lapsilisat

    #def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara: float,tyotaikaisettulot: float,vakpalkka: float,vakiintunutpalkka: float,peruspvraha: float) -> float:
    #    if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
    #        return max(0,vakpalkka-tyotaikaisettulot) 
    #       
    #    return ansiopaivarahamaara 

    def tyotulovahennys2023(self,ika: float,lapsia: int):
        if ika>=65:
            max_tyotulovahennys=3230/self.kk_jakaja
        else:
            max_tyotulovahennys=2030/self.kk_jakaja
        ttulorajat=np.array([0,22000,77000])/self.kk_jakaja # 127000??
        ttulopros=np.array([0.13,0.0203,0.121])
        return max_tyotulovahennys,ttulorajat,ttulopros
  