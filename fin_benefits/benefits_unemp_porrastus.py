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
        self.porrasta_1askel=True
        self.porrasta_2askel=True
        self.porrasta_3askel=True
        self.porrasta_1porras=3*21.5
        self.porrasta_2porras=6*21.5
        super().__init__(**kwargs)
        if 'kwargs' in kwargs:
            kwarg=kwargs['kwargs']
        else:
            kwarg={}
        for key, value in kwarg.items():
            if key=='porrasta_putki':
                if value is not None:
                    self.porrasta_putki=value        
            if key=='porrasta_1askel':
                if value is not None:
                    self.porrasta_1askel=value        
            if key=='porrasta_2askel':
                if value is not None:
                    self.porrasta_2askel=value        
            if key=='porrasta_3askel':
                if value is not None:
                    self.porrasta_3askel=value        
            if key=='porrasta_1porras':
                if value is not None:
                    self.porrasta_1porras=value        
            if key=='porrasta_2porras':
                if value is not None:
                    self.porrasta_2porras=value        
    
    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0):
        if tyoton>0:
            # porrastetaan ansio-osa keston mukaan
            if self.porrastus:
                if kesto<self.porrasta_1porras:
                    if self.porrasta_1askel:
                        kerroin=1.05 # 1.05
                    else:
                        kerroin=1.0
                elif kesto<self.porrasta_2porras:
                    if self.porrasta_2askel:
                        kerroin=0.95 # 0.95
                    else:
                        kerroin=1.0
                elif kesto>=400 and not self.porrasta_putki:
                    kerroin=1.0
                else:
                    if self.porrasta_3askel:
                        kerroin=0.85 # 0.85
                    else:
                        kerroin=1.0
            else:
                kerroin=1.0
        else:
            kerroin=0.0
            
        #print('kesto {} kerroin {}'.format(kesto,kerroin))

        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha(tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=kerroin)