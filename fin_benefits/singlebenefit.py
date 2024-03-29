"""

    benefits
    
    implements the single benefit scheme


"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite
from .labels import Labels
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
from .benefits import Benefits

class SingleBenefit(Benefits):
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
        self.include_perustulo=False
        
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
            elif key=='valtionverotaso':
                if value is not None:
                    self.valtionverotaso=value
                    
        print(f'Single benefit scheme')
                    
        super().__init__(**kwargs)
        self.setup_single_benefit()
    
        # choose the correct set of benefit functions for computations
        self.set_year(self.year)
        self.lab=Labels()
        self.labels=self.lab.ben_labels(self.language)
        
        if self.vaihtuva_tyelmaksu:
            self.get_tyelpremium()
            
        
    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_single_benefit()
        
    def veroparam2018_single_benefit(self):
        super().veroparam2018()

    def veroparam2019_single_benefit(self):
        super().veroparam2019()

    def veroparam2020_single_benefit(self):
        super().veroparam2020()

    def veroparam2021_single_benefit(self):
        super().veroparam2021()

    def veroparam2022_single_benefit(self):
        super().veroparam2022()

    def setup_single_benefit(self):
        if self.year==2018:
            self.veroparam2018=self.veroparam2018_single_benefit
            self.veroparam=self.veroparam2018
            self.nykyperuspaivaraha=super().peruspaivaraha2018
        elif self.year==2019:
            self.veroparam2019=self.veroparam2019_single_benefit
            self.veroparam=self.veroparam2019
            self.nykyperuspaivaraha=super().peruspaivaraha2019
        elif self.year==2020:
            self.veroparam2020=self.veroparam2020_single_benefit
            self.veroparam=self.veroparam2020
            self.nykyperuspaivaraha=super().peruspaivaraha2020
        elif self.year==2021:
            self.veroparam2021=self.veroparam2021_single_benefit
            self.veroparam=self.veroparam2021
            self.nykyperuspaivaraha=super().peruspaivaraha2021
        elif self.year==2022:
            self.veroparam2022=self.veroparam2022_single_benefit
            self.veroparam=self.veroparam2022
            self.nykyperuspaivaraha=super().peruspaivaraha2022
        elif self.year==2023:
            self.veroparam2023=self.veroparam2023_single_benefit
            self.veroparam=self.veroparam2023
            self.nykyperuspaivaraha=super().peruspaivaraha2023
        
    def kotihoidontuki(self,lapsia,allekolmev,alle_kouluikaisia):
        # korvataan perustulolla
        return self.perustulo()
    
    def valtionvero_asteikko_perustulo_1500(self):
        rajat=np.array([12*1500,50000,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.79,0.79,0.79,0.79]) # 800 e/kk # tasavero 52,5 %
        return rajat,pros        
        
    def universalcredit(self,palkka):
        return max(0.0,742.0 - 0.5*palkka)
        
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,
                             muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.0,alennus=0):
                             
        return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,
                             muuttulot,verot,0*asumismenot,muutmenot,p,omavastuuprosentti=omavastuuprosentti,alennus=alennus)
        
    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,peruspvraha):
        if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
            return max(0,vakpalkka-tyotaikaisettulot) 
            
        return ansiopaivarahamaara   
        
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
                perus=self.universalcredit(0)
                vakpalkka=vakiintunutpalkka*(1-self.sotumaksu)
                
                if vakpalkka>taite:
                    tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus
                else:
                    tuki2=0.45*max(0,vakpalkka-perus)+perus

                tuki2=tuki2+lapsikorotus[min(lapsia,3)]
                tuki2=tuki2*ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa=0 #self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)    

                perus=self.universalcredit(0)    
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)
        
                vahentavat_tulot=max(0,tyotaikaisettulot-suojaosa) 
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavat_tulot)
                soviteltuperus=self.universalcredit(tyotaikaisettulot)
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,soviteltuperus)

                perus=self.universalcredit(tyotaikaisettulot)
                tuki=omavastuukerroin*max(0,ansiopaivarahamaara-perus)
                ansiopaivarahamaara=omavastuukerroin*max(0,ansiopaivarahamaara-perus)
                perus=0
            else:
                # perustulo korvaa peruspäivärahan
                ansiopaivarahamaara=0    
                perus=0 # self.universalcredit(tyotaikaisettulot)    
                tuki=0 # perus
        else:
            perus=0    
            tuki=0    
            ansiopaivarahamaara=0   

        return tuki,ansiopaivarahamaara,perus

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
        valtionvero+=self.raippavero(elaketulot_valtio)
        
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
        perusvahennys_pros,max_perusvahennys=self.perusvahennys()
        peruste=max(0,tulot_kunnallis-ansiotulovahennys)
        if peruste<max_perusvahennys:
            perusvahennys=peruste
        else:
            perusvahennys=max(0,max_perusvahennys-perusvahennys_pros*max(0,peruste-max_perusvahennys))
            
        # Yhteensä
        kunnallisveronperuste=max(0,peruste-perusvahennys)
        
        # korotettu maksuperuste puuttuu? =max(0,palkkatulot-peritty_sairaanhoitomaksu)*korotus
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
            peritty_sairaanhoitomaksu=max(0,peritty_sairaanhoitomaksu-svhen)
        else:
            kunnallisvero=kunnallisveronperuste*self.kunnallisvero_pros
            
        sairausvakuutusmaksu += peritty_sairaanhoitomaksu
        
        peritytverot += peritty_sairaanhoitomaksu + kunnallisvero
        
        #palkkatulot=palkkatulot-peritty_sairaanhoitomaksu 
        # sairausvakuutusmaksu=sairausvakuutusmaksu+kunnallisveronperuste*sairaanhoitomaksu
        # yhteensä
        netto=tulot-peritytverot
        
        d1=peritytverot
        d2=valtionvero+kunnallisvero+ptel+tyotvakmaksu+ylevero+sairausvakuutusmaksu
        
        if np.abs(d2-d1)>1e-6:
            print('verotus',d2-d1)

        return netto,peritytverot,valtionvero,kunnallisvero,kunnallisveronperuste,\
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
    
    def valtionvero_asteikko_2018(self):
        rajat=np.array([17200,25700,42400,74200])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.06,0.1725,0.2125,0.3125+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.3125+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros
    
    def valtionvero_asteikko_2019(self):
        rajat=np.array([17600,26400,43500,76100])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.06,0.1725,0.2125,0.3125+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.3125+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros

    def valtionvero_asteikko_2020(self):
        rajat=np.array([18100,27200,44800,78500])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.06,0.1725,0.2125,0.3125+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.3125+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros

    def valtionvero_asteikko_2021(self):
        rajat=np.array([18600,27900,45900,80500])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.06,0.1725,0.2125,0.3125+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.3125+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros
        
    def valtionvero_asteikko_2022(self):
        rajat=np.array([19200,28700,47300,82900])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.06,0.1725,0.2125,0.3125+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.3125+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros
        
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
        p=super().check_p(p)

        return p
        
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
        suojaosa=300
        tulot=palkkatulot+muuttulot-suojaosa
        tuki=max(0,(min(max_meno,vuokra)-0.5*tulot)*prosentti)

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
        max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=300
        tulot=palkkatulot+muuttulot-suojaosa
        tuki=max(0,(min(max_meno,vuokra)-0.5*tulot)*prosentti)

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
        max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=300
        tulot=palkkatulot+muuttulot-suojaosa
        tuki=max(0,(min(max_meno,vuokra)-0.5*tulot)*prosentti)

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
        suojaosa=300
        tulot=palkkatulot+muuttulot-suojaosa
        tuki=max(0,(min(max_meno,vuokra)-0.5*tulot)*prosentti)

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
        suojaosa=742
        tulot=palkkatulot+muuttulot-suojaosa
        tuki=max(0,(min(max_meno,vuokra)-0.5*tulot)*prosentti)

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
        
    def laske_tulot_v2(self,p,tt_alennus=0,include_takuuelake=True,omat='omat_',omatalku='',puoliso='puoliso_',puolisoalku='puoliso_'):
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
            self.verotus(q[omat+'palkkatulot'],q[omat+'ansiopvraha']+q[omat+'aitiyspaivaraha']+q[omat+'isyyspaivaraha']\
                +q[omat+'kotihoidontuki']+q[omat+'sairauspaivaraha']+q[omat+'opintotuki']+q[omat+'perustulo'],
                q[omat+'kokoelake'],p['lapsia'],p,alku=omatalku)
        _,q[omat+'verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[omat+'palkkatulot'],q[omat+'perustulo'],0,0,p,alku=omatalku)
        _,q[omat+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[omat+'palkkatulot'],0,0,p['lapsia'],p,alku=omatalku)

        if p['aikuisia']>1 and p[puoliso+'alive']>0:
            _,q[puoliso+'verot'],q[puoliso+'valtionvero'],q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveronperuste'],q[puoliso+'valtionveroperuste'],\
            q[puoliso+'ansiotulovahennys'],q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon'],\
            q[puoliso+'ptel'],q[puoliso+'sairausvakuutusmaksu'],q[puoliso+'tyotvakmaksu'],q[puoliso+'tyel_kokomaksu'],q[puoliso+'ylevero']=\
                self.verotus(q[puoliso+'palkkatulot'],
                    q[puoliso+'ansiopvraha']+q[puoliso+'aitiyspaivaraha']+q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                    +q[puoliso+'sairauspaivaraha']+q[puoliso+'opintotuki']+q[puoliso+'perustulo'],
                    q[puoliso+'kokoelake'],0,p,alku=puoliso) # onko oikein että lapsia 0 tässä????
            _,q[puoliso+'verot_ilman_etuuksia_pl_pt'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],q[puoliso+'perustulo'],0,0,p,alku=puoliso)
            _,q[puoliso+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],0,0,0,p,alku=puoliso)
        else:
            q[puoliso+'verot_ilman_etuuksia'],q[puoliso+'verot'],q[puoliso+'valtionvero']=0,0,0
            q[puoliso+'verot_ilman_etuuksia_pl_pt']=0
            q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveronperuste'],q[puoliso+'valtionveroperuste']=0,0,0
            q[puoliso+'tyotulovahennys'],q[puoliso+'ansiotulovahennys']=0,0
            q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon']=0,0
            q[puoliso+'ptel']=0
            q[puoliso+'sairausvakuutusmaksu']=0
            q[puoliso+'tyotvakmaksu']=0
            q[puoliso+'tyel_kokomaksu']=0
            q[puoliso+'ylevero']=0
            
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
                    suhde=max(0,q[puoliso+'perustulo_netto']/(q[puoliso+'perustulo_netto']+q['perustulo_netto']))
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
                    
        q['kateen']=kateen # tulot yhteensä perheessä
        q['etuustulo_netto']=q['ansiopvraha']+q['opintotuki']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimeentulotuki']+q['kokoelake']+q['elatustuki']+q['lapsilisa']+q['perustulo']+q['sairauspaivaraha']\
            -(q['pvhoito']-q['pvhoito_ilman_etuuksia'])-(q['verot']-q['verot_ilman_etuuksia'])
            
        asumismeno=p['asumismenot_asumistuki']
            
        q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        
        # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
        q['netto']=max(0,kateen-q['alv'])
        
        if p['aikuisia']>1:
            brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
                +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                +q[puoliso+'ansiopvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']+q[puoliso+'perustulo']
            kateen_puoliso=brutto_puoliso-q[puoliso+'verot']
            etuusnetto_puoliso=brutto_puoliso-q[puoliso+'palkkatulot']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
            
            if kateen_puoliso+kateen_omat<1e-6:
                suhde=0.5
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

            if kateen_omat>0:
                r2=etuusnetto_omat/kateen_omat
            else:
                r2=1
            
            etuusnetto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-r2*(q['alv']+q['pvhoito']))*suhde
            kateen_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])*suhde
            brutto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
            q[omat+'toimeentulotuki']=q['toimeentulotuki']*suhde
            q[omat+'asumistuki']=q['asumistuki']*suhde
            q[omat+'pvhoito']=q['pvhoito']*suhde
            q[omat+'lapsilisa']=q['lapsilisa']*suhde
            q[omat+'alv']=q['alv']*suhde
            
            if kateen_puoliso>0:
                r2=etuusnetto_puoliso/kateen_puoliso
            else:
                r2=1
            
            etuusnetto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-r2*(q['alv']+q['pvhoito']))*(1-suhde)
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

            if kateen_omat>0:
                r2=etuusnetto_omat/kateen_omat
            else:
                r2=1

            etuusnetto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-r2*(q['alv']+q['pvhoito'])
            q[omat+'toimeentulotuki']=q['toimeentulotuki']
            q[omat+'asumistuki']=q['asumistuki']
            q[omat+'pvhoito']=q['pvhoito']
            q[omat+'lapsilisa']=q['lapsilisa']
            q[omat+'alv']=q['alv']
            kateen_puoliso=0
            brutto_puoliso=0
            etuusnetto_puoliso=0
            q[puoliso+'toimeentulotuki']=0
            q[puoliso+'asumistuki']=0
            q[puoliso+'pvhoito']=0
            q[puoliso+'lapsilisa']=0
            q[puoliso+'alv']=0

        q[omat+'netto']=kateen_omat
        q[puoliso+'netto']=kateen_puoliso
        q[omat+'etuustulo_netto']=etuusnetto_omat
        q[puoliso+'etuustulo_netto']=etuusnetto_puoliso
        q['etuustulo_netto_v2']=q[puoliso+'etuustulo_netto']+q[omat+'etuustulo_netto']

        #q[omat+'etuustulo_brutto']=brutto_omat
        #q[puoliso+'etuustulo_brutto']=brutto_puoliso
        
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
                q[puoliso+'perustulo']=self.universalcredit(p[puoliso+'t'])
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
                q[puoliso+'perustulo']=self.universalcredit(p[puoliso+'t'])
                
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
            q[omat+'perustulo']=self.universalcredit(p[alku+'t'])
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
            q[omat+'perustulo']=self.universalcredit(p[alku+'t'])
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