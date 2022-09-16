"""

    benefits
    
    implements universal basic income on top of benefits module


    - pitääkö asumistuen suojaosa olla 300 e/kk vai 600 e/kk?? Nyt 600 e/kk.

"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite
from .labels import Labels
from .ben_utils import print_q
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
from .benefits import Benefits

class BasicIncomeBenefits(Benefits):
    """
    Description:
        The Finnish Earnings-related Social Security

    Source:
        AT

    """
    
    def __init__(self,**kwargs):
        self.year=2018
        self.additional_income_tax=0.0
        self.additional_tyel_premium=0.0
        self.additional_kunnallisvero=0.0
        self.additional_income_tax_high=0.0
        self.additional_vat=0.0
        self.extra_ppr_factor=1.0 # kerroin peruspäivärahalle
        self.language='Finnish' # 'English'
        self.use_extra_ppr=False
        self.vaihtuva_tyelmaksu=False
        self.tyel_perusvuosi=1970 # ikäluokan syntymävuosi
        self.irr_vain_tyoelake=False
        self.include_perustulo=True
        self.perustulomalli='Sotu'
        
        self.osittainen_perustulo=True
        self.perustulo_korvaa_toimeentulotuen=False
        
        if 'kwargs' in kwargs:
            kwarg=kwargs['kwargs']
        else:
            kwarg=kwargs
            
        for key, value in kwarg.items():
            if key=='year':
                if value is not None:
                    self.year=value
            elif key=='language': # language for plotting
                if value is not None:
                    self.language=value        
            elif key=='perustulomalli':
                if value is not None:
                    self.perustulomalli=value
            elif key=='osittainen_perustulo':
                if value is not None:
                    self.osittainen_perustulo=value
            elif key=='valtionverotaso':
                if value is not None:
                    self.valtionverotaso=value
            elif key=='perustulo_asetettava':
                if value is not None:
                    self.perustulo_asetettava=value
            elif key=='perustulo_kela_asetettava':
                if value is not None:
                    self.perustulo_asetettava=value
                    self.valtionverotaso=self.Kela_kustannusneutraali_veroaste(value)
            elif key=='perustulo_korvaa_toimeentulotuen':
                if value is not None:
                    self.perustulo_korvaa_toimeentulotuen=value
                    
        print(f'UBI-model {self.perustulomalli}\nPartial UBI {self.osittainen_perustulo}\nperustulo_korvaa_toimeentulotuen {self.perustulo_korvaa_toimeentulotuen}')
                    
        super().__init__(**kwargs)
        self.setup_basic_income()
    
        # choose the correct set of benefit functions for computations
        self.set_year(self.year)
        self.lab=Labels()
        self.labels=self.lab.ben_labels(self.language)
        
        if self.vaihtuva_tyelmaksu:
            self.get_tyelpremium()
            
        
    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_basic_income()
        
    def veroparam2018_perustulokokeilu(self):
        super().veroparam2018()

    def veroparam2018_perustulo(self):
        super().veroparam2018()
        self.kunnallisvero_pros=0.0    
        
    def veroparam2018_perustulo_sotu(self):
        super().veroparam2018()
        
    def veroparam2019_perustulokokeilu(self):
        super().veroparam2018()

    def veroparam2019_perustulo(self):
        super().veroparam2018()
        self.kunnallisvero_pros=0.0    

    def veroparam2020_perustulokokeilu(self):
        super().veroparam2018()

    def veroparam2020_perustulo(self):
        super().veroparam2018()
        self.kunnallisvero_pros=0.0    

    def veroparam2021_perustulokokeilu(self):
        super().veroparam2018()

    def veroparam2021_perustulo(self):
        super().veroparam2018()
        self.kunnallisvero_pros=0.0    

    def veroparam2022_perustulokokeilu(self):
        super().veroparam2018()

    def veroparam2022_perustulo(self):
        super().veroparam2018()
        self.kunnallisvero_pros=0.0    

    def veroparam2022_perustulo_sotu(self):
        super().veroparam2022()

    def veroparam2018_perustulo_sotu(self):
        super().veroparam2018()

    def setup_basic_income(self):
        self.nyky_soviteltu_peruspaivaraha=super().soviteltu_peruspaivaraha
        self.laske_perustulovero=self.laske_perustulovero_perus
        if self.year==2018:
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018_perustulo
            self.nykyperuspaivaraha=super().peruspaivaraha2018
        elif self.year==2019:
            self.veroparam2018=self.veroparam2019_perustulo
            self.veroparam=self.veroparam2019_perustulo
            self.nykyperuspaivaraha=super().peruspaivaraha2019
        elif self.year==2020:
            self.veroparam2018=self.veroparam2020_perustulo
            self.veroparam=self.veroparam2020_perustulo
            self.nykyperuspaivaraha=super().peruspaivaraha2020
        elif self.year==2021:
            self.veroparam2018=self.veroparam2021_perustulo
            self.veroparam=self.veroparam2021_perustulo
            self.nykyperuspaivaraha=super().peruspaivaraha2021
        elif self.year==2022:
            self.veroparam2018=self.veroparam202_perustulo
            self.veroparam=self.veroparam2022_perustulo
            self.nykyperuspaivaraha=super().peruspaivaraha2022
        elif self.year==2023:
            self.veroparam2018=self.veroparam2023_perustulo
            self.veroparam=self.veroparam2023_perustulo
            self.nykyperuspaivaraha=super().peruspaivaraha2023
    
        if self.perustulomalli=='perustulokokeilu':
            # Kela-malli
            self.perustulo=self.laske_perustulo_Kelamalli
            self.asumistuen_suojaosa=600
            #self.max_tyotulovahennys=1540
            #self.max_perusvahennys=3020
            #self.max_ansiotulovahennys=3570
            self.valtionvero_asteikko=self.valtionvero_asteikko_2018
            self.verotus=super().verotus
            self.veroparam2018=self.veroparam2018_perustulokokeilu
            self.veroparam=self.veroparam2018            
            # ei muutosta verotukseen, ei aktiivimallia toteutettuna
        elif self.perustulomalli=='Kela':
            # Kela-malli
            self.perustulo=self.laske_perustulo_Kelamalli
            self.asumistuen_suojaosa=600
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018            
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_Kela
        elif self.perustulomalli=='BI':
            # Artikkelin BI-malli
            self.perustulo=self.laske_perustulo_BI
            self.asumistuen_suojaosa=600
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018            
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_BI
        elif self.perustulomalli in set(['vasemmistoliitto','Vasemmistoliitto']):        
            # Vasemmistoliitto
            self.perustulo=self.laske_perustulo_vasemmistoliitto
            self.asumistuen_suojaosa=600
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018            
            #self.max_ansiotulovahennys=0
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_vasemmistoliitto
        elif self.perustulomalli in set(['sotu','Sotu','SOTU']):        
            # Sotu-komiten perustulomalli
            self.perustulo=self.laske_perustulo_sotu
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            if self.year==2018:
                self.veroparam=super().veroparam2018
                self.valtionvero_asteikko=super().valtionvero_asteikko_2018
            elif self.year==2019:
                self.veroparam=super().veroparam2019
                self.valtionvero_asteikko=super().valtionvero_asteikko_2019
            elif self.year==2020:
                self.veroparam=super().veroparam2020
                self.valtionvero_asteikko=super().valtionvero_asteikko_2020
            elif self.year==2021:
                self.veroparam=super().veroparam2021
                self.valtionvero_asteikko=super().valtionvero_asteikko_2021
            elif self.year==2022:
                self.veroparam=super().veroparam2022
                self.valtionvero_asteikko=super().valtionvero_asteikko_2022
            elif self.year==2023:
                self.veroparam=super().veroparam2023
                self.valtionvero_asteikko=super().valtionvero_asteikko_2023
            self.laske_perustulovero=self.laske_perustulovero_sotu
        elif self.perustulomalli in set(['sotu_matala','Sotu_matala','SOTU_matala','sotu matala','Sotu matala','SOTU matala']):        
            # matala perustulo sotu-komitean malli
            self.perustulo=self.laske_perustulo_sotu_matala
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2022=self.veroparam2022_perustulo_sotu
            if self.year==2018:
                self.veroparam=super().veroparam2018
                self.valtionvero_asteikko=super().valtionvero_asteikko_2018
            elif self.year==2019:
                self.veroparam=super().veroparam2019
                self.valtionvero_asteikko=super().valtionvero_asteikko_2019
            elif self.year==2020:
                self.veroparam=super().veroparam2020
                self.valtionvero_asteikko=super().valtionvero_asteikko_2020
            elif self.year==2021:
                self.veroparam=super().veroparam2021
                self.valtionvero_asteikko=super().valtionvero_asteikko_2021
            elif self.year==2022:
                self.veroparam=super().veroparam2022
                self.valtionvero_asteikko=super().valtionvero_asteikko_2022
            elif self.year==2023:
                self.veroparam=super().veroparam2023
                self.valtionvero_asteikko=super().valtionvero_asteikko_2023
            self.laske_perustulovero=self.laske_perustulovero_sotu_matala
        elif self.perustulomalli in set (['asetettava']):
            # asetettava
            self.perustulo=self.laske_perustulo_asetettava
            self.asumistuen_suojaosa=600
            #self.perustulo_asetettava=
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018            
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_asetettava
            self.peruspaivaraha=self.peruspaivaraha_bi
        elif self.perustulomalli in set (['kela_asetettava']):
            # asetettava
            self.perustulo=self.laske_perustulo_asetettava
            self.asumistuen_suojaosa=600
            #self.perustulo_asetettava=
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018            
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_asetettava
            self.peruspaivaraha=self.peruspaivaraha_bi
        elif self.perustulomalli in set (['vihreat','Vihreät','vihreät','Vihreat']):
            # Vihreiden malli
            self.perustulo=self.laske_perustulo_vihreat
            self.asumistuen_suojaosa=600
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018            
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_vihreat
            self.peruspaivaraha=self.peruspaivaraha_bi
        elif self.perustulomalli=='tonni':        
            # Tonnin täysi perustulo
            self.perustulo=self.laske_perustulo_tonni
            self.asumistuen_suojaosa=600
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.veroparam2018=self.veroparam2018_perustulo
            self.veroparam=self.veroparam2018            
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_tonni
            self.peruspaivaraha=self.peruspaivaraha_bi
        elif self.perustulomalli=='puolitoista':        
            # Tonnin täysi perustulo
            self.perustulo=self.laske_perustulo_puolitoista
            self.asumistuen_suojaosa=600
            self.ansiotulovahennys=self.ansiotulovahennys_perustulo_sotu
            self.tyotulovahennys=self.tyotulovahennys_perustulo_sotu
            self.valtionvero_asteikko=self.valtionvero_asteikko_perustulo_1500
            self.peruspaivaraha=self.peruspaivaraha_bi
        else:
            print('basic_income: unknown basic income model',self.perustulomalli)
        
    def laske_perustulo_Kelamalli(self):
        return 560.0
        
    def laske_perustulo_BI(self):
        '''
        Artikkelia varten
        '''
        return 600.0
        
    def laske_perustulo_tm(self):
        return 660
        
    def laske_perustulo_vihreat(self):
        return 600

    def laske_perustulo_asetettava(self):
        return self.perustulo_asetettava
        
    def laske_perustulo_696(self):
        return 696.6
        
    def laske_perustulo_vasemmistoliitto(self):
        return 800.0
    
    def laske_perustulo_sotu(self):
        return 742.0
    
    def laske_perustulo_sotu_matala(self):
        return 300.0
    
    def laske_perustulo_tonni(self):
        return 1000.0
        
    def laske_perustulo_puolitoista(self):
        return 1500.0
        
    #def sairauspaivaraha(self,vakiintunutpalkka : float):
    #    return max(self.laske_perustulo(),super().sairauspaivaraha(vakiintunutpalkka))
        
    def kotihoidontuki(self,lapsia,allekolmev,alle_kouluikaisia):
        # korvataan perustulolla
        return self.perustulo()
    
    def valtionvero_asteikko_perustulo_Kela(self):
        rajat=np.array([6720,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.43,0.43,0.43,0.43]) # 560 e/kk
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_BI(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.5475,0.5475,0.5475,0.5475]) # 800 e/kk # tasavero 52,5 % vastaa 750e ja 48% 650e
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_vihreat(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.4750,0.4750,0.4750,0.4750]) # 600 e/kk Vai 44,75 %??
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_asetettava(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([self.valtionverotaso,self.valtionverotaso,self.valtionverotaso,self.valtionverotaso]) # 600 e/kk Vai 44,75 %??
        return rajat,pros
            
    def valtionvero_asteikko_perustulo_kela_asetettava(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([self.valtionverotaso,self.valtionverotaso,self.valtionverotaso,self.valtionverotaso]) # 600 e/kk Vai 44,75 %??
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_vasemmistoliitto(self):
        rajat=np.array([12*800,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.5475,0.5475,0.5475,0.5475]) # 800 e/kk # tasavero 52,5 % vastaa 750e ja 48% 650e
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_tonni(self):
        rajat=np.array([12*1000,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.64,0.64,0.64,0.64]) # 800 e/kk # tasavero 52,5 %
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_1500(self):
        rajat=np.array([12*1500,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.79,0.79,0.79,0.79]) # 800 e/kk # tasavero 52,5 %
        return rajat,pros        
        
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,
                             muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.0,alennus=0):
                             
        return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,
                             muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=omavastuuprosentti,alennus=alennus)
        
    def peruspaivaraha_bi(self,lapsia):
        return self.perustulo()
                
    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,peruspvraha):
        if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
            return max(0,vakpalkka-tyotaikaisettulot) 
            
        return ansiopaivarahamaara   

    def laske_perustulovero_perus(self,tulo,puhdas_ansiotulo):
        return 0.0

    def laske_perustulovero_sotu(self,palkkatulo,puhdas_ansiotulo):
        return min(0.25*palkkatulo,3_383/self.kk_jakaja)+0.0037*puhdas_ansiotulo

    def laske_perustulovero_sotu_matala(self,palkkatulo,puhdas_ansiotulo):
        return 0.0
        #return min(0.05*palkkatulo,3_383/self.kk_jakaja)+0.0037*puhdas_ansiotulo
        
    def laske_sotumaksu(self,vuosi):
        if vuosi==2018:
            sotumaksu=0.0448+0.6*self.additional_tyel_premium
        elif vuosi==2019:
            sotumaksu=0.0448+0.6*self.additional_tyel_premium
        elif vuosi==2020:
            sotumaksu=0.0414+0.6*self.additional_tyel_premium
        elif vuosi==2021:
            sotumaksu=0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2022:
            sotumaksu=0.0434+0.6*self.additional_tyel_premium
        else:
            sotumaksu=0.0448+0.6*self.additional_tyel_premium
            
        return sotumaksu
        
    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0,omavastuukerroin=1.0,alku=''):
        ansiopvrahan_suojaosa=p['ansiopvrahan_suojaosa']
        lapsikorotus=p['ansiopvraha_lapsikorotus']
    
        if tyoton>0 and p[alku+'elakkeella']<1:
            if lapsikorotus<1:
                lapsia=0    

            if self.year==2018:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                taite=3078.60    
            elif self.year==2019:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                taite=3078.60    
            elif self.year==2020:
                lapsikorotus=np.array([0,5.28,7.76,10.00])*21.5    
                taite=3197.70    
            elif self.year==2021:
                lapsikorotus=np.array([0,5.30,7.78,10.03])*21.5    
                taite=3209.10    
            elif self.year==2022:
                lapsikorotus=np.array([0,5.41,7.95,10.25])*21.5    
                taite=3277.50    
            else:
                lapsikorotus=np.array([0,5.41,7.95,10.25])*21.5    
                taite=3277.50    
                            
            if saa_ansiopaivarahaa>0: # & (kesto<400.0): # ei keston tarkastusta!
                #print(f'tyoton {tyoton} vakiintunutpalkka {vakiintunutpalkka} lapsia {lapsia} tyotaikaisettulot {tyotaikaisettulot} saa_ansiopaivarahaa {saa_ansiopaivarahaa} kesto {kesto} ansiokerroin {ansiokerroin} omavastuukerroin {omavastuukerroin}')
            
                # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                # käytetään nykyistä peruspäivärahaa, jotta ansiosidonnainen ei kasva
                perus=self.nykyperuspaivaraha(0)
                vakpalkka=vakiintunutpalkka*(1-self.sotumaksu)
                
                #print(f'vakpalkka {vakpalkka}')
                if vakpalkka>taite:
                    tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus
                else:
                    tuki2=0.45*max(0,vakpalkka-perus)+perus

                tuki2=tuki2+lapsikorotus[min(lapsia,3)]
                tuki2=tuki2*ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)    

                perus=self.nykyperuspaivaraha(lapsia)     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)
        
                vahentavat_tulot=max(0,tyotaikaisettulot-suojaosa) 
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavat_tulot)
                soviteltuperus=self.nyky_soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,soviteltuperus)

                perus=self.perustulo()
                tuki=omavastuukerroin*max(0,ansiopaivarahamaara-perus)
                ansiopaivarahamaara=omavastuukerroin*max(0,ansiopaivarahamaara-perus)
                perus=0 # perustulo maksetaan muualla
            else:
                # perustulo korvaa peruspäivärahan
                ansiopaivarahamaara=0    
                perus=0 #self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                tuki=0 #self.perustulo()
        else:
            perus=0    
            tuki=0    
            ansiopaivarahamaara=0   

        return tuki,ansiopaivarahamaara,perus

    def soviteltu_peruspaivaraha(self,lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p):
        return self.perustulo()
        
    def tyotulovahennys2018(self):
        max_tyotulovahennys=1540/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
        ttulopros=np.array([0.120,0.0165,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2019(self):
        max_tyotulovahennys=1630/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
        ttulopros=np.array([0.120,0.0172,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2020(self):
        max_tyotulovahennys=1770/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja # 127000??
        ttulopros=np.array([0.125,0.0184,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2021(self):
        max_tyotulovahennys=1840/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja # 127000??
        ttulopros=np.array([0.127,0.0189,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2022(self):
        max_tyotulovahennys=1840/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja # 127000??
        ttulopros=np.array([0.127,0.0189,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys_perustulo_sotu(self):
        max_tyotulovahennys=0
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja # 127000??
        ttulopros=np.array([0,0,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def ansiotulovahennys_perustulo_sotu(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=0/self.kk_jakaja
        ansvah=np.array([0,0,0])
        return rajat,maxvahennys,ansvah

    def ansiotulovahennys2018(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2019(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2020(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2020(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2021(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2022(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def laske_ylevero2018(self,palkkatulot,elaketulot):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14750/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,elaketulot+palkkatulot-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2019(self,palkkatulot,elaketulot):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14750/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,elaketulot+palkkatulot-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2020(self,palkkatulot,elaketulot):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,elaketulot+palkkatulot-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2021(self,palkkatulot,elaketulot):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,elaketulot+palkkatulot-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2022(self,palkkatulot,elaketulot):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,elaketulot+palkkatulot-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def perusvahennys2018(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3020/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2019(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3305/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2020(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3540/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2021(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3630/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2022(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3740/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def verotus(self,palkkatulot,muuttulot,elaketulot,lapsia,p,alku=''):
        lapsivahennys=0 # poistui 2018
    
        peritytverot=0
        self.kk_jakaja=12
        
        self.veroparam()
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        
        tulot=palkkatulot+muuttulot+elaketulot
    
        # vähennetään sosiaaliturvamaksut
        if palkkatulot>self.elakemaksu_alaraja: 
            if p['ika']<68 and palkkatulot>self.elakemaksu_alaraja:
                if p['ika']>=52 and p['ika']<63:
                    ptel=palkkatulot*self.tyontekijan_maksu_52
                else:
                    ptel=palkkatulot*self.tyontekijan_maksu
                koko_tyoelakemaksu=palkkatulot*self.koko_tyel_maksu
            else:
                ptel=0
                koko_tyoelakemaksu=0
        else:
            ptel=0
            koko_tyoelakemaksu=0

        if p[alku+'tyoton']>0:
            if p[alku+'saa_ansiopaivarahaa']>0:
                koko_tyoelakemaksu+=p[alku+'vakiintunutpalkka']*self.koko_tyel_maksu
            #else:
            #    koko_tyoelakemaksu+=1413.75*self.koko_tyel_maksu

        if p[alku+'isyysvapaalla']>0:
            koko_tyoelakemaksu+=p[alku+'vakiintunutpalkka']*self.koko_tyel_maksu
        
        if p[alku+'aitiysvapaalla']>0:
            koko_tyoelakemaksu+=p[alku+'vakiintunutpalkka']*self.koko_tyel_maksu

        if p[alku+'kotihoidontuella']>0:
            koko_tyoelakemaksu+=719.0*self.koko_tyel_maksu

        if p['ika']<65:
            tyotvakmaksu=palkkatulot*self.tyottomyysvakuutusmaksu
        else:
            tyotvakmaksu=0
        
        if palkkatulot>self.paivarahamaksu_raja and p['ika']<68:
            sairausvakuutusmaksu=palkkatulot*self.paivarahamaksu_pros
        else:
            sairausvakuutusmaksu=0

        peritytverot += sairausvakuutusmaksu+ptel+tyotvakmaksu
        palkkatulot = palkkatulot-sairausvakuutusmaksu-ptel-tyotvakmaksu 
    
        # tulonhankkimisvähennys pienentää ansiotuloa
    
        palkkatulot_puhdas=max(0,palkkatulot-self.tulonhankkimisvahennys) # puhdas ansiotulo
        
        # eläketulovähennys
        puhdas_ansiotulo=palkkatulot_puhdas+muuttulot+elaketulot
        
        elaketulovahennys_valtio,elaketulovahennys_kunnallis=self.elaketulovahennys(elaketulot,puhdas_ansiotulo)
        elaketulot_valtio=max(0,elaketulot-elaketulovahennys_valtio)
        elaketulot_kunnallis=max(0,elaketulot-elaketulovahennys_kunnallis)
        elaketulot_puhdas=elaketulot
        
        tulot_valtio=palkkatulot_puhdas+muuttulot+elaketulot_valtio
        tulot_kunnallis=palkkatulot_puhdas+muuttulot+elaketulot_kunnallis
    
        # ylevero
    
        ylevero=self.laske_ylevero(palkkatulot_puhdas,elaketulot_puhdas)
        peritytverot += ylevero
        
        # perustulovero
        perustulovero=self.laske_perustulovero(palkkatulot_puhdas,puhdas_ansiotulo)
        peritytverot += perustulovero
    
        # työtulovähennys vähennetään valtionveroista
        
        max_tyotulovahennys,ttulorajat,ttulopros=self.tyotulovahennys()
    
        if palkkatulot_puhdas>ttulorajat[1]:
            if palkkatulot_puhdas>ttulorajat[2]:
                tyotulovahennys=0
            else:
                tyotulovahennys=min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot_puhdas-ttulorajat[0])))
        else:
            if palkkatulot_puhdas>ttulorajat[0]:
                tyotulovahennys=min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot_puhdas-ttulorajat[0])))
            else:
                tyotulovahennys=0

        if puhdas_ansiotulo>ttulorajat[1]:
            if puhdas_ansiotulo>ttulorajat[2]:
                tyotulovahennys=0
            else:
                tyotulovahennys=max(0,tyotulovahennys-ttulopros[1]*max(0,puhdas_ansiotulo-ttulorajat[1]))

        # valtioverotus
        # varsinainen verotus
        valtionveroperuste=tulot_valtio
        valtionvero = self.laske_valtionvero(valtionveroperuste,p)
        valtionvero += self.raippavero(elaketulot_valtio)
        
        # työtulovähennys
        valtionvero=max(0,valtionvero-lapsivahennys)
        if tyotulovahennys>valtionvero:
            tyotulovahennys_kunnallisveroon=max(0,tyotulovahennys-valtionvero)
            tyotulovahennys=valtionvero
            valtionvero=0
        else:
            tyotulovahennys_kunnallisveroon=0
            valtionvero=max(0,valtionvero-tyotulovahennys)

        peritytverot += valtionvero
        valtionvero += perustulovero

        # kunnallisverotus
        rajat,maxvahennys,ansvah=self.ansiotulovahennys()
        if palkkatulot_puhdas>rajat[1]:
            if palkkatulot_puhdas>rajat[2]:
                ansiotulovahennys=max(0,min(maxvahennys,ansvah[0]*(rajat[1]-rajat[0])+ansvah[1]*(rajat[2]-rajat[1])))
            else:
                ansiotulovahennys=max(0,min(maxvahennys,ansvah[0]*(rajat[1]-rajat[0])+ansvah[1]*(palkkatulot_puhdas-rajat[1])))
        else:
            if palkkatulot_puhdas>rajat[0]:
                ansiotulovahennys=max(0,min(maxvahennys,ansvah[0]*(palkkatulot_puhdas-rajat[0])))
            else:
                ansiotulovahennys=0
        
        if puhdas_ansiotulo>rajat[2]:
            ansiotulovahennys=max(0,ansiotulovahennys-ansvah[2]*(puhdas_ansiotulo-rajat[2]))
        
        # perusvähennys
        perusvahennys_pros,max_perusvahennys=self.perusvahennys()
        peruste=max(0,tulot_kunnallis-ansiotulovahennys)
        if peruste<max_perusvahennys:
            perusvahennys=peruste
        else:
            perusvahennys=max(0,max_perusvahennys-perusvahennys_pros*max(0,peruste-max_perusvahennys))
            
        # Yhteensä
        kunnallisveroperuste=max(0,peruste-perusvahennys)
        
        # korotettu maksuperuste puuttuu? =max(0,palkkatulot-peritty_sairaanhoitomaksu)*korotus
        peritty_sairaanhoitomaksu=max(0,palkkatulot_puhdas-perusvahennys)*self.sairaanhoitomaksu+(muuttulot+elaketulot_kunnallis)*self.sairaanhoitomaksu_etuus
        
        if tyotulovahennys_kunnallisveroon>0:
            kunnallisvero_0=kunnallisveroperuste*self.kunnallisvero_pros
            if peritty_sairaanhoitomaksu+kunnallisvero_0>0:
                kvhen=tyotulovahennys_kunnallisveroon*kunnallisvero_0/(peritty_sairaanhoitomaksu+kunnallisvero_0)
                svhen=tyotulovahennys_kunnallisveroon*peritty_sairaanhoitomaksu/(peritty_sairaanhoitomaksu+kunnallisvero_0)
            else:
                kvhen=0
                svhen=0

            kunnallisvero=max(0,kunnallisveroperuste*self.kunnallisvero_pros-kvhen)
            peritty_sairaanhoitomaksu=max(0,peritty_sairaanhoitomaksu-svhen)
        else:
            kunnallisvero=kunnallisveroperuste*self.kunnallisvero_pros
            
        sairausvakuutusmaksu += peritty_sairaanhoitomaksu
        
        peritytverot += peritty_sairaanhoitomaksu + kunnallisvero
        
        #palkkatulot=palkkatulot-peritty_sairaanhoitomaksu 
        # sairausvakuutusmaksu=sairausvakuutusmaksu+kunnallisveroperuste*sairaanhoitomaksu
        # yhteensä
        netto=tulot-peritytverot
        
        d1=peritytverot
        d2=valtionvero+kunnallisvero+ptel+tyotvakmaksu+ylevero+sairausvakuutusmaksu
        
#        if np.abs(d2-d1)>1e-6:
#            print('verotus',d2-d1)

        return netto,peritytverot,valtionvero,kunnallisvero,kunnallisveroperuste,\
               valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
               tyotulovahennys_kunnallisveroon,ptel,sairausvakuutusmaksu,tyotvakmaksu,koko_tyoelakemaksu,ylevero

    def raippavero2018(self,elaketulo):
        alaraja=47_000*self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2019(self,elaketulo):
        alaraja=47_000*self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2020(self,elaketulo):
        alaraja=47_000*self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2021(self,elaketulo):
        alaraja=47_000*self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2022(self,elaketulo):
        alaraja=47_000*self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
        
    def valtionvero_asteikko_perustulo_Kela(self):
        rajat=np.array([6720,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.43,0.43,0.43,0.43]) # 560 e/kk
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_BI(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.40,0.40,0.40,0.40]) # 500 e/kk
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_vihreat(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        #pros=np.array([0.4575,0.4575,0.4575,0.4575]) # 600 e/kk Vai 44,75 %??
        pros=np.array([0.4750,0.4750,0.4750,0.4750]) # 600 e/kk Vai 44,75 %??

        return rajat,pros
    
    def valtionvero_asteikko_perustulo_asetettava(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([self.valtionverotaso,self.valtionverotaso,self.valtionverotaso,self.valtionverotaso]) # 600 e/kk Vai 44,75 %??
        return rajat,pros
            
    def valtionvero_asteikko_perustulo_kela_asetettava(self):
        rajat=np.array([12*600,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([self.valtionverotaso,self.valtionverotaso,self.valtionverotaso,self.valtionverotaso]) # 600 e/kk Vai 44,75 %??
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_vasemmistoliitto(self):
        rajat=np.array([12*800,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.5475,0.5475,0.5475,0.5475]) # 800 e/kk # tasavero 52,5 % vastaa 750e ja 48% 650e
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_tonni(self):
        rajat=np.array([12*1000,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.64,0.64,0.64,0.64]) # 800 e/kk # tasavero 52,5 %
        return rajat,pros
    
    def valtionvero_asteikko_perustulo_1500(self):
        rajat=np.array([12*1500,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.79,0.79,0.79,0.79]) # 800 e/kk # tasavero 52,5 %
        return rajat,pros
                
    def laske_elatustuki(self,lapsia,aikuisia):
        if self.year==2018:
            elatustuki=156.39*lapsia
        elif self.year==2019:
            elatustuki=167.35*lapsia
        elif self.year==2020:
            elatustuki=167.35*lapsia
        elif self.year==2021:
            elatustuki=167.35*lapsia
        elif self.year==2022:
            elatustuki=172.59*lapsia
        else:
            error()
        
        return elatustuki
    
    def laske_raippavero(self,tulot,p):
        rajat,pros=self.valtionvero_asteikko()

        if tulot>=rajat[0]:
            vero=8/self.kk_jakaja
        else:
            vero=0

        for k in range(0,3):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[3]:
            vero=vero+(tulot-rajat[3])*pros[3]
        
        return vero

    def laske_valtionvero(self,tulot,p):
        rajat,pros=self.valtionvero_asteikko()

        if tulot>=rajat[0]:
            vero=8/self.kk_jakaja
        else:
            vero=0

        for k in range(0,3):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[3]:
            vero=vero+(tulot-rajat[3])*pros[3]
        
        return vero

    def tyottomyysturva_suojaosa(self,suojaosamalli,p=None):
        if suojaosamalli==2:
            suojaosa=0
        elif suojaosamalli==3:
            suojaosa=400
        elif suojaosamalli==4:
            suojaosa=500
        elif suojaosamalli==5:
            suojaosa=600
        elif suojaosamalli==0:
            suojaosa=p['tyottomyysturva_suojaosa_taso']
        else: # perusmallis
            suojaosa=300
        
        return suojaosa
        
    def opintoraha(self,palkka,p):
        '''
        18-vuotias itsellisesti asuva opiskelija
        '''
        tuki=0 #self.perustulo()
                    
        return tuki
        
    def check_p(self,p):
        super().check_p(p)
        
    def asumistuki2018(self,palkkatulot,muuttulot,vuokra,p):
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
        max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(597+99*p['aikuisia']+221*p['lapsia'])))
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
        
    def asumistuki2019(self,palkkatulot,muuttulot,vuokra,p):
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
        max_menot=np.array([[516, 499, 396, 349],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([139, 132, 119, 114])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(597+99*p['aikuisia']+221*p['lapsia'])))
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


        
    def asumistuki2020(self,palkkatulot,muuttulot,vuokra,p):
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
        max_menot=np.array([[520, 503, 399, 352],[752, 722, 583, 513],[958, 910, 740, 656],[1120, 1062, 876, 781]])
        max_lisa=np.array([140, 133, 120, 115])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
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
        

    def asumistuki2021(self,palkkatulot,muuttulot,vuokra,p):
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
        max_menot=np.array([[521, 504, 400, 353],[754, 723, 584, 514],[960, 912, 741, 657],[1122, 1064, 878, 783]])
        max_lisa=np.array([140, 133, 120, 115])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(606+100*p['aikuisia']+224*p['lapsia'])))
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

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(619+103*p['aikuisia']+228*p['lapsia'])))
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
        
    def asumistuki2023(self,palkkatulot,muuttulot,vuokra,p):
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

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(619+103*p['aikuisia']+228*p['lapsia'])))
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


    def isyysraha_perus(self,vakiintunutpalkka):
        if self.year==2018:
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2019:
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2020:
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2021:
            minimi=self.perustulo()
            taite1=39_144/12  
            taite2=60_225/12  
        elif self.year==2022:
            minimi=self.perustulo()
            taite1=39_144/12  
            taite2=60_225/12  
        elif self.year==2023:
            minimi=self.perustulo()
            taite1=39_144/12  
            taite2=60_225/12  
        else:
            print('isyysraha: unknown year',year)  

        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
        raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))-minimi

        return raha
        
    def aitiysraha2018(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))-minimi
        else: 
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))-minimi

        return raha
        
    def aitiysraha2019(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))-minimi
        else: 
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))-minimi

        return raha
        
    def aitiysraha2020(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))-minimi
        else: 
            minimi=self.perustulo()
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))-minimi

        return raha
        
    def aitiysraha2021(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=self.perustulo()
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))-minimi
        else: 
            minimi=self.perustulo()
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))-minimi

        return raha
        
    def aitiysraha2022(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=self.perustulo()
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))-minimi
        else: 
            minimi=self.perustulo()
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))-minimi

        return raha
        
    def sairauspaivaraha2018(self,vakiintunutpalkka):
        minimi=self.perustulo()
        taite1=30_394/12
        taite2=58_252/12
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))-minimi

        return raha
        
    def sairauspaivaraha2019(self,vakiintunutpalkka):
        minimi=self.perustulo()
        taite1=30_394/12
        taite2=57_183/12
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    

        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))-minimi

        return raha

    def sairauspaivaraha2020(self,vakiintunutpalkka):
        minimi=self.perustulo()
        taite1=31_595/12  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return raha
        
    def sairauspaivaraha2021(self,vakiintunutpalkka):
        minimi=self.perustulo()
        taite1=32_011/12  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))-minimi

        return raha
        
    def sairauspaivaraha2022(self,vakiintunutpalkka):
        minimi=self.perustulo()
        taite1=32_011/12  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))-minimi

        return raha

#     def laske_tulot(self,p,tt_alennus=0,include_takuuelake=True,legacy=True):
#         q={} # tulokset tänne
#         self.check_p(p)
#         q['perustulo']=0
#         q['puoliso_perustulo']=0
#         q['puhdas_tyoelake']=0
#         q['multiplier']=1
#         q['kotihoidontuki']=0
#         q['kotihoidontuki_netto']=0
#         q['puoliso_opintotuki']=0
#         q['puoliso_kotihoidontuki']=0
#         q['puoliso_kotihoidontuki_netto']=0
#         q['puoliso_ansiopvraha_netto']=0
#         q['puoliso_kotihoidontuki_netto']=0
#         q['puoliso_opintotuki_netto']=0
#         if p['elakkeella']>0: # vanhuuseläkkeellä
#             p['tyoton']=0
#             q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
#             q['elake_maksussa']=p['tyoelake']
#             q['elake_tuleva']=0
#             p['saa_ansiopaivarahaa']=0
#             # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
#             if (p['aikuisia']>1):
#                 q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,disability=p['disabled'])
#                 q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'],yksin=0)
#             else:
#                 q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,disability=p['disabled'])
#                 q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'],yksin=1)
# 
#             q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
#             #oletetaan että myös puoliso eläkkeellä
#             q['puoliso_ansiopvraha']=0
#             q['opintotuki']=0
#         elif p['opiskelija']>0:
#             q['elake_maksussa']=p['tyoelake']
#             q['kokoelake']=p['tyoelake']
#             q['elake_tuleva']=0
#             q['puoliso_ansiopvraha']=0
#             q['perustulo']=self.perustulo()
#             q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
#             q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
#             q['opintotuki']=0
#             if p['aitiysvapaalla']>0:
#                 q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
#             elif p['isyysvapaalla']>0:
#                 q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
#             elif p['kotihoidontuella']>0:
#                 q['kotihoidontuki']=0 #self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
#             else:
#                 q['opintotuki']=0 #self.opintoraha(0,p)
#         else: # ei eläkkeellä     
#             q['opintotuki']=0
#             q['elake_maksussa']=p['tyoelake']
#             q['kokoelake']=p['tyoelake']
#             q['elake_tuleva']=0
#             q['puoliso_ansiopvraha']=0
#             q['perustulo']=self.perustulo() # ei opiskelijoille?
#             q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
#             q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
#             if p['aitiysvapaalla']>0:
#                 q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
#             elif p['isyysvapaalla']>0:
#                 q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
#             elif p['sairauspaivarahalla']>0:
#                 q['sairauspaivaraha']=self.sairauspaivaraha(p['vakiintunutpalkka'])
#             elif p['kotihoidontuella']>0:
#                 q['kotihoidontuki']=0 #self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
#             elif p['tyoton']>0:
#                 if 'omavastuukerroin' in p:
#                     omavastuukerroin=p['omavastuukerroin']
#                 else:
#                     omavastuukerroin=1.0
#                 q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=\
#                     self.ansiopaivaraha(p['tyoton'],p['vakiintunutpalkka'],p['lapsia'],p['t'],p['saa_ansiopaivarahaa'],
#                         p['tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin)
#                 
#         if p['aikuisia']>1:
#             if p['puoliso_elakkeella']>0: # vanhuuseläkkeellä
#                 p['puoliso_tyoton']=0
#                 q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
#                 q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
#                 q['puoliso_elake_tuleva']=0
#                 p['puoliso_saa_ansiopaivarahaa']=0
#                 # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
#                 q['puoliso_kokoelake']=self.laske_kokonaiselake(p['puoliso_ika'],q['puoliso_elake_maksussa'],yksin=0)
#                 q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=(0,0,0)
#                 q['puoliso_opintotuki']=0
#             elif p['puoliso_opiskelija']>0:
#                 q['puoliso_kokoelake']=0
#                 q['puoliso_perustulo']=self.perustulo()
#                 q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
#                 q['puoliso_elake_tuleva']=0
#                 q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=(0,0,0)
#                 q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
#                 q['puoliso_opintotuki']=0
#                 if p['puoliso_aitiysvapaalla']>0:
#                     q['puoliso_aitiyspaivaraha']=self.aitiysraha(p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
#                 elif p['puoliso_isyysvapaalla']>0:
#                     q['puoliso_isyyspaivaraha']=self.isyysraha(p['puoliso_vakiintunutpalkka'])
#                 elif p['sairauspaivarahalla']>0:
#                     q['puoliso_sairauspaivaraha']=self.sairauspaivaraha(p['puoliso_vakiintunutpalkka'])
#                 elif p['puoliso_kotihoidontuella']>0:
#                     q['puoliso_kotihoidontuki']=0 #self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
#                 else:
#                     q['puoliso_opintotuki']=0 #self.opintoraha(0,p)
#             else: # ei eläkkeellä     
#                 q['puoliso_kokoelake']=0
#                 q['puoliso_opintotuki']=0
#                 q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
#                 q['puoliso_elake_tuleva']=0
#                 q['puoliso_puolison_ansiopvraha']=0
#                 q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=(0,0,0)
#                 q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
#                 q['puoliso_perustulo']=self.perustulo() # ei opiskelijoille?
#                 if p['puoliso_aitiysvapaalla']>0:
#                     q['puoliso_aitiyspaivaraha']=self.aitiysraha(p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
#                 elif p['puoliso_isyysvapaalla']>0:
#                     q['puoliso_isyyspaivaraha']=self.isyysraha(p['puoliso_vakiintunutpalkka'])
#                 elif p['puoliso_sairauspaivarahalla']>0:
#                     q['puoliso_sairauspaivaraha']=self.sairauspaivaraha(p['puoliso_vakiintunutpalkka'])
#                 elif p['puoliso_kotihoidontuella']>0:
#                     q['puoliso_kotihoidontuki']=0 #self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
#                 elif p['puoliso_tyoton']>0:
#                     q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=\
#                         self.ansiopaivaraha(p['puoliso_tyoton'],p['puoliso_vakiintunutpalkka'],p['lapsia'],p['puoliso_tulot'],
#                             p['puoliso_saa_ansiopaivarahaa'],p['puoliso_tyottomyyden_kesto'],p)
#             
#         # q['verot] sisältää kaikki veronluonteiset maksut
#         _,q['verot'],q['valtionvero'],q['kunnallisvero'],q['kunnallisveroperuste'],q['valtionveroperuste'],\
#             q['ansiotulovahennys'],q['perusvahennys'],q['tyotulovahennys'],q['tyotulovahennys_kunnallisveroon'],\
#             q['ptel'],q['sairausvakuutusmaksu'],q['tyotvakmaksu'],q['tyel_kokomaksu'],q['ylevero']=self.verotus(p['t'],
#                 q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki']+q['perustulo'],
#                 q['kokoelake'],p['lapsia'],p)
#         _,q['verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p)
#         _,q['verot_ilman_etuuksia_pl_pt'],valtionvero,kunnallisvero,kunnallisveroperuste,\
#                valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
#                tyotulovahennys_kunnallisveroon,ptel,sairausvakuutus,tyotvakmaksu,\
#                koko_tyelmaksu,ylevero=self.verotus(p['t'],q['perustulo'],0,p['lapsia'],p)
# 
#         if (p['aikuisia']>1):
#             _,q['puoliso_verot'],_,_,_,_,_,_,_,_,q['puoliso_ptel'],q['puoliso_sairausvakuutusmaksu'],\
#                 q['puoliso_tyotvakmaksu'],q['puoliso_tyel_kokomaksu'],q['puoliso_ylevero']\
#                 =self.verotus(p['puoliso_tulot'],q['puoliso_ansiopvraha']+q['puoliso_aitiyspaivaraha']+q['puoliso_isyyspaivaraha']
#                     +q['puoliso_kotihoidontuki']+q['puoliso_sairauspaivaraha']+q['puoliso_opintotuki']+q['puoliso_perustulo'],
#                     q['puoliso_kokoelake'],p['lapsia'],p)
#             _,q['puoliso_verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puoliso_tulot'],q['puoliso_perustulo'],0,0,p)
#             _,q['puoliso_verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puoliso_tulot'],0,0,0,p)
#         else:
#             q['puoliso_verot_ilman_etuuksia']=0
#             q['puoliso_verot_ilman_etuuksia_pl_pt']=0
#             q['puoliso_verot']=0
#             q['puoliso_ptel']=0
#             q['puoliso_sairausvakuutusmaksu']=0
#             q['puoliso_tyotvakmaksu']=0
#     
#         if p['aikuisia']==1 and p['saa_elatustukea']>0:
#             q['elatustuki']=self.laske_elatustuki(p['lapsia'],p['aikuisia'])
#         else:
#             q['elatustuki']=0
#         
#         if p['elakkeella']>0:
#             q['asumistuki']=self.elakkeensaajan_asumistuki(p['puoliso_tulot']+p['t'],q['kokoelake'],p['asumismenot_asumistuki'],p)
#         else:
#             q['asumistuki']=self.asumistuki(p['puoliso_tulot']+p['t'],q['ansiopvraha']+q['puoliso_ansiopvraha']+q['aitiyspaivaraha']
#                 +q['perustulo']+q['puoliso_perustulo']
#                 +q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],p['asumismenot_asumistuki'],p)
#             
#         if p['lapsia']>0:
#             q['pvhoito']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['kokoelake']
#                 +q['elatustuki']+q['ansiopvraha']+q['puoliso_ansiopvraha']+q['sairauspaivaraha']+q['perustulo']+q['puoliso_perustulo'],p)
#             if (p['lapsia_kotihoidontuella']>0):
#                 alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
#                 q['pvhoito']=0 #max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
#             q['pvhoito_ilman_etuuksia_pl_pt']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['elatustuki']+q['perustulo']+q['puoliso_perustulo'],p)
#             q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['elatustuki'],p)
#             if p['aikuisia']==1:
#                 yksinhuoltajakorotus=1
#             else:
#                 yksinhuoltajakorotus=0
#             q['lapsilisa']=self.laske_lapsilisa(p['lapsia'],yksinhuoltajakorotus=yksinhuoltajakorotus)
#         else:
#             q['pvhoito']=0
#             q['pvhoito_ilman_etuuksia']=0
#             q['pvhoito_ilman_etuuksia_pl_pt']=0
#             q['lapsilisa']=0
#     
#         # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
#         q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
#             q['puoliso_ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
# 
#         q['perustulo_netto']=q['perustulo']-(q['verot_ilman_etuuksia_pl_pt']-q['verot_ilman_etuuksia'])
#         q['puoliso_perustulo_netto']=q['puoliso_perustulo']-(q['puoliso_verot_ilman_etuuksia_pl_pt']-q['puoliso_verot_ilman_etuuksia'])
# 
#         if p['elakkeella']>0:
#             q['kokoelake_netto']=q['kokoelake']-(q['verot']-q['verot_ilman_etuuksia'])
#         elif p['opiskelija']>0:
#             q['opintotuki_netto']=q['opintotuki']-(q['verot']-q['verot_ilman_etuuksia_pl_pt'])
#         elif p['aitiysvapaalla']>0:
#             q['aitiyspaivaraha_netto']=q['aitiyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia_pl_pt']) 
#         elif p['isyysvapaalla']>0:
#             q['isyyspaivaraha_netto']=q['isyyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia_pl_pt']) 
#         elif p['kotihoidontuella']>0:
#             q['kotihoidontuki_netto']=q['kotihoidontuki']-(q['verot']-q['verot_ilman_etuuksia_pl_pt']) 
#         elif p['sairauspaivarahalla']>0:
#             q['sairauspaivaraha_netto']=q['sairauspaivaraha']-(q['verot']-q['verot_ilman_etuuksia_pl_pt']) 
#         else:
#             q['ansiopvraha_netto']=q['ansiopvraha']-(q['verot']-q['verot_ilman_etuuksia_pl_pt'])
#             
#         if p['aikuisia']>1:
#             if p['puoliso_tyoton']>0: # vanhuuseläkkeellä
#                 q['puoliso_ansiopvraha_netto']=q['puoliso_ansiopvraha']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia_pl_pt'])
#             elif p['puoliso_opiskelija']>0:
#                 q['puoliso_opintotuki_netto']=q['puoliso_opintotuki']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia_pl_pt'])
#             elif p['puoliso_kotihoidontuella']>0:
#                 q['puoliso_kotihoidontuki_netto']=q['puoliso_kotihoidontuki']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia_pl_pt']) 
#         else:
#             q['puoliso_ansiopvraha_netto']=0
#         #print('ptyötön',q['puoliso_ansiopvraha_netto'],q['puoliso_ansiopvraha'],q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
#             
#         if (p['isyysvapaalla']>0 or p['aitiysvapaalla']>0) and p['tyoton']>0:
#             print('error: vanhempainvapaalla & työtön ei toteutettu')
#     
#         # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
#         # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
#         # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia
# 
#         if q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']>0:
#             suhde=max(0,q['ansiopvraha_netto']/(q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']))
#             q['ansiopvraha_nettonetto']=q['ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
#             q['puoliso_ansiopvraha_nettonetto']=q['puoliso_ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
#         else:
#             q['ansiopvraha_nettonetto']=0
#             q['puoliso_ansiopvraha_nettonetto']=0
# 
#         if q['perustulo_netto']+q['puoliso_perustulo_netto']>0:
#             suhde=max(0,q['puoliso_perustulo_netto']/(q['puoliso_perustulo_netto']+q['perustulo_netto']))
#             q['puoliso_perustulo_nettonetto']=q['puoliso_perustulo_netto']-suhde*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
#             q['perustulo_nettonetto']=q['perustulo_netto']-(1-suhde)*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
#         else:
#             q['perustulo_nettonetto']=0
#             q['puoliso_perustulo_nettonetto']=0
# 
#         if (not self.osittainen_perustulo) or self.perustulo_korvaa_toimeentulotuen: # toimeentulotuki korvattu perustulolla
#             q['toimeentulotuki']=0
#         else:
#             if p['opiskelija']>0:
#                 q['toimeentulotuki']=0
#             else:
#                 # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
#                 q['toimeentulotuki']=self.toimeentulotuki(p['t'],q['verot_ilman_etuuksia'],p['puoliso_tulot'],q['puoliso_verot_ilman_etuuksia'],
#                     q['elatustuki']+q['opintotuki_netto']+q['puoliso_opintotuki_netto']+q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']
#                     +q['asumistuki']+q['sairauspaivaraha_netto']+q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']
#                     +q['kotihoidontuki_netto']+q['puoliso_kotihoidontuki_netto']+q['perustulo_netto']+q['puoliso_perustulo_netto'],
#                     0,p['asumismenot_toimeentulo'],q['pvhoito'],p)
# 
#         kateen=q['perustulo']+q['puoliso_perustulo']+q['opintotuki']+q['kokoelake']+p['puoliso_tulot']+p['t']\
#             +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
#             +q['ansiopvraha']+q['puoliso_ansiopvraha']+q['elatustuki']-q['puoliso_verot']-q['verot']-q['pvhoito']\
#             +q['lapsilisa']+q['sairauspaivaraha']
#         omanetto=q['opintotuki']+q['kokoelake']+p['t']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']\
#             +q['asumistuki']+q['toimeentulotuki']+q['ansiopvraha']+q['elatustuki']\
#             -q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']
#             
#         q['kateen']=kateen # tulot yhteensä perheessä
#         q['perhetulot_netto']=p['puoliso_tulot']+p['t']-q['verot_ilman_etuuksia']-q['puoliso_verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
#         q['omattulot_netto']=p['t']-q['verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
#         q['etuustulo_netto']=q['puoliso_perustulo_netto']+q['perustulo_netto']+q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['opintotuki']\
#             +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
#             +q['toimeentulotuki']-(q['pvhoito_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'])
#         q['etuustulo_brutto']=q['puoliso_perustulo']+q['perustulo']+q['ansiopvraha']+q['puoliso_ansiopvraha']+q['opintotuki']\
#             +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
#             +q['toimeentulotuki']+q['kokoelake']
#         q['brutto']=q['etuustulo_brutto']+p['t']
# 
#         asumismeno=p['asumismenot_asumistuki']
#             
#         q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
#         
#         # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
#         q['netto']=max(0,kateen-q['alv'])
#         #q['netto']=max(0,omanetto-q['alv']-asumismeno)
#         
#         if not legacy:
#             kateen=q['netto']
#         
#         q['palkkatulot']=p['t']
#         if p['elakkeella']<1:
#             q['palkkatulot_eielakkeella']=p['t']
#         else:
#             q['palkkatulot_eielakkeella']=0
#             
#         q['puoliso_palkkatulot']=p['puoliso_tulot']
#         q['puoliso_tulot_netto']=p['puoliso_tulot']-q['puoliso_verot_ilman_etuuksia']
# 
#         return kateen,q
        
#     def laske_tulot_v2(self,p,tt_alennus=0,include_takuuelake=True,omat='omat_',omatalku='',puoliso='puoliso_',puolisoalku='puoliso_',
#         include_alv=True):
#         '''
#         v4:ää varten tehty tulonlaskenta
#         - eroteltu paremmin omat ja puolison tulot ja etuudet 
#         - perusmuuttujat ovat summamuuttujia
#         '''
#         self.check_p(p)
# 
#         q=self.setup_omat_q(p,omat=omat,alku=omatalku,include_takuuelake=include_takuuelake)
#         q=self.setup_puoliso_q(p,q,puoliso=puoliso)
#         
#         # q['verot] sisältää kaikki veronluonteiset maksut
#         _,q[omat+'verot'],q[omat+'valtionvero'],q[omat+'kunnallisvero'],q[omat+'kunnallisveroperuste'],q[omat+'valtionveroperuste'],\
#             q[omat+'ansiotulovahennys'],q[omat+'perusvahennys'],q[omat+'tyotulovahennys'],q[omat+'tyotulovahennys_kunnallisveroon'],\
#             q[omat+'ptel'],q[omat+'sairausvakuutusmaksu'],q[omat+'tyotvakmaksu'],q[omat+'tyel_kokomaksu'],q[omat+'ylevero']=\
#             self.verotus(q[omat+'palkkatulot'],q[omat+'ansiopvraha']+q[omat+'aitiyspaivaraha']+q[omat+'isyyspaivaraha']\
#                 +q[omat+'kotihoidontuki']+q[omat+'sairauspaivaraha']+q[omat+'opintotuki']+q[omat+'perustulo'],
#                 q[omat+'kokoelake'],p['lapsia'],p,alku=omatalku)
#         _,q[omat+'verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[omat+'palkkatulot'],q[omat+'perustulo'],0,0,p,alku=omatalku)
#         _,q[omat+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[omat+'palkkatulot'],0,0,0,p,alku=omatalku)
#         if q[omat+'kokoelake']>0:
#             _,q[omat+'verot_vain_elake'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(0,0,q[omat+'kokoelake'],p['lapsia'],p,alku=omatalku)
#         else:
#             q[omat+'verot_vain_elake']=0
# 
#         if p['aikuisia']>1 and p[puoliso+'alive']>0:
#             _,q[puoliso+'verot'],q[puoliso+'valtionvero'],q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveroperuste'],q[puoliso+'valtionveroperuste'],\
#             q[puoliso+'ansiotulovahennys'],q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon'],\
#             q[puoliso+'ptel'],q[puoliso+'sairausvakuutusmaksu'],q[puoliso+'tyotvakmaksu'],q[puoliso+'tyel_kokomaksu'],q[puoliso+'ylevero']=\
#                 self.verotus(q[puoliso+'palkkatulot'],
#                     q[puoliso+'ansiopvraha']+q[puoliso+'aitiyspaivaraha']+q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
#                     +q[puoliso+'sairauspaivaraha']+q[puoliso+'opintotuki']+q[puoliso+'perustulo'],
#                     q[puoliso+'kokoelake'],0,p,alku=puoliso) # onko oikein että lapsia 0 tässä????
#             _,q[puoliso+'verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],q[puoliso+'perustulo'],0,0,p,alku=puoliso)
#             _,q[puoliso+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],0,0,0,p,alku=puoliso)
#             if q[puoliso+'kokoelake']>0:
#                 _,q[puoliso+'verot_vain_elake'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(0,0,q[puoliso+'kokoelake'],p['lapsia'],p,alku=omatalku)
#             else:
#                 q[puoliso+'verot_vain_elake']=0
#         else:
#             q[puoliso+'verot_ilman_etuuksia'],q[puoliso+'verot'],q[puoliso+'valtionvero']=0,0,0
#             q[puoliso+'verot_ilman_etuuksia_pl_pt']=0
#             q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveroperuste'],q[puoliso+'valtionveroperuste']=0,0,0
#             q[puoliso+'tyotulovahennys'],q[puoliso+'ansiotulovahennys']=0,0
#             q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon']=0,0
#             q[puoliso+'ptel']=0
#             q[puoliso+'sairausvakuutusmaksu']=0
#             q[puoliso+'tyotvakmaksu']=0
#             q[puoliso+'tyel_kokomaksu']=0
#             q[puoliso+'ylevero']=0
#             q[puoliso+'verot_vain_elake']=0
#             
#         # elatustuki (ei vaikuta kannnusteisiin, vain tuloihin, koska ei yhteensovitusta)
#         if p['aikuisia']==1 and p['saa_elatustukea']>0 and p[omatalku+'alive']>0:
#             q[omat+'elatustuki']=self.laske_elatustuki(p['lapsia'],p['aikuisia'])
#         else:
#             q[omat+'elatustuki']=0
#         
#         q[puoliso+'elatustuki']=0
#         
#         q=self.summaa_q(p,q,omat=omat,puoliso=puoliso)
# 
#         if p[puolisoalku+'alive']<1 and p[omatalku+'alive']<1:
#             q['asumistuki'] = 0
#         elif p[omatalku+'elakkeella']>0 and p[puolisoalku+'elakkeella']>0 :
#             q['asumistuki']=self.elakkeensaajan_asumistuki(q['palkkatulot'],q['kokoelake'],p['asumismenot_asumistuki'],p)
#         else:
#             q['asumistuki']=self.asumistuki(q['palkkatulot'],q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['perustulo']
#                                             +q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
#                                             p['asumismenot_asumistuki'],p)
#             
#         if p['lapsia']>0:
#             if p['aikuisia']>1:
#                 if p[omatalku+'aitiysvapaalla']>0 or p[omatalku+'isyysvapaalla']>0 or p[omatalku+'kotihoidontuella']>0 \
#                     or p[puolisoalku+'aitiysvapaalla']>0 or p[puolisoalku+'isyysvapaalla']>0 or p[puolisoalku+'kotihoidontuella']>0:
#                     ei_pvhoitoa=True
#                 else:
#                     ei_pvhoitoa=False
#             else:
#                 if p[omatalku+'aitiysvapaalla']>0 or p[omatalku+'isyysvapaalla']>0 or p[omatalku+'kotihoidontuella']>0:
#                     ei_pvhoitoa=True
#                 else:
#                     ei_pvhoitoa=False
#         
#             if ei_pvhoitoa:
#                 q['pvhoito']=0
#                 q['pvhoito_ilman_etuuksia']=0
#                 q['pvhoito_ilman_etuuksia_pl_pt']=0
#             else:
#                 # kuukausi lomalla, jolloin ei päivähoitoa
#                 q['pvhoito']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['kokoelake']+q['elatustuki']
#                     +q['ansiopvraha']+q['sairauspaivaraha']+q['perustulo'],p)
#                 q['pvhoito_ilman_etuuksia_pl_pt']=self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['elatustuki']+q['perustulo'],p)
#                 q['pvhoito_ilman_etuuksia']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['elatustuki'],p)
#                 #if p['lapsia_paivahoidossa']>0:
#                 #    print('pv',q['pvhoito'],'lapsia',p['lapsia_paivahoidossa'],'t',q['palkkatulot'],'etuus',q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['sairauspaivaraha'])
#                 
#             if p['aikuisia']==1:
#                 yksinhuoltajakorotus=1
#             else:
#                 yksinhuoltajakorotus=0
#             q['lapsilisa']=self.laske_lapsilisa(p['lapsia'],yksinhuoltajakorotus=yksinhuoltajakorotus)
#         else:
#             q['pvhoito']=0
#             q['pvhoito_ilman_etuuksia']=0
#             q['pvhoito_ilman_etuuksia_pl_pt']=0
#             q['lapsilisa']=0
#     
#         # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
#         q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
#             q[puoliso+'ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
#         q[omat+'kokoelake_netto'],q[omat+'isyyspaivaraha_netto'],q[omat+'ansiopvraha_netto'],q[omat+'aitiyspaivaraha_netto'],q[omat+'sairauspaivaraha_netto'],\
#             q[omat+'opintotuki_netto'],q[omat+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
#         q[puoliso+'kokoelake_netto'],q[puoliso+'isyyspaivaraha_netto'],q[puoliso+'ansiopvraha_netto'],q[puoliso+'aitiyspaivaraha_netto'],q[puoliso+'sairauspaivaraha_netto'],\
#             q[puoliso+'opintotuki_netto'],q[puoliso+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
#             
#         if p[omatalku+'elakkeella']>0:
#             q[omat+'kokoelake_netto']=q[omat+'kokoelake']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt'])
#         elif p[omatalku+'opiskelija']>0:
#             q[omat+'opintotuki_netto']=q[omat+'opintotuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt'])
#         elif p[omatalku+'aitiysvapaalla']>0:
#             q[omat+'aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
#         elif p[omatalku+'isyysvapaalla']>0:
#             q[omat+'isyyspaivaraha_netto']=q[omat+'isyyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
#         elif p[omatalku+'kotihoidontuella']>0:
#             q[omat+'kotihoidontuki_netto']=q[omat+'kotihoidontuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
#         elif p[omatalku+'sairauspaivarahalla']>0:
#             q[omat+'sairauspaivaraha_netto']=q[omat+'sairauspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
#         else:
#             q[omat+'ansiopvraha_netto']=q[omat+'ansiopvraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt'])
# 
#         q[omat+'perustulo_netto']=q[omat+'perustulo']-(q[omat+'verot_ilman_etuuksia_pl_pt']-q[omat+'verot_ilman_etuuksia'])
# 
#         if p[puolisoalku+'elakkeella']>0:
#             q[puoliso+'kokoelake_netto']=q[puoliso+'kokoelake']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt'])
#         elif p[puolisoalku+'opiskelija']>0:
#             q[puoliso+'opintotuki_netto']=q[puoliso+'opintotuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt'])
#         elif p[puolisoalku+'aitiysvapaalla']>0:
#             q[puoliso+'aitiyspaivaraha_netto']=q[puoliso+'aitiyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
#         elif p[puolisoalku+'isyysvapaalla']>0:
#             q[puoliso+'isyyspaivaraha_netto']=q[puoliso+'isyyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
#         elif p[puolisoalku+'kotihoidontuella']>0:
#             q[puoliso+'kotihoidontuki_netto']=q[puoliso+'kotihoidontuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
#         elif p[puolisoalku+'sairauspaivarahalla']>0:
#             q[puoliso+'sairauspaivaraha_netto']=q[puoliso+'sairauspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
#         else:
#             q[puoliso+'ansiopvraha_netto']=q[puoliso+'ansiopvraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt'])
# 
#         q[puoliso+'perustulo_netto']=q[puoliso+'perustulo']-(q[puoliso+'verot_ilman_etuuksia_pl_pt']-q[puoliso+'verot_ilman_etuuksia'])
#         
#         q[puoliso+'palkkatulot_netto']=q[puoliso+'palkkatulot']-q[puoliso+'verot_ilman_etuuksia']
#         q[omat+'palkkatulot_netto']=q[omat+'palkkatulot']-q[omat+'verot_ilman_etuuksia']
#         q['palkkatulot_netto']=q[omat+'palkkatulot_netto']+q[puoliso+'palkkatulot_netto']
#         
#         q['perustulo_netto']=q[omat+'perustulo_netto']+q[puoliso+'perustulo_netto']
#         q['ansiopvraha_netto']=q[omat+'ansiopvraha_netto']+q[puoliso+'ansiopvraha_netto']
#         q['kokoelake_netto']=q[omat+'kokoelake_netto']+q[puoliso+'kokoelake_netto']
#         q['aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha_netto']+q[puoliso+'aitiyspaivaraha_netto']
#         q['isyyspaivaraha_netto']=q[omat+'isyyspaivaraha_netto']+q[puoliso+'isyyspaivaraha_netto']
#         q['kotihoidontuki_netto']=q[omat+'kotihoidontuki_netto']+q[puoliso+'kotihoidontuki_netto']
#         q['sairauspaivaraha_netto']=q[omat+'sairauspaivaraha_netto']+q[puoliso+'sairauspaivaraha_netto']
#             
#         if (p[omatalku+'isyysvapaalla']>0 or p[omatalku+'aitiysvapaalla']>0) and p[omatalku+'tyoton']>0:
#             print('error: vanhempainvapaalla & työtön ei toteutettu')
#         if (p[puolisoalku+'isyysvapaalla']>0 or p[puolisoalku+'aitiysvapaalla']>0) and p[puolisoalku+'tyoton']>0:
#             print('error: vanhempainvapaalla & työtön ei toteutettu')
#     
#         # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
#         # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
#         # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia
#         if q['palkkatulot_netto']>0:
#             if p['aikuisia']>1:
#                 if p[omatalku+'alive']>0 and p[puolisoalku+'alive']>0:
#                     suhde=max(0,q[omat+'palkkatulot_netto']/q['palkkatulot_netto'])
#                     q[omat+'palkkatulot_nettonetto']=q[omat+'palkkatulot_netto']-suhde*q['pvhoito_ilman_etuuksia']
#                     q[puoliso+'palkkatulot_nettonetto']=q[puoliso+'palkkatulot_netto']-(1-suhde)*q['pvhoito_ilman_etuuksia']
#                 elif p[omatalku+'alive']>0:
#                     q[omat+'palkkatulot_nettonetto']=q[omat+'palkkatulot_netto']-q['pvhoito_ilman_etuuksia']
#                     q[puoliso+'palkkatulot_nettonetto']=0
#                 elif p[puolisoalku+'alive']>0:
#                     q[puoliso+'palkkatulot_nettonetto']=q[puoliso+'palkkatulot_netto']-q['pvhoito_ilman_etuuksia']
#                     q[omat+'palkkatulot_nettonetto']=0
#                 else:
#                     q[omat+'palkkatulot_nettonetto']=0
#                     q[puoliso+'palkkatulot_nettonetto']=0
#             else:
#                 q[omat+'palkkatulot_nettonetto']=q[omat+'palkkatulot_netto']-q['pvhoito_ilman_etuuksia']
#                 q[puoliso+'palkkatulot_nettonetto']=0
#                 
#             q['palkkatulot_nettonetto']=q[puoliso+'palkkatulot_nettonetto']+q[omat+'palkkatulot_nettonetto']
#         else:
#             q[omat+'palkkatulot_nettonetto']=0
#             q[puoliso+'palkkatulot_nettonetto']=0
#             q['palkkatulot_nettonetto']=0
#             
#         if q['ansiopvraha_netto']>0:
#             if p['aikuisia']>1:
#                 if p[omatalku+'alive']>0 and p[puolisoalku+'alive']>0:
#                     suhde=max(0,q[omat+'ansiopvraha_netto']/q['ansiopvraha_netto'])
#                     q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
#                     q[puoliso+'ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
#                 elif p[omatalku+'alive']>0:
#                     q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
#                     q[puoliso+'ansiopvraha_nettonetto']=0
#                 elif p[puolisoalku+'alive']>0:
#                     q[puoliso+'ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
#                     q[omat+'ansiopvraha_nettonetto']=0
#                 else:
#                     q[omat+'ansiopvraha_nettonetto']=0
#                     q[puoliso+'ansiopvraha_nettonetto']=0
#             else:
#                 q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
#                 q[puoliso+'ansiopvraha_nettonetto']=0
#                 
#             q['ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_nettonetto']+q[omat+'ansiopvraha_nettonetto']
#         else:
#             q[omat+'ansiopvraha_nettonetto']=0
#             q[puoliso+'ansiopvraha_nettonetto']=0
#             q['ansiopvraha_nettonetto']=0
#             
#         if q['perustulo_netto']>0:
#             if p['aikuisia']>1:
#                 if q[omat+'perustulo_netto']+q[puoliso+'perustulo_netto']>0:
#                     suhde=max(0,q[puoliso+'perustulo_netto']/(q[puoliso+'perustulo_netto']+q[omat+'perustulo_netto']))
#                     q[puoliso+'perustulo_nettonetto']=q[puoliso+'perustulo_netto']-suhde*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
#                     q[omat+'perustulo_nettonetto']=q[omat+'perustulo_netto']-(1-suhde)*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
#                 else:
#                     q[omat+'perustulo_nettonetto']=0
#                     q[puoliso+'perustulo_nettonetto']=0
#             else:
#                 q[omat+'perustulo_nettonetto']=q[omat+'perustulo_netto']-(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
#                 q[puoliso+'perustulo_nettonetto']=0
#             
#             q['perustulo_nettonetto']=q[puoliso+'perustulo_nettonetto']+q[omat+'perustulo_nettonetto']
#         else:
#             q[omat+'perustulo_nettonetto']=0
#             q[puoliso+'perustulo_nettonetto']=0
#             q['perustulo_nettonetto']=0
# 
#         if p['aikuisia']<2:
#             if p[omatalku+'opiskelija']>0 or p[omatalku+'alive']<1:
#                 q['toimeentulotuki']=0
#             else:
#                 q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],0,0,\
#                     q['elatustuki']+q['opintotuki_netto']+q['perustulo_netto']+q['ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
#                     +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
#                     0,p['asumismenot_toimeentulo'],q['pvhoito'],p)
#         else:
#             if p[omatalku+'opiskelija']>0 and p[puolisoalku+'opiskelija']>0:
#                 q['toimeentulotuki']=0
#             else:
#                 # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
#                 q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],p[puolisoalku+'t'],q[puoliso+'verot_ilman_etuuksia'],\
#                     q['elatustuki']+q['opintotuki_netto']+q['ansiopvraha_netto']+q['perustulo_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
#                     +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
#                     0,p['asumismenot_toimeentulo'],q['pvhoito'],p)
#                     
#         # sisältää sekä omat että puolison tulot ja menot
#         kateen=q['perustulo']+q['opintotuki']+q['kokoelake']+q['palkkatulot']+q['aitiyspaivaraha']+q['isyyspaivaraha']\
#             +q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']+q['ansiopvraha']+q['elatustuki']\
#             -q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']
# 
#         brutto_omat=q[omat+'opintotuki']+q[omat+'kokoelake']+q[omat+'palkkatulot']+q[omat+'aitiyspaivaraha']\
#             +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+\
#             +q[omat+'ansiopvraha']+q[omat+'elatustuki']+q[omat+'sairauspaivaraha']+q[omat+'perustulo']
#         kateen_omat=brutto_omat-q[omat+'verot']
#         etuusnetto_omat=brutto_omat-q[omat+'palkkatulot']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
#                     
#         q['kateen']=kateen # tulot yhteensä perheessä
#         q['etuustulo_netto']=q['ansiopvraha']+q['opintotuki']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
#             +q['toimeentulotuki']+q['kokoelake']+q['elatustuki']+q['lapsilisa']+q['perustulo']+q['sairauspaivaraha']\
#             -(q['pvhoito']-q['pvhoito_ilman_etuuksia'])-(q['verot']-q['verot_ilman_etuuksia'])
#             
#         asumismeno=p['asumismenot_asumistuki']
#             
#         if include_alv:
#             q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
#         else:
#             q['alv']=0
#         
#         # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
#         q['netto']=max(0,kateen-q['alv'])
#         
#         if p['aikuisia']>1:
#             brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
#                 +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
#                 +q[puoliso+'ansiopvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']+q[puoliso+'perustulo']
#             kateen_puoliso=brutto_puoliso-q[puoliso+'verot']
#             etuusnetto_puoliso=brutto_puoliso-q[puoliso+'palkkatulot']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
#             
#             if kateen_puoliso+kateen_omat<1e-6:
#                 suhde=0.5
#             else: # jaetaan bruttotulojen suhteessa, mutta tasoitetaan eroja
#                 if kateen_omat>kateen_puoliso:
#                     if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0:
#                         suhde=kateen_puoliso/(kateen_puoliso+kateen_omat)
#                     else:
#                         suhde=kateen_omat/(kateen_puoliso+kateen_omat)
#                 else:
#                     if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0:
#                         suhde=kateen_puoliso/(kateen_puoliso+kateen_omat)
#                     else:
#                         suhde=kateen_omat/(kateen_puoliso+kateen_omat)
#                 
#             #print(suhde,1.0-suhde,q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'],kateen_omat,kateen_puoliso)
# 
#             etuusnetto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
#             kateen_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
#             brutto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
#             if kateen_omat>0:
#                 r2=etuusnetto_omat/kateen_omat
#             else:
#                 r2=1
# 
#             q[omat+'toimeentulotuki']=q['toimeentulotuki']*suhde
#             q[omat+'asumistuki']=q['asumistuki']*suhde
#             q[omat+'lapsilisa']=q['lapsilisa']*suhde
# 
#             if etuusnetto_omat>0:
#                 r_t_e=q[omat+'toimeentulotuki']/etuusnetto_omat
#                 r_a_e=q[omat+'asumistuki']/etuusnetto_omat
#                 r_tt_e=q[omat+'ansiopvraha_nettonetto']/etuusnetto_omat
#                 r_tt_l=q[omat+'lapsilisa']/etuusnetto_omat
#                 r_tt_ko=q[omat+'kokoelake']/etuusnetto_omat
#                 r_tt_op=q[omat+'opintotuki']/etuusnetto_puoliso
#                 r_pt=q[omat+'perustulo']/etuusnetto_omat
#             else:
#                 r_t_e=0
#                 r_a_e=0
#                 r_tt_e=0
#                 r_tt_l=0
#                 r_tt_ko=0
#                 r_tt_op=0
#                 r_pt=0
#             
#             etuusnetto_omat+=(-r2*(q['alv']+q['pvhoito']))*suhde
#             kateen_omat+=(-q['alv']-q['pvhoito'])*suhde
#             q[omat+'palkkatulot_nettonetto']+=-q['alv']*suhde*(1-r2)
#             q[omat+'toimeentulotuki']+=-r_t_e*q['alv']*suhde*r2
#             q[omat+'asumistuki']+=-r_a_e*q['alv']*suhde*r2
#             q[omat+'ansiopvraha_nettonetto']+=-r_tt_e*q['alv']*suhde*r2
#             q[omat+'opintotuki']+=-r_tt_op*q['alv']*suhde*r2
#             q[omat+'kokoelake']+=-r_tt_ko*q['alv']*suhde*r2
#             q[omat+'pvhoito']=q['pvhoito']*suhde
#             q[omat+'lapsilisa']+=-r_tt_l*q['alv']*suhde*r2
#             q[omat+'perustulo']+=-r_pt*q['alv']*suhde*r2
#             q[omat+'alv']=q['alv']*suhde
#             
#             etuusnetto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
#             kateen_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
#             brutto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
#             if kateen_puoliso>0:
#                 r2=etuusnetto_puoliso/kateen_puoliso
#             else:
#                 r2=1
#             
#             q[puoliso+'toimeentulotuki']=q['toimeentulotuki']*(1-suhde)
#             q[puoliso+'asumistuki']=q['asumistuki']*(1-suhde)
#             q[puoliso+'lapsilisa']=q['lapsilisa']*(1-suhde)
#             if etuusnetto_puoliso>0:
#                 r_t_e=q[puoliso+'toimeentulotuki']/etuusnetto_puoliso
#                 r_a_e=q[puoliso+'asumistuki']/etuusnetto_puoliso
#                 r_tt_e=q[puoliso+'ansiopvraha_nettonetto']/etuusnetto_puoliso
#                 r_tt_l=q[puoliso+'lapsilisa']/etuusnetto_puoliso
#                 r_tt_ko=q[puoliso+'kokoelake']/etuusnetto_puoliso
#                 r_tt_op=q[puoliso+'opintotuki']/etuusnetto_puoliso
#                 r_pt=q[puoliso+'perustulo']/etuusnetto_puoliso
#             else:
#                 r_t_e=0
#                 r_a_e=0
#                 r_tt_e=0
#                 r_tt_l=0
#                 r_tt_ko=0
#                 r_tt_op=0
#                 r_pt=0
# 
#             etuusnetto_puoliso+=(-r2*(q['alv']+q['pvhoito']))*(1-suhde)
#             kateen_puoliso+=(-q['alv']-q['pvhoito'])*(1-suhde)
#             q[puoliso+'palkkatulot_nettonetto']+=-(1-r2)*q['alv']*(1-suhde)
#             q[puoliso+'toimeentulotuki']+=-r_t_e*q['alv']*(1-suhde)*r2
#             q[puoliso+'asumistuki']+=-r_a_e*q['alv']*(1-suhde)*r2
#             q[puoliso+'ansiopvraha_nettonetto']+=-r_tt_e*q['alv']*suhde*r2
#             q[puoliso+'kokoelake']+=-r_tt_ko*q['alv']*suhde*r2
#             q[puoliso+'opintotuki']+=-r_tt_op*q['alv']*suhde*r2
#             q[puoliso+'pvhoito']=q['pvhoito']*(1-suhde)
#             q[puoliso+'lapsilisa']+=-r_tt_l*q['alv']*suhde*r2
#             q[puoliso+'perustulo']+=-r_pt*q['alv']*suhde*r2
#             q[puoliso+'alv']=q['alv']*(1-suhde)
#         else:
#             kateen_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
#             brutto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
#             etuusnetto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
#             if kateen_omat>0:
#                 r2=etuusnetto_omat/kateen_omat
#             else:
#                 r2=1
#                 
#             kateen_omat += -q['alv']-q['pvhoito']
#                 
#             if etuusnetto_omat>0:
#                 r_t_e=q['toimeentulotuki']/etuusnetto_omat
#                 r_a_e=q['asumistuki']/etuusnetto_omat
#                 r_tt_e=q['ansiopvraha_nettonetto']/etuusnetto_omat
#                 r_tt_l=q['lapsilisa']/etuusnetto_omat
#                 r_tt_el=q['elatustuki']/etuusnetto_omat
#                 r_tt_op=q['opintotuki']/etuusnetto_omat
#                 r_tt_ko=q['kokoelake']/etuusnetto_omat
#                 r_pt=q['perustulo']/etuusnetto_omat
#             else:
#                 r_t_e=0
#                 r_a_e=0
#                 r_tt_e=0
#                 r_tt_l=0
#                 r_tt_el=0
#                 r_tt_op=0
#                 r_tt_ko=0
#                 r_pt=0
# 
#             etuusnetto_omat+=-r2*(q['alv']+q['pvhoito'])
#             q[omat+'palkkatulot_nettonetto']+=-(1-r2)*q['alv']
#             q[omat+'toimeentulotuki']=q['toimeentulotuki']-r_t_e*q['alv']*r2
#             q[omat+'asumistuki']=q['asumistuki']-r_a_e*q['alv']*r2
#             q[omat+'ansiopvraha_nettonetto']+=-r_tt_e*q['alv']*r2
#             q[omat+'kokoelake']+=-r_tt_ko*q['alv']*r2
#             q[omat+'opintotuki']+=-r_tt_op*q['alv']*r2
#             q[omat+'pvhoito']=q['pvhoito']
#             q[omat+'lapsilisa']=q['lapsilisa']-r_tt_l*q['alv']*r2
#             q['elatustuki']=q['elatustuki']-r_tt_el*q['alv']*r2
#             q[omat+'perustulo']+=-r_pt*q['alv']*r2
#             q[omat+'alv']=q['alv']
#             kateen_puoliso=0
#             brutto_puoliso=0
#             etuusnetto_puoliso=0
#             q[puoliso+'toimeentulotuki']=0
#             q[puoliso+'asumistuki']=0
#             q[puoliso+'pvhoito']=0
#             q[puoliso+'lapsilisa']=0
#             q[puoliso+'perustulo']=0
#             q[puoliso+'alv']=0
# 
#         q[omat+'netto']=kateen_omat
#         q[puoliso+'netto']=kateen_puoliso
#         q[omat+'etuustulo_netto']=etuusnetto_omat
#         q[puoliso+'etuustulo_netto']=etuusnetto_puoliso
#         q['perustulo']=q[puoliso+'perustulo']+q[omat+'perustulo']
#         q['toimeentulotuki']=q[puoliso+'toimeentulotuki']+q[omat+'toimeentulotuki']
#         q['asumistuki']=q[puoliso+'asumistuki']+q[omat+'asumistuki']
#         q['kokoelake']=q[puoliso+'kokoelake']+q[omat+'kokoelake']
#         q['opintotuki']=q[puoliso+'opintotuki']+q[omat+'opintotuki']
#         q['lapsilisa']=q[puoliso+'lapsilisa']+q[omat+'lapsilisa']
#         q['ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_nettonetto']+q[omat+'ansiopvraha_nettonetto']
#         q['etuustulo_netto_v2']=q[puoliso+'etuustulo_netto']+q[omat+'etuustulo_netto']
#         q['palkkatulot_nettonetto']=q[puoliso+'palkkatulot_nettonetto']+q[omat+'palkkatulot_nettonetto']
#         
#         #q[omat+'etuustulo_brutto']=brutto_omat
#         #q[puoliso+'etuustulo_brutto']=brutto_puoliso
#         
#         q[omat+'etuustulo_brutto']=q[omat+'ansiopvraha']+q[omat+'opintotuki']+q[omat+'aitiyspaivaraha']\
#             +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+q[omat+'asumistuki']+q[omat+'perustulo']\
#             +q[omat+'toimeentulotuki']+q[omat+'kokoelake']+q[omat+'elatustuki']+q[omat+'lapsilisa'] # + sairauspaivaraha
#         q[puoliso+'etuustulo_brutto']=q[puoliso+'ansiopvraha']+q[puoliso+'opintotuki']+q[puoliso+'aitiyspaivaraha']\
#             +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'asumistuki']+q[puoliso+'perustulo']\
#             +q[puoliso+'toimeentulotuki']+q[puoliso+'kokoelake']+q[puoliso+'elatustuki']+q[puoliso+'lapsilisa']
#         q['etuustulo_brutto']=q[omat+'etuustulo_brutto']+q[puoliso+'etuustulo_brutto'] # + sairauspaivaraha
#         
#         kateen=q['netto']
#         
#         # check that omat, puoliso split is ok
#         #self.check_q_netto(q,p['aikuisia'],omat,puoliso)
# 
#         return kateen,q
                
    def laske_tulot_v3(self,p,tt_alennus=0,include_takuuelake=True,omat='omat_',omatalku='',puoliso='puoliso_',puolisoalku='puoliso_',
        include_alv=True,split_costs=True):
        '''
        v4:ää varten tehty tulonlaskenta
        - eroteltu paremmin omat ja puolison tulot ja etuudet 
        - perusmuuttujat ovat summamuuttujia
        '''
        self.check_p(p)

        q=self.setup_omat_q(p,omat=omat,alku=omatalku,include_takuuelake=include_takuuelake)
        q=self.setup_puoliso_q(p,q,puoliso=puoliso)
        
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q[omat+'verot'],q[omat+'valtionvero'],q[omat+'kunnallisvero'],q[omat+'kunnallisveroperuste'],q[omat+'valtionveroperuste'],\
            q[omat+'ansiotulovahennys'],q[omat+'perusvahennys'],q[omat+'tyotulovahennys'],q[omat+'tyotulovahennys_kunnallisveroon'],\
            q[omat+'ptel'],q[omat+'sairausvakuutusmaksu'],q[omat+'tyotvakmaksu'],q[omat+'tyel_kokomaksu'],q[omat+'ylevero']=\
            self.verotus(q[omat+'palkkatulot'],q[omat+'ansiopvraha']+q[omat+'aitiyspaivaraha']+q[omat+'isyyspaivaraha']\
                +q[omat+'kotihoidontuki']+q[omat+'sairauspaivaraha']+q[omat+'opintotuki']+q[omat+'perustulo'],
                q[omat+'kokoelake'],p['lapsia'],p,alku=omatalku)
        _,q[omat+'verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[omat+'palkkatulot'],q[omat+'perustulo'],0,0,p,alku=omatalku)
        _,q[omat+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[omat+'palkkatulot'],0,0,0,p,alku=omatalku)
        if q[omat+'kokoelake']>0:
            _,q[omat+'verot_vain_elake'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(0,0,q[omat+'kokoelake'],p['lapsia'],p,alku=omatalku)
        else:
            q[omat+'verot_vain_elake']=0

        if p['aikuisia']>1 and p[puoliso+'alive']>0:
            _,q[puoliso+'verot'],q[puoliso+'valtionvero'],q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveroperuste'],q[puoliso+'valtionveroperuste'],\
            q[puoliso+'ansiotulovahennys'],q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon'],\
            q[puoliso+'ptel'],q[puoliso+'sairausvakuutusmaksu'],q[puoliso+'tyotvakmaksu'],q[puoliso+'tyel_kokomaksu'],q[puoliso+'ylevero']=\
                self.verotus(q[puoliso+'palkkatulot'],
                    q[puoliso+'ansiopvraha']+q[puoliso+'aitiyspaivaraha']+q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                    +q[puoliso+'sairauspaivaraha']+q[puoliso+'opintotuki']+q[puoliso+'perustulo'],
                    q[puoliso+'kokoelake'],0,p,alku=puoliso) # onko oikein että lapsia 0 tässä????
            _,q[puoliso+'verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],q[puoliso+'perustulo'],0,0,p,alku=puoliso)
            _,q[puoliso+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],0,0,0,p,alku=puoliso)
            if q[puoliso+'kokoelake']>0:
                _,q[puoliso+'verot_vain_elake'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(0,0,q[puoliso+'kokoelake'],p['lapsia'],p,alku=omatalku)
            else:
                q[puoliso+'verot_vain_elake']=0
        else:
            q[puoliso+'verot_ilman_etuuksia'],q[puoliso+'verot'],q[puoliso+'valtionvero']=0,0,0
            q[puoliso+'verot_ilman_etuuksia_pl_pt']=0
            q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveroperuste'],q[puoliso+'valtionveroperuste']=0,0,0
            q[puoliso+'tyotulovahennys'],q[puoliso+'ansiotulovahennys']=0,0
            q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon']=0,0
            q[puoliso+'ptel']=0
            q[puoliso+'sairausvakuutusmaksu']=0
            q[puoliso+'tyotvakmaksu']=0
            q[puoliso+'tyel_kokomaksu']=0
            q[puoliso+'ylevero']=0
            q[puoliso+'verot_vain_elake']=0
            
        # elatustuki (ei vaikuta kannnusteisiin, vain tuloihin, koska ei yhteensovitusta)
        if p['aikuisia']==1 and p['saa_elatustukea']>0 and p[omatalku+'alive']>0:
            q[omat+'elatustuki']=self.laske_elatustuki(p['lapsia'],p['aikuisia'])
        else:
            q[omat+'elatustuki']=0
        
        q[puoliso+'elatustuki']=0
        
        q=self.summaa_q(p,q,omat=omat,puoliso=puoliso)

        if p[puolisoalku+'alive']<1 and p[omatalku+'alive']<1:
            q['asumistuki'] = 0
        elif p[omatalku+'elakkeella']>0 and p[puolisoalku+'elakkeella']>0 :
            q['asumistuki']=self.elakkeensaajan_asumistuki(q['palkkatulot'],q['kokoelake'],p['asumismenot_asumistuki'],p)
        else:
            q['asumistuki']=self.asumistuki(q['palkkatulot'],q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['perustulo']
                                            +q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
                                            p['asumismenot_asumistuki'],p)
            
        if p['lapsia']>0:
            if p['aikuisia']>1:
                if p[omatalku+'aitiysvapaalla']>0 or p[omatalku+'isyysvapaalla']>0 or p[omatalku+'kotihoidontuella']>0 \
                    or p[puolisoalku+'aitiysvapaalla']>0 or p[puolisoalku+'isyysvapaalla']>0 or p[puolisoalku+'kotihoidontuella']>0:
                    ei_pvhoitoa=True
                else:
                    ei_pvhoitoa=False
            else:
                if p[omatalku+'aitiysvapaalla']>0 or p[omatalku+'isyysvapaalla']>0 or p[omatalku+'kotihoidontuella']>0:
                    ei_pvhoitoa=True
                else:
                    ei_pvhoitoa=False
        
            if ei_pvhoitoa:
                q['pvhoito']=0
                q['pvhoito_ilman_etuuksia']=0
                q['pvhoito_ilman_etuuksia_pl_pt']=0
            else:
                # kuukausi lomalla, jolloin ei päivähoitoa
                q['pvhoito']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['kokoelake']+q['elatustuki']
                    +q['ansiopvraha']+q['sairauspaivaraha']+q['perustulo'],p)
                q['pvhoito_ilman_etuuksia_pl_pt']=self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['elatustuki']+q['perustulo'],p)
                q['pvhoito_ilman_etuuksia']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['elatustuki'],p)
                #if p['lapsia_paivahoidossa']>0:
                #    print('pv',q['pvhoito'],'lapsia',p['lapsia_paivahoidossa'],'t',q['palkkatulot'],'etuus',q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['sairauspaivaraha'])
                
            if p['aikuisia']==1:
                yksinhuoltajakorotus=1
            else:
                yksinhuoltajakorotus=0
            q['lapsilisa']=self.laske_lapsilisa(p['lapsia'],yksinhuoltajakorotus=yksinhuoltajakorotus)
        else:
            q['pvhoito']=0
            q['pvhoito_ilman_etuuksia']=0
            q['pvhoito_ilman_etuuksia_pl_pt']=0
            q['lapsilisa']=0
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
            q[puoliso+'ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
        q[omat+'kokoelake_netto'],q[omat+'isyyspaivaraha_netto'],q[omat+'ansiopvraha_netto'],q[omat+'aitiyspaivaraha_netto'],q[omat+'sairauspaivaraha_netto'],\
            q[omat+'opintotuki_netto'],q[omat+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
        q[puoliso+'kokoelake_netto'],q[puoliso+'isyyspaivaraha_netto'],q[puoliso+'ansiopvraha_netto'],q[puoliso+'aitiyspaivaraha_netto'],q[puoliso+'sairauspaivaraha_netto'],\
            q[puoliso+'opintotuki_netto'],q[puoliso+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
            
        if p[omatalku+'elakkeella']>0:
            q[omat+'kokoelake_netto']=q[omat+'kokoelake']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt'])
        elif p[omatalku+'opiskelija']>0:
            q[omat+'opintotuki_netto']=q[omat+'opintotuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt'])
        elif p[omatalku+'aitiysvapaalla']>0:
            q[omat+'aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
        elif p[omatalku+'isyysvapaalla']>0:
            q[omat+'isyyspaivaraha_netto']=q[omat+'isyyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
        elif p[omatalku+'kotihoidontuella']>0:
            q[omat+'kotihoidontuki_netto']=q[omat+'kotihoidontuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
        elif p[omatalku+'sairauspaivarahalla']>0:
            q[omat+'sairauspaivaraha_netto']=q[omat+'sairauspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt']) 
        else:
            q[omat+'ansiopvraha_netto']=q[omat+'ansiopvraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia_pl_pt'])

        q[omat+'perustulo_netto']=q[omat+'perustulo']-(q[omat+'verot_ilman_etuuksia_pl_pt']-q[omat+'verot_ilman_etuuksia'])

        if p[puolisoalku+'elakkeella']>0:
            q[puoliso+'kokoelake_netto']=q[puoliso+'kokoelake']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt'])
        elif p[puolisoalku+'opiskelija']>0:
            q[puoliso+'opintotuki_netto']=q[puoliso+'opintotuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt'])
        elif p[puolisoalku+'aitiysvapaalla']>0:
            q[puoliso+'aitiyspaivaraha_netto']=q[puoliso+'aitiyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
        elif p[puolisoalku+'isyysvapaalla']>0:
            q[puoliso+'isyyspaivaraha_netto']=q[puoliso+'isyyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
        elif p[puolisoalku+'kotihoidontuella']>0:
            q[puoliso+'kotihoidontuki_netto']=q[puoliso+'kotihoidontuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
        elif p[puolisoalku+'sairauspaivarahalla']>0:
            q[puoliso+'sairauspaivaraha_netto']=q[puoliso+'sairauspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt']) 
        else:
            q[puoliso+'ansiopvraha_netto']=q[puoliso+'ansiopvraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia_pl_pt'])

        q[puoliso+'perustulo_netto']=q[puoliso+'perustulo']-(q[puoliso+'verot_ilman_etuuksia_pl_pt']-q[puoliso+'verot_ilman_etuuksia'])
        
        q[puoliso+'palkkatulot_netto']=q[puoliso+'palkkatulot']-q[puoliso+'verot_ilman_etuuksia']
        q[omat+'palkkatulot_netto']=q[omat+'palkkatulot']-q[omat+'verot_ilman_etuuksia']
        q['palkkatulot_netto']=q[omat+'palkkatulot_netto']+q[puoliso+'palkkatulot_netto']
        
        q['perustulo_netto']=q[omat+'perustulo_netto']+q[puoliso+'perustulo_netto']
        q['ansiopvraha_netto']=q[omat+'ansiopvraha_netto']+q[puoliso+'ansiopvraha_netto']
        q['kokoelake_netto']=q[omat+'kokoelake_netto']+q[puoliso+'kokoelake_netto']
        q['aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha_netto']+q[puoliso+'aitiyspaivaraha_netto']
        q['isyyspaivaraha_netto']=q[omat+'isyyspaivaraha_netto']+q[puoliso+'isyyspaivaraha_netto']
        q['kotihoidontuki_netto']=q[omat+'kotihoidontuki_netto']+q[puoliso+'kotihoidontuki_netto']
        q['sairauspaivaraha_netto']=q[omat+'sairauspaivaraha_netto']+q[puoliso+'sairauspaivaraha_netto']
            
        if (p[omatalku+'isyysvapaalla']>0 or p[omatalku+'aitiysvapaalla']>0) and p[omatalku+'tyoton']>0:
            print('error: vanhempainvapaalla & työtön ei toteutettu')
        if (p[puolisoalku+'isyysvapaalla']>0 or p[puolisoalku+'aitiysvapaalla']>0) and p[puolisoalku+'tyoton']>0:
            print('error: vanhempainvapaalla & työtön ei toteutettu')
    
        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia
        if q['palkkatulot_netto']>0:
            if p['aikuisia']>1:
                if p[omatalku+'alive']>0 and p[puolisoalku+'alive']>0:
                    suhde=max(0,q[omat+'palkkatulot_netto']/q['palkkatulot_netto'])
                    q[omat+'palkkatulot_nettonetto']=q[omat+'palkkatulot_netto']-suhde*q['pvhoito_ilman_etuuksia']
                    q[puoliso+'palkkatulot_nettonetto']=q[puoliso+'palkkatulot_netto']-(1-suhde)*q['pvhoito_ilman_etuuksia']
                elif p[omatalku+'alive']>0:
                    q[omat+'palkkatulot_nettonetto']=q[omat+'palkkatulot_netto']-q['pvhoito_ilman_etuuksia']
                    q[puoliso+'palkkatulot_nettonetto']=0
                elif p[puolisoalku+'alive']>0:
                    q[puoliso+'palkkatulot_nettonetto']=q[puoliso+'palkkatulot_netto']-q['pvhoito_ilman_etuuksia']
                    q[omat+'palkkatulot_nettonetto']=0
                else:
                    q[omat+'palkkatulot_nettonetto']=0
                    q[puoliso+'palkkatulot_nettonetto']=0
            else:
                q[omat+'palkkatulot_nettonetto']=q[omat+'palkkatulot_netto']-q['pvhoito_ilman_etuuksia']
                q[puoliso+'palkkatulot_nettonetto']=0
                
            q['palkkatulot_nettonetto']=q[puoliso+'palkkatulot_nettonetto']+q[omat+'palkkatulot_nettonetto']
        else:
            q[omat+'palkkatulot_nettonetto']=0
            q[puoliso+'palkkatulot_nettonetto']=0
            q['palkkatulot_nettonetto']=0
            
        if q['ansiopvraha_netto']>0:
            if p['aikuisia']>1:
                if p[omatalku+'alive']>0 and p[puolisoalku+'alive']>0:
                    suhde=max(0,q[omat+'ansiopvraha_netto']/q['ansiopvraha_netto'])
                    q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
                    q[puoliso+'ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
                elif p[omatalku+'alive']>0:
                    q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
                    q[puoliso+'ansiopvraha_nettonetto']=0
                elif p[puolisoalku+'alive']>0:
                    q[puoliso+'ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
                    q[omat+'ansiopvraha_nettonetto']=0
                else:
                    q[omat+'ansiopvraha_nettonetto']=0
                    q[puoliso+'ansiopvraha_nettonetto']=0
            else:
                q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
                q[puoliso+'ansiopvraha_nettonetto']=0
                
            q['ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_nettonetto']+q[omat+'ansiopvraha_nettonetto']
        else:
            q[omat+'ansiopvraha_nettonetto']=0
            q[puoliso+'ansiopvraha_nettonetto']=0
            q['ansiopvraha_nettonetto']=0
            
        if q['perustulo_netto']>0:
            if p['aikuisia']>1:
                if q[omat+'perustulo_netto']+q[puoliso+'perustulo_netto']>0:
                    suhde=max(0,q[puoliso+'perustulo_netto']/(q[puoliso+'perustulo_netto']+q[omat+'perustulo_netto']))
                    q[puoliso+'perustulo_nettonetto']=q[puoliso+'perustulo_netto']-suhde*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
                    q[omat+'perustulo_nettonetto']=q[omat+'perustulo_netto']-(1-suhde)*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
                else:
                    q[omat+'perustulo_nettonetto']=0
                    q[puoliso+'perustulo_nettonetto']=0
            else:
                q[omat+'perustulo_nettonetto']=q[omat+'perustulo_netto']-(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
                q[puoliso+'perustulo_nettonetto']=0
            
            q['perustulo_nettonetto']=q[puoliso+'perustulo_nettonetto']+q[omat+'perustulo_nettonetto']
        else:
            q[omat+'perustulo_nettonetto']=0
            q[puoliso+'perustulo_nettonetto']=0
            q['perustulo_nettonetto']=0

        if p['aikuisia']<2:
            if p[omatalku+'opiskelija']>0 or p[omatalku+'alive']<1:
                q['toimeentulotuki']=0
            else:
                q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],0,0,\
                    q['elatustuki']+q['opintotuki_netto']+q['perustulo_netto']+q['ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                    +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
                    0,p['asumismenot_toimeentulo'],q['pvhoito'],p)
        else:
            if p[omatalku+'opiskelija']>0 and p[puolisoalku+'opiskelija']>0:
                q['toimeentulotuki']=0
            else:
                # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
                q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],p[puolisoalku+'t'],q[puoliso+'verot_ilman_etuuksia'],\
                    q['elatustuki']+q['opintotuki_netto']+q['ansiopvraha_netto']+q['perustulo_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                    +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
                    0,p['asumismenot_toimeentulo'],q['pvhoito'],p)
                    
        # sisältää sekä omat että puolison tulot ja menot
        kateen=q['perustulo']+q['opintotuki']+q['kokoelake']+q['palkkatulot']+q['aitiyspaivaraha']+q['isyyspaivaraha']\
            +q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']+q['ansiopvraha']+q['elatustuki']\
            -q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']

        brutto_omat=q[omat+'opintotuki']+q[omat+'kokoelake']+q[omat+'palkkatulot']+q[omat+'aitiyspaivaraha']\
            +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+\
            +q[omat+'ansiopvraha']+q[omat+'elatustuki']+q[omat+'sairauspaivaraha']+q[omat+'perustulo']
        kateen_omat=brutto_omat-q[omat+'verot']
        etuusnetto_omat=brutto_omat-q[omat+'palkkatulot']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
        
        if p['aikuisia']>1:
            brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
                +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                +q[puoliso+'ansiopvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']+q[puoliso+'perustulo']
            kateen_puoliso=brutto_puoliso-q[puoliso+'verot']
            etuusnetto_puoliso=brutto_puoliso-q[puoliso+'palkkatulot']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
        else:
            brutto_puoliso=0
            kateen_puoliso=0
            etuusnetto_puoliso=0
                    
        q['kateen']=kateen # tulot yhteensä perheessä
        q['etuustulo_netto']=q['ansiopvraha']+q['opintotuki']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimeentulotuki']+q['kokoelake']+q['elatustuki']+q['lapsilisa']+q['perustulo']+q['sairauspaivaraha']\
            -(q['pvhoito']-q['pvhoito_ilman_etuuksia'])-(q['verot']-q['verot_ilman_etuuksia'])
            
        asumismeno=p['asumismenot_asumistuki']
            
        if include_alv:
            q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        else:
            q['alv']=0
        
        # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
        q['netto']=max(0,kateen-q['alv'])
        
        if split_costs:
            super().split_cost_to_wage_unemp(p,q,omat,puoliso,omatalku,puolisoalku)
        
            if p['aikuisia']>1:
                if kateen_puoliso+kateen_omat<1e-6:
                    suhde=0.5  # FIXME???
                else: # jaetaan bruttotulojen suhteessa, mutta tasoitetaan eroja
                    if kateen_omat>kateen_puoliso:
                        if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0:
                            suhde=kateen_puoliso/(kateen_puoliso+kateen_omat)
                        else:
                            suhde=kateen_omat/(kateen_puoliso+kateen_omat)
                    else:
                        if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0:
                            suhde=kateen_puoliso/(kateen_puoliso+kateen_omat)
                        else:
                            suhde=kateen_omat/(kateen_puoliso+kateen_omat)
                
                #print(suhde,1.0-suhde,q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'],kateen_omat,kateen_puoliso)

                etuusnetto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
                kateen_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
                brutto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
                if kateen_omat>0:
                    r2=etuusnetto_omat/kateen_omat
                else:
                    r2=1

                q[omat+'toimeentulotuki']=q['toimeentulotuki']*suhde
                q[omat+'asumistuki']=q['asumistuki']*suhde
                q[omat+'lapsilisa']=q['lapsilisa']*suhde

                if etuusnetto_omat>0:
                    r_t_e=q[omat+'toimeentulotuki']/etuusnetto_omat
                    r_a_e=q[omat+'asumistuki']/etuusnetto_omat
                    r_tt_e=q[omat+'ansiopvraha_nettonetto']/etuusnetto_omat
                    r_tt_l=q[omat+'lapsilisa']/etuusnetto_omat
                    r_tt_ko=q[omat+'kokoelake_netto']/etuusnetto_omat
                    r_tt_op=q[omat+'opintotuki_netto']/etuusnetto_omat
                    r_ko=q[omat+'kotihoidontuki_netto']/etuusnetto_omat
                    r_e=q[omat+'elatustuki']/etuusnetto_omat
                    r_pt=q[omat+'perustulo_nettonetto']/etuusnetto_omat
                else:
                    r_t_e=0
                    r_a_e=0
                    r_tt_e=0
                    r_tt_l=0
                    r_tt_ko=0
                    r_tt_op=0
                    r_ko=0
                    r_e=0
                    r_pt=0                    
            
                etuusnetto_omat+=(-r2*(q['alv']+q['pvhoito']))*suhde
                kateen_omat+=(-q['alv']-q['pvhoito'])*suhde
                q[omat+'palkkatulot_nettonetto']+=-(1-r2)*q['alv']*suhde
                omat_alv=q['alv']*suhde*r2
                q[omat+'toimeentulotuki_nettonetto']=q[omat+'toimeentulotuki']-r_t_e*omat_alv
                q[omat+'asumistuki_nettonetto']=q[omat+'asumistuki']-r_a_e*omat_alv
                q[omat+'ansiopvraha_nettonetto']+=-r_tt_e*omat_alv
                q[omat+'opintotuki_nettonetto']=q[omat+'opintotuki_netto']-r_tt_op*omat_alv
                q[omat+'kokoelake_nettonetto']=q[omat+'kokoelake_netto']-r_tt_ko*omat_alv
                q[omat+'kotihoidontuki_nettonetto']=q[omat+'kotihoidontuki_netto']-r_ko*omat_alv
                q[omat+'elatustuki_nettonetto']=q[omat+'elatustuki']-r_e*omat_alv
                q[omat+'lapsilisa_nettonetto']=q[omat+'lapsilisa']-r_tt_l*omat_alv
                q[omat+'perustulo_nettonetto']=q[omat+'perustulo_nettonetto']-r_pt*omat_alv
                q[omat+'pvhoito']=q['pvhoito']*suhde
                q[omat+'alv']=q['alv']*suhde
            
                etuusnetto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
                kateen_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
                brutto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
                if kateen_puoliso>0:
                    r2=etuusnetto_puoliso/kateen_puoliso
                else:
                    r2=1
            
                q[puoliso+'toimeentulotuki']=q['toimeentulotuki']*(1-suhde)
                q[puoliso+'asumistuki']=q['asumistuki']*(1-suhde)
                q[puoliso+'lapsilisa']=q['lapsilisa']*(1-suhde)
                if etuusnetto_puoliso>0:
                    r_t_e=q[puoliso+'toimeentulotuki']/etuusnetto_puoliso
                    r_a_e=q[puoliso+'asumistuki']/etuusnetto_puoliso
                    r_tt_e=q[puoliso+'ansiopvraha_nettonetto']/etuusnetto_puoliso
                    r_tt_l=q[puoliso+'lapsilisa']/etuusnetto_puoliso
                    r_tt_ko=q[puoliso+'kokoelake_netto']/etuusnetto_puoliso
                    r_tt_op=q[puoliso+'opintotuki_netto']/etuusnetto_puoliso
                    r_ko=q[puoliso+'kotihoidontuki_netto']/etuusnetto_puoliso
                    r_e=q[puoliso+'elatustuki']/etuusnetto_puoliso
                    r_pt=q[puoliso+'perustulo_nettonetto']/etuusnetto_puoliso
                else:
                    r_t_e=0
                    r_a_e=0
                    r_tt_e=0
                    r_tt_l=0
                    r_tt_ko=0
                    r_tt_op=0
                    r_ko=0
                    r_e=0
                    r_pt=0

                etuusnetto_puoliso+=(-r2*(q['alv']+q['pvhoito']))*(1-suhde)
                kateen_puoliso+=(-q['alv']-q['pvhoito'])*(1-suhde)
                puoliso_alv=q['alv']*(1-suhde)*r2
                q[puoliso+'palkkatulot_nettonetto']+=-(1-r2)*q['alv']*(1-suhde)
                q[puoliso+'toimeentulotuki_nettonetto']=q[puoliso+'toimeentulotuki']-r_t_e*puoliso_alv
                q[puoliso+'asumistuki_nettonetto']=q[puoliso+'asumistuki']-r_a_e*puoliso_alv
                q[puoliso+'ansiopvraha_nettonetto']+=-r_tt_e*puoliso_alv
                q[puoliso+'kokoelake_nettonetto']=q[puoliso+'kokoelake_netto']-r_tt_ko*puoliso_alv
                q[puoliso+'opintotuki_nettonetto']=q[puoliso+'opintotuki_netto']-r_tt_op*puoliso_alv
                q[puoliso+'kotihoidontuki_nettonetto']=q[puoliso+'kotihoidontuki_netto']-r_ko*puoliso_alv
                q[puoliso+'elatustuki_nettonetto']=q[puoliso+'elatustuki']-r_e*puoliso_alv
                q[puoliso+'lapsilisa_nettonetto']=q[puoliso+'lapsilisa']-r_tt_l*puoliso_alv
                q[puoliso+'perustulo_nettonetto']=q[puoliso+'perustulo_nettonetto']-r_pt*puoliso_alv
                q[puoliso+'pvhoito']=q['pvhoito']*(1-suhde)
                q[puoliso+'alv']=q['alv']*(1-suhde)
            else:
                kateen_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                brutto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                etuusnetto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                if kateen_omat>0:
                    r2=etuusnetto_omat/kateen_omat
                else:
                    r2=1
                
                kateen_omat += -q['alv']-q['pvhoito']
                
                q[omat+'toimeentulotuki']=q['toimeentulotuki']
                q[omat+'asumistuki']=q['asumistuki']
                q[omat+'lapsilisa']=q['lapsilisa']
                q[puoliso+'toimeentulotuki']=0
                q[puoliso+'asumistuki']=0
                q[puoliso+'lapsilisa']=0
                
                if etuusnetto_omat>0:
                    r_t_e=q['toimeentulotuki']/etuusnetto_omat
                    r_a_e=q['asumistuki']/etuusnetto_omat
                    r_tt_e=q['ansiopvraha_nettonetto']/etuusnetto_omat
                    r_tt_l=q['lapsilisa']/etuusnetto_omat
                    r_tt_el=q['elatustuki']/etuusnetto_omat
                    r_tt_op=q['opintotuki']/etuusnetto_omat
                    r_tt_ko=q['kokoelake']/etuusnetto_omat
                    r_ko=q[omat+'kotihoidontuki_netto']/etuusnetto_omat
                    r_e=q[omat+'elatustuki']/etuusnetto_omat
                    r_pt=q['perustulo_nettonetto']/etuusnetto_omat
                else:
                    r_t_e=0
                    r_a_e=0
                    r_tt_e=0
                    r_tt_l=0
                    r_tt_el=0
                    r_tt_op=0
                    r_tt_ko=0
                    r_pt=0
                    r_ko=0
                    r_e=0

                etuusnetto_omat+=-r2*(q['alv']+q['pvhoito'])
                q[omat+'palkkatulot_nettonetto']+=-(1-r2)*q['alv']
                omat_alv=q['alv']*r2
                q[omat+'toimeentulotuki_nettonetto']=q[omat+'toimeentulotuki']-r_t_e*omat_alv
                q[omat+'asumistuki_nettonetto']=q[omat+'asumistuki']-r_a_e*omat_alv
                q[omat+'ansiopvraha_nettonetto']+=-r_tt_e*omat_alv
                q[omat+'opintotuki_nettonetto']=q[omat+'opintotuki_netto']-r_tt_op*omat_alv
                q[omat+'kokoelake_nettonetto']=q[omat+'kokoelake_netto']-r_tt_ko*omat_alv
                q[omat+'kotihoidontuki_nettonetto']=q[omat+'kotihoidontuki_netto']-r_ko*omat_alv
                q[omat+'elatustuki_nettonetto']=q[omat+'elatustuki']-r_e*omat_alv
                q[omat+'lapsilisa_nettonetto']=q[omat+'lapsilisa']-r_tt_l*omat_alv
                q[omat+'kotihoidontuki_nettonetto']=q[omat+'kotihoidontuki_netto']-r_ko*omat_alv
                q[omat+'perustulo_nettonetto']=q[omat+'perustulo_nettonetto']-r_pt*omat_alv
                q[omat+'pvhoito']=q['pvhoito']
                q[omat+'alv']=q['alv']
                
                kateen_puoliso=0
                brutto_puoliso=0
                etuusnetto_puoliso=0
                q[puoliso+'toimeentulotuki_nettonetto']=0
                q[puoliso+'asumistuki_nettonetto']=0
                q[puoliso+'lapsilisa_nettonetto']=0
                q[puoliso+'kokoelake_nettonetto']=0
                q[puoliso+'kotihoidontuki_nettonetto']=0
                q[puoliso+'opintotuki_nettonetto']=0
                q[puoliso+'elatustuki_nettonetto']=0
                q[puoliso+'perustulo_nettonetto']=0
                q[puoliso+'pvhoito']=0
                q[puoliso+'alv']=0
                
            q['toimeentulotuki_nettonetto']=q[puoliso+'toimeentulotuki_nettonetto']+q[omat+'toimeentulotuki_nettonetto']
            q['asumistuki_nettonetto']=q[puoliso+'asumistuki_nettonetto']+q[omat+'asumistuki_nettonetto']
            q['kokoelake_nettonetto']=q[puoliso+'kokoelake_nettonetto']+q[omat+'kokoelake_nettonetto']
            q['opintotuki_nettonetto']=q[puoliso+'opintotuki_nettonetto']+q[omat+'opintotuki_nettonetto']
            q['lapsilisa_nettonetto']=q[puoliso+'lapsilisa_nettonetto']+q[omat+'lapsilisa_nettonetto']
            q['ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_nettonetto']+q[omat+'ansiopvraha_nettonetto']
            q['kotihoidontuki_nettonetto']=q[puoliso+'kotihoidontuki_nettonetto']+q[omat+'kotihoidontuki_nettonetto']
            q['elatustuki_nettonetto']=q[puoliso+'elatustuki_nettonetto']+q[omat+'elatustuki_nettonetto']
            q['palkkatulot_nettonetto']=q[puoliso+'palkkatulot_nettonetto']+q[omat+'palkkatulot_nettonetto']
            q['perustulo_nettonetto']=q[puoliso+'perustulo_nettonetto']+q[omat+'perustulo_nettonetto']
#         else: # FIXME: faster version with little extra for unemployment -modules
#             if p['aikuisia']>1:
#                 brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
#                     +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
#                     +q[puoliso+'ansiopvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']
#                 kateen_puoliso=brutto_puoliso-q[puoliso+'verot']
#                 etuusnetto_puoliso=brutto_puoliso-q[puoliso+'palkkatulot']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
#             
#                 if kateen_puoliso+kateen_omat<1e-6:
#                     suhde=0.5
#                 else: # jaetaan bruttotulojen suhteessa, mutta tasoitetaan eroja
#                     if kateen_omat>kateen_puoliso:
#                         if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0:
#                             suhde=kateen_puoliso/(kateen_puoliso+kateen_omat)
#                         else:
#                             suhde=kateen_omat/(kateen_puoliso+kateen_omat)
#                     else:
#                         if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0:
#                             suhde=kateen_puoliso/(kateen_puoliso+kateen_omat)
#                         else:
#                             suhde=kateen_omat/(kateen_puoliso+kateen_omat)
#                 
#                 #print(suhde,1.0-suhde,q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'],kateen_omat,kateen_puoliso)
#             
#                 etuusnetto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
#                 kateen_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
#                 brutto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
#                 if kateen_omat>0:
#                     r2=etuusnetto_omat/kateen_omat
#                 else:
#                     r2=1
#                 
#                 q[omat+'toimeentulotuki']=q['toimeentulotuki']*suhde
#                 q[omat+'asumistuki']=q['asumistuki']*suhde
#                 q[omat+'lapsilisa']=q['lapsilisa']*suhde
#                 q[omat+'alv']=q['alv']*suhde
#                 q[puoliso+'toimeentulotuki']=q['toimeentulotuki']*(1-suhde)
#                 q[puoliso+'asumistuki']=q['asumistuki']*(1-suhde)
#                 q[puoliso+'lapsilisa']=q['lapsilisa']*(1-suhde)
#                 q[puoliso+'alv']=q['alv']*(1-suhde)
#             else:
#                 kateen_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
#                 brutto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
#                 etuusnetto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
#                 if kateen_omat>0:
#                     r2=etuusnetto_omat/kateen_omat
#                 else:
#                     r2=1
#                 
#                 q[omat+'toimeentulotuki']=q['toimeentulotuki']
#                 q[omat+'asumistuki']=q['asumistuki']
#                 q[omat+'lapsilisa']=q['lapsilisa']
#                 q[puoliso+'toimeentulotuki']=0
#                 q[puoliso+'asumistuki']=0
#                 q[puoliso+'lapsilisa']=0
#                 q[omat+'alv']=q['alv']
#                 q[puoliso+'alv']=0

        q[omat+'netto']=kateen_omat
        q[puoliso+'netto']=kateen_puoliso
        q[omat+'etuustulo_netto']=etuusnetto_omat
        q[puoliso+'etuustulo_netto']=etuusnetto_puoliso
        
        q[omat+'etuustulo_brutto']=q[omat+'ansiopvraha']+q[omat+'opintotuki']+q[omat+'aitiyspaivaraha']\
            +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+q[omat+'asumistuki']+q[omat+'perustulo']\
            +q[omat+'toimeentulotuki']+q[omat+'kokoelake']+q[omat+'elatustuki']+q[omat+'lapsilisa'] # + sairauspaivaraha
        q[puoliso+'etuustulo_brutto']=q[puoliso+'ansiopvraha']+q[puoliso+'opintotuki']+q[puoliso+'aitiyspaivaraha']\
            +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'asumistuki']+q[puoliso+'perustulo']\
            +q[puoliso+'toimeentulotuki']+q[puoliso+'kokoelake']+q[puoliso+'elatustuki']+q[puoliso+'lapsilisa']
        q['etuustulo_brutto']=q[omat+'etuustulo_brutto']+q[puoliso+'etuustulo_brutto'] # + sairauspaivaraha
        
        kateen=q['netto']
        
        # check that omat, puoliso split is ok
        #self.check_q_netto(q,p['aikuisia'],omat,puoliso)

        return kateen,q
                
                
    def setup_puoliso_q(self,p,q,puoliso='puoliso_',alku='puoliso_',include_takuuelake=True):
        q[puoliso+'multiplier']=1
        q[puoliso+'perustulo']=0 # eläkkeelle ei makseta
        q[puoliso+'puhdas_tyoelake']=0
        q[puoliso+'kansanelake']=0
        q[puoliso+'tyoelake']=0
        q[puoliso+'takuuelake']=0
            
        q[puoliso+'perustulo']=0
        q[puoliso+'perustulo_netto']=0
        q[puoliso+'perustulo_nettonetto']=0
        
        if 'lapsikorotus_lapsia' not in p:
            p['lapsikorotus_lapsia']=p['lapsia']
        
        if p['aikuisia']>1 and p[puoliso+'alive']>0:
            q[puoliso+'palkkatulot']=p[alku+'t']
            if p[alku+'elakkeella']<1:
                q[puoliso+'palkkatulot_eielakkeella']=p[alku+'t']
            else:
                q[puoliso+'palkkatulot_eielakkeella']=0

            if p[alku+'elakkeella']>0: # vanhuuseläkkeellä
                #p[alku+'tyoton']=0
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                q[puoliso+'elake_maksussa']=p[alku+'elake_maksussa']
                q[puoliso+'tyoelake']=p[alku+'tyoelake']
                q[puoliso+'kansanelake']=p[alku+'kansanelake']
                q[puoliso+'elake_tuleva']=0
                #p[alku+'saa_ansiopaivarahaa']=0
                # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
                q[puoliso+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[puoliso+'elake_maksussa'],include_takuuelake=include_takuuelake,yksin=0,
                                            disability=p[puoliso+'disabled'],lapsia=p['lapsikorotus_lapsia'])
                q[puoliso+'takuuelake']=q[puoliso+'kokoelake']-q[puoliso+'elake_maksussa']
                q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'opintotuki']=0
                q[puoliso+'puhdas_tyoelake']=self.laske_puhdas_tyoelake_v2(p['ika'],q[puoliso+'tyoelake'],q[puoliso+'kansanelake'],disability=p[alku+'disabled'],yksin=0,lapsia=p['lapsia'])
            elif p[alku+'opiskelija']>0:
                q[puoliso+'kokoelake']=p[alku+'tyoelake']
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'tyoelake']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                q[puoliso+'opintotuki']=0
                q[puoliso+'perustulo']=self.perustulo()
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=0
                else:
                    q[puoliso+'opintotuki']=0
            else: # ei eläkkeellä     
                q[puoliso+'kokoelake']=p[alku+'tyoelake']
                q[puoliso+'opintotuki']=0
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'tyoelake']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                q[puoliso+'perustulo']=self.perustulo()
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'sairauspaivarahalla']>0:
                    q[puoliso+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=0
                elif p[alku+'tyoton']>0:
                    q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=\
                        self.ansiopaivaraha(p[alku+'tyoton'],p[alku+'vakiintunutpalkka'],p['lapsikorotus_lapsia'],p[alku+'t'],
                            p[alku+'saa_ansiopaivarahaa'],p[alku+'tyottomyyden_kesto'],p,alku=alku)
        else:
            q[puoliso+'kokoelake']=0
            q[puoliso+'opintotuki']=0
            q[puoliso+'elake_maksussa']=0
            q[puoliso+'tyoelake']=0
            q[puoliso+'elake_tuleva']=0
            q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
            q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
            q[puoliso+'palkkatulot']=0
            q[puoliso+'palkkatulot_eielakkeella']=0
                
        return q
        
    def setup_omat_q(self,p,omat='omat_',alku='',include_takuuelake=True):
        q={} # tulokset tänne
        q[omat+'multiplier']=1
        q[omat+'perustulo']=0
        q[omat+'puhdas_tyoelake']=0
        q[omat+'perustulo_netto']=0
        q[omat+'perustulo_nettonetto']=0
        q[omat+'palkkatulot']=p[alku+'t']
        q[omat+'tyoelake']=0
        q[omat+'kansanelake']=0
        q[omat+'takuuelake']=0
        
        if p[alku+'elakkeella']<1 and p[alku+'alive']>0:
            q[omat+'palkkatulot_eielakkeella']=p[alku+'t']
        else:
            q[omat+'palkkatulot_eielakkeella']=0
            
        if p[alku+'alive']<1:
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'elake_maksussa'],q[omat+'tyoelake'],q[omat+'kansanelake'],q[omat+'elake_tuleva']=0,0,0,0
            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'opintotuki']=0
            q[omat+'kokoelake'],q[omat+'takuuelake'],q[omat+'puhdas_tyoelake']=0,0,0
        elif p[alku+'elakkeella']>0: # vanhuuseläkkeellä
            #p['tyoton']=0
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'elake_maksussa']=p[alku+'elake_maksussa']
            q[omat+'tyoelake']=p[alku+'tyoelake']
            q[omat+'kansanelake']=p[alku+'kansanelake']
            q[omat+'elake_tuleva']=0
            #p['omat_saa_ansiopaivarahaa']=0
            # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
            if (p['aikuisia']>1):
                q[omat+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[omat+'elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,
                                            disability=p[alku+'disabled'],lapsia=p['lapsikorotus_lapsia'])
                q[omat+'takuuelake']=q[omat+'kokoelake']-q[omat+'elake_maksussa']
                q[omat+'puhdas_tyoelake']=self.laske_puhdas_tyoelake_v2(p['ika'],q[omat+'tyoelake'],q[omat+'kansanelake'],
                                            disability=p[alku+'disabled'],yksin=0,lapsia=p['lapsia'])
            else:
                q[omat+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[omat+'elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,
                                            disability=p[alku+'disabled'],lapsia=p['lapsikorotus_lapsia'])
                q[omat+'takuuelake']=q[omat+'kokoelake']-q[omat+'elake_maksussa']
                q[omat+'puhdas_tyoelake']=self.laske_puhdas_tyoelake_v2(p['ika'],q[omat+'tyoelake'],q[omat+'kansanelake'],
                                            disability=p[alku+'disabled'],yksin=1,lapsia=p['lapsia'])

            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'opintotuki']=0
        elif p[alku+'opiskelija']>0:
            q[omat+'elake_maksussa']=p[alku+'tyoelake']
            q[omat+'kokoelake']=p[alku+'tyoelake']
            q[omat+'tyoelake']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'opintotuki']=0
            q[omat+'perustulo']=self.perustulo()
            if p[alku+'aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p[alku+'isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
            elif p[alku+'kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=0
            else:
                q[omat+'opintotuki']=0
        else: # ei eläkkeellä     
            q[omat+'opintotuki']=0
            q[omat+'elake_maksussa']=p[alku+'elake_maksussa']
            q[omat+'kokoelake']=p[alku+'tyoelake']
            q[omat+'tyoelake']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'perustulo']=self.perustulo()
            if p[alku+'aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p[alku+'isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
            elif p[alku+'sairauspaivarahalla']>0:
                q[omat+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'vakiintunutpalkka'])
            elif p[alku+'kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=0
            elif p['tyoton']>0:
                if alku+'omavastuukerroin' in p:
                    omavastuukerroin=p[alku+'omavastuukerroin']
                else:
                    omavastuukerroin=1.0
                q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=\
                    self.ansiopaivaraha(p[alku+'tyoton'],p[alku+'vakiintunutpalkka'],p['lapsikorotus_lapsia'],p[alku+'t'],
                        p[alku+'saa_ansiopaivarahaa'],p[alku+'tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin,alku=omat)
        return q                        