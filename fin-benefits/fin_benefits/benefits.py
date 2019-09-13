"""
Etuuslajien funktioita
"""

import numpy as np
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
        
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,p):

        menot=asumismenot+muutmenot    
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
        if p['piikit_pois']<1: 
            if tuki<10:
                tuki=0    
            
        return tuki
    

    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot_2018_EK(self,hoidossa,tulot,p):
        if p['piikit_pois']>0:
            minimimaksu=0    
        else:
            minimimaksu=10    

        prosentti1=0.08    
        prosentti2=0.5    
        prosentti3=0.2    
        maksimimaksu=250    

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
                if (pmaksu<minimimaksu):
                    kerroin=0    
                else:
                    kerroin=1    
                end
            elif hoidossa==2:
                if (pmaksu<minimimaksu):
                    kerroin=0    
                else:
                    if (prosentti2*pmaksu<minimimaksu):
                        kerroin=1    
                    else:
                        kerroin=1+prosentti2    
            else:
                if (pmaksu<minimimaksu):
                    kerroin=0    
                else:
                    if (prosentti2*pmaksu<minimimaksu):
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

    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,ansiopvrahan_suojaosa,lapsikorotus):
        if tyoton>0:
            if lapsikorotus<1:
                lapsia=0    

            lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
            sotumaksu=0.0448     # 2015 0.0428 2016 0.0460
            if saa_ansiopaivarahaa>0: 
                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-sotumaksu)     
        
                taite=3078.60    
                if vakpalkka>taite:
                    tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus    
                else:
                    tuki2=0.45*max(0,vakpalkka-perus)+perus    

                tuki2=tuki2+lapsikorotus[min(lapsia+1,4)]    
                suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa)    
        
                perus=peruspaivaraha(lapsia)     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavattulo=max(0,tyotaikaisettulot-suojaosa)    
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavattulo)    
                if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
                    ansiopaivarahamaara=max(0,vakpalkka-tyotaikaisettulot)    

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

    def verotus2018(self,palkkatulot,muuttulot,elaketulot,lapsia,p):
    
        # tulot e/kk sisältää työttömyyskorvauksen, palkkatulot ei
        # 
        # Vuoden 2018 tuloveroasteikko

        lapsivahennys=0 # poistui 2018
    
        peritytverot=0
        kk_jakaja=12
    
        kunnallisvero_pros=0.1984 # Viitamäen raportista
        tyottomyysvakuutusmaksu=0.0190 #
        tyontekijan_maksu=0.0635 # PTEL
    
        # sairausvakuutus
        sairaanhoitomaksu=0.0
        #sairaanhoitomaksu_etuus=0.0147 # muut
        paivarahamaksu_pros=0.0153 # palkka
        paivarahamaksu_raja=14020/kk_jakaja
    
        # vähennetään sosiaaliturvamaksut
        if p['piikit_pois']<1:
            if palkkatulot>58.27:
                ptel=(palkkatulot-58.27)*tyontekijan_maksu
            else:
                ptel=0
        else:
            ptel=(palkkatulot-58.27)*tyontekijan_maksu

        tyotvakmaksu=palkkatulot*tyottomyysvakuutusmaksu
        if p['piikit_pois']>0:
            sairausvakuutus=palkkatulot*paivarahamaksu_pros
        else:
            if palkkatulot>paivarahamaksu_raja:
                sairausvakuutus=palkkatulot*paivarahamaksu_pros
            else:
                sairausvakuutus=0

        peritytverot=peritytverot+sairausvakuutus+ptel+tyotvakmaksu
        palkkatulot=palkkatulot-sairausvakuutus-ptel-tyotvakmaksu 
        tulot=palkkatulot+muuttulot
    
        # tulonhankkimisvähennys pienentää ansiotuloa
    
        tulonhankkimisvahennys=750/kk_jakaja
        palkkatulot=max(0,palkkatulot-tulonhankkimisvahennys) # puhdas ansiotulo
        tulot=palkkatulot+muuttulot+elaketulot
    
        # ylevero
    
        yleveropros=0.025
        min_ylevero=0/kk_jakaja
        max_ylevero=163/kk_jakaja
        ylevero_alaraja=14750
    
        ylevero=min(max_ylevero,yleveropros*max(0,elaketulot+palkkatulot-ylevero_alaraja))
    
        if p['piikit_pois']<1:
            if ylevero<min_ylevero:
                ylevero=0
    
        valtionvero=ylevero
    
        peritytverot=peritytverot+ylevero
        palkkatulot=max(0,palkkatulot-ylevero)

        # työtulovähennys vähennetään valtionveroista
    
        #switch (p['veromalli)
        max_tyotulovahennys=1540/kk_jakaja
        ttulorajat=np.array([2500,33000,127000])/kk_jakaja
        ttulopros=np.array([0.120,0.0165,0])
        #end
    
        if palkkatulot>ttulorajat[1]:
            if palkkatulot>ttulorajat[2]:
                tyotulovahennys=0
            else:
                tyotulovahennys=min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot-ttulorajat[0])))
        else:
            if palkkatulot>ttulorajat[0]:
                tyotulovahennys=min(max_tyotulovahennys,max(0,ttulopros[0]*(palkkatulot-ttulorajat[0])))
            else:
                tyotulovahennys=0

        if tulot>ttulorajat[1]:
            if tulot>ttulorajat[2]:
                tyotulovahennys=0
            else:
                tyotulovahennys=max(0,tyotulovahennys-ttulopros[1]*max(0,tulot-ttulorajat[0]))

        # valtioverotus
        # varsinainen verotus

        valtionvero=valtionvero+self.laske_valtionvero_2018(tulot,p)
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
        rajat=np.array([2500,7230,14000])/kk_jakaja
        maxvahennys=3570/kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
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
        max_perusvahennys=3020/kk_jakaja
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
    
        return [netto,peritytverot,valtionvero,kunnallisvero,kunnallisveronperuste,\
        valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,tyotulovahennys_kunnallisveroon,\
        ptel,sairausvakuutus,tyotvakmaksu]


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
    
    def laske_valtionvero_2018(self,tulot,p):

        rajat=np.array([17200,25700,42400,74200])/12
        pros=np.array([0.06,0.1725,0.2125,0.3125])

        if p['piikit_pois']>0:
            vero=0
        else:
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

        ansiopvraha=0
        #switch (p['ansiopvrahamalli'])
        #    case 3
        #        [ansiopvraha,puhdasansiopvraha,peruspvraha]=ansiopaivaraha_v3(p['tyoton,p['vakiintunutpalkka,p['lapsia,p['t,p['saa_ansiopaivarahaa,p['ansiopvrahan_suojaosa,p['ansiopvraha_kulmakerroin,p['ansiopvraha_ylarajamalli,p['ansiopvraha_lapsikorotus,p['ansiopvraha_korotus)
        #    case 2
        #        [ansiopvraha,puhdasansiopvraha,peruspvraha]=ansiopaivaraha_v2(p['tyoton,p['vakiintunutpalkka,p['lapsia,p['t,p['saa_ansiopaivarahaa,p['ansiopvrahan_suojaosa,p['ansiopvraha_kulmakerroin,p['ansiopvraha_ylarajamalli,p['ansiopvraha_lapsikorotus,p['ansiopvraha_korotus)
        #    case 0
        #        ansiopvraha=0
        #        puhdasansiopvraha=0
        #        peruspvraha=0
        #    else:
        if p['elakkeella']<0:
            ansiopvraha,puhdasansiopvraha,peruspvraha=self.ansiopaivaraha(p['tyoton'],p['vakiintunutpalkka'],p['lapsia'],p['t'],p['saa_ansiopaivarahaa'],p['ansiopvrahan_suojaosa'],p['ansiopvraha_lapsikorotus'])
            kokoelake=0
        else:
            p['tyoton']=0
            p['saa_ansiopaivarahaa']=0
            kokoelake=self.laske_kokonaiselake(p['ika'], elake, 1)
            ansiopvraha,puhdasansiopvraha,peruspvraha=(0,0,0)

        if (p['aikuisia']>1):
            #switch (p['ansiopvrahamalli)
            #    case 3
            #        [puolison_ansiopvraha]=ansiopaivaraha_v3(p['puoliso_tyoton,p['puolison_vakiintunutpalkka,p['lapsia,p['puolison_tulot,p['puoliso_saa_ansiopaivarahaa,p['ansiopvrahan_suojaosa,p['ansiopvraha_kulmakerroin,p['ansiopvraha_ylarajamalli,p['ansiopvraha_lapsikorotus,p['ansiopvraha_korotus)
            #    case 2
            #        [puolison_ansiopvraha]=ansiopaivaraha_v2(p['puoliso_tyoton,p['puolison_vakiintunutpalkka,p['lapsia,p['puolison_tulot,p['puoliso_saa_ansiopaivarahaa,p['ansiopvrahan_suojaosa,p['ansiopvraha_kulmakerroin,p['ansiopvraha_ylarajamalli,p['ansiopvraha_lapsikorotus,p['ansiopvraha_korotus)
            #    case 0
            #        puolison_ansiopvraha=0
            #    else:
            puolison_ansiopvraha=self.ansiopaivaraha(p['puoliso_tyoton'],p['puolison_vakiintunutpalkka'],p['lapsia'],p['puolison_tulot'],p['puoliso_saa_ansiopaivarahaa'],p['ansiopvrahan_suojaosa'],p['ansiopvraha_lapsikorotus'])
        else:
            puolison_ansiopvraha=0
    
        _,verot,valtionvero,kunnallisvero,kunnallisveronperuste,valtionveroperuste,\
            ansiotulovahennys,perusvahennys,tyotulovahennys,tyotulovahennys_kunnallisveroon,\
            ptel,sairausvakuutus,tyotvakmaksu=self.verotus(p['t'],ansiopvraha,kokoelake,p['lapsia'],p)
        _,verot_ilman_etuuksia,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,kokoelake,p['lapsia'],p)

        if (p['aikuisia']>0):
            _,puolison_verot,_,_,_,_,_,_,_,_,puolison_ptel,puolison_sairausvakuutus,\
                puolison_tyotvakmaksu=self.verotus(p['puolison_tulot'],puolison_ansiopvraha,0,0,p) # onko oikein että lapsia 0 tässä????
            _,puolison_verot_ilman_etuuksia,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puolison_tulot'],0,0,0,p)
        else:
            puolison_verot_ilman_etuuksia=0
            puolison_verot=0
            puolison_ptel=0
            puolison_sairausvakuutus=0
            puolison_tyotvakmaksu=0
    
        #switch (p['elatustukimalli)
        #    case 0
        elatustuki=0
        #    else:
        #        elatustuki=laske_elatustuki(p['lapsia'],p['aikuisia)
        #end

        #switch (p['asumistukimalli)
        #    case 2
        #        atuki=asumistuki_v2(p['puolison_tulot+p['t,ansiopvraha+puolison_ansiopvraha,p['asumismenot_asumistuki,p)
        #    case 3
        #        atuki=asumistuki_v3(p['puolison_tulot+p['t,ansiopvraha+puolison_ansiopvraha,p['asumismenot_asumistuki,p)
        #    case 4
        #        atuki=asumistuki_v4(p['puolison_tulot+p['t,ansiopvraha+puolison_ansiopvraha,p['asumismenot_asumistuki,p)
        #    case 5
        #        atuki=asumistuki_v5(p['puolison_tulot+p['t,ansiopvraha+puolison_ansiopvraha,p['asumismenot_asumistuki,p)
        #    case 6
        #        atuki=asumistuki_v6(p['puolison_tulot+p['t,ansiopvraha+puolison_ansiopvraha,p['asumismenot_asumistuki,p)
        #    case 0
        #        atuki=0
        #    else:
        atuki=self.asumistuki(p['puolison_tulot']+p['t'],ansiopvraha+puolison_ansiopvraha,p['asumismenot_asumistuki'],p)
        #end
    
        #pvhoito=0
        #switch (p['paivahoitomalli)
        #    case 2
        #        pvhoito=paivahoitomenot_v2(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #    case 3
        #        pvhoito=paivahoitomenot_v3(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #    case 4
        #        pvhoito=paivahoitomenot_v4(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #    case 5
        #        pvhoito=paivahoitomenot_v5(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #    case 6
        #        pvhoito=paivahoitomenot_2018(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #    case 7
        #        pvhoito=paivahoitomenot_2018_EK(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #    case 8
        #        pvhoito=paivahoitomenot_2018_EK_35alennus(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #    case 0
        #        pvhoito=0
        #    else:
        pvhoito=self.paivahoitomenot_2018_EK(p['paivahoidossa'],p['puolison_tulot']+p['t']+elatustuki+ansiopvraha+puolison_ansiopvraha,p)
        #end
    
        #switch (p['kotihoidontukimalli)
        #case 1
        if (p['lapsia_kotihoidontuella']>0):
            alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['alle3v'])
            pvhoito=pvhoito-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['alle3v'],alle_kouluikaisia) # etumerkki!
        #    end
        #case 2
        #    if (p['lapsia_kotihoidontuella>0)
        #        alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella-p['alle3v)
        #        pvhoito=pvhoito-kotihoidontuki2(p['lapsia_kotihoidontuella,p['alle3v,alle_kouluikaisia) # etumerkki!
        #    end
        #case 0
        #    # ei tehdä mitään.
        #end

        #switch (p['paivahoitomalli)
        #    case 2
        #        pvhoito_ilman_etuuksia=paivahoitomenot_v2(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki,p)
        #    case 3
        #        pvhoito_ilman_etuuksia=paivahoitomenot_v3(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki,p)
        #    case 4
        #        pvhoito_ilman_etuuksia=paivahoitomenot_v4(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki,p)
        #    case 5
        #        pvhoito_ilman_etuuksia=paivahoitomenot_v5(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki,p)
        #    case 6
        #        pvhoito_ilman_etuuksia=paivahoitomenot_2018(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki,p)
        #    case 7
        pvhoito_ilman_etuuksia=self.paivahoitomenot_2018_EK(p['paivahoidossa'],p['puolison_tulot']+p['t']+elatustuki,p)
        #    case 8
        #        pvhoito_ilman_etuuksia=paivahoitomenot_2018_EK_35alennus(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki,p)
        #    case 0
        #        pvhoito_ilman_etuuksia=0
        #    else:
        #        pvhoito_ilman_etuuksia=paivahoitomenot(p['paivahoidossa,p['puolison_tulot+p['t+elatustuki,p)
        #end
    
        #switch (p['lapsilisamalli)
        #    case 0
        #        lapsilisa=0
        #    else:
        lapsilisa=self.laske_lapsilisa(p['lapsia'])
        #end
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot
        puolison_ansiopvraha_netto=puolison_ansiopvraha-(puolison_verot-puolison_verot_ilman_etuuksia)
        ansiopvraha_netto=ansiopvraha-(verot-verot_ilman_etuuksia)
    
        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia
        # käytässä??
        if (puolison_ansiopvraha_netto+ansiopvraha_netto>0):
            suhde=max(0,ansiopvraha_netto/(puolison_ansiopvraha_netto+ansiopvraha_netto))
            ansiopvraha_nettonetto=ansiopvraha_netto-suhde*(pvhoito-pvhoito_ilman_etuuksia)
            puolison_ansiopvraha_nettonetto=puolison_ansiopvraha_netto-(1-suhde)*(pvhoito-pvhoito_ilman_etuuksia)
            #ansiopvraha_nettonetto=ansiopvraha_netto
            #puolison_ansiopvraha_nettonetto=puolison_ansiopvraha_netto
        else:
            ansiopvraha_nettonetto=0
            puolison_ansiopvraha_nettonetto=0

        #switch (p['perustulomalli)
        #    case 1 # Kelan malli
        #        perustulo=laske_perustulo_Kelamalli(ansiopvraha_netto) # yhteensovitus
        #        puolison_perustulo=laske_perustulo_Kelamalli(puolison_ansiopvraha_netto) # yhteensovitus
        #    case 0
        perustulo=0
        puolison_perustulo=0

        #     switch (p['toimeentulotukimalli)
        #     case 2
        #         toimtuki=toimeentulotuki_v2(p['t,verot_ilman_etuuksia,p['puolison_tulot,puolison_verot_ilman_etuuksia,\
        #             elatustuki+ansiopvraha_netto+puolison_ansiopvraha_netto+atuki+lapsilisa,0,\
        #             p['asumismenot_toimeentulo,pvhoito,p)
        #     case 3
        #         toimtuki=toimeentulotuki_v3(p['t,verot_ilman_etuuksia,p['puolison_tulot,puolison_verot_ilman_etuuksia,\
        #             elatustuki+ansiopvraha_netto+puolison_ansiopvraha_netto+atuki+lapsilisa,0,\
        #             p['asumismenot_toimeentulo,pvhoito,p)
        #     case 4
        #         toimtuki=asumis_ja_toimeentulotuki(p['t,verot_ilman_etuuksia,p['puolison_tulot,puolison_verot_ilman_etuuksia,\
        #             ansiopvraha+puolison_ansiopvraha,\
        #             elatustuki+ansiopvraha_netto+puolison_ansiopvraha_netto+atuki+lapsilisa,\
        #             p['asumismenot_yhdistetty,p['asumismenot_toimeentulo,pvhoito,p)
        #     case 5
        #         toimtuki=asumis_ja_toimeentulotuki_v2(p['t,verot_ilman_etuuksia,p['puolison_tulot,puolison_verot_ilman_etuuksia,\
        #             ansiopvraha+puolison_ansiopvraha,\
        #             elatustuki+ansiopvraha_netto+puolison_ansiopvraha_netto+atuki+lapsilisa,\
        #             p['asumismenot_yhdistetty,p['asumismenot_toimeentulo,pvhoito,p)
        #     case 6
        #         toimtuki=asumis_ja_toimeentulotuki_v3(p['t,verot_ilman_etuuksia,p['puolison_tulot,puolison_verot_ilman_etuuksia,\
        #             ansiopvraha+puolison_ansiopvraha,\
        #             elatustuki+ansiopvraha_netto+puolison_ansiopvraha_netto+atuki+lapsilisa,\
        #             p['asumismenot_yhdistetty,p['asumismenot_toimeentulo,pvhoito,p)
        #     case 7
        #         toimtuki=asumis_ja_toimeentulotuki_v4(p['t,verot_ilman_etuuksia,p['puolison_tulot,puolison_verot_ilman_etuuksia,\
        #             ansiopvraha+puolison_ansiopvraha,\
        #             elatustuki+ansiopvraha_netto+puolison_ansiopvraha_netto+atuki+lapsilisa,\
        #             p['asumismenot_yhdistetty,pvhoito,p)
        #     case 0
        #         toimtuki=0
        #     else:
        toimtuki=self.toimeentulotuki(p['t'],verot_ilman_etuuksia,p['puolison_tulot'],puolison_verot_ilman_etuuksia,\
            elatustuki+elake+ansiopvraha_netto+puolison_ansiopvraha_netto+atuki+lapsilisa,0,\
            p['asumismenot_toimeentulo'],pvhoito,p)
        #end
    
        perustulo=0
        puolison_perustulo=0
    
        perustulo_netto=0
        puolison_perustulo_netto=0
    
        kateen=kokoelake+p['puolison_tulot']+p['t']+atuki+toimtuki+ansiopvraha+puolison_ansiopvraha+elatustuki-puolison_verot-verot-pvhoito+lapsilisa
        tulotnetto=kokoelake+p['puolison_tulot']+p['t']-verot_ilman_etuuksia-puolison_verot_ilman_etuuksia-pvhoito_ilman_etuuksia # ilman etuuksia
    
        q={}
        q['qansiopvraha']=ansiopvraha
        q['puhdasansiopvraha']=puhdasansiopvraha
        q['peruspvraha']=peruspvraha
        q['puolison_ansiopvraha']=puolison_ansiopvraha
        q['verot']=verot
        q['valtionvero']=valtionvero
        q['kunnallisvero']=kunnallisvero
        q['kunnallisveronperuste']=kunnallisveronperuste
        q['valtionveroperuste']=valtionveroperuste
        q['ansiotulovahennys']=ansiotulovahennys
        q['perusvahennys']=perusvahennys
        q['tyotulovahennys']=tyotulovahennys
        q['tyotulovahennys_kunnallisveroon']=tyotulovahennys_kunnallisveroon
        q['ptel']=ptel
        q['sairausvakuutus']=sairausvakuutus
        q['tyotvakmaksu']=tyotvakmaksu
        q['verot_ilman_etuuksia']=verot_ilman_etuuksia
        q['puolison_verot']=puolison_verot
        q['puolison_verot_ilman_etuuksia']=puolison_verot_ilman_etuuksia
        q['elatustuki']=elatustuki
        q['atuki']=atuki
        q['pvhoito']=pvhoito
        q['pvhoito_ilman_etuuksia']=pvhoito_ilman_etuuksia
        q['ansiopvraha_netto']=ansiopvraha_netto
        q['puolison_ansiopvraha_netto']=puolison_ansiopvraha_netto
        q['toimtuki']=toimtuki
        q['lapsilisa']=lapsilisa
        q['ansiopvraha_nettonetto']=ansiopvraha_nettonetto
        q['puolison_ansiopvraha_nettonetto']=puolison_ansiopvraha_nettonetto
        q['puolison_ptel']=puolison_ptel
        q['puolison_sairausvakuutus']=puolison_sairausvakuutus
        q['puolison_tyotvakmaksu']=puolison_tyotvakmaksu
        q['perustulo']=perustulo
        q['puolison_perustulo']=puolison_perustulo
        q['perustulo_netto']=perustulo_netto
        q['puolison_perustulo_netto']=puolison_perustulo_netto
    
        #print(q)
    
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

        max_meno=max_menot[min(4,p['aikuisia']+p['lapsia']),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=300*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
        if p['piikit_pois']<1:
            if perusomavastuu<10:
                perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
    
        return tuki


    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot(self,hoidossa,tulot,p):
        if p['piikit_pois']>0:
            minimimaksu=0
        else:
            minimimaksu=10

        prosentti2=0.5
        prosentti3=0.2
        maksimimaksu=290

        if p['lapsia']>0:
            vakea=p['lapsia']+p['aikuisia']
            if vakea==1:
                alaraja=2050
                prosentti=0.107
            elif vakea==2:
                alaraja=2050
                prosentti=0.107
            elif vakea==3:
                alaraja=2646
                prosentti=0.107
            elif vakea==4:
                alaraja=3003
                prosentti=0.107
            elif vakea==5:
                alaraja=3361
                prosentti=0.107
            elif vakea==6:
                alaraja=3718
                prosentti=0.107
            else:
                alaraja=3718+138*(vakea-6)
                prosentti=0.107

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
    
    def laske_kokonaiselake(self,ika,tyoelake,yksin):
        kansanelake=self.laske_kansanelake(ika,tyoelake,yksin)
        takuuelake=self.laske_takuuelake(ika,kansanelake,tyoelake)
        kokoelake=tyoelake+kansanelake+takuuelake
    
        return kokoelake
    
    def laske_ja_plottaa(self,p=None,min_salary=0,max_salary=6000):
        netto=np.zeros(max_salary+1)
        palkka=np.zeros(max_salary+1)
        tva=np.zeros(max_salary+1)
        
        if p==None:
            p=self.get_default_parameter()

        dt=100

        for t in range(0,max_salary):
            p['t']=t # palkka
            n1,q1=self.laske_tulot(p,elake=0)
            p['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p,elake=0)
            netto[t]=n1
            palkka[t]=t
            tva[t]=(n2-n1)/dt*100
        
        fig, axs = plt.subplots()
        axs.plot(netto)

        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Käteen')
        
        axs.grid(True)
        axs.set_xlim(0, max_salary)

        fig, axs = plt.subplots()
        axs.plot(tva)
        axs.set_xlabel('Palkka (e/kk)')
        axs.set_ylabel('Työllistymisveroaste (%)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)

        plt.show()

    def perheparametrit(self,perhetyyppi):

        lapsia_kotihoidontuella=0    
        alle3v=0    

        if perhetyyppi==1: # 1+0, töissä
            lapsia=0    
            paivahoidossa=0    
            aikuisia=1    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=0    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==2: # 1+0, työtön ansiopäivärahalla 
            lapsia=0    
            paivahoidossa=0    
            aikuisia=1    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==3: # 1+0, työtön työmarkkinatuella
            lapsia=0    
            paivahoidossa=0    
            aikuisia=1    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==4: # 1+1, 
            lapsia=1    
            paivahoidossa=1    
            aikuisia=1    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==5: # 2+1, molemmat töissä (puoliso osapäivätöissä)
            lapsia=1    
            paivahoidossa=1    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=0    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=1250    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==6: # 2+1, puoliso ansioturvalla
            lapsia=2    
            paivahoidossa=2    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=0    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==7: # 2+1, molemmat ansiopaivarahalla
            lapsia=1    
            paivahoidossa=1    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==8: # 2+2, molemmat töissä
            lapsia=1    
            paivahoidossa=1    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=1    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==9: # 2+3, molemmat töissä
            lapsia=3    
            paivahoidossa=1    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=1    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==10: # 1+1, 
            lapsia=1    
            paivahoidossa=1    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==11: # 1+3, ansiopaivarahalla
            lapsia=3    
            paivahoidossa=2    
            aikuisia=1    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==12: # 2+2, työmarkkinatuella
            lapsia=2    
            paivahoidossa=2    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    
        elif perhetyyppi==13: # 2+2, ansiosidonnaisella
            lapsia=2    
            paivahoidossa=2    
            aikuisia=2    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0            
        elif perhetyyppi==14: # 2+1, puoliso työssä
            lapsia=1    
            paivahoidossa=1    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=1250    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0          
        elif perhetyyppi==16: # 1+2, työmarkkinatuelta töihin, Kaupalle: #1
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=0    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==17: # 2+2, työssä, työllistyvä puolis0 1250e/kk
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=2    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=0    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=2000    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0         
        elif perhetyyppi==18: # 2+2, kotihoidontuella, puolis0 2500e/kk
            lapsia=2    
            paivahoidossa=0    
            lapsia_kotihoidontuella=2    
            alle3v=2    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=0    
            saa_ansiopaivarahaa=0    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==19: # 2+2, kotihoidontuelta työhön, puolis0 2500e/kk
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=2    
            aikuisia=2    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==20: # 1+2, työmarkkinatuelta töihin, Kaupalle: #2
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=0    
            aikuisia=1    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==21: # 1+2, ansiosidonnaiselta töihin, Kaupalle: #3
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=0    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==22: # 1+1, työmarkkinatuelta töihin, Kaupalle: #4
            lapsia=1    
            paivahoidossa=1    
            lapsia_kotihoidontuella=0    
            alle3v=0    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==23: # 2+2, työmarkkinatuelta töihin, Kaupalle: #5
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=0    
            aikuisia=2    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==24: # 2+2, työmarkkinatuelta töihin, puoliso tm-tuella, Viitamäki kuvio: #12 & #13
            lapsia=2    
            paivahoidossa=1    
            lapsia_kotihoidontuella=0    
            alle3v=0    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==25: # 2+2, ansiopäivärahalta töihin, puoliso tm-tuella, Viitamäki kuvio #14 & #15
            lapsia=2    
            paivahoidossa=1    
            lapsia_kotihoidontuella=0    
            alle3v=0    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==26: # 2+2, työmarkkinatuella, päivähoidossa 0
            lapsia=2    
            paivahoidossa=0    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0            
        elif perhetyyppi==27: # 2+2, työmarkkinatuella, päivähoidossa 2
            lapsia=2    
            paivahoidossa=2    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0            
        elif perhetyyppi==28: # 2+2, ei työmarkkinatuella, päivähoidossa 2
            lapsia=2    
            paivahoidossa=2    
            aikuisia=2    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=2500    
            puolison_vakiintunutpalkka=2500    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0            
        elif perhetyyppi==29: # 1+1, työmarkkinatuelta töihin, Viitamäki HS 
            lapsia=1    
            paivahoidossa=1    
            lapsia_kotihoidontuella=0    
            alle3v=1    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=1    
            puoliso_saa_ansiopaivarahaa=0                  
        elif perhetyyppi==30: # 2+1, tmtuki, puoliso osapäivätyössä
            lapsia=1    
            paivahoidossa=1    
            aikuisia=2    
            vakiintunutpalkka=2500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=1250    
            puolison_vakiintunutpalkka=1250    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0       
        elif perhetyyppi==31: # 1+3, työmarkkinatuelta töihin, Viitamäki HS 
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=1    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=0    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0       
        elif 32: # 1+1, työmarkkinatuelta töihin, Viitamäki HS 
            lapsia=2    
            paivahoidossa=2    
            lapsia_kotihoidontuella=0    
            alle3v=1    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0                
        else: # 1+0
            lapsia=0    
            paivahoidossa=0    
            aikuisia=1    
            vakiintunutpalkka=1500    
            tyoton=1    
            saa_ansiopaivarahaa=1    
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    

        # perhekoko          1   2   3   4    5
        # luvut peräisin Viitamäeltä
        vuokra_toimeentulo=np.array([440,660,850,980,1150]) # helsinki 675 800 919 1008 +115/hlo
        vuokra_asumistuki =np.array([411,600,761,901,1024])
        vuokra_yhdistetty =vuokra_toimeentulo    

        asumismenot_toimeentulo=vuokra_toimeentulo[lapsia+aikuisia]
        asumismenot_asumistuki=vuokra_asumistuki[lapsia+aikuisia]
        asumismenot_yhdistetty=vuokra_yhdistetty[lapsia+aikuisia]
    
        if (aikuisia<2):
            puolison_tulot=0    
            puolison_vakiintunutpalkka=0    
            puoliso_tyoton=0    
            puoliso_saa_ansiopaivarahaa=0    

        if (puoliso_tyoton>0):
            puolison_tulot=0    

        if (paivahoidossa>lapsia):
            paivahoidossa=lapsia   
        
        return lapsia,paivahoidossa,lapsia_kotihoidontuella,aikuisia,vakiintunutpalkka,tyoton,saa_ansiopaivarahaa, \
        puolison_tulot,puolison_vakiintunutpalkka,puoliso_tyoton,puoliso_saa_ansiopaivarahaa, \
        asumismenot_asumistuki,asumismenot_toimeentulo,alle3v,asumismenot_yhdistetty 

