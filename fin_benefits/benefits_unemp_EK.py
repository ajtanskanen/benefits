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
        self.year=2022
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
        if self.porrastus:
            if kesto>6*25:
                kerroin=0.85
            elif kesto>3*25:
                kerroin=0.95
            else:
                kerroin=1.00
        else:
            kerroin=1.00
            
        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha(tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=kerroin,omavastuukerroin=omavastuukerroin,alku=alku)

    # yläraja 80% ansionalenemasta
    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,peruspvraha):
        if self.muuta_ansiopv_ylaraja:
            perus=self.peruspaivaraha(0) 
            ansiopv = peruspvraha+max(0,min(ansiopaivarahamaara-peruspvraha,0.8*(vakiintunutpalkka-peruspvraha-tyotaikaisettulot)))
            #ansiopv = peruspvraha+max(0,min(ansiopaivarahamaara-peruspvraha,0.8*(vakpalkka-peruspvraha-tyotaikaisettulot)))
        
            if ansiopv<20:
                ansiopv=0
                
            return ansiopv
        
            #if ansiopaivarahamaara>peruspvraha:
            #    return peruspvraha+min(ansiopaivarahamaara-peruspvraha,0.8*max(0,vakiintunutpalkka-peruspvraha))   
            #else:
            #    return peruspvraha
        else:
            return super().ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,peruspvraha)
     
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.10):
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

    #def tyotulovahennys(self):
    #    max_tyotulovahennys=3000/self.kk_jakaja
    #    ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
    #    ttulopros=np.array([0.120,0.0165,0])
    #    return max_tyotulovahennys,ttulorajat,ttulopros
    
    def paivahoitomenot2022(self,hoidossa,tulot,p,prosentti1=None,prosentti2=None,prosentti3=None,maksimimaksu=None):
        '''
        Päivähoitomaksut 1.8.2021
        '''
        minimimaksu=27

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.4
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=288

        if p['lapsia']>0:
            vakea=p['lapsia']+p['aikuisia']
            if vakea==1:
                alaraja=2789
                prosentti=prosentti1
            elif vakea==2:
                alaraja=2789
                prosentti=prosentti1
            elif vakea==3:
                alaraja=3610
                prosentti=prosentti1
            elif vakea==4:
                alaraja=4099
                prosentti=prosentti1
            elif vakea==5:
                alaraja=4588
                prosentti=prosentti1
            elif vakea==6:
                alaraja=5075
                prosentti=prosentti1
            else:
                alaraja=5075+138*(vakea-6)
                prosentti=prosentti1

            pmaksu=min(maksimimaksu,max(0,tulot-alaraja)*prosentti)
            if hoidossa==0:
                kerroin=0
            elif hoidossa==1:
                if pmaksu<minimimaksu:
                    kerroin=0
                else:
                    kerroin=1
            elif hoidossa==2:
                if pmaksu<minimimaksu:
                    kerroin=0
                else:
                    if (prosentti2*pmaksu<minimimaksu):
                        kerroin=1
                    else:
                        kerroin=1+prosentti2
            else:
                if pmaksu<minimimaksu:
                    kerroin=0
                else:
                    if prosentti2*pmaksu<minimimaksu:
                        kerroin=1
                    else:
                        if (prosentti3*pmaksu<minimimaksu):
                            kerroin=1+prosentti2
                        else:
                            kerroin=1+prosentti2+prosentti3*(p['lapsia']-2)
            maksu=kerroin*pmaksu*0.8
        else:
            maksu=0
        
        return maksu                    