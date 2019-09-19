"""
Etuuslajien funktioita
"""

import numpy as np
from .parameters import perheparametrit
import matplotlib.pyplot as plt

class Benefits():
    """
    Description:
        The Finnish Earnings-related Social Security

    Source:
        AT

    """
    
    def __init__(self):
        self.max_age=69
        self.min_age=25
        self.vuosi=2018
        
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.0):

        omavastuu=omavastuuprosentti*asumismenot
        menot=max(0,asumismenot-omavastuu)+muutmenot

        #menot=asumismenot+muutmenot    
        bruttopalkka=omabruttopalkka+puolison_bruttopalkka    
        palkkavero=omapalkkavero+puolison_palkkavero    
        palkkatulot=bruttopalkka-palkkavero    
        omaetuoikeutettuosa=min(150,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
        puolison_etuoikeutettuosa=min(150,0.2*puolison_bruttopalkka)    
        etuoikeutettuosa=omaetuoikeutettuosa+puolison_etuoikeutettuosa    
        lapsi1=305.87     # e/kk     alle 10v lapsi
        lapsi2=281.59     # e/kk
        lapsi3=257.32     # e/kk
        yksinhuoltaja=534.05     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=412.68    
        yksinasuva=485.50    

        if p['aikuisia']<2:
            if p['lapsia']<1: 
                tuki1=yksinasuva     # yksinasuva 485,50
            elif p['lapsia']==1:
                tuki1=yksinhuoltaja+lapsi1     # yksinhuoltaja 534,05
            elif p['lapsia']==2:
                tuki1=yksinhuoltaja+lapsi1+lapsi2     # yksinhuoltaja 534,05
            else:
                tuki1=yksinhuoltaja+lapsi1+lapsi2+lapsi3*(p['lapsia']-2)     # yksinhuoltaja 534,05
        else:
            if p['lapsia']<1:
                tuki1=muu*p['aikuisia']   
            elif p['lapsia']==1:
                tuki1=muu*p['aikuisia']+lapsi1     # yksinhuoltaja 534,05
            elif p['lapsia']==2:
                tuki1=muu*p['aikuisia']+lapsi1+lapsi2     # yksinhuoltaja 534,05
            else:
                tuki1=muu*p['aikuisia']+lapsi1+lapsi2+lapsi3*(p['lapsia']-2)     # yksinhuoltaja 534,05

        # if (bruttopalkka-etuoikeutettuosa>palkkavero)
        #     tuki=max(0,tuki1+menot-max(0,bruttopalkka-etuoikeutettuosa-palkkavero)-verot-muuttulot)    
        # else 
        #     verot2=palkkavero+verot-max(0,(bruttopalkka-etuoikeutettuosa))    
        #     tuki=max(0,tuki1+menot-muuttulot+verot2)    
        # end
        tuki=max(0,tuki1+menot-max(0,omabruttopalkka-omaetuoikeutettuosa-omapalkkavero)\
                -max(0,puolison_bruttopalkka-puolison_etuoikeutettuosa-puolison_palkkavero)-verot-muuttulot)    
        if tuki<10:
            tuki=0    
            
        return tuki
    
    def get_default_parameter():
        return perheparametrit(perhetyyppi=1)
    
    # tmtuki samankokoinen
    def peruspaivaraha(self,lapsia):
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.23     # e/pv
        elif lapsia==2:
            lisa=7.68     # e/pv
        else:
            lisa=9.90     # e/pv
        
        pvraha=21.5*(32.40+lisa)    
        tuki=max(0,pvraha)    
    
        return tuki
        
    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka):
        if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
            return max(0,vakpalkka-tyotaikaisettulot) 
            
        return ansiopaivarahamaara   

    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0):
    #def ansiopaivaraha(self,p,ansiokerroin=1.0):
        #tyoton=p['tyoton']
        #vakiintunutpalkka=p['vakiintunutpalkka']
        #lapsia=p['lapsia']
        #tyotaikaisettulot=p['tyotaikaisettulot']
        #saa_ansiopaivarahaa=p['saa_ansiopaivarahaa']
        ansiopvrahan_suojaosa=p['ansiopvrahan_suojaosa']
        lapsikorotus=p['ansiopvraha_lapsikorotus']
    
        if tyoton>0:
            if lapsikorotus<1:
                lapsia=0    

            lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
            sotumaksu=0.0448     # 2015 0.0428 2016 0.0460
            if saa_ansiopaivarahaa>0 & p['tyottomyyden_kesto']<400: 
                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-sotumaksu)     
        
                taite=3078.60    
                if vakpalkka>taite:
                    tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus    
                else:
                    tuki2=0.45*max(0,vakpalkka-perus)+perus    

                tuki2=tuki2+lapsikorotus[min(lapsia+1,4)]    
                tuki2=tuki2*ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa)    
        
                perus=self.peruspaivaraha(lapsia)     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavattulo=max(0,tyotaikaisettulot-suojaosa)    
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavattulo)  
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka)  
                #if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
                #    ansiopaivarahamaara=max(0,vakpalkka-tyotaikaisettulot)    

                tuki=ansiopaivarahamaara    
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa)    
                tuki=max(perus,tuki)     # voi tulla vastaan pienillä tasoilla
            else:
                ansiopaivarahamaara=0    
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa)    
                tuki=perus    
        else:
            perus=0    
            tuki=0    
            ansiopaivarahamaara=0   
        
        return tuki,ansiopaivarahamaara,perus

    def soviteltu_peruspaivaraha(self,lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa):
        suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa)

        pvraha=self.peruspaivaraha(lapsia)
        vahentavattulo=max(0,tyotaikaisettulot-suojaosa)
        tuki=max(0,pvraha-0.5*vahentavattulo)
    
        return tuki
        
    def tyotulovahennys(self):
        max_tyotulovahennys=1540/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/self.kk_jakaja
        ttulopros=np.array([0.120,0.0165,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def ansiotulovahennys(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah

    def verotus2018(self,palkkatulot,muuttulot,elaketulot,lapsia,p):
    
        # tulot e/kk sisältää työttömyyskorvauksen, palkkatulot ei
        # 
        # Vuoden 2018 tuloveroasteikko

        lapsivahennys=0 # poistui 2018
    
        peritytverot=0
        self.kk_jakaja=12
    
        kunnallisvero_pros=0.1984 # Viitamäen raportista
        tyottomyysvakuutusmaksu=0.0190 #
        tyontekijan_maksu=0.0635 # PTEL
    
        # sairausvakuutus
        sairaanhoitomaksu=0.0
        #sairaanhoitomaksu_etuus=0.0147 # muut
        paivarahamaksu_pros=0.0153 # palkka
        paivarahamaksu_raja=14020/self.kk_jakaja
    
        # vähennetään sosiaaliturvamaksut
        if palkkatulot>58.27:
            ptel=(palkkatulot-58.27)*tyontekijan_maksu
        else:
            ptel=0

        tyotvakmaksu=palkkatulot*tyottomyysvakuutusmaksu
        if palkkatulot>paivarahamaksu_raja:
            sairausvakuutus=palkkatulot*paivarahamaksu_pros
        else:
            sairausvakuutus=0

        peritytverot=peritytverot+sairausvakuutus+ptel+tyotvakmaksu
        palkkatulot=palkkatulot-sairausvakuutus-ptel-tyotvakmaksu 
        #tulot=palkkatulot+muuttulot
    
        # tulonhankkimisvähennys pienentää ansiotuloa
    
        tulonhankkimisvahennys=750/self.kk_jakaja
        palkkatulot=max(0,palkkatulot-tulonhankkimisvahennys) # puhdas ansiotulo
        tulot=palkkatulot+muuttulot+elaketulot
    
        # ylevero
    
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14750
    
        ylevero=min(max_ylevero,yleveropros*max(0,elaketulot+palkkatulot-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
    
        valtionvero=ylevero
    
        peritytverot=peritytverot+ylevero
        palkkatulot=max(0,palkkatulot-ylevero)

        # työtulovähennys vähennetään valtionveroista
    
        #switch (p['veromalli)
        #max_tyotulovahennys=1540/kk_jakaja
        #ttulorajat=np.array([2500,33000,127000])/kk_jakaja
        #ttulopros=np.array([0.120,0.0165,0])
        #end
        
        max_tyotulovahennys,ttulorajat,ttulopros=self.tyotulovahennys()
    
        if palkkatulot>ttulorajat[1]:
            if palkkatulot>ttulorajat[2]:
                tyotulovahennys=0
            else:
                tyotulovahennys=min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot-ttulorajat[0])))
        else:
            if palkkatulot>ttulorajat[0]:
                tyotulovahennys=min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot-ttulorajat[0])))
            else:
                tyotulovahennys=0

        if tulot>ttulorajat[1]:
            if tulot>ttulorajat[2]:
                tyotulovahennys=0
            else:
                tyotulovahennys=max(0,tyotulovahennys-ttulopros[1]*max(0,tulot-ttulorajat[1]))

        #tyotulovahennys=0

        # valtioverotus
        # varsinainen verotus

        valtionvero=valtionvero+self.laske_valtionvero(tulot,p)
        valtionveroperuste=tulot
    
        # työtulovähennys
        valtionvero=max(0,valtionvero-lapsivahennys)
        if tyotulovahennys>valtionvero:
            tyotulovahennys_kunnallisveroon=max(0,tyotulovahennys-valtionvero)
            tyotulovahennys=valtionvero
            valtionvero=0
        else:
            tyotulovahennys_kunnallisveroon=0
            valtionvero=max(0,valtionvero-tyotulovahennys)
    
        peritytverot=peritytverot+valtionvero

        # kunnallisverotus
    
        # ansiotulovahennys
        #rajat=np.array([2500,7230,14000])/kk_jakaja
        #maxvahennys=3570/kk_jakaja
        #ansvah=np.array([0.51,0.28,0.045])
        
        rajat,maxvahennys,ansvah=self.ansiotulovahennys()
        if palkkatulot>rajat[1]:
            if palkkatulot>rajat[2]:
                ansiotulovahennys=max(0,min(maxvahennys,ansvah[0]*(rajat[1]-rajat[0])+ansvah[1]*(rajat[2]-rajat[1])))
            else:
                ansiotulovahennys=max(0,min(maxvahennys,ansvah[0]*(rajat[1]-rajat[0])+ansvah[1]*(palkkatulot-rajat[1])))
        else:
            if palkkatulot>rajat[0]:
                ansiotulovahennys=max(0,min(maxvahennys,ansvah[0]*(palkkatulot-rajat[0])))
            else:
                ansiotulovahennys=0

        if palkkatulot>rajat[2]:
            ansiotulovahennys=max(0,ansiotulovahennys-ansvah[2]*(palkkatulot-rajat[2]))
    
        # perusvähennys
        #max_perusvahennys=3020/self.kk_jakaja
        max_perusvahennys=3020/self.kk_jakaja
        if tulot-ansiotulovahennys<max_perusvahennys:
            perusvahennys=tulot-ansiotulovahennys
        else:
            perusvahennys=max(0,max_perusvahennys-0.18*max(0,(elaketulot+max(0,tulot-elaketulot-ansiotulovahennys)-max_perusvahennys)))
    
        # Yhteensä
        kunnallisveronperuste=max(0,elaketulot+max(0,tulot-elaketulot-ansiotulovahennys)-perusvahennys)
        peritty_sairaanhoitomaksu=kunnallisveronperuste*sairaanhoitomaksu 
    
        if tyotulovahennys_kunnallisveroon>0:
            kunnallisvero_0=kunnallisveronperuste*kunnallisvero_pros
            if peritty_sairaanhoitomaksu+kunnallisvero_0>0:
                kvhen=tyotulovahennys_kunnallisveroon*kunnallisvero_0/(peritty_sairaanhoitomaksu+kunnallisvero_0)
                svhen=tyotulovahennys_kunnallisveroon*peritty_sairaanhoitomaksu/(peritty_sairaanhoitomaksu+kunnallisvero_0)
            else:
                kvhen=0
                svhen=0

            kunnallisvero=max((tulot-ansiotulovahennys-perusvahennys)*kunnallisvero_pros-kvhen,0)
            peritty_sairaanhoitomaksu=max(0,kunnallisveronperuste*sairaanhoitomaksu-svhen)
        else:
            kunnallisvero=kunnallisveronperuste*kunnallisvero_pros

        sairausvakuutus=sairausvakuutus+peritty_sairaanhoitomaksu
    
        peritytverot=peritytverot+peritty_sairaanhoitomaksu
        palkkatulot=kunnallisveronperuste-peritty_sairaanhoitomaksu 
        tulot=palkkatulot+muuttulot
    
        # sairausvakuutus=sairausvakuutus+kunnallisveronperuste*sairaanhoitomaksu
        # yhteensä
        peritytverot=peritytverot+kunnallisvero

        netto=tulot-peritytverot
    
        return netto,peritytverot,valtionvero,kunnallisvero,kunnallisveronperuste,\
        valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,tyotulovahennys_kunnallisveroon,\
        ptel,sairausvakuutus,tyotvakmaksu


    def kotihoidontuki(self,lapsia,allekolmev,alle_kouluikaisia):
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=341.27 # e/kk
            seuraavat_alle_3v=102.17 # e/kk
            yli_3v=65.65 #e_kk
            if allekolmev>0:
                kerroin1=1
                if allekolmev>1:
                    kerroin2=allekolmev-1
                else:
                    kerroin2=0
            else:
                kerroin1=0
                kerroin2=0
            
            arvo=alle_kouluikaisia*yli_3v+tuki_alle_3v*kerroin1+kerroin2*seuraavat_alle_3v        
        
        return arvo
    
    def valtionvero_asteikko_2018(self):
        rajat=np.array([17200,25700,42400,74200])/self.kk_jakaja
        pros=np.array([0.06,0.1725,0.2125,0.3125])
        return rajat,pros
    
    def laske_valtionvero(self,tulot,p):

        #rajat=np.array([17200,25700,42400,74200])/12
        #pros=np.array([0.06,0.1725,0.2125,0.3125])
        rajat,pros=self.valtionvero_asteikko_2018()

        if tulot>=rajat[0]:
            vero=8
        else:
            vero=0

        for k in range(0,3):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[3]:
            vero=vero+(tulot-rajat[3])*pros[3]
        
        return vero

    def laske_valtionvero_2019(self,tulot,p):

        rajat=np.array([17600,26400,43500,76100])/12
        pros=np.array([0.06,0.1725,0.2125,0.3125])

        if tulot>=rajat[0]:
            vero=8
        else:
            vero=0

        for k in range(0,3):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[3]:
            vero=vero+(tulot-rajat[3])*pros[3]
        
        return vero

    # ei-eläkeläinen
    def laske_valtionvero_2020(self,tulot,p):
        # tässä vielä 2019 tiedot
        rajat=np.array([17600,26400,43500,76100])/12
        pros=np.array([0.06,0.1725,0.2125,0.3125])

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
    
    def laske_lapsilisa(self,lapsia):
        lapsilisat=np.array([95.75,105.80,135.01,154.64,174.27])
    
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
        elif lapsia>5:
            tuki=sum(lapsilisat[0:5])+(lapsia-5)*lapsilisat(5)
        else:
            error(1)
        
        return tuki

    def laske_tulot(self,p,elake=0):

        q={} # tulokset tänne
        q['elake']=elake
        if p['elakkeella']<1: # ei eläkkeellä
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=self.ansiopaivaraha(p['tyoton'],p['vakiintunutpalkka'],p['lapsia'],p['t'],p['saa_ansiopaivarahaa'],p['tyottomyyden_kesto'],p)
            q['kokoelake']=0
        else: # eläkkeellä
            p['tyoton']=0
            p['saa_ansiopaivarahaa']=0
            q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake'], 1)
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)

        if (p['aikuisia']>1): # perheessä 2 aikuista
            q['puolison_ansiopvraha'],_,_=self.ansiopaivaraha(p['puoliso_tyoton'],p['puolison_vakiintunutpalkka'],p['lapsia'],p['puolison_tulot'],p['puoliso_saa_ansiopaivarahaa'],p['puolison_tyottomyyden_kesto'],p)
        else: # perheessä 1 aikuinen
            q['puolison_ansiopvraha']=0
    
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q['verot'],q['valtionvero'],q['kunnallisvero'],q['kunnallisveronperuste'],q['valtionveroperuste'],\
            q['ansiotulovahennys'],q['perusvahennys'],q['tyotulovahennys'],q['tyotulovahennys_kunnallisveroon'],\
            q['ptel'],q['sairausvakuutus'],q['tyotvakmaksu']=self.verotus(p['t'],q['ansiopvraha'],q['kokoelake'],p['lapsia'],p)
        _,q['verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,q['kokoelake'],p['lapsia'],p)

        if (p['aikuisia']>1):
            _,q['puolison_verot'],_,_,_,_,_,_,_,_,q['puolison_ptel'],q['puolison_sairausvakuutus'],\
                q['puolison_tyotvakmaksu']=self.verotus(p['puolison_tulot'],q['puolison_ansiopvraha'],0,0,p) # onko oikein että lapsia 0 tässä????
            _,q['puolison_verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puolison_tulot'],0,0,0,p)
        else:
            q['puolison_verot_ilman_etuuksia']=0
            q['puolison_verot']=0
            q['puolison_ptel']=0
            q['puolison_sairausvakuutus']=0
            q['puolison_tyotvakmaksu']=0
    
        q['elatustuki']=0
        #elatustuki=laske_elatustuki(p['lapsia'],p['aikuisia)

        q['asumistuki']=self.asumistuki(p['puolison_tulot']+p['t'],q['ansiopvraha']+q['puolison_ansiopvraha'],p['asumismenot_asumistuki'],p)
        q['pvhoito']=self.paivahoitomenot(p['paivahoidossa'],p['puolison_tulot']+p['t']+q['elatustuki']+q['ansiopvraha']+q['puolison_ansiopvraha'],p)
    
        if (p['lapsia_kotihoidontuella']>0):
            alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['alle3v'])
            q['pvhoito']=q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['alle3v'],alle_kouluikaisia) # etumerkki!

        q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['paivahoidossa'],p['puolison_tulot']+p['t']+q['elatustuki'],p)
        q['lapsilisa']=self.laske_lapsilisa(p['lapsia'])
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        q['puolison_ansiopvraha_netto']=q['puolison_ansiopvraha']-(q['puolison_verot']-q['puolison_verot_ilman_etuuksia'])
        q['ansiopvraha_netto']=q['ansiopvraha']-(q['verot']-q['verot_ilman_etuuksia'])
    
        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia
        # käytässä??
        if (q['puolison_ansiopvraha_netto']+q['ansiopvraha_netto']>0):
            suhde=max(0,q['ansiopvraha_netto']/(q['puolison_ansiopvraha_netto']+q['ansiopvraha_netto']))
            q['ansiopvraha_nettonetto']=q['ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
            q['puolison_ansiopvraha_nettonetto']=q['puolison_ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
        else:
            q['ansiopvraha_nettonetto']=0
            q['puolison_ansiopvraha_nettonetto']=0

        #    case 1 # Kelan malli
        #        perustulo=laske_perustulo_Kelamalli(ansiopvraha_netto) # yhteensovitus
        #        puolison_perustulo=laske_perustulo_Kelamalli(puolison_ansiopvraha_netto) # yhteensovitus
        #    case 0
        q['perustulo']=0
        q['puolison_perustulo']=0
    
        q['perustulo_netto']=0
        q['puolison_perustulo_netto']=0

        q['toimtuki']=self.toimeentulotuki(p['t'],q['verot_ilman_etuuksia'],p['puolison_tulot'],q['puolison_verot_ilman_etuuksia'],\
            q['elatustuki']+q['elake']+q['ansiopvraha_netto']+q['puolison_ansiopvraha_netto']+q['asumistuki']+q['lapsilisa'],0,\
            p['asumismenot_toimeentulo'],q['pvhoito'],p)
    
        kateen=q['kokoelake']+p['puolison_tulot']+p['t']+q['asumistuki']+q['toimtuki']+q['ansiopvraha']+q['puolison_ansiopvraha']+q['elatustuki']-q['puolison_verot']-q['verot']-q['pvhoito']+q['lapsilisa']
        q['kateen']=kateen
        q['tulotnetto']=q['kokoelake']+p['puolison_tulot']+p['t']-q['verot_ilman_etuuksia']-q['puolison_verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['tulot']=p['t']
        q['puolison_tulot']=p['puolison_tulot']
    
        return kateen,q

    def verotus(self,palkkatulot,muuttulot,elaketulot,lapsia,p):

        verovuosi=2018
    
        return self.verotus2018(palkkatulot,muuttulot,elaketulot,lapsia,p)


    def asumistuki(self,palkkatulot,muuttulot,vuokra,p):
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
        suojaosa=300*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
    
        return tuki


    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot(self,hoidossa,tulot,p,prosentti1=None,prosentti2=None,prosentti3=None,maksimimaksu=None):
        minimimaksu=10

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.5
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=290

        if p['lapsia']>0:
            vakea=p['lapsia']+p['aikuisia']
            if vakea==1:
                alaraja=2050
                prosentti=prosentti1
            elif vakea==2:
                alaraja=2050
                prosentti=prosentti1
            elif vakea==3:
                alaraja=2646
                prosentti=prosentti1
            elif vakea==4:
                alaraja=3003
                prosentti=prosentti1
            elif vakea==5:
                alaraja=3361
                prosentti=prosentti1
            elif vakea==6:
                alaraja=3718
                prosentti=prosentti1
            else:
                alaraja=3718+138*(vakea-6)
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
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        return maksu
    
    def laske_kansanelake(self,ika,tyoelake,yksin):
        if ika>=65:
            if yksin>0:
                maara=628.85
            else:
                maara=557.79
            
            maara = maara-np.maximum(0,(tyoelake-55.54))/2
        
            return maara
        else:
            return 0
        
    def laske_takuuelake(self,ika,kansanelake,tyoelake):
        if ika<65:
            return 0
        
        if kansanelake+tyoelake<777.84:
            elake=784.52-kansanelake-tyoelake
        else:
            elake=0
        
        return elake
    
    def laske_kokonaiselake(self,ika,tyoelake,yksin=1):
        kansanelake=self.laske_kansanelake(ika,tyoelake,yksin)
        takuuelake=self.laske_takuuelake(ika,kansanelake,tyoelake)
        kokoelake=tyoelake+kansanelake+takuuelake
    
        return kokoelake
        
    def laske_marginaalit(self,q1,q2,dt,laske_tyollistymisveroaste=0):
    
        if dt<1:
            dt=1

        # lasketaan marginaalit
        marg={}        
        marg['asumistuki']=(-q2['asumistuki']+q1['asumistuki'])*100/dt
        marg['ansiopvraha']=(+q1['ansiopvraha_netto']-q2['ansiopvraha_netto']+q1['puolison_ansiopvraha_netto']-q2['puolison_ansiopvraha_netto'])*100/dt 
        marg['pvhoito']=(-q1['pvhoito']+q2['pvhoito'])*100/dt
        marg['toimtuki']=(+q1['toimtuki']-q2['toimtuki'])*100/dt
        marg['palkkaverot']=(-q1['verot_ilman_etuuksia']+q2['verot_ilman_etuuksia']-q1['puolison_verot_ilman_etuuksia']+q2['puolison_verot_ilman_etuuksia'])*100/dt
        marg['valtionvero']=(-q1['valtionvero']+q2['valtionvero'])*100/dt
        marg['kunnallisvero']=(-q1['kunnallisvero']+q2['kunnallisvero'])*100/dt
        marg['ansiotulovah']=(+q1['ansiotulovahennys']-q2['ansiotulovahennys'])*100/dt
        marg['tyotulovahennys']=(+q1['tyotulovahennys']-q2['tyotulovahennys'])*100/dt
        marg['perusvahennys']=(+q1['perusvahennys']-q2['perusvahennys'])*100/dt
        marg['tyotulovahennys_kunnallisveroon']=(+q1['tyotulovahennys_kunnallisveroon']-q2['tyotulovahennys_kunnallisveroon'])*100/dt
        marg['ptel']=(-q1['ptel']+q2['ptel']-q1['puolison_ptel']+q2['puolison_ptel'])*100/dt
        marg['sairausvakuutus']=(-q1['sairausvakuutus']+q2['sairausvakuutus']-q1['puolison_sairausvakuutus']+q2['puolison_sairausvakuutus'])*100/dt
        marg['tyotvakmaksu']=(-q1['tyotvakmaksu']+q2['tyotvakmaksu']-q1['puolison_tyotvakmaksu']+q2['puolison_tyotvakmaksu'])*100/dt
        marg['perustulo']=(+q1['perustulo_netto']-q2['perustulo_netto']+q1['puolison_perustulo_netto']-q2['puolison_perustulo_netto'])*100/dt 
        marg['puolison_verot']=(-q1['puolison_verot']+q2['puolison_verot'])*100/dt
    
        marg['sivukulut']=marg['tyotvakmaksu']+marg['sairausvakuutus']+marg['ptel'] # sisältyvät jo veroihin
        marg['etuudet']=marg['ansiopvraha']+marg['asumistuki']+marg['toimtuki']
        marg['verot']=marg['palkkaverot'] # sisältää sivukulut
        marg['marginaali']=marg['pvhoito']+marg['etuudet']+marg['verot']
    
        # ja käteen jää
        tulot={}
        tulot['kateen1']=q1['kateen']
        tulot['kateen2']=q2['kateen']
    
        omattulotnetto1=q1['tulot']-q1['verot_ilman_etuuksia']-q1['pvhoito_ilman_etuuksia'] # ilman etuuksia
        omattulotnetto2=q2['tulot']-q2['verot_ilman_etuuksia']-q2['pvhoito_ilman_etuuksia'] # ilman etuuksia
        puolisontulotnetto1=q1['puolison_tulot']-q1['puolison_verot_ilman_etuuksia'] # ilman etuuksia
        puolisontulotnetto2=q2['puolison_tulot']-q2['puolison_verot_ilman_etuuksia'] # ilman etuuksia
        if laske_tyollistymisveroaste>0:
            tulot['tulotnetto']=omattulotnetto2+puolisontulotnetto2
            tulot['puolisontulotnetto']=puolisontulotnetto2
            tulot['omattulotnetto']=omattulotnetto2
        else:
            tulot['tulotnetto']=omattulotnetto1+puolisontulotnetto1
            tulot['puolisontulotnetto']=puolisontulotnetto1
            tulot['omattulotnetto']=omattulotnetto1
            
        marg['marginaaliveroprosentti']=100-(tulot['kateen2']-tulot['kateen1'])*100/dt 
    
        return tulot,marg
    
    def laske_ja_plottaa(self,p=None,min_salary=0,max_salary=6000,basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus"):
        netto=np.zeros(max_salary+1)
        palkka=np.zeros(max_salary+1)
        tva=np.zeros(max_salary+1)
        eff=np.zeros(max_salary+1)
        
        if p is None:
            p=self.get_default_parameter()

        p2=p.copy()
        p2['t']=0 # palkka
        n0,q0=self.laske_tulot(p2,elake=0)
        for t in range(0,max_salary):
            p2['t']=t # palkka
            n1,q1=self.laske_tulot(p2,elake=0)
            p2['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p2,elake=0)
            netto[t]=n1
            palkka[t]=t
            eff[t]=(1-(n2-n1)/dt)*100
            if t>0:
                tva[t]=(1-(n1-n0)/t)*100
            else:
                tva[t]=0
                
        if plottaa:
            fig, axs = plt.subplots()
            if basenetto is not None:
                axs.plot(basenetto,label=otsikkobase)
                axs.plot(netto,label=otsikko)
                axs.legend(loc='upper right')
            else:
                axs.plot(netto)        
            axs.set_xlabel('Palkka (e/kk)')
            axs.set_ylabel('Käteen (e/kk)')
            axs.grid(True)
            axs.set_xlim(0, max_salary)

            fig, axs = plt.subplots()
            if baseeff is not None:
                axs.plot(baseeff,label=otsikkobase)
                axs.plot(eff,label=otsikko)
                axs.legend(loc='upper right')
            else:
                axs.plot(eff)        
            axs.set_xlabel('Palkka (e/kk)')
            axs.set_ylabel('Eff.marg.veroaste (%)')
            axs.grid(True)
            axs.set_xlim(0, max_salary)

            fig, axs = plt.subplots()
            if basenetto is not None:
                axs.plot(basetva,label=otsikkobase)
                axs.plot(tva,label=otsikko)
                axs.legend(loc='upper right')
            else:
                axs.plot(tva)
            axs.set_xlabel('Palkka (e/kk)')
            axs.set_ylabel('Työllistymisveroaste (%)')
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 120)

            plt.show()
        
        return netto,eff,tva
        
    def laske_ja_plottaa_marginaalit(self,p=None,min_salary=0,max_salary=6000,basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus"):
        netto=np.zeros(max_salary+1)
        palkka=np.zeros(max_salary+1)
        tva=np.zeros(max_salary+1)
        eff=np.zeros(max_salary+1)
        asumistuki=np.zeros(max_salary+1)
        toimeentulotuki=np.zeros(max_salary+1)
        ansiopvraha=np.zeros(max_salary+1)
        nettotulot=np.zeros(max_salary+1)
        lapsilisa=np.zeros(max_salary+1)
        perustulo=np.zeros(max_salary+1)
        elatustuki=np.zeros(max_salary+1)
        margasumistuki=np.zeros(max_salary+1)
        margtoimeentulotuki=np.zeros(max_salary+1)
        margansiopvraha=np.zeros(max_salary+1)
        margverot=np.zeros(max_salary+1)        
        margpvhoito=np.zeros(max_salary+1)        
        margyht=np.zeros(max_salary+1)        
        margyht2=np.zeros(max_salary+1)        
        tva_asumistuki=np.zeros(max_salary+1)
        tva_toimeentulotuki=np.zeros(max_salary+1)
        tva_ansiopvraha=np.zeros(max_salary+1)
        tva_verot=np.zeros(max_salary+1)        
        tva_pvhoito=np.zeros(max_salary+1)        
        tva_yht=np.zeros(max_salary+1)        
        tva_yht2=np.zeros(max_salary+1)        
        
        if p is None:
            p=self.get_default_parameter()
            
        p2=p.copy()

        p2['t']=0 # palkka
        n0,q0=self.laske_tulot(p2,elake=0)
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1,q1=self.laske_tulot(p2,elake=0)
            p2['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p2,elake=0)
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            tulot2,tvat=self.laske_marginaalit(q0,q1,t,laske_tyollistymisveroaste=1)
            netto[t]=n1
            palkka[t]=t
            margasumistuki[t]=marg['asumistuki']
            margtoimeentulotuki[t]=marg['toimtuki']
            margverot[t]=marg['verot']
            margansiopvraha[t]=marg['ansiopvraha']
            margpvhoito[t]=marg['pvhoito']
            margyht[t]=marg['marginaali']
            margyht2[t]=marg['marginaaliveroprosentti']
            asumistuki[t]=q1['asumistuki']
            toimeentulotuki[t]=q1['toimtuki']
            ansiopvraha[t]=q1['ansiopvraha_nettonetto']+q1['puolison_ansiopvraha_nettonetto']
            lapsilisa[t]=q1['lapsilisa']
            nettotulot[t]=tulot['tulotnetto']
            tva_asumistuki[t]=tvat['asumistuki']
            tva_toimeentulotuki[t]=tvat['toimtuki']
            tva_verot[t]=tvat['verot']
            tva_ansiopvraha[t]=tvat['ansiopvraha']
            tva_pvhoito[t]=tvat['pvhoito']
            tva_yht[t]=tvat['marginaali']
            tva_yht2[t]=tvat['marginaaliveroprosentti']

            eff[t]=(1-(n2-n1)/dt)*100
            if t>0:
                tva[t]=(1-(n1-n0)/t)*100
            else:
                tva[t]=0
                
        fig,axs = plt.subplots()
        axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,labels=('Verot','Asumistuki','Toimeentulotuki','Työttömyysturva','Päivähoito'))
        axs.plot(eff,label='Vaihtoehto')
        #axs.plot(margyht,label='Vaihtoehto2')
        #axs.plot(margyht2,label='Vaihtoehto3')
        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Eff.marginaalivero (%)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        axs.set_ylim(0, 120)
        axs.legend(loc='upper right')
        plt.show()
        
        fig,axs = plt.subplots()
        axs.stackplot(palkka,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,labels=('Asumistuki','Toimeentulotuki','Työttömyysturva','Palkka','Lapsilisä'))
        axs.plot(netto,label='Vaihtoehto')
        
        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Käteen (e/kk)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        axs.legend(loc='lower right')
        plt.show()

        fig,axs = plt.subplots()
        axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,labels=('Verot','Asumistuki','Toimeentulotuki','Työttömyysturva','Päivähoito'))
        axs.plot(tva,label='Vaihtoehto')
        #axs.plot(tva_yht,label='Vaihtoehto2')
        #axs.plot(tva_yht2,label='Vaihtoehto3')
        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Työllistymisveroaste (e/kk)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        axs.set_ylim(0, 120)
        axs.legend(loc='upper right')
        plt.show()
                
        return netto,eff,tva        

    def laske_ja_plottaa_veromarginaalit(self,p=None,min_salary=0,max_salary=6000,basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus"):
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
        
        if p is None:
            p=self.get_default_parameter()
            
        p2=p.copy()

        p2['t']=0 # palkka
        n0,q0=self.laske_tulot(p2,elake=0)
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1,q1=self.laske_tulot(p2,elake=0)
            p2['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p2,elake=0)
            palkka[t]=t
            
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            margvaltionvero[t]=marg['valtionvero']
            margkunnallisvero[t]=marg['kunnallisvero']
            margverot[t]=marg['verot']
            margansiotulovah[t]=marg['ansiotulovah']
            margtyotulovah[t]=marg['tyotulovahennys']
            margperusvahennys[t]=marg['perusvahennys']
            margptel[t]=marg['ptel']
            margsairausvakuutus[t]=marg['sairausvakuutus']
            margtyotvakmaksu[t]=marg['tyotvakmaksu']
            margpuolisonverot[t]=marg['puolison_verot']
                
        fig,axs = plt.subplots()
        axs.stackplot(palkka,margvaltionvero,margkunnallisvero,margansiotulovah,margtyotulovah,margperusvahennys,margptel,margsairausvakuutus,margtyotvakmaksu,margpuolisonverot,\
            labels=('Valtionvero','Kunnallisvero','Ansiotulovähennys','Työtulovähennys','Perusvähennys','PTEL','sairausvakuutus','työttömyysvakuutusmaksu','puolison verot'))
        axs.plot(margverot,label='Yht')
        #axs.plot(margyht,label='Vaihtoehto2')
        #axs.plot(margyht2,label='Vaihtoehto3')
        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Eff.marginaalivero (%)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        axs.set_ylim(0, 120)
        axs.legend(loc='upper left')
        plt.show()
                
        #return netto,eff,tva        
