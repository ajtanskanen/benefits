import math
import gym
from gym import spaces, logger, utils, error
from gym.utils import seeding
import numpy as np
from .benefits import Benefits
import random

class BenefitsPuoliväliriihi2025(Benefits):
    """
    Description:
        Changes to unemployment benefits in the EK model

    Source:
        AT

    """
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.porrastus=True
        self.set_year(self.year)

        print(f'Puoliväliriihi 2025 BENEFITS (year {self.year})')

    def set_year(self,vuosi):
        super().set_year(vuosi)
        if self.year in set([2024,2026]):
            self.setup_puoliväliriihi()
            if self.year==2024:
                self.veroparam2024_puoliväliriihi()
            elif self.year==2026:
                self.veroparam2026_puoliväliriihi()
        else:
            print('puoliväliriihi, unknown year',vuosi)

    def setup_puoliväliriihi(self):
        '''
        korvataan benefits-modulissa olevat rutiinit
        '''
        if self.year==2024:
            self.tyotulovahennys = self.tyotulovahennys2024_puoliväliriihi
            #self.valtionvero_asteikko = self.valtionvero_asteikko_2024_puoliväliriihi
            #self.valtionvero_asteikko_2024 = self.valtionvero_asteikko_2024_puoliväliriihi
            self.veroparam = self.veroparam2024_puoliväliriihi
            self.laske_tyotulovahennys = self.laske_tyotulovahennys2024_puoliväliriihi
        else:
            self.tyotulovahennys = self.tyotulovahennys2026_puoliväliriihi
            #self.valtionvero_asteikko = self.valtionvero_asteikko_2024_puoliväliriihi
            #self.valtionvero_asteikko_2024 = self.valtionvero_asteikko_2024_puoliväliriihi
            self.veroparam = self.veroparam2026_puoliväliriihi
            self.laske_tyotulovahennys = self.laske_tyotulovahennys2026_puoliväliriihi
            self.raippavero = self.raippavero2026

    def veroparam2024_puoliväliriihi(self):
        '''
        Päivitetty 2.5.2025
        '''
        super().veroparam2024()

    def tyotulovahennys2024_puoliväliriihi(self,ika: float,lapsia: int):
        if ika>=65:
            max_tyotulovahennys=3340/self.kk_jakaja
        else:
            max_tyotulovahennys=2140/self.kk_jakaja
        ttulorajat=np.array([0,23420,71900])/self.kk_jakaja
        ttulopros=np.array([0.13,0.0203,0.121])
        return max_tyotulovahennys,ttulorajat,ttulopros
               
    def laske_tyotulovahennys2024_puoliväliriihi(self,puhdas_ansiotulo: float,palkkatulot_puhdas: float,ika: float,lapsia: float):
        '''
        Vuosille 2023-
        '''
        max_tyotulovahennys,ttulorajat,ttulopros = self.tyotulovahennys2024_puoliväliriihi(puhdas_ansiotulo,palkkatulot_puhdas,ika,lapsia)
    
        tyotulovahennys = min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot_puhdas-ttulorajat[0])))
        tyotulovahennys = max(0,tyotulovahennys-ttulopros[1]*max(0,min(ttulorajat[2],puhdas_ansiotulo)-ttulorajat[1]))    
        #tyotulovahennys = max(0,tyotulovahennys-ttulopros[1]*max(0,min(ttulorajat[2],puhdas_ansiotulo)-ttulorajat[1])-ttulopros[2]*max(0,puhdas_ansiotulo-ttulorajat[2]))    
                
        return tyotulovahennys
    
    def raippavero2026(self,elaketulo: float):
        alaraja=57_000/self.kk_jakaja
        pros=0.0400
        vero=max(elaketulo-alaraja,0)*pros
        return vero

    def veroparam2026_puoliväliriihi(self):
        '''
        Päivitetty 2.5.2025
        '''
        super().veroparam2026()

    def tyotulovahennys2026_puoliväliriihi(self,ika: float,lapsia: int,yksinhuoltaja: int=0):
        max_tyotulovahennys=(3_385+105*lapsia+105*yksinhuoltaja+45)/self.kk_jakaja
        ttulorajat=np.array([0,35_000+450,50_000])/self.kk_jakaja
        ttulopros=np.array([0.18,0.020,0.0])
        return max_tyotulovahennys,ttulorajat,ttulopros
               
    def laske_tyotulovahennys2026_puoliväliriihi(self,puhdas_ansiotulo: float,palkkatulot_puhdas: float,ika: float,lapsia: int,yksinhuoltaja: int=0):
        '''
        Vuosille 2023-
        '''
        max_tyotulovahennys,ttulorajat,ttulopros = self.tyotulovahennys2026_puoliväliriihi(ika,lapsia,yksinhuoltaja)
    
        tyotulovahennys = min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot_puhdas-ttulorajat[0])))
        tyotulovahennys = max(0,tyotulovahennys-ttulopros[1]*max(0,min(ttulorajat[2],puhdas_ansiotulo)-ttulorajat[1]))    
        #tyotulovahennys = max(0,tyotulovahennys-ttulopros[1]*max(0,min(ttulorajat[2],puhdas_ansiotulo)-ttulorajat[1])-ttulopros[2]*max(0,puhdas_ansiotulo-ttulorajat[2]))    
                
        return tyotulovahennys    