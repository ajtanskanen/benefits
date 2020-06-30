import math
import gym
from gym import spaces, logger, utils, error
from gym.utils import seeding
import numpy as np
from .benefits import Benefits
import random

class BenefitsKorotus(Benefits):
    """
    Description:
        Changes to unemployment benefits in the EK model

    Source:
        AT

    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.porrastus=False
        
    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0):
        ansiopvrahan_suojaosa=p['ansiopvrahan_suojaosa']
        lapsikorotus=p['ansiopvraha_lapsikorotus']
        lisakorotus=p['ansiopvraha_lisakorotus']
    
        if tyoton>0:
            if lapsikorotus<1:
                lapsia=0    

            if self.year==2018:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                sotumaksu=0.0448     # 2015 0.0428 2016 0.0460
                taite=3078.60    
            elif self.year==2019:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                sotumaksu=0.0448     # 2015 0.0428 2016 0.0460
                taite=3078.60    
            elif self.year==2020:
                lapsikorotus=np.array([0,5.28,7.76,10.00])*21.5    
                sotumaksu=0.0414     # 2015 0.0428 2016 0.0460
                taite=3197.70    
            elif self.year==2021:
                lapsikorotus=np.array([0,5.28,7.76,10.00])*21.5    
                sotumaksu=0.0414     # 2015 0.0428 2016 0.0460
                taite=3197.70    
            else:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                sotumaksu=0.0448     # 2015 0.0428 2016 0.0460
                taite=3078.60    
                            
            if (saa_ansiopaivarahaa>0): # & (kesto<400.0): # ei keston tarkastusta!
                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-sotumaksu)     
        
                if vakpalkka>taite:
                    tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus    
                else:
                    tuki2=0.45*max(0,vakpalkka-perus)+perus    

                tuki2=tuki2+lapsikorotus[min(lapsia,3)]+lisakorotus    
                tuki2=tuki2*ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)    
        
                perus=self.peruspaivaraha(lapsia)+lisakorotus     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavattulo=max(0,tyotaikaisettulot-suojaosa)    
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavattulo)  
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka)  

                tuki=ansiopaivarahamaara    
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                tuki=max(perus,tuki)     # voi tulla vastaan pienillä tasoilla4
            else:
                ansiopaivarahamaara=0    
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)+lisakorotus  
                tuki=perus    
        else:
            perus=0    
            tuki=0    
            ansiopaivarahamaara=0   

        return tuki,ansiopaivarahamaara,perus