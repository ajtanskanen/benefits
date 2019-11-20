"""
Pohja perustulo-mallille. Ei läheskään täysin toiminnallinen. Verotus kirjoittamatta
kokonaan.
"""

import numpy as np
from .parameters import perheparametrit
import matplotlib.pyplot as plt
from fin_benefits import Benefits

class BasicIncomeBenefits(Benefits):
    """
    Description:
        The Finnish Earnings-related Social Security modified to include basic income

    Source:
        AT

    """
    
    def __init__(self):
        super().__init__()
        self.laske_perustulo=self.laske_perustulo_Kelamalli
        
    def laske_perustulo_Kelamalli(self):
        return 560.0
        
    def elaketulovahennys2018(self,elaketulot,tulot):
        max_elaketulovahennys_valtio=11590/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9050/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2019(self,elaketulot,tulot):
        max_elaketulovahennys_valtio=11590/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9050/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

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
        
    def veroparam2018(self):
        self.kunnallisvero_pros=0.1984 # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0190 #
        self.tyontekijan_maksu=0.0635 # PTEL
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0
        #sairaanhoitomaksu_etuus=0.0147 # muut
        
        self.paivarahamaksu_pros=0.0153 # palkka
        self.paivarahamaksu_raja=14020/self.kk_jakaja    
        
        self.elakemaksu_alaraja=58.27
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def laske_ylevero2018(self,palkkatulot,elaketulot):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14750/self.kk_jakaja
    
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
    
    def verotus(self,palkkatulot,muuttulot,elaketulot,lapsia,p):
        lapsivahennys=0 # poistui 2018
    
        peritytverot=0
        self.kk_jakaja=12
        
        self.veroparam()
        
        tulot=palkkatulot+muuttulot+elaketulot
    
        # vähennetään sosiaaliturvamaksut
        if palkkatulot>self.elakemaksu_alaraja:
            ptel=(palkkatulot-self.elakemaksu_alaraja)*self.tyontekijan_maksu
        else:
            ptel=0

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
        peritty_sairaanhoitomaksu=kunnallisveronperuste*self.sairaanhoitomaksu
        
        if tyotulovahennys_kunnallisveroon>0:
            kunnallisvero_0=kunnallisveronperuste*self.kunnallisvero_pros
            if peritty_sairaanhoitomaksu+kunnallisvero_0>0:
                kvhen=tyotulovahennys_kunnallisveroon*kunnallisvero_0/(peritty_sairaanhoitomaksu+kunnallisvero_0)
                svhen=tyotulovahennys_kunnallisveroon*peritty_sairaanhoitomaksu/(peritty_sairaanhoitomaksu+kunnallisvero_0)
            else:
                kvhen=0
                svhen=0

            kunnallisvero=max(0,kunnallisveronperuste*self.kunnallisvero_pros-kvhen)
            peritty_sairaanhoitomaksu=max(0,kunnallisveronperuste*self.sairaanhoitomaksu-svhen)
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
               tyotulovahennys_kunnallisveroon,ptel,sairausvakuutus,tyotvakmaksu

    def kotihoidontuki(self,lapsia,allekolmev,alle_kouluikaisia):
        # korvataan perustulolla
        return 0
    
    def valtionvero_asteikko_perustulo(self):
        rajat=np.array([0,9999999,9999999,9999999])/self.kk_jakaja
        pros=np.array([0.40,0.40,0.40,0.40])
        return rajat,pros
    
    def laske_valtionvero(self,tulot,p):
        rajat,pros=self.valtionvero_asteikko()

        if tulot>=rajat[0]:
            vero=8
        else:
            vero=0

        for k in range(0,3):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[3]:
            vero=vero+(tulot-rajat[3])*pros[3]
        
        return vero

    def tyottomyysturva_suojaosa(self,suojaosamalli):
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
        
    def lapsilisa2018(self,yksinhuoltajakorotus=False):
        lapsilisat=np.array([95.75,105.80,135.01,154.64,174.27])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 53.3

        return lapsilisat
    
    def lapsilisa2019(self,yksinhuoltajakorotus=False):
        lapsilisat=np.array([94.88,104.84,133.79,153.24,172.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 53.3
            
        return lapsilisat
    
    def laske_lapsilisa(self,lapsia):
        lapsilisat=self.lapsilisa()
    
        if lapsia==0:
            tuki=0
        elif lapsia==1:
            tuki=lapsilisat[0]
        elif lapsia==2:
            tuki=sum(lapsilisat[0:1])
        elif lapsia==3:
            tuki=sum(lapsilisat[0:2])
        elif lapsia==4:
            tuki=sum(lapsilisat[0:3])
        elif lapsia==5:
            tuki=sum(lapsilisat[0:4])
        elif lapsia>5:
            tuki=sum(lapsilisat[0:5])+(lapsia-5)*lapsilisat(5)
        else:
            error(1)
        
        return tuki
        
    def opintoraha(self,palkka,p):
        tuki=250.28
        if palkka>667+222/12: # oletetaan että täysiaikainen opiskelija
            tuki=0
            
        return tuki
        
        
    def check_p(self,p):
        if 'toimeentulotuki_vahennys' not in p:
            p['toimeentulotuki_vahennys']=0
        if 'opiskelija' not in p:
            p['opiskelija']=0
        if 'elakkeella' not in p:
            p['elakkeella']=0
        return p

    def laske_tulot(self,p,tt_alennus=0):
        q={} # tulokset tänne
        p=self.check_p(p)
        if p['elakkeella']>0: # vanhuuseläkkeellä
            p['tyoton']=0
            q['perustulo']=0
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki']=(0,0,0)
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            p['saa_ansiopaivarahaa']=0
            # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
            if (p['aikuisia']>1):
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=0)
            else:
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=1)

            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            #oletetaan että myös puoliso eläkkeellä
            q['puolison_ansiopvraha']=0
        elif p['opiskelija']>0:
            q['kokoelake']=0
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            q['puolison_ansiopvraha']=0
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki']=(0,0,0)
            q['opintotuki']=0
            q['perustulo']=self.laske_perustulo() # ei opiskelijoille?
            if p['aitiysvapaalla']>0:
                q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
            elif p['isyysvapaalla']>0:
                q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
            elif p['kotihoidontuella']>0:
                q['kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['alle3v'],p['alle_kouluikaisia'])
            else:
                q['opintotuki']=0 #self.opintoraha(0,p)
        else: # ei eläkkeellä     
            q['kokoelake']=0
            q['opintotuki']=0
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            q['puolison_ansiopvraha']=0
            q['perustulo']=self.laske_perustulo()
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki']=(0,0,0)
            if p['aitiysvapaalla']>0:
                q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
            elif p['isyysvapaalla']>0:
                q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
            elif p['kotihoidontuella']>0:
                q['kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['alle3v'],p['alle_kouluikaisia'])
            elif p['tyoton']>0:
                q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=self.ansiopaivaraha(p['tyoton'],p['vakiintunutpalkka'],p['lapsia'],p['t'],p['saa_ansiopaivarahaa'],p['tyottomyyden_kesto'],p)
                if (p['aikuisia']>1): # perheessä 2 aikuista
                    q['puolison_ansiopvraha'],_,_=self.ansiopaivaraha(p['puoliso_tyoton'],p['puolison_vakiintunutpalkka'],p['lapsia'],p['puolison_tulot'],p['puoliso_saa_ansiopaivarahaa'],p['puolison_tyottomyyden_kesto'],p)
                else: # perheessä 1 aikuinen
                    q['puolison_ansiopvraha']=0 
            
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q['verot'],q['valtionvero'],q['kunnallisvero'],q['kunnallisveronperuste'],q['valtionveroperuste'],\
            q['ansiotulovahennys'],q['perusvahennys'],q['tyotulovahennys'],q['tyotulovahennys_kunnallisveroon'],\
            q['ptel'],q['sairausvakuutus'],q['tyotvakmaksu']=self.verotus(p['t'],\
                q['perustulo']+q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki'],\
                q['kokoelake'],p['lapsia'],p)
        _,q['verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p)

        if (p['aikuisia']>1):
            _,q['puolison_verot'],_,_,_,_,_,_,_,_,q['puolison_ptel'],q['puolison_sairausvakuutus'],\
                q['puolison_tyotvakmaksu']=self.verotus(p['puolison_tulot'],q['puolison_perustulo']+q['puolison_ansiopvraha'],0,0,p) # onko oikein että lapsia 0 tässä????
            _,q['puolison_verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puolison_tulot'],0,0,0,p)
        else:
            q['puolison_verot_ilman_etuuksia']=0
            q['puolison_verot']=0
            q['puolison_ptel']=0
            q['puolison_sairausvakuutus']=0
            q['puolison_tyotvakmaksu']=0
    
        q['elatustuki']=0
        #elatustuki=laske_elatustuki(p['lapsia'],p['aikuisia)
        
        if p['elakkeella']<1:
            q['perustulo']=self.laske_perustulo_Kelamalli(ansiopvraha_netto) # yhteensovitus
            q['puolison_perustulo']=self.laske_perustulo_Kelamalli(puolison_ansiopvraha_netto) # yhteensovitus

        if p['elakkeella']>0: # ei perustuloa
            q['asumistuki']=self.elakkeensaajan_asumistuki(p['puolison_tulot']+p['t'],q['kokoelake']+q['puolison_ansiopvraha'],p['asumismenot_asumistuki'],p)
        else:
            q['asumistuki']=self.asumistuki(p['puolison_tulot']+p['t'],q['ansiopvraha']+q['puolison_ansiopvraha']+q['perustulo']+q['puolison_perustulo'],p['asumismenot_asumistuki'],p)
            
        if p['lapsia']>0:
            q['pvhoito']=self.paivahoitomenot(p['paivahoidossa'],p['puolison_tulot']+p['t']+q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['puolison_ansiopvraha'],p)
            if (p['lapsia_kotihoidontuella']>0):
                alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['alle3v'])
                q['pvhoito']=q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['alle3v'],alle_kouluikaisia) # etumerkki!
            q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['paivahoidossa'],p['puolison_tulot']+p['t']+q['elatustuki'],p)
            q['lapsilisa']=self.laske_lapsilisa(p['lapsia'])
        else:
            q['pvhoito']=0
            q['pvhoito_ilman_etuuksia']=0
            q['lapsilisa']=0
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        if p['elakkeella']>0:
            q['kokoelake_netto']=q['kokoelake']-(q['verot']-q['verot_ilman_etuuksia'])
            q['ansiopvraha_netto']=0
            q['aitiyspaivaraha_netto'],q['kotihoidontuki_netto'],q['aitiyspaivaraha_netto']=(0,0,0)
            q['puolison_ansiopvraha_netto']=0
        elif p['aitiysvapaalla']>0:
            q['aitiyspaivaraha_netto']=q['aitiyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
            q['kokoelake_netto'],q['ansiopvraha_netto'],q['kotihoidontuki_netto'],q['aitiyspaivaraha_netto']=(0,0,0,0)
            q['puolison_ansiopvraha_netto']=0
        elif p['isyysvapaalla']>0:
            q['isyyspaivaraha_netto']=q['isyyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
            q['kokoelake_netto'],q['aitiyspaivaraha_netto'],q['kotihoidontuki_netto'],q['ansiopvraha_netto']=(0,0,0,0)
            q['puolison_ansiopvraha_netto']=0
        elif p['kotihoidontuella']>0:
            q['kotihoidontuki_netto']=q['kotihoidontuki']-(q['verot']-q['verot_ilman_etuuksia']) 
            q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto']=(0,0,0,0)
            q['puolison_ansiopvraha_netto']=0
        else:
            q['puolison_ansiopvraha_netto']=q['puolison_ansiopvraha']-(q['puolison_verot']-q['puolison_verot_ilman_etuuksia'])
            q['ansiopvraha_netto']=q['ansiopvraha']-(q['verot']-q['verot_ilman_etuuksia'])
            q['kokoelake_netto'],q['aitiyspaivaraha_netto'],q['kotihoidontuki_netto'],q['aitiyspaivaraha_netto']=(0,0,0,0)
            q['puolison_ansiopvraha_netto']=0
    
        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia
        # käytässä??
        if q['puolison_ansiopvraha_netto']+q['ansiopvraha_netto']>0:
            suhde=max(0,q['ansiopvraha_netto']/(q['puolison_ansiopvraha_netto']+q['ansiopvraha_netto']))
            q['ansiopvraha_nettonetto']=q['ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
            q['puolison_ansiopvraha_nettonetto']=q['puolison_ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
        else:
            q['ansiopvraha_nettonetto']=0
            q['puolison_ansiopvraha_nettonetto']=0

        q['perustulo_netto']=q['perustulo']
        q['puolison_perustulo_netto']=q['puolison_perustulo']

        #(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.0)
        q['toimtuki']=0 #self.toimeentulotuki(p['t'],q['verot_ilman_etuuksia'],p['puolison_tulot'],q['puolison_verot_ilman_etuuksia'],\
            #q['elatustuki']+q['opintotuki']+q['ansiopvraha_netto']+q['puolison_ansiopvraha_netto']+q['asumistuki']+q['lapsilisa']+q['kokoelake_netto'],0,\
            #p['asumismenot_toimeentulo'],q['pvhoito'],p)
        #except:   
        #    print('error in toimtuki:') 
        #    print((p['t'],q['verot_ilman_etuuksia'],p['puolison_tulot'],q['puolison_verot_ilman_etuuksia'],\
        #        	q['elatustuki']+q['ansiopvraha_netto']+q['puolison_ansiopvraha_netto']+q['asumistuki']+q['lapsilisa']+q['kokoelake_netto'],0,\
        #        	p['asumismenot_toimeentulo'],q['pvhoito'],p))
        #print(q['toimtuki'],(p['t']+q['kokoelake'],q['verot_ilman_etuuksia'],p['puolison_tulot'],q['puolison_verot_ilman_etuuksia'],\
        #    q['elatustuki']+q['ansiopvraha_netto']+q['puolison_ansiopvraha_netto']+q['asumistuki']+q['lapsilisa'],0,\
        #    p['asumismenot_toimeentulo'],q['pvhoito']))

        kateen=q['perustulo_netto']+q['puolison_perustulo_netto']+q['opintotuki']+q['kokoelake']+p['puolison_tulot']+p['t']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimtuki']+q['ansiopvraha']+q['puolison_ansiopvraha']+q['elatustuki']-q['puolison_verot']-q['verot']-q['pvhoito']+q['lapsilisa']
        q['kateen']=kateen
        q['perhetulot_netto']=p['puolison_tulot']+p['t']-q['verot_ilman_etuuksia']-q['puolison_verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['omattulot_netto']=p['t']-q['verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['palkkatulot']=p['t']
        q['puolison_palkkatulot']=p['puolison_tulot']
        q['puolison_tulot_netto']=p['puolison_tulot'] # verot??

        return kateen,q

    def laske_ja_plottaa_veromarginaalit(self,p=None,min_salary=0,max_salary=6000,basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",selite=True):
        palkka=np.zeros(max_salary+1)
        margtyotvakmaksu=np.zeros(max_salary+1)        
        margsairausvakuutus=np.zeros(max_salary+1)
        margptel=np.zeros(max_salary+1)
        margtyotulovah=np.zeros(max_salary+1)
        margansiotulovah=np.zeros(max_salary+1)        
        margverot=np.zeros(max_salary+1)        
        margkunnallisvero=np.zeros(max_salary+1)        
        margvaltionvero=np.zeros(max_salary+1)  
        margperusvahennys=np.zeros(max_salary+1)  
        margpuolisonverot=np.zeros(max_salary+1)  
        tyotvakmaksu=np.zeros(max_salary+1)        
        sairausvakuutus=np.zeros(max_salary+1)
        ptel=np.zeros(max_salary+1)
        tyotulovah=np.zeros(max_salary+1)
        ansiotulovah=np.zeros(max_salary+1)        
        verot=np.zeros(max_salary+1)        
        kunnallisvero=np.zeros(max_salary+1)        
        valtionvero=np.zeros(max_salary+1)  
        perusvahennys=np.zeros(max_salary+1)  
        puolisonverot=np.zeros(max_salary+1)  
        
        if p is None:
            p=self.get_default_parameter()
            
        p2=p.copy()

        p2['t']=0 # palkka
        n0,q0=self.laske_tulot(p2)
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1,q1=self.laske_tulot(p2)
            p2['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p2)
            palkka[t]=t
            
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            margvaltionvero[t]=marg['valtionvero']
            margkunnallisvero[t]=marg['kunnallisvero']
            margverot[t]=marg['ansioverot']
            margansiotulovah[t]=marg['ansiotulovah']
            margtyotulovah[t]=marg['tyotulovahennys']
            margperusvahennys[t]=marg['perusvahennys']
            margptel[t]=marg['ptel']
            margsairausvakuutus[t]=marg['sairausvakuutus']
            margtyotvakmaksu[t]=marg['tyotvakmaksu']
            margpuolisonverot[t]=marg['puolison_verot']
            tyotvakmaksu[t]=q1['tyotvakmaksu']
            sairausvakuutus[t]=q1['sairausvakuutus']
            ptel[t]=q1['ptel']
            kunnallisvero[t]=q1['kunnallisvero']
            valtionvero[t]=q1['valtionvero']
            puolisonverot[t]=0 #q1['puolisonverot']
            
                
        fig,axs = plt.subplots()
        axs.stackplot(palkka,margvaltionvero,margkunnallisvero,margptel,margsairausvakuutus,margtyotvakmaksu,margpuolisonverot,\
            labels=('Valtionvero','Kunnallisvero','PTEL','sairausvakuutus','työttömyysvakuutusmaksu','puolison verot'))
        axs.plot(margverot,label='Yht')
        #axs.plot(margyht,label='Vaihtoehto2')
        #axs.plot(margyht2,label='Vaihtoehto3')
        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Eff.marginaalivero (%)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        axs.set_ylim(-50, 120)
        if selite:
            axs.legend(loc='upper left')
        plt.show()
        
        fig,axs = plt.subplots()
        axs.stackplot(palkka,tyotvakmaksu,sairausvakuutus,ptel,kunnallisvero,valtionvero,puolisonverot,\
            labels=('tyotvakmaksu','sairausvakuutus','ptel','kunnallisvero','valtionvero','puolisonverot'))
        #axs.plot(netto)
        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Verot yhteensä (e/kk)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        if selite:        
            axs.legend(loc='lower right')
        plt.show()