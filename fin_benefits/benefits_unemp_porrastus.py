import math
import gym
from gym import spaces, logger, utils, error
from gym.utils import seeding
import numpy as np
from .benefits import Benefits
import random

class BenefitsPorrastus(Benefits):
    """
    Description:
        Reduces unemployment benefit in steps

    Source:
        AT

    """
    def __init__(self,**kwargs):
        self.porrastus=True
        self.porrasta_putki=True
        super().__init__(**kwargs)
        if 'kwargs' in kwargs:
            kwarg=kwargs['kwargs']
        else:
            kwarg={}
        for key, value in kwarg.items():
            if key=='porrasta_putki':
                if value is not None:
                    self.porrasta_putki=value        
    
    def ansiopaivaraha2018(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0):
        if tyoton>0:
            # porrastetaan ansio-osa keston mukaan
            if self.porrastus:
                if kesto<3*21.5:
                    kerroin=1.05 # 1.05
                elif kesto<6*21.5:
                    kerroin=0.95 # 0.95
                elif kesto>=400 and not self.porrasta_putki:
                    kerroin=1.0
                else:
                    kerroin=0.85 # 0.85
            else:
                kerroin=1.0
        else:
            kerroin=0.0
            
        #print('kesto {} kerroin {}'.format(kesto,kerroin))

        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha2018(tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=kerroin)