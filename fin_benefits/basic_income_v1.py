"""
Pohja perustulo-mallille. 

Päivitä vastaamaan uusinta benefits-tiedostoa.

"""

import numpy as np
from .parameters import perheparametrit
import matplotlib.pyplot as plt
from .benefits import Benefits
from .labels import Labels
from scipy.interpolate import interp1d

class BasicIncomeBenefits(Benefits):
    """
    Description:
        The Finnish Earnings-related Social Security modified to include basic income

    Source:
        AT

    """
    
    def __init__(self,**kwargs):
        self.year=2018
        self.irr_vain_tyoelake=True
        self.additional_income_tax=0.0
        self.additional_tyel_premium=0.0
        self.additional_kunnallisvero=0.0
        self.additional_income_tax_high=0.0
        self.extra_ppr_factor=1.0 # kerroin peruspäivärahalle
        self.language='Finnish' # 'English'
    
        self.perustulomalli='BI'
        self.osittainen_perustulo=True
        self.perustulo_korvaa_toimeentulotuen=False
        self.koko_tyel_maksu=0.244
        self.kk_jakaja=12
                
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
        #self.setup_labels()        
        self.lab=Labels()
        self.labels=self.lab.ben_labels(self.language)
        
    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_basic_income()
        
    def setup_basic_income(self):
        if self.perustulomalli=='perustulokokeilu':
            # Kela-malli
            self.perustulo=self.laske_perustulo_Kelamalli
            self.asumistuen_suojaosa=600
            self.max_tyotulovahennys=1540
            self.max_perusvahennys=3020
            self.max_ansiotulovahennys=3570
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_2018
            self.verotus=super().verotus
            self.veroparam2018=self.veroparam2018_perustulokokeilu
            # ei muutosta verotukseen, ei aktiivimallia toteutettuna
        elif self.perustulomalli=='Kela':
            # Kela-malli
            self.perustulo=self.laske_perustulo_Kelamalli
            self.asumistuen_suojaosa=600
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.max_ansiotulovahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_Kela
        elif self.perustulomalli=='BI':
            # Artikkelin BI-malli
            self.perustulo=self.laske_perustulo_BI
            self.asumistuen_suojaosa=600
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.max_ansiotulovahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_BI
        elif self.perustulomalli in set(['vasemmistoliitto','Vasemmistoliitto']):        
            # Vasemmistoliitto
            self.perustulo=self.laske_perustulo_vasemmistoliitto
            self.asumistuen_suojaosa=600
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.max_ansiotulovahennys=0
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_vasemmistoliitto
        elif self.perustulomalli in set (['asetettava']):
            # asetettava
            self.perustulo=self.laske_perustulo_asetettava
            self.asumistuen_suojaosa=600
            #self.perustulo_asetettava=
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.max_ansiotulovahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_asetettava
            self.peruspaivaraha=self.peruspaivaraha_bi
        elif self.perustulomalli in set (['kela_asetettava']):
            # asetettava
            self.perustulo=self.laske_perustulo_asetettava
            self.asumistuen_suojaosa=600
            #self.perustulo_asetettava=
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.max_ansiotulovahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_asetettava
            self.peruspaivaraha=self.peruspaivaraha_bi
        elif self.perustulomalli in set (['vihreat','Vihreät','vihreät','Vihreat']):
            # Vihreiden malli
            self.perustulo=self.laske_perustulo_vihreat
            self.asumistuen_suojaosa=600
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.max_ansiotulovahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_vihreat
            self.peruspaivaraha=self.peruspaivaraha_bi
        elif self.perustulomalli=='tonni':        
            # Tonnin täysi perustulo
            self.perustulo=self.laske_perustulo_tonni
            self.asumistuen_suojaosa=600
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.max_ansiotulovahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_tonni
        elif self.perustulomalli=='puolitoista':        
            # Tonnin täysi perustulo
            self.perustulo=self.laske_perustulo_puolitoista
            self.asumistuen_suojaosa=600
            self.max_tyotulovahennys=0
            self.max_perusvahennys=0
            self.max_ansiotulovahennys=0
            self.veroparam2018=self.veroparam2018_perustulo
            self.valtionvero_asteikko_perustulo=self.valtionvero_asteikko_perustulo_1500
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
    
    def laske_perustulo_tonni(self):
        return 1000.0
        
    def laske_perustulo_puolitoista(self):
        return 1500.0
        
    def verotus(self,palkkatulot,muuttulot,elaketulot,lapsia,p):
        lapsivahennys=0 # poistui 2018
    
        peritytverot=0
        
        self.veroparam()
        
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

        if p['tyoton']>0:
            if p['saa_ansiopaivarahaa']>0:
                koko_tyoelakemaksu+=p['vakiintunutpalkka']*self.koko_tyel_maksu
            #else:
            #    koko_tyoelakemaksu+=1413.75*self.koko_tyel_maksu

        if p['isyysvapaalla']>0:
            koko_tyoelakemaksu+=p['vakiintunutpalkka']*self.koko_tyel_maksu
        
        if p['aitiysvapaalla']>0:
            koko_tyoelakemaksu+=p['vakiintunutpalkka']*self.koko_tyel_maksu

        if p['kotihoidontuella']>0:
            koko_tyoelakemaksu+=719.0*self.koko_tyel_maksu


        tyotvakmaksu=palkkatulot*self.tyottomyysvakuutusmaksu
        if palkkatulot>self.paivarahamaksu_raja:
            sairausvakuutus=palkkatulot*self.paivarahamaksu_pros
        else:
            sairausvakuutus=0

        peritytverot += sairausvakuutus+ptel+tyotvakmaksu
        palkkatulot = palkkatulot-sairausvakuutus-ptel-tyotvakmaksu 
    
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
        #valtionvero=ylevero
    
        peritytverot += ylevero

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
        valtionvero=self.laske_valtionvero(valtionveroperuste,p)
    
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
        max_perusvahennys,perusvahennys_pros=self.perusvahennys()
        peruste=max(0,tulot_kunnallis-ansiotulovahennys)
        if peruste<max_perusvahennys:
            perusvahennys=peruste
        else:
            perusvahennys=max(0,max_perusvahennys-perusvahennys_pros*max(0,peruste-max_perusvahennys))
        
        # Yhteensä
        kunnallisveronperuste=max(0,peruste-perusvahennys)
        peritty_sairaanhoitomaksu=max(0,palkkatulot_puhdas-perusvahennys)*self.sairaanhoitomaksu+(muuttulot+elaketulot_kunnallis)*self.sairaanhoitomaksu_etuus
        
        if tyotulovahennys_kunnallisveroon>0:
            kunnallisvero_0=kunnallisveronperuste*self.kunnallisvero_pros
            if peritty_sairaanhoitomaksu+kunnallisvero_0>0:
                kvhen=tyotulovahennys_kunnallisveroon*kunnallisvero_0/(peritty_sairaanhoitomaksu+kunnallisvero_0)
                svhen=tyotulovahennys_kunnallisveroon*peritty_sairaanhoitomaksu/(peritty_sairaanhoitomaksu+kunnallisvero_0)
            else:
                kvhen=0
                svhen=0

            kunnallisvero=max(0,kunnallisveronperuste*self.kunnallisvero_pros-kvhen)
            peritty_sairaanhoitomaksu=max(0,peritty_sairaanhoitomaksu*self.sairaanhoitomaksu-svhen)
        else:
            kunnallisvero=kunnallisveronperuste*self.kunnallisvero_pros
            
        sairausvakuutus += peritty_sairaanhoitomaksu
        
        peritytverot += peritty_sairaanhoitomaksu + kunnallisvero
        
        #palkkatulot=palkkatulot-peritty_sairaanhoitomaksu 
        # sairausvakuutus=sairausvakuutus+kunnallisveronperuste*sairaanhoitomaksu
        # yhteensä
        netto=tulot-peritytverot
    
        return netto,peritytverot,valtionvero,kunnallisvero,kunnallisveronperuste,\
               valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
               tyotulovahennys_kunnallisveroon,ptel,sairausvakuutus,tyotvakmaksu,koko_tyoelakemaksu,ylevero

    def tyotulovahennys2018(self):
        max_tyotulovahennys=self.max_tyotulovahennys/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
        ttulopros=np.array([0.120,0.0165,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2019(self):
        max_tyotulovahennys=self.max_tyotulovahennys/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
        ttulopros=np.array([0.120,0.0172,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2020(self):
        max_tyotulovahennys=self.max_tyotulovahennys/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja # 127000??
        ttulopros=np.array([0.122,0.0184,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def ansiotulovahennys2018(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=self.max_ansiotulovahennys/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2019(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=self.max_ansiotulovahennys/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2020(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=self.max_ansiotulovahennys/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah

    def perusvahennys2018(self):
        perusvahennys_pros=0.18
        max_perusvahennys=self.max_perusvahennys/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2019(self):
        perusvahennys_pros=0.18
        max_perusvahennys=self.max_perusvahennys/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2020(self):
        perusvahennys_pros=0.18
        max_perusvahennys=self.max_perusvahennys/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys

    def veroparam2018_perustulokokeilu(self):
        self.kunnallisvero_pros=0.1984 # Viitamäen raportista            
        self.tyottomyysvakuutusmaksu=0.0190 #
        self.tyontekijan_maksu=0.0635 # PTEL
        self.tyontekijan_maksu_52=0.0785+self.additional_tyel_premium # PTEL
        self.koko_tyel_maksu=0.2440+self.additional_tyel_premium # PTEL 
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0
        self.sairaanhoitomaksu_etuus=0.0147 # muut
        
        self.paivarahamaksu_pros=0.0153 # palkka
        self.paivarahamaksu_raja=14020/self.kk_jakaja    
        
        self.elakemaksu_alaraja=58.27
        self.tulonhankkimisvahennys=750/self.kk_jakaja

    def veroparam2018_perustulo(self):
        self.kunnallisvero_pros=0.0 # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0190 #
        self.tyontekijan_maksu=0.0635 # PTEL
        self.tyontekijan_maksu_52=0.0785
        self.koko_tyel_maksu=0.2440
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0
        self.sairaanhoitomaksu_etuus=0.0147 # muut
        
        self.paivarahamaksu_pros=0.0153 # palkka
        self.paivarahamaksu_raja=14020/self.kk_jakaja    
        
        self.elakemaksu_alaraja=58.27
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2019(self):
        self.kunnallisvero_pros=0.0 # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0125 #
        self.tyontekijan_maksu=0.0715 # PTEL
        self.tyontekijan_maksu_52=0.0865 # PTEL
        self.koko_tyel_maksu=0.2440
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0
        self.sairaanhoitomaksu_etuus=0.0161 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=14282/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2020(self):
        self.kunnallisvero_pros=0.0 # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0125 #
        self.tyontekijan_maksu=0.0715 # PTEL
        self.tyontekijan_maksu_52=0.0865 # PTEL
        self.koko_tyel_maksu=0.2440
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0068
        self.sairaanhoitomaksu_etuus=0.0161 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=14574/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def kotihoidontuki(self,lapsia,allekolmev,alle_kouluikaisia):
        # korvataan perustulolla
        return self.perustulo()
    
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
    
    def laske_valtionvero(self,tulot,p):
        rajat,pros=self.valtionvero_asteikko_perustulo()

        if tulot>=rajat[0]:
            vero=8/self.kk_jakaja
        else:
            vero=0

        for k in range(0,3):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[3]:
            vero=vero+(tulot-rajat[3])*pros[3]
        
        return vero

    def tyottomyysturva_suojaosa(self,suojaosamalli,p):
        if suojaosamalli==2:
            suojaosa=0
        elif suojaosamalli==3:
            suojaosa=400
        elif suojaosamalli==4:
            suojaosa=500
        elif suojaosamalli==5:
            suojaosa=600
        else:
            suojaosa=300
        
        return suojaosa
                
    def laske_tulot(self,p,tt_alennus=0,include_takuuelake=True):
        q={} # tulokset tänne
        p=self.check_p(p)
        q['sairauspaivaraha']=0
        q['puhdas_tyoelake']=0
        q['multiplier']=1
        if p['elakkeella']>0: # vanhuuseläkkeellä
            p['tyoton']=0
            q['perustulo']=0
            q['opintotuki']=0
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki']=(0,0,0)
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            p['saa_ansiopaivarahaa']=0
            q['puoliso_perustulo']=0 
            # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
            if (p['aikuisia']>1):
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,disability=p['disabled'])
            else:
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,disability=p['disabled'])

            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            #oletetaan että myös puoliso eläkkeellä
            q['puoliso_ansiopvraha']=0
            q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'])
        elif p['opiskelija']>0:
            q['kokoelake']=0
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            q['puoliso_ansiopvraha']=0
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki']=(0,0,0)
            q['opintotuki']=0
            q['perustulo']=0 # huomioitu etuuksien koossa
            q['puoliso_perustulo']=0 
            if self.osittainen_perustulo:
                if p['aitiysvapaalla']>0:
                    q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
                elif p['isyysvapaalla']>0:
                    q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
                elif p['kotihoidontuella']>0:
                    q['kotihoidontuki']=0 #self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['alle_kouluikaisia'])
                    q['perustulo']=self.perustulo()
                else:
                    q['perustulo']=self.perustulo() # ei opiskelijoille?
                    q['opintotuki']=0 #self.opintoraha(0,p)
            else:
                q['perustulo']=self.perustulo() # ei opiskelijoille?
                q['opintotuki']=0 #self.opintoraha(0,p)
        else: # ei eläkkeellä     
            q['kokoelake']=0
            q['opintotuki']=0
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            q['puoliso_ansiopvraha']=0
            q['perustulo']=0 # huomioitu etuuksien koossa
            q['puoliso_perustulo']=0 
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki']=(0,0,0)
            if self.osittainen_perustulo:
                if p['aitiysvapaalla']>0:
                    q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
                elif p['isyysvapaalla']>0:
                    q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
                elif p['kotihoidontuella']>0:
                    q['kotihoidontuki']=0 #self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['alle_kouluikaisia'])
                    q['perustulo']=self.perustulo()
                elif p['tyoton']>0:
                    if 'omavastuukerroin' in p:
                        omavastuukerroin=p['omavastuukerroin']
                    else:
                        omavastuukerroin=1.0
                    q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=\
                        self.ansiopaivaraha(p['tyoton'],p['vakiintunutpalkka'],p['lapsia'],p['t'],p['saa_ansiopaivarahaa'],
                                            p['tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin)
                    q['peruspvraha']=0
                    q['ansiopvraha']=max(0,q['ansiopvraha']-self.perustulo())
                    q['perustulo']=self.perustulo()
                else:
                    q['perustulo']=self.perustulo()
            else:
                q['perustulo']=self.perustulo() # ei opiskelijoille?
        if p['aikuisia']>1:
            if p['puoliso_elakkeella']>0: # vanhuuseläkkeellä
                p['puoliso_tyoton']=0
                q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
                q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
                q['puoliso_elake_tuleva']=0
                p['puoliso_saa_ansiopaivarahaa']=0
                # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
                q['puoliso_kokoelake']=self.laske_kokonaiselake(p['puoliso_ika'],q['puoliso_elake_maksussa'],yksin=0)
                q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=(0,0,0)
                q['puoliso_opintotuki']=0
            elif p['puoliso_opiskelija']>0:
                q['puoliso_kokoelake']=0
                q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
                q['puoliso_elake_tuleva']=0
                q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=(0,0,0)
                q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
                q['puoliso_opintotuki']=0
                if self.osittainen_perustulo:
                    if p['puoliso_aitiysvapaalla']>0:
                        q['puoliso_aitiyspaivaraha']=self.aitiysraha(p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
                    elif p['puoliso_isyysvapaalla']>0:
                        q['puoliso_isyyspaivaraha']=self.isyysraha(p['puoliso_vakiintunutpalkka'])
                    elif p['puoliso_kotihoidontuella']>0:
                        q['puoliso_kotihoidontuki']=0
                        q['puoliso_perustulo']=self.perustulo()
                    else:
                        q['puoliso_opintotuki']=0
                        q['puoliso_perustulo']=self.perustulo()
                else:
                    q['puoliso_opintotuki']=0
                    q['puoliso_perustulo']=self.perustulo()
            else: # ei eläkkeellä     
                q['puoliso_kokoelake']=0
                q['puoliso_opintotuki']=0
                q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
                q['puoliso_elake_tuleva']=0
                q['puoliso_puolison_ansiopvraha']=0
                q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=(0,0,0)
                q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
                if self.osittainen_perustulo:
                    if p['puoliso_aitiysvapaalla']>0:
                        q['puoliso_aitiyspaivaraha']=self.aitiysraha(p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
                    elif p['puoliso_isyysvapaalla']>0:
                        q['puoliso_isyyspaivaraha']=self.isyysraha(p['puoliso_vakiintunutpalkka'])
                    elif p['puoliso_sairauspaivarahalla']>0:
                        q['puoliso_sairauspaivaraha']=self.sairauspaivaraha(p['puoliso_vakiintunutpalkka'])
                    elif p['puoliso_kotihoidontuella']>0:
                        q['puoliso_kotihoidontuki']=0
                        q['puoliso_perustulo']=self.perustulo()
                    elif p['puoliso_tyoton']>0:
                        q['puoliso_ansiopvraha'],_,_=self.ansiopaivaraha(p['puoliso_tyoton'],p['puoliso_vakiintunutpalkka'],p['lapsia'],p['puoliso_tulot'],p['puoliso_saa_ansiopaivarahaa'],p['puoliso_tyottomyyden_kesto'],p)
                        q['puoliso_ansiopvraha']=max(0,q['puoliso_ansiopvraha']-self.perustulo())
                        q['puoliso_perustulo']=self.perustulo()
                else:
                    q['puoliso_perustulo']=self.perustulo()
                
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q['verot'],q['valtionvero'],q['kunnallisvero'],q['kunnallisveronperuste'],q['valtionveroperuste'],\
            q['ansiotulovahennys'],q['perusvahennys'],q['tyotulovahennys'],q['tyotulovahennys_kunnallisveroon'],\
            q['ptel'],q['sairausvakuutusmaksu'],q['tyotvakmaksu'],q['tyel_kokomaksu'],q['ylevero']=self.verotus(p['t'],\
                q['perustulo']+q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki'],\
                q['kokoelake'],p['lapsia'],p)
        #_,q['verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],q['perustulo'],0,p['lapsia'],p)
        _,q['verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p)
        _,q['verot_ilman_etuuksia_pl_pt'],valtionvero,kunnallisvero,kunnallisveronperuste,\
               valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
               tyotulovahennys_kunnallisveroon,ptel,sairausvakuutus,tyotvakmaksu,\
               koko_tyelmaksu,ylevero=self.verotus(p['t'],q['perustulo'],0,p['lapsia'],p)
        
        #print('split',valtionvero,kunnallisvero,kunnallisveronperuste,\
        #       valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
        #       tyotulovahennys_kunnallisveroon,ptel,sairausvakuutus,tyotvakmaksu)

        if (p['aikuisia']>1):
            _,q['puoliso_verot'],_,_,_,_,_,_,_,_,q['puoliso_ptel'],q['puoliso_sairausvakuutusmaksu'],\
                q['puoliso_tyotvakmaksu'],_,_=self.verotus(p['puoliso_tulot'],q['puoliso_perustulo']+q['puoliso_ansiopvraha'],0,0,p) # onko oikein että lapsia 0 tässä????
            _,q['puoliso_verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puoliso_tulot'],q['puoliso_perustulo'],0,0,p)
            _,q['puoliso_verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puoliso_tulot'],0,0,0,p)
        else:
            q['puoliso_verot_ilman_etuuksia']=0
            q['puoliso_verot_ilman_etuuksia_pl_pt']=0
            q['puoliso_verot']=0
            q['puoliso_ptel']=0
            q['puoliso_sairausvakuutusmaksu']=0
            q['puoliso_tyotvakmaksu']=0
    
        if p['aikuisia']==1 and p['saa_elatustukea']>0:
            q['elatustuki']=self.laske_elatustuki(p['lapsia'],p['aikuisia'])
        else:
            q['elatustuki']=0
        
        if p['elakkeella']>0: # ei perustuloa
            q['asumistuki']=self.elakkeensaajan_asumistuki(p['puoliso_tulot']+p['t'],q['kokoelake']+q['puoliso_ansiopvraha'],p['asumismenot_asumistuki'],p)
        else:
            q['asumistuki']=self.asumistuki(p['puoliso_tulot']+p['t'],q['ansiopvraha']+q['puoliso_ansiopvraha']+q['perustulo']+q['puoliso_perustulo'],p['asumismenot_asumistuki'],p)
            #q['asumistuki']=self.asumistuki(p['puoliso_tulot']+p['t']+q['perustulo']+q['puoliso_perustulo'],q['ansiopvraha']+q['puoliso_ansiopvraha'],p['asumismenot_asumistuki'],p)
            
        if p['lapsia']>0:
            q['pvhoito']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['kokoelake']+q['elatustuki']
                +q['ansiopvraha']+q['puoliso_ansiopvraha']+q['perustulo']+q['puoliso_perustulo'],p)
            if (p['lapsia_kotihoidontuella']>0):
                alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
                q['pvhoito']=max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
            q['pvhoito_ilman_etuuksia_pl_pt']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['elatustuki']+q['perustulo']+q['puoliso_perustulo'],p)
            q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['elatustuki'],p)
            q['lapsilisa']=self.laske_lapsilisa(p['lapsia'])
        else:
            q['pvhoito']=0
            q['pvhoito_ilman_etuuksia']=0
            q['pvhoito_ilman_etuuksia_pl_pt']=0
            q['lapsilisa']=0
    
        q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
            q['puoliso_ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
    
        q['perustulo_netto']=q['perustulo']-(q['verot_ilman_etuuksia_pl_pt']-q['verot_ilman_etuuksia'])
        q['puoliso_perustulo_netto']=q['puoliso_perustulo']-(q['puoliso_verot_ilman_etuuksia_pl_pt']-q['puoliso_verot_ilman_etuuksia'])

        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        if p['elakkeella']>0:
            q['kokoelake_netto']=q['kokoelake']-(q['verot']-q['verot_ilman_etuuksia'])
        elif p['opiskelija']>0:
            q['opintotuki_netto']=q['opintotuki']-(q['verot']-q['verot_ilman_etuuksia'])
        elif p['aitiysvapaalla']>0:
            q['aitiyspaivaraha_netto']=q['aitiyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
        elif p['isyysvapaalla']>0:
            q['isyyspaivaraha_netto']=q['isyyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
        elif p['kotihoidontuella']>0:
            q['kotihoidontuki_netto']=q['kotihoidontuki']-(q['verot']-q['verot_ilman_etuuksia']) 
        elif p['sairauspaivarahalla']>0:
            q['sairauspaivaraha_netto']=q['sairauspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
        else:
            if (p['aikuisia']>1):
                q['puoliso_ansiopvraha_netto']=q['puoliso_ansiopvraha']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia_pl_pt'])
            else:
                q['puoliso_ansiopvraha_netto']=0
            
            q['ansiopvraha_netto']=q['ansiopvraha']-(q['verot']-q['verot_ilman_etuuksia_pl_pt'])
            q['kokoelake_netto'],q['aitiyspaivaraha_netto'],q['kotihoidontuki_netto'],q['aitiyspaivaraha_netto']=(0,0,0,0)

        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia

        if q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']>0:
            suhde=max(0,q['ansiopvraha_netto']/(q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']))
            q['ansiopvraha_nettonetto']=q['ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
            q['puoliso_ansiopvraha_nettonetto']=q['puoliso_ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia_pl_pt'])
        else:
            q['ansiopvraha_nettonetto']=0
            q['puoliso_ansiopvraha_nettonetto']=0
        
        if q['perustulo_netto']+q['puoliso_perustulo_netto']>0:
            suhde=max(0,q['puoliso_perustulo_netto']/(q['puoliso_perustulo_netto']+q['perustulo_netto']))
            q['puoliso_perustulo_nettonetto']=q['puoliso_perustulo_netto']-suhde*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
            q['perustulo_nettonetto']=q['perustulo_netto']-(1-suhde)*(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia'])
        else:
            q['perustulo_nettonetto']=0
            q['puoliso_perustulo_nettonetto']=0

        if (not self.osittainen_perustulo) or self.perustulo_korvaa_toimeentulotuen: # toimeentulotuki korvattu perustulolla
            q['toimeentulotuki']=0
        else: # ei korvattu
            if p['opiskelija']>0:
                q['toimeentulotuki']=0
            else:
                q['toimeentulotuki']=self.toimeentulotuki(p['t'],q['verot_ilman_etuuksia'],p['puoliso_tulot'],q['puoliso_verot_ilman_etuuksia'],\
                    q['elatustuki']+q['opintotuki']+q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['asumistuki']+q['lapsilisa']\
                    +q['kokoelake_netto']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['perustulo_netto']+q['puoliso_perustulo_netto'],\
                    0,p['asumismenot_toimeentulo'],q['pvhoito'],p)

        #print(q['ansiopvraha']+q['perustulo'],q['ansiopvraha_netto']+q['perustulo_netto'],-(q['pvhoito_ilman_etuuksia_pl_pt']-q['pvhoito_ilman_etuuksia']),-(q['verot_ilman_etuuksia_pl_pt']-q['verot_ilman_etuuksia']),-(q['verot']-q['verot_ilman_etuuksia_pl_pt']))


        kateen=q['perustulo']+q['puoliso_perustulo']+q['opintotuki']+q['kokoelake']+p['puoliso_tulot']+p['t']\
            +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']+q['ansiopvraha']\
            +q['puoliso_ansiopvraha']+q['elatustuki']-q['puoliso_verot']-q['verot']-q['pvhoito']+q['lapsilisa']
        q['kateen']=kateen
        q['perhetulot_netto']=p['puoliso_tulot']+p['t']-q['verot_ilman_etuuksia']-q['puoliso_verot_ilman_etuuksia']\
            -q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['etuustulo_netto']=q['puoliso_perustulo_netto']+q['perustulo_netto']+q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']\
            +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
            -(q['pvhoito']-q['pvhoito_ilman_etuuksia'])+q['lapsilisa']
        q['etuustulo_brutto']=q['puoliso_perustulo']+q['perustulo']+q['ansiopvraha']+q['puoliso_ansiopvraha']\
            +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
            +q['lapsilisa']+q['kokoelake']
        q['omattulot_netto']=p['t']-q['verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['palkkatulot']=p['t']
        if p['elakkeella']<1:
            q['palkkatulot_eielakkeella']=p['t']
        else:
            q['palkkatulot_eielakkeella']=0        

        asumismeno=p['asumismenot_asumistuki']
        q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        
        
        q['puoliso_palkkatulot']=p['puoliso_tulot']
        q['puoliso_tulot_netto']=p['puoliso_tulot']-q['puoliso_verot_ilman_etuuksia']
        
        #print(p['t'],kateen,q['perhetulot_netto'],q['etuustulo_netto'],q['perhetulot_netto']+q['etuustulo_netto'],q['toimeentulotuki'])
        #print(q['puoliso_perustulo_netto'],q['perustulo_netto'],q['ansiopvraha_netto'],q['puoliso_ansiopvraha_netto'],
        #    q['aitiyspaivaraha'],q['isyyspaivaraha'],q['kotihoidontuki'],
        #    q['asumistuki'],q['toimeentulotuki'],
        #    (q['pvhoito']-q['pvhoito_ilman_etuuksia']),q['lapsilisa'])
        #print(q['pvhoito'],q['pvhoito_ilman_etuuksia'])
        
        return kateen,q

        
    def setup_puoliso_q(self,p,q,puoliso='puoliso_',alku='puoliso_'):
        q[puoliso+'puhdas_tyoelake']=0
        q[puoliso+'perustulo']=0
        q[puoliso+'perustulo_netto']=0
        q[puoliso+'perustulo_nettonetto']=0
        
        if p['aikuisia']>1:
            q[puoliso+'palkkatulot']=p[alku+'t']
            if p['puoliso_elakkeella']<1:
                q[puoliso+'palkkatulot_eielakkeella']=p[alku+'t']
            else:
                q[puoliso+'palkkatulot_eielakkeella']=0

            if p[alku+'elakkeella']>0: # vanhuuseläkkeellä
                #p[alku+'tyoton']=0
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                #p[alku+'saa_ansiopaivarahaa']=0
                # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
                q[puoliso+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[puoliso+'elake_maksussa'],yksin=0)
                q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'opintotuki']=0
                q[puoliso+'puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p[alku+'tyoelake'],disability=p[alku+'disabled'])
            elif p[alku+'opiskelija']>0:
                q[puoliso+'kokoelake']=0
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                q[puoliso+'opintotuki']=0
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
                else:
                    q[puoliso+'opintotuki']=self.opintoraha(0,p)
            else: # ei eläkkeellä     
                q[puoliso+'kokoelake']=0
                q[puoliso+'opintotuki']=0
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                q[puoliso+'puolison_ansiopvraha']=0
                q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'sairauspaivarahalla']>0:
                    q[puoliso+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['alle_3v'],p['alle_kouluikaisia'])
                elif p[alku+'tyoton']>0:
                    q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=\
                        self.ansiopaivaraha(p[alku+'tyoton'],p[alku+'vakiintunutpalkka'],p['lapsia'],p[alku+'t'],
                            p[alku+'saa_ansiopaivarahaa'],p[alku+'tyottomyyden_kesto'],p,alku=alku)
        else:
            q[puoliso+'kokoelake']=0
            q[puoliso+'opintotuki']=0
            q[puoliso+'elake_maksussa']=0
            q[puoliso+'elake_tuleva']=0
            q[puoliso+'puolison_ansiopvraha']=0
            q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
            q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
            q[puoliso+'palkkatulot']=0
            q[puoliso+'palkkatulot_eielakkeella']=0
                
        return q
        
    def setup_omat_q(self,p,omat='omat_',alku='',include_takuuelake=True):
        q={} # tulokset tänne
        q['multiplier']=1
        q[omat+'perustulo']=0
        q[omat+'puhdas_tyoelake']=0
        q[omat+'perustulo_netto']=0
        q[omat+'perustulo_nettonetto']=0
        q[omat+'palkkatulot']=p[alku+'t']
        
        if p[alku+'elakkeella']<1:
            q[omat+'palkkatulot_eielakkeella']=p[alku+'t']
        else:
            q[omat+'palkkatulot_eielakkeella']=0
            
        if p['elakkeella']>0: # vanhuuseläkkeellä
            #p['tyoton']=0
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'elake_maksussa']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            #p['omat_saa_ansiopaivarahaa']=0
            # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
            if (p['aikuisia']>1):
                q[omat+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[omat+'elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,disability=p[alku+'disabled'])
            else:
                q[omat+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[omat+'elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,disability=p[alku+'disabled'])

            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'opintotuki']=0
            q[omat+'puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p[alku+'tyoelake'],disability=p[alku+'disabled'])
        elif p['opiskelija']>0:
            q[omat+'elake_maksussa']=p[alku+'tyoelake']
            q[omat+'kokoelake']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'opintotuki']=0
            if p['aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p['isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
            elif p['kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            else:
                q[omat+'opintotuki']=self.opintoraha(0,p)
        else: # ei eläkkeellä     
            q[omat+'opintotuki']=0
            q[omat+'elake_maksussa']=p[alku+'tyoelake']
            q[omat+'kokoelake']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            if p['aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p['isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
            elif p['sairauspaivarahalla']>0:
                q[omat+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'vakiintunutpalkka'])
            elif p['kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            elif p['tyoton']>0:
                if alku+'omavastuukerroin' in p:
                    omavastuukerroin=p[alku+'omavastuukerroin']
                else:
                    omavastuukerroin=1.0
                q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=\
                    self.ansiopaivaraha(p[alku+'tyoton'],p[alku+'vakiintunutpalkka'],p['lapsia'],p[alku+'t'],
                        p[alku+'saa_ansiopaivarahaa'],p[alku+'tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin,alku=omat)
        return q        
        
    def laske_tulot_v2(self,p,tt_alennus=0,include_takuuelake=True,omat='omat_',omatalku='',puoliso='puoliso_'):
        '''
        v4:ää varten tehty tulonlaskenta
        - eroteltu paremmin omat ja puolison tulot ja etuudet 
        - perusmuuttujat ovat summamuuttujia
        '''
        p=self.check_p(p)

        q=self.setup_omat_q(p,omat=omat,alku=omatalku,include_takuuelake=include_takuuelake)
        q=self.setup_puoliso_q(p,q,puoliso=puoliso)
        
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q[omat+'verot'],q[omat+'valtionvero'],q[omat+'kunnallisvero'],q[omat+'kunnallisveronperuste'],q[omat+'valtionveroperuste'],\
            q[omat+'ansiotulovahennys'],q[omat+'perusvahennys'],q[omat+'tyotulovahennys'],q[omat+'tyotulovahennys_kunnallisveroon'],\
            q[omat+'ptel'],q[omat+'sairausvakuutusmaksu'],q[omat+'tyotvakmaksu'],q[omat+'tyel_kokomaksu'],q[omat+'ylevero']=\
            self.verotus(q[omat+'palkkatulot'],q[omat+'ansiopvraha']+q[omat+'aitiyspaivaraha']+q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+q[omat+'sairauspaivaraha']+q[omat+'opintotuki'],
                q[omat+'kokoelake'],p['lapsia'],p,alku=omatalku)
        _,q[omat+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p,alku=omatalku)

        if p['aikuisia']>1:
            _,q[puoliso+'verot'],q[puoliso+'valtionvero'],q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveronperuste'],q[puoliso+'valtionveroperuste'],\
            q[puoliso+'ansiotulovahennys'],q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon'],\
            q[puoliso+'ptel'],q[puoliso+'sairausvakuutusmaksu'],q[puoliso+'tyotvakmaksu'],q[puoliso+'tyel_kokomaksu'],q[puoliso+'ylevero']=\
                self.verotus(q[puoliso+'palkkatulot'],
                    q[puoliso+'ansiopvraha']+q[puoliso+'aitiyspaivaraha']+q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'sairauspaivaraha']+q[puoliso+'opintotuki'],
                    q[puoliso+'kokoelake'],0,p,alku=puoliso) # onko oikein että lapsia 0 tässä????
            _,q[puoliso+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],0,0,0,p,alku=puoliso)
        else:
            q[puoliso+'verot_ilman_etuuksia']=0
            q[puoliso+'verot']=0
            q[puoliso+'valtionvero']=0
            q[puoliso+'kunnallisvero']=0
            q[puoliso+'tyotulovahennys']=0
            q[puoliso+'ptel']=0
            q[puoliso+'sairausvakuutusmaksu']=0
            q[puoliso+'tyotvakmaksu']=0
            q[puoliso+'tyel_kokomaksu']=0
            q[puoliso+'ylevero']=0
            
        # elatustuki (ei vaikuta kannnusteisiin, vain tuloihin, koska ei yhteensovitusta)
        if p['aikuisia']==1 and p['saa_elatustukea']>0:
            q[omat+'elatustuki']=self.laske_elatustuki(p['lapsia'],p['aikuisia'])
        else:
            q[omat+'elatustuki']=0
        
        q[puoliso+'elatustuki']=0
        
        q=self.summaa_q(p,q,omat=omat,puoliso=puoliso)

        if p['elakkeella']>0:
            q['asumistuki']=self.elakkeensaajan_asumistuki(q['palkkatulot'],q['kokoelake'],p['asumismenot_asumistuki'],p)
        else:
            q['asumistuki']=self.asumistuki(q['palkkatulot'],q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
                                p['asumismenot_asumistuki'],p)
            
        if p['lapsia']>0:
            if p['aikuisia']>1:
                if p['aitiysvapaalla']>0 or p['isyysvapaalla']>0 or p['kotihoidontuella']>0 or p['puoliso_aitiysvapaalla']>0 or p['puoliso_isyysvapaalla']>0 or p['puoliso_kotihoidontuella']>0:
                    ei_pvhoitoa=True
                else:
                    ei_pvhoitoa=False
            else:
                if p['aitiysvapaalla']>0 or p['isyysvapaalla']>0 or p['kotihoidontuella']>0:
                    ei_pvhoitoa=True
                else:
                    ei_pvhoitoa=False
        
            if p['aitiysvapaalla']>0 or p['isyysvapaalla']>0 or p['kotihoidontuella']>0 or p['puoliso_aitiysvapaalla']>0 or p['puoliso_isyysvapaalla']>0 or p['puoliso_kotihoidontuella']>0:
                q['pvhoito']=0
                q['pvhoito_ilman_etuuksia']=0
            else:
                q['pvhoito']=self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['sairauspaivaraha'],p)
                if (p['lapsia_kotihoidontuella']>0):
                    alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
                    q['pvhoito']=max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
                q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_t']+p['t']+q['elatustuki'],p)
                
            if p['aikuisia']==1:
                yksinhuoltajakorotus=1
            else:
                yksinhuoltajakorotus=0
            q['lapsilisa']=self.laske_lapsilisa(p['lapsia'],yksinhuoltajakorotus=yksinhuoltajakorotus)
        else:
            q['pvhoito']=0
            q['pvhoito_ilman_etuuksia']=0
            q['lapsilisa']=0
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
            q[puoliso+'ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
        q[omat+'kokoelake_netto'],q[omat+'isyyspaivaraha_netto'],q[omat+'ansiopvraha_netto'],q[omat+'aitiyspaivaraha_netto'],q[omat+'sairauspaivaraha_netto'],\
            q[omat+'opintotuki_netto'],q[omat+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
        q[puoliso+'kokoelake_netto'],q[puoliso+'isyyspaivaraha_netto'],q[puoliso+'ansiopvraha_netto'],q[puoliso+'aitiyspaivaraha_netto'],q[puoliso+'sairauspaivaraha_netto'],\
            q[puoliso+'opintotuki_netto'],q[puoliso+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
            
        if p['elakkeella']>0:
            q[omat+'kokoelake_netto']=q[omat+'kokoelake']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
        elif p['opiskelija']>0:
            q[omat+'opintotuki_netto']=q[omat+'opintotuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
        elif p['aitiysvapaalla']>0:
            q[omat+'aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        elif p['isyysvapaalla']>0:
            q[omat+'isyyspaivaraha_netto']=q[omat+'isyyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        elif p['kotihoidontuella']>0:
            q[omat+'kotihoidontuki_netto']=q[omat+'kotihoidontuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        elif p['sairauspaivarahalla']>0:
            q[omat+'sairauspaivaraha_netto']=q[omat+'sairauspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        else:
            q[omat+'ansiopvraha_netto']=q[omat+'ansiopvraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])

        if p['puoliso_elakkeella']>0:
            q[puoliso+'kokoelake_netto']=q[puoliso+'kokoelake']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
        elif p['puoliso_opiskelija']>0:
            q[puoliso+'opintotuki_netto']=q[puoliso+'opintotuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
        elif p['puoliso_aitiysvapaalla']>0:
            q[puoliso+'aitiyspaivaraha_netto']=q[puoliso+'aitiyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        elif p['puoliso_isyysvapaalla']>0:
            q[puoliso+'isyyspaivaraha_netto']=q[puoliso+'isyyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        elif p['puoliso_kotihoidontuella']>0:
            q[puoliso+'kotihoidontuki_netto']=q[puoliso+'kotihoidontuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        elif p['puoliso_sairauspaivarahalla']>0:
            q[puoliso+'sairauspaivaraha_netto']=q[puoliso+'sairauspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        else:
            q[puoliso+'ansiopvraha_netto']=q[puoliso+'ansiopvraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])

        q['ansiopvraha_netto']=q[omat+'ansiopvraha_netto']+q[puoliso+'ansiopvraha_netto']
        q['kokoelake_netto']=q[omat+'kokoelake_netto']+q[puoliso+'kokoelake_netto']
        q['aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha_netto']+q[puoliso+'aitiyspaivaraha_netto']
        q['isyyspaivaraha_netto']=q[omat+'isyyspaivaraha_netto']+q[puoliso+'isyyspaivaraha_netto']
        q['kotihoidontuki_netto']=q[omat+'kotihoidontuki_netto']+q[puoliso+'kotihoidontuki_netto']
        q['sairauspaivaraha_netto']=q[omat+'sairauspaivaraha_netto']+q[puoliso+'sairauspaivaraha_netto']
            
        if (p['isyysvapaalla']>0 or p['aitiysvapaalla']>0) and p['tyoton']>0:
            print('error: vanhempainvapaalla & työtön ei toteutettu')
    
        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia

        if q['ansiopvraha_netto']>0:
            suhde=max(0,q[omat+'ansiopvraha_netto']/q['ansiopvraha_netto'])
            q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
            q[puoliso+'ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
            q['ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_nettonetto']+q[omat+'ansiopvraha_nettonetto']
        else:
            q[omat+'ansiopvraha_nettonetto']=0
            q[puoliso+'ansiopvraha_nettonetto']=0
            q['ansiopvraha_nettonetto']=0

        if p['aikuisia']<2:
            if p['opiskelija']>0:
                q['toimeentulotuki']=0
            else:
                # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
                q['toimeentulotuki']=self.toimeentulotuki(p['t'],q[omat+'verot_ilman_etuuksia'],0,q[puoliso+'verot_ilman_etuuksia'],\
                    q['elatustuki']+q['opintotuki']+q['ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                    +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki'],\
                    0,p['asumismenot_toimeentulo'],q['pvhoito'],p)
        else:
            if p['opiskelija']>0 and p['puoliso_opiskelija']>0:
                q['toimeentulotuki']=0
            else:
                # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
                q['toimeentulotuki']=self.toimeentulotuki(p['t'],q[omat+'verot_ilman_etuuksia'],p['puoliso_t'],q[puoliso+'verot_ilman_etuuksia'],\
                    q['elatustuki']+q['opintotuki']+q['ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                    +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki'],\
                    0,p['asumismenot_toimeentulo'],q['pvhoito'],p)

        # sisältää sekä omat että puolison tulot ja menot
        kateen=q['opintotuki']+q['kokoelake']+q['palkkatulot']+q['aitiyspaivaraha']+q['isyyspaivaraha']\
            +q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
            +q['ansiopvraha']+q['elatustuki']-q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']

        brutto_omat=q[omat+'opintotuki']+q[omat+'kokoelake']+q[omat+'palkkatulot']+q[omat+'aitiyspaivaraha']\
            +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+\
            +q[omat+'ansiopvraha']+q[omat+'elatustuki']+q[omat+'sairauspaivaraha']
        kateen_omat=brutto_omat-q[omat+'verot']
                    
        q['kateen']=kateen # tulot yhteensä perheessä
        q['etuustulo_netto']=q['ansiopvraha_netto']+q['opintotuki']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimeentulotuki']+q['kokoelake']+q['elatustuki']+q['lapsilisa']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])-(q['verot']-q['verot_ilman_etuuksia'])
            
        asumismeno=p['asumismenot_asumistuki']
            
        q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        
        # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
        q['netto']=max(0,kateen-q['alv'])
        
        if p['aikuisia']>1:
            brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
                +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                +q[puoliso+'ansiopvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']
            kateen_puoliso=brutto_puoliso-q[puoliso+'verot']
            
            if kateen_puoliso+kateen_omat<1e-6:
                suhde=0.5
            else: # jaetaan bruttotulojen suhteessa
                suhde=kateen_omat/(kateen_puoliso+kateen_omat)
                
            kateen_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])*suhde
            brutto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
            q[omat+'toimeentulotuki']=q['toimeentulotuki']*suhde
            q[omat+'asumistuki']=q['asumistuki']*suhde
            q[omat+'pvhoito']=q['pvhoito']*suhde
            q[omat+'lapsilisa']=q['lapsilisa']*suhde
            q[omat+'alv']=q['alv']*suhde
            kateen_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])*(1-suhde)
            brutto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
            q[puoliso+'toimeentulotuki']=q['toimeentulotuki']*(1-suhde)
            q[puoliso+'asumistuki']=q['asumistuki']*(1-suhde)
            q[puoliso+'pvhoito']=q['pvhoito']*(1-suhde)
            q[puoliso+'lapsilisa']=q['lapsilisa']*(1-suhde)
            q[puoliso+'alv']=q['alv']*(1-suhde)
            #if kateen_puoliso<1e-6:
            #    print(kateen_omat,kateen_puoliso)
        else:
            kateen_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito']
            brutto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
            q[omat+'toimeentulotuki']=q['toimeentulotuki']
            q[omat+'asumistuki']=q['asumistuki']
            q[omat+'pvhoito']=q['pvhoito']
            q[omat+'lapsilisa']=q['lapsilisa']
            q[omat+'alv']=q['alv']
            kateen_puoliso=0
            brutto_puoliso=0
            q[puoliso+'toimeentulotuki']=0
            q[puoliso+'asumistuki']=0
            q[puoliso+'pvhoito']=0
            q[puoliso+'lapsilisa']=0
            q[puoliso+'alv']=0

        q[omat+'netto']=kateen_omat
        q[puoliso+'netto']=kateen_puoliso

        #q[omat+'etuustulo_brutto']=brutto_omat
        #q[puoliso+'etuustulo_brutto']=brutto_puoliso
        
        q[omat+'etuustulo_brutto']=q[omat+'ansiopvraha']+q[omat+'opintotuki']+q[omat+'aitiyspaivaraha']+q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+q[omat+'asumistuki']\
            +q[omat+'toimeentulotuki']+q[omat+'kokoelake']+q[omat+'elatustuki']+q[omat+'lapsilisa'] # + sairauspaivaraha
        q[puoliso+'etuustulo_brutto']=q[puoliso+'ansiopvraha']+q[puoliso+'opintotuki']+q[puoliso+'aitiyspaivaraha']+q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'asumistuki']\
            +q[puoliso+'toimeentulotuki']+q[puoliso+'kokoelake']+q[puoliso+'elatustuki']+q[puoliso+'lapsilisa']
        q['etuustulo_brutto']=q[omat+'etuustulo_brutto']+q[puoliso+'etuustulo_brutto'] # + sairauspaivaraha
        
        kateen=q['netto']
        
        # check that omat, puoliso split is ok
        #self.check_q_netto(q,p['aikuisia'],omat,puoliso)

        return kateen,q        
    def Kela_kustannusneutraali_veroaste(self,perustulo):
        '''
        Lähteestä Honkanen, Simanainen, sivu 8, Kuvio 1
        '''
        a=[400,800] # e/kk
        b=[0.40,0.525]
        f=interp1d(a,b,fill_value='extrapolate')
        ip=f(perustulo)
        return max(b[0],ip)
                
    def opintoraha(self,palkka,p):
        if p['lapsia']>0:
            tuki=self.perustulo()+650*0.4 # opintolainahyvitys mukana
        else:
            tuki=self.perustulo()+650*0.4 # opintolainahyvitys mukana
            
        if palkka>667+222/12: # oletetaan että täysiaikainen opiskelija
            tuki=self.perustulo() # ei opintolainaa
            
        return tuki
                
    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0,omavastuukerroin=None):
        if not self.osittainen_perustulo:
            perus=self.perustulo()
            tuki=self.perustulo()
            ansiopaivarahamaara=0   
            
            return tuki,ansiopaivarahamaara,perus
    
        ansiopvrahan_suojaosa=p['ansiopvrahan_suojaosa']
        lapsikorotus=p['ansiopvraha_lapsikorotus']
    
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
                            
            if saa_ansiopaivarahaa>0: 
                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-sotumaksu)     
        
                if vakpalkka>taite:
                    tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus    
                else:
                    tuki2=0.45*max(0,vakpalkka-perus)+perus    

                tuki2=tuki2+lapsikorotus[min(lapsia,3)]    
                tuki2=tuki2*ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)    
        
                perus=self.perustulo()
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavattulo=max(0,tyotaikaisettulot-suojaosa)    
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavattulo)  
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,perus)  

                tuki=ansiopaivarahamaara
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)
                tuki=max(perus,tuki)     # voi tulla vastaan pienillä tasoilla4
            else:
                ansiopaivarahamaara=0    
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)
                tuki=perus    
        else:
            perus=self.perustulo()
            tuki=self.perustulo()
            ansiopaivarahamaara=0   
            
        return tuki,ansiopaivarahamaara,perus

    def soviteltu_peruspaivaraha(self,lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p):
        suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)

        pvraha=self.peruspaivaraha(lapsia)
        vahentavattulo=max(0,tyotaikaisettulot-suojaosa)
        tuki=max(self.perustulo(),max(0,pvraha-0.5*vahentavattulo))
    
        return tuki

    def peruspaivaraha_bi(self,lapsia):
        return self.perustulo()
        
    # tmtuki samankokoinen
    def peruspaivaraha2018(self,lapsia):
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.23     # e/pv
        elif lapsia==2:
            lisa=7.68     # e/pv
        else:
            lisa=9.90     # e/pv
        
        pvraha=21.5*lisa+self.perustulo()
        return pvraha
        
    # tmtuki samankokoinen
    def peruspaivaraha2019(self,lapsia):
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.23     # e/pv
        elif lapsia==2:
            lisa=7.68     # e/pv
        else:
            lisa=9.90     # e/pv
        
        pvraha=21.5*lisa+self.perustulo()
    
        return pvraha

    # tmtuki samankokoinen
    def peruspaivaraha2020(self,lapsia):
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.28     # e/pv
        elif lapsia==2:
            lisa=7.76     # e/pv
        else:
            lisa=10.00     # e/pv
        
        pvraha=21.5*lisa+self.perustulo()
    
        return pvraha

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

        if not self.osittainen_perustulo:
            return 0
    
        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=self.asumistuen_suojaosa*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
    
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
        max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3
        
        if not self.osittainen_perustulo:
            return 0

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
    
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
        max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        if not self.osittainen_perustulo:
            return 0

        prosentti=0.8 # vastaa 80 %
        suojaosa=600*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
    
        return tuki
        
    def aitiysraha2019(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=self.perustulo()
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12 
                
            raha=max(minimi,0.9*min(taite1,vakiintunutpalkka)+0.325*max(vakiintunutpalkka-taite1,0))
        else: 
            minimi=self.perustulo()
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12 
                        
            raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha        
        
    def isyysraha_perus(self,vakiintunutpalkka):
        if self.year==2018:
            minimi=self.perustulo() #27.86*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2019:
            minimi=self.perustulo() #27.86*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12  
        else:
            minimi=self.perustulo() #27.86*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12  
                        
        raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha        