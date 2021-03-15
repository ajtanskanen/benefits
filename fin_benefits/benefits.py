"""

    benefits
    
    implements social security and social insurance benefits in the Finnish social security schemes


"""

import numpy as np
from .parameters import perheparametrit
import matplotlib.pyplot as plt
import seaborn as sns

class Benefits():
    """
    Description:
        The Finnish Earnings-related Social Security

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
        self.language='Finnish' # 'English'
        
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
            elif key=='irr_vain_tyoelake': # lasketaanko irr
                if value is not None:
                    self.irr_vain_tyoelake=value
            elif key=='additional_income_tax':
                if value is not None:
                    self.additional_income_tax=value
            elif key=='additional_income_tax_high':
                if value is not None:
                    self.additional_income_tax_high=value
            elif key=='additional_tyel_premium':
                if value is not None:
                    self.additional_tyel_premium=value
            elif key=='additional_kunnallisvero':
                if value is not None:
                    self.additional_kunnallisvero=value
    
        # choose the correct set of benefit functions for computations
        self.set_year(self.year)
        self.setup_labels()
        
    def explain(self,p=None):
        #self.tee_selite()
        if p is None:
            print('Ei parametrejä')
        else:
            selite=tee_selite(p)
            print(p)
            
    def setup_labels(self):
        self.labels={}
        if self.language=='English':
            self.labels['wage']='Wage (e/m)'
            self.labels['effective']='Eff.marg.tax (%)'
            self.labels['valtionvero']='State tax'
            self.labels['kunnallisvero']='Municipal tax'
            self.labels['telp']='Employee pension premium'
            self.labels['sairausvakuutus']='Health insurance'
            self.labels['työttömyysvakuutusmaksu']='työttömyysvakuutusmaksu'
            self.labels['puolison verot']='puolison verot'
            self.labels['taxes']='Taxes'
            self.labels['asumistuki']='Housing benefit'
            self.labels['toimeentulotuki']='Supplementary benefit'
            self.labels['tyottomyysturva']='Unemployment benefit'
            self.labels['paivahoito']='Daycare'
            self.labels['elake']='Pension'
        else:
            self.labels['wage']='Palkka (e/kk)'
            self.labels['effective']='Eff.marg.veroaste (%)'
            self.labels['valtionvero']='Valtionvero'
            self.labels['kunnallisvero']='Kunnallisvero'
            self.labels['telp']='TEL-P'
            self.labels['sairausvakuutus']='Sairausvakuutus'
            self.labels['työttömyysvakuutusmaksu']='Työttömyysvakuutusmaksu'
            self.labels['puolison verot']='puolison verot'
            self.labels['taxes']='Verot'
            self.labels['asumistuki']='Asumistuki'
            self.labels['toimeentulotuki']='Toimeentulotuki'
            self.labels['tyottomyysturva']='Työttömyysturva'
            self.labels['paivahoito']='Päivähoito'
            self.labels['elake']='Elake'
    
    def toimeentulotuki_param2018(self):
        min_etuoikeutettuosa=150
        lapsi1=305.87     # e/kk     alle 10v lapsi
        lapsi2=281.59     # e/kk
        lapsi3=257.32     # e/kk
        yksinhuoltaja=534.05     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=412.68    
        yksinasuva=485.50
        
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva
    
    def toimeentulotuki_param2019(self):
        min_etuoikeutettuosa=150
        lapsi1=313.29     # e/kk     alle 10v lapsi
        lapsi2=288.43     # e/kk
        lapsi3=263.56     # e/kk
        yksinhuoltaja=547.02     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=422.70    
        yksinasuva=497.29
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva

    def toimeentulotuki_param2020(self):
        min_etuoikeutettuosa=150
        lapsi1=317.56     # e/kk     alle 10v lapsi
        lapsi2=292.35     # e/kk
        lapsi3=267.15     # e/kk
        yksinhuoltaja=572.52     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=412.68    
        yksinasuva=502.21
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva
        
    def toimeentulotuki_param2021(self):
        min_etuoikeutettuosa=150
        lapsi1=317.56     # e/kk     alle 10v lapsi
        lapsi2=292.35     # e/kk
        lapsi3=267.15     # e/kk
        yksinhuoltaja=574.63     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=428.45
        yksinasuva=504.16
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva
        
    def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,
                             muuttulot,verot,asumismenot,muutmenot,p,omavastuuprosentti=0.0,alennus=0):

        omavastuu=omavastuuprosentti*asumismenot
        menot=max(0,asumismenot-omavastuu)+muutmenot
        
        min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva=self.toimeentulotuki_param()

        #menot=asumismenot+muutmenot    
        bruttopalkka=omabruttopalkka+puolison_bruttopalkka    
        palkkavero=omapalkkavero+puolison_palkkavero    
        palkkatulot=bruttopalkka-palkkavero    
        omaetuoikeutettuosa=min(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
        puolison_etuoikeutettuosa=min(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
        etuoikeutettuosa=omaetuoikeutettuosa+puolison_etuoikeutettuosa    

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
        if alennus>0:
            tuki1=tuki1*(1-alennus)
        
        tuki=max(0,tuki1+menot-max(0,omabruttopalkka-omaetuoikeutettuosa-omapalkkavero)\
                -max(0,puolison_bruttopalkka-puolison_etuoikeutettuosa-puolison_palkkavero)-verot-muuttulot)
                
        if p['toimeentulotuki_vahennys']>0: # vähennetään 20%
            tuki=tuki*0.8
                
        if tuki<10:
            tuki=0    
            
        return tuki
        
    def get_default_parameter(self):
        return perheparametrit(perhetyyppi=1)
    
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
        
        pvraha=21.5*(32.40+lisa)    
        tuki=max(0,pvraha)    
    
        return tuki
        
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
        
        pvraha=21.5*(32.40+lisa)    
        tuki=max(0,pvraha)    
    
        return tuki

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
        
        pvraha=21.5*(33.66+lisa)    
        tuki=max(0,pvraha)    
    
        return tuki

    # tmtuki samankokoinen
    def peruspaivaraha2021(self,lapsia):
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.28     # e/pv
        elif lapsia==2:
            lisa=7.76     # e/pv
        else:
            lisa=10.00     # e/pv
        
        pvraha=21.5*(33.66+lisa)    
        tuki=max(0,pvraha)    
    
        return tuki
                
    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka):
        if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
            return max(0,vakpalkka-tyotaikaisettulot) 
            
        return ansiopaivarahamaara   

    def ansiopaivaraha(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0,omavastuukerroin=1.0):
        ansiopvrahan_suojaosa=p['ansiopvrahan_suojaosa']
        lapsikorotus=p['ansiopvraha_lapsikorotus']
    
        if tyoton>0:
            if lapsikorotus<1:
                lapsia=0    

            if self.year==2018:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                sotumaksu=0.0448+0.6*self.additional_tyel_premium
                taite=3078.60    
            elif self.year==2019:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                sotumaksu=0.0448+0.6*self.additional_tyel_premium
                taite=3078.60    
            elif self.year==2020:
                lapsikorotus=np.array([0,5.28,7.76,10.00])*21.5    
                sotumaksu=0.0414+0.6*self.additional_tyel_premium
                taite=3197.70    
            elif self.year==2021:
                lapsikorotus=np.array([0,5.28,7.76,10.00])*21.5    
                sotumaksu=0.0414+0.6*self.additional_tyel_premium
                taite=3197.70    
            else:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                sotumaksu=0.0448+0.6*self.additional_tyel_premium
                taite=3078.60    
                            
            if saa_ansiopaivarahaa>0: # & (kesto<400.0): # ei keston tarkastusta!
                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-sotumaksu)     
        
                if vakpalkka>taite:
                    tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus    
                else:
                    tuki2=0.45*max(0,vakpalkka-perus)+perus    

                tuki2=tuki2+lapsikorotus[min(lapsia,3)]    
                tuki2=tuki2*ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)    
        
                perus=self.peruspaivaraha(lapsia)     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavattulo=max(0,tyotaikaisettulot-suojaosa)    
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavattulo)  
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka)  

                tuki=ansiopaivarahamaara    
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                tuki=omavastuukerroin*max(perus,tuki)     # voi tulla vastaan pienillä tasoilla4
            else:
                ansiopaivarahamaara=0    
                perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                tuki=omavastuukerroin*perus    
        else:
            perus=0    
            tuki=0    
            ansiopaivarahamaara=0   

        return tuki,ansiopaivarahamaara,perus

    def soviteltu_peruspaivaraha(self,lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p):
        suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)

        pvraha=self.peruspaivaraha(lapsia)
        vahentavattulo=max(0,tyotaikaisettulot-suojaosa)
        tuki=max(0,pvraha-0.5*vahentavattulo)
    
        return tuki
        
    def elaketulovahennys2018(self,elaketulot,tulot):
        max_elaketulovahennys_valtio=11560/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9040/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2019(self,elaketulot,tulot):
        max_elaketulovahennys_valtio=11590/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9050/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2020(self,elaketulot,tulot):
        max_elaketulovahennys_valtio=11540/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9230/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2021(self,elaketulot,tulot):
        max_elaketulovahennys_valtio=11150/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9270/self.kk_jakaja
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
        
    def ansiotulovahennys2021(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def veroparam2018(self):
        self.kunnallisvero_pros=max(0,max(0,0.1984+self.additional_kunnallisvero)) # Viitamäen raportista 19,84; verotuloilla painotettu k.a. 19,86
        self.tyottomyysvakuutusmaksu=0.0190 #
        self.tyontekijan_maksu=max(0,max(0,0.0635+self.additional_tyel_premium)) # PTEL
        self.tyontekijan_maksu_52=max(0,max(0,0.0785+self.additional_tyel_premium)) # PTEL
        self.koko_tyel_maksu=max(0,max(0,0.2440+self.additional_tyel_premium)) # PTEL 
        self.tyonantajan_sivukulut=max(0,0.6*0.0065+0.4*0.205+0.0007+0.1695+0.0134+0.01) # työttömyysvakuutusmaksu, ryhmähv, tyel, sv, työtapaturma
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0
        self.sairaanhoitomaksu_etuus=0.0147 # muut
        
        self.paivarahamaksu_pros=0.0153 # palkka
        self.paivarahamaksu_raja=14020/self.kk_jakaja    
        
        self.elakemaksu_alaraja=58.27
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2019(self):
        self.kunnallisvero_pros=max(0,0.1988+self.additional_kunnallisvero) # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0125 #
        self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
        self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
        self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0
        self.sairaanhoitomaksu_etuus=0.0161 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=14282/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2020(self):
        self.kunnallisvero_pros=max(0,0.1997+self.additional_kunnallisvero) # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0125 #
        self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
        self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
        self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0068
        self.sairaanhoitomaksu_etuus=0.0161 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=14574/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2021(self):
        self.kunnallisvero_pros=max(0,0.2002+self.additional_kunnallisvero) # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0125 #
        self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
        self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
        self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
    
        # sairausvakuutus ??
        self.sairaanhoitomaksu=0.0068
        self.sairaanhoitomaksu_etuus=0.0165 # muut
        
        self.paivarahamaksu_pros=0.0136 # palkka
        self.paivarahamaksu_raja=14766/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
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
    
    def verotus(self,palkkatulot,muuttulot,elaketulot,lapsia,p):
        lapsivahennys=0 # poistui 2018
    
        peritytverot=0
        self.kk_jakaja=12
        
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
        if palkkatulot>self.paivarahamaksu_raja: # FIXME lisää ikätarkastus
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

        #print('palkka {} valtionveroperuste {} valtionvero {} ptel {} tyotulovahennys {} sairausvakuutus {}'.format(palkkatulot,valtionveroperuste,valtionvero,ptel,tyotulovahennys,sairausvakuutus))

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
        
        # korotettu maksuperuste puuttuu? =max(0,palkkatulot-peritty_sairaanhoitomaksu)*korotus
        peritty_sairaanhoitomaksu=max(0,palkkatulot_puhdas-perusvahennys)*self.sairaanhoitomaksu+(muuttulot+elaketulot_kunnallis)*self.sairaanhoitomaksu_etuus
        
        # etuuksista peritty sairaanhoitomaksu puuttuu
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
        
        #print(peritytverot,valtionvero,kunnallisvero)
    
        return netto,peritytverot,valtionvero,kunnallisvero,kunnallisveronperuste,\
               valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
               tyotulovahennys_kunnallisveroon,ptel,sairausvakuutus,tyotvakmaksu,koko_tyoelakemaksu,ylevero

    def kotihoidontuki2018(self,lapsia,allekolmev,alle_kouluikaisia):
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
    
    def kotihoidontuki2019(self,lapsia,allekolmev,alle_kouluikaisia):
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=338.34 # e/kk
            seuraavat_alle_3v=101.29 # e/kk
            yli_3v=65.09 #e_kk
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
    
    def kotihoidontuki2020(self,lapsia,allekolmev,alle_kouluikaisia):
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=341.69 # e/kk
            seuraavat_alle_3v=102.30 # e/kk
            yli_3v=65.73 #e_kk
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
    
    def lapsilisa2020(self,yksinhuoltajakorotus=False):
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 63.3
            
        return lapsilisat
    
    def lapsilisa2021(self,yksinhuoltajakorotus=False):
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 63.3
            
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
            tuki=sum(lapsilisat[0:4])+(lapsia-5)*lapsilisat[4]
        else:
            print('error(1))')
        
        return tuki
        
    def opintoraha(self,palkka,p):
        if p['lapsia']>0:
            tuki=350.28 # +650*0.4 = opintolainahyvitys mukana?
        else:
            tuki=250.28 #+650*0.4 # opintolainahyvitys mukana
            
        if palkka>667: #+222/12: # oletetaan että täysiaikainen opiskelija
            tuki=0
            
        return tuki
        
    def check_p(self,p):
        if 'toimeentulotuki_vahennys' not in p:
            p['toimeentulotuki_vahennys']=0
        if 'opiskelija' not in p:
            p['opiskelija']=0
        if 'elakkeella' not in p:
            p['elakkeella']=0
        if 'tyoelake' not in p:
            p['tyoelake']=0
        if 'sairauspaivarahalla' not in p:
            p['sairauspaivarahalla']=0
        if 'disabled' not in p:
            p['disabled']=0
        return p

    def laske_tulot(self,p,tt_alennus=0,include_takuuelake=True):
        q={} # tulokset tänne
        q['perustulo']=0
        q['puoliso_perustulo']=0
        q['puhdas_tyoelake']=0
        q['multiplier']=1
        p=self.check_p(p)
        if p['elakkeella']>0: # vanhuuseläkkeellä
            p['tyoton']=0
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            p['saa_ansiopaivarahaa']=0
            # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
            if (p['aikuisia']>1):
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,disability=p['disabled'])
            else:
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,disability=p['disabled'])

            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            #oletetaan että myös puoliso eläkkeellä
            q['puoliso_ansiopvraha']=0
            q['opintotuki']=0
            q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'])
        elif p['opiskelija']>0:
            q['elake_maksussa']=p['tyoelake']
            q['kokoelake']=p['tyoelake']
            q['elake_tuleva']=0
            q['puoliso_ansiopvraha']=0
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
            q['opintotuki']=0
            if p['aitiysvapaalla']>0:
                q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
            elif p['isyysvapaalla']>0:
                q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
            elif p['kotihoidontuella']>0:
                q['kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            else:
                q['opintotuki']=self.opintoraha(0,p)
        else: # ei eläkkeellä     
            q['opintotuki']=0
            q['elake_maksussa']=p['tyoelake']
            q['kokoelake']=p['tyoelake']
            q['elake_tuleva']=0
            q['puoliso_ansiopvraha']=0
            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
            if p['aitiysvapaalla']>0:
                q['aitiyspaivaraha']=self.aitiysraha(p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
            elif p['isyysvapaalla']>0:
                q['isyyspaivaraha']=self.isyysraha(p['vakiintunutpalkka'])
            elif p['sairauspaivarahalla']>0:
                q['sairauspaivaraha']=self.sairauspaivaraha(p['vakiintunutpalkka'])
            elif p['kotihoidontuella']>0:
                q['kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            elif p['tyoton']>0:
                if 'omavastuukerroin' in p:
                    omavastuukerroin=p['omavastuukerroin']
                else:
                    omavastuukerroin=1.0
                q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=self.ansiopaivaraha(p['tyoton'],p['vakiintunutpalkka'],p['lapsia'],p['t'],p['saa_ansiopaivarahaa'],p['tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin)
                
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
                if p['puoliso_aitiysvapaalla']>0:
                    q['puoliso_aitiyspaivaraha']=self.aitiysraha(p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
                elif p['puoliso_isyysvapaalla']>0:
                    q['puoliso_isyyspaivaraha']=self.isyysraha(p['puoliso_vakiintunutpalkka'])
                elif p['puoliso_kotihoidontuella']>0:
                    q['puoliso_kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
                else:
                    q['puoliso_opintotuki']=self.opintoraha(0,p)
            else: # ei eläkkeellä     
                q['puoliso_kokoelake']=0
                q['puoliso_opintotuki']=0
                q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
                q['puoliso_elake_tuleva']=0
                q['puoliso_puolison_ansiopvraha']=0
                q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=(0,0,0)
                q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
                if p['puoliso_aitiysvapaalla']>0:
                    q['puoliso_aitiyspaivaraha']=self.aitiysraha(p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
                elif p['puoliso_isyysvapaalla']>0:
                    q['puoliso_isyyspaivaraha']=self.isyysraha(p['puoliso_vakiintunutpalkka'])
                elif p['puoliso_sairauspaivarahalla']>0:
                    q['puoliso_sairauspaivaraha']=self.sairauspaivaraha(p['puoliso_vakiintunutpalkka'])
                elif p['puoliso_kotihoidontuella']>0:
                    q['puoliso_kotihoidontuki']=self.kotihoidontuki(p['puoliso_lapsia_kotihoidontuella'],p['puoliso_alle_3v'],p['puoliso_alle_kouluikaisia'])
                elif p['puoliso_tyoton']>0:
                    q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=self.ansiopaivaraha(p['puoliso_tyoton'],p['puoliso_vakiintunutpalkka'],p['lapsia'],p['puoliso_tulot'],p['puoliso_saa_ansiopaivarahaa'],p['puoliso_tyottomyyden_kesto'],p)
            
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q['verot'],q['valtionvero'],q['kunnallisvero'],q['kunnallisveronperuste'],q['valtionveroperuste'],\
            q['ansiotulovahennys'],q['perusvahennys'],q['tyotulovahennys'],q['tyotulovahennys_kunnallisveroon'],\
            q['ptel'],q['sairausvakuutus'],q['tyotvakmaksu'],q['tyel_kokomaksu'],q['ylevero']=self.verotus(p['t'],
                q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
                q['kokoelake'],p['lapsia'],p)
        _,q['verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p)

        if (p['aikuisia']>1):
            _,q['puoliso_verot'],_,_,_,_,_,_,_,_,q['puoliso_ptel'],q['puoliso_sairausvakuutus'],\
                q['puoliso_tyotvakmaksu'],q['puoliso_tyel_kokomaksu'],q['puolison_ylevero']=self.verotus(p['puoliso_tulot'],q['puoliso_ansiopvraha'],0,0,p) # onko oikein että lapsia 0 tässä????
            _,q['puoliso_verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puoliso_tulot'],0,0,0,p)
        else:
            q['puoliso_verot_ilman_etuuksia']=0
            q['puoliso_verot']=0
            q['puoliso_ptel']=0
            q['puoliso_sairausvakuutus']=0
            q['puoliso_tyotvakmaksu']=0
    
        q['elatustuki']=0
        #elatustuki=laske_elatustuki(p['lapsia'],p['aikuisia)
        
        if p['elakkeella']>0:
            q['asumistuki']=self.elakkeensaajan_asumistuki(p['puoliso_tulot']+p['t'],q['kokoelake'],p['asumismenot_asumistuki'],p)
        else:
            q['asumistuki']=self.asumistuki(p['puoliso_tulot']+p['t'],q['ansiopvraha']+q['puoliso_ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],p['asumismenot_asumistuki'],p)
            
        if p['lapsia']>0:
            q['pvhoito']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['puoliso_ansiopvraha']+q['sairauspaivaraha'],p)
            if (p['lapsia_kotihoidontuella']>0):
                alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
                q['pvhoito']=max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
            q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['elatustuki'],p)
            q['lapsilisa']=self.laske_lapsilisa(p['lapsia'])
        else:
            q['pvhoito']=0
            q['pvhoito_ilman_etuuksia']=0
            q['lapsilisa']=0
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],q['puoliso_ansiopvraha_netto']=(0,0,0,0,0,0)
        if p['elakkeella']>0:
            q['kokoelake_netto']=q['kokoelake']-(q['verot']-q['verot_ilman_etuuksia'])
        elif p['aitiysvapaalla']>0:
            q['aitiyspaivaraha_netto']=q['aitiyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
        elif p['isyysvapaalla']>0:
            q['isyyspaivaraha_netto']=q['isyyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
        elif p['kotihoidontuella']>0:
            q['kotihoidontuki_netto']=q['kotihoidontuki']-(q['verot']-q['verot_ilman_etuuksia']) 
        elif p['sairauspaivarahalla']>0:
            q['sairauspaivaraha_netto']=q['sairauspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
        else:
            q['puoliso_ansiopvraha_netto']=q['puoliso_ansiopvraha']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
            q['ansiopvraha_netto']=q['ansiopvraha']-(q['verot']-q['verot_ilman_etuuksia'])
    
        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia

        if q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']>0:
            suhde=max(0,q['ansiopvraha_netto']/(q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']))
            q['ansiopvraha_nettonetto']=q['ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
            q['puoliso_ansiopvraha_nettonetto']=q['puoliso_ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
        else:
            q['ansiopvraha_nettonetto']=0
            q['puoliso_ansiopvraha_nettonetto']=0

        if p['opiskelija']>0:
            q['toimtuki']=0
        else:
            q['toimtuki']=self.toimeentulotuki(p['t'],q['verot_ilman_etuuksia'],p['puoliso_tulot'],q['puoliso_verot_ilman_etuuksia'],\
                q['elatustuki']+q['opintotuki']+q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha']+q['lapsilisa']\
                +q['kokoelake_netto']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki'],\
                0,p['asumismenot_toimeentulo'],q['pvhoito'],p)

        #print(q['ansiopvraha']+q['perustulo'],q['ansiopvraha_netto'],-(q['pvhoito']-q['pvhoito_ilman_etuuksia']),-(q['verot']-q['verot_ilman_etuuksia']))
                
        kateen=q['opintotuki']+q['kokoelake']+p['puoliso_tulot']+p['t']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimtuki']\
            +q['ansiopvraha']+q['puoliso_ansiopvraha']+q['elatustuki']-q['puoliso_verot']-q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']
        q['kateen']=kateen
        q['perhetulot_netto']=p['puoliso_tulot']+p['t']-q['verot_ilman_etuuksia']-q['puoliso_verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['omattulot_netto']=p['t']-q['verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['etuustulo_netto']=q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['opintotuki']\
            +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimtuki']-(q['pvhoito_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'])
        q['etuustulo_brutto']=q['ansiopvraha']+q['puoliso_ansiopvraha']+q['opintotuki']\
            +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimtuki']+q['kokoelake']
        
        q['palkkatulot']=p['t']
        q['puoliso_palkkatulot']=p['puoliso_tulot']
        q['puoliso_tulot_netto']=p['puoliso_tulot']-q['puoliso_verot_ilman_etuuksia']
        q['perustulo']=0
        q['puoliso_perustulo']=0
        q['perustulo_netto']=0
        q['puoliso_perustulo_netto']=0
        q['perustulo_nettonetto']=0
        q['puoliso_perustulo_nettonetto']=0

        return kateen,q
        
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
        suojaosa=300*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
        
        #print('palkka {:.1f} muuttulot {:.1f} perusomavastuu {:.1f} vuokra {:.1f} max_meno {:.1f} tuki {:.1f}'.format(palkkatulot,muuttulot,perusomavastuu,vuokra,max_meno,tuki))
    
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
        suojaosa=300*p['aikuisia']
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

        prosentti=0.8 # vastaa 80 %
        suojaosa=300*p['aikuisia']
        perusomavastuu=max(0,0.42*(max(0,palkkatulot-suojaosa)+muuttulot-(603+100*p['aikuisia']+223*p['lapsia'])))
        if perusomavastuu<10:
            perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
    
        return tuki
        

    def elakkeensaajan_asumistuki(self,palkkatulot,muuttulot,vuokra,p):
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
        # tarkasta
        max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=50.87 # e/kk, 2019
        if p['aikuisia']<2:
            tuloraja=8_676/12
        else:
            tuloraja=12_717/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.4*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
    
        return tuki

    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot2018(self,hoidossa,tulot,p,prosentti1=None,prosentti2=None,prosentti3=None,maksimimaksu=None):
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
        
    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot2019(self,hoidossa,tulot,p,prosentti1=None,prosentti2=None,prosentti3=None,maksimimaksu=None):
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
        
    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot2020(self,hoidossa,tulot,p,prosentti1=None,prosentti2=None,prosentti3=None,maksimimaksu=None):
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
    
    def laske_kansanelake2018(self,ika,tyoelake,yksin,disability=False):
        if yksin>0:
            maara=628.85
        else:
            maara=557.79
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
        else:
            if ika>=65:
                maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
            elif ika>=62: # varhennus
                maara = max(0,0.048*(65-ika)-np.maximum(0,(tyoelake-55.54))/2)
            else:
                maara=0
            
        return maara
            
    def laske_kansanelake2019(self,ika,tyoelake,yksin,disability=False):
        if yksin>0:
            maara=628.85
        else:
            maara=557.79
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
        else:
            if ika>=65:
                maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
            elif ika>=62: # varhennus
            
                maara = max(0,0.048*(65-ika)-np.maximum(0,(tyoelake-55.54))/2)
            else:
                maara=0
            
        return maara
        
    def laske_kansanelake2020(self,ika,tyoelake,yksin,disability=False):
        if yksin>0:
            maara=662.86
        else:
            maara=591.79
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
        else:
            if ika>=65:
                maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
            elif ika>=62: # varhennus
                maara = max(0,0.048*(65-ika)-np.maximum(0,(tyoelake-55.54))/2)
            else:
                maara=0
            
        return maara
        
    def laske_takuuelake2018(self,ika,muuelake,disability=False):
        if ika<65 and not disability:
            return 0
        
        if muuelake<777.84:
            elake=784.52-muuelake
        else:
            elake=0
        
        return elake
    
    def laske_takuuelake2019(self,ika,muuelake,disability=False):
        if ika<65 and not disability:
            return 0
        
        if muuelake<777.84:
            elake=784.52-muuelake
        else:
            elake=0
        
        return elake
    
    def laske_takuuelake2020(self,ika,muuelake,disability=False):
        if ika<65 and not disability:
            return 0
        
        if muuelake<834.52:
            elake=834.52-muuelake
        else:
            elake=0
        
        return elake
        
    def laske_puhdas_tyoelake(self,ika,elake,disability=False):
        if self.irr_vain_tyoelake:
            return elake 
        else:
            kansanelake=self.laske_kansanelake(ika,elake,1,disability=disability)
            self.elakeindeksi=(0*1+1.0*1.0/1.016)**0.25
            indeksi=self.elakeindeksi**max(0,ika-40) # 2020-1980=40
            if ika>=65 or disability:
                return max(0,elake-(self.laske_takuuelake(ika,0,disability=disability)-kansanelake)*indeksi)
            else:
                return max(0,elake-self.laske_kansanelake(ika,0,1)*indeksi)
    
    def laske_kokonaiselake(self,ika,muuelake,yksin=1,include_takuuelake=True,include_kansanelake=False,disability=False):
        if include_kansanelake:
            kansanelake=self.laske_kansanelake(ika,muuelake,yksin,disability=disability)
            muuelake=muuelake+kansanelake
            
        if include_takuuelake:
            takuuelake=self.laske_takuuelake(ika,muuelake,disability=disability)
            kokoelake=takuuelake+muuelake
        else:
            kokoelake=muuelake
    
        return kokoelake
        
    def isyysraha_perus(self,vakiintunutpalkka):
        if self.year==2018:
            minimi=27.86*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2019:
            minimi=27.86*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12  
        else:
            minimi=27.86*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12  
                        
        raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def aitiysraha2019(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=0
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12 
                
            raha=max(minimi,0.9*min(taite1,vakiintunutpalkka)+0.325*max(vakiintunutpalkka-taite1,0))
        else: 
            minimi=27.86*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12 
                        
            raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def aitiysraha2020(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=0
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12 
                
            raha=max(minimi,0.9*min(taite1,vakiintunutpalkka)+0.325*max(vakiintunutpalkka-taite1,0))
        else: 
            minimi=28.94*25
            sotumaksu=0.0448
            taite1=37_861/12  
            taite2=58_252/12 
                        
            raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def sairauspaivaraha2018(self,vakiintunutpalkka):
        minimi=24.64*25
        sotumaksu=0.0448
        taite1=30_394/12
        taite2=58_252/12
        vakiintunut=(1-sotumaksu)*vakiintunutpalkka                    

        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))

        return raha
        
    def sairauspaivaraha2019(self,vakiintunutpalkka):
        minimi=27.86*25
        sotumaksu=0.05
        taite1=30_394/12
        taite2=57_183/12
        vakiintunut=(1-sotumaksu)*vakiintunutpalkka                    

        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))

        return raha

    def sairauspaivaraha2020(self,vakiintunutpalkka):
        minimi=28.94*25
        sotumaksu=0.0958
        taite1=31_595/12  
        vakiintunut=(1-sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return raha
        
    def laske_marginaalit(self,q1,q2,dt,laske_tyollistymisveroaste=0):
    
        if dt<1:
            dt=1

        # lasketaan marginaalit
        marg={}        
        marg['asumistuki']=(-q2['asumistuki']+q1['asumistuki'])*100/dt
        marg['ansiopvraha']=(+q1['ansiopvraha_netto']-q2['ansiopvraha_netto']+q1['puoliso_ansiopvraha_netto']-q2['puoliso_ansiopvraha_netto'])*100/dt 
        marg['pvhoito']=(-q1['pvhoito']+q2['pvhoito'])*100/dt
        marg['toimtuki']=(+q1['toimtuki']-q2['toimtuki'])*100/dt
        marg['palkkaverot']=(-q1['verot_ilman_etuuksia']+q2['verot_ilman_etuuksia']-q1['puoliso_verot_ilman_etuuksia']+q2['puoliso_verot_ilman_etuuksia'])*100/dt
        marg['valtionvero']=(-q1['valtionvero']+q2['valtionvero'])*100/dt
        marg['elake']=(q1['kokoelake_netto']-q2['kokoelake_netto'])*100/dt
        marg['kunnallisvero']=(-q1['kunnallisvero']+q2['kunnallisvero'])*100/dt
        marg['ansiotulovah']=(+q1['ansiotulovahennys']-q2['ansiotulovahennys'])*100/dt
        marg['tyotulovahennys']=(+q1['tyotulovahennys']-q2['tyotulovahennys'])*100/dt
        marg['perusvahennys']=(+q1['perusvahennys']-q2['perusvahennys'])*100/dt
        marg['tyotulovahennys_kunnallisveroon']=(+q1['tyotulovahennys_kunnallisveroon']-q2['tyotulovahennys_kunnallisveroon'])*100/dt
        marg['ptel']=(-q1['ptel']+q2['ptel']-q1['puoliso_ptel']+q2['puoliso_ptel'])*100/dt
        marg['sairausvakuutus']=(-q1['sairausvakuutus']+q2['sairausvakuutus']-q1['puoliso_sairausvakuutus']+q2['puoliso_sairausvakuutus'])*100/dt
        marg['tyotvakmaksu']=(-q1['tyotvakmaksu']+q2['tyotvakmaksu']-q1['puoliso_tyotvakmaksu']+q2['puoliso_tyotvakmaksu'])*100/dt
        marg['puoliso_verot']=(-q1['puoliso_verot']+q2['puoliso_verot'])*100/dt
        marg['perustulo']=(-q2['perustulo_netto']+q1['perustulo_netto']-q2['puoliso_perustulo_netto']+q1['puoliso_perustulo_netto'])*100/dt
    
        marg['sivukulut']=marg['tyotvakmaksu']+marg['sairausvakuutus']+marg['ptel'] # sisältyvät jo veroihin
        marg['etuudet']=marg['ansiopvraha']+marg['asumistuki']+marg['toimtuki']
        marg['verot']=marg['palkkaverot'] # sisältää sivukulut
        marg['ansioverot']=marg['palkkaverot']+marg['elake'] # sisältää sivukulut
        marg['marginaali']=marg['pvhoito']+marg['etuudet']+marg['verot']+marg['elake']
    
        # ja käteen jää
        tulot={}
        tulot['kateen1']=q1['kateen']
        tulot['kateen2']=q2['kateen']
    
        omattulotnetto1=q1['omattulot_netto'] # ilman etuuksia
        omattulotnetto2=q2['omattulot_netto'] # ilman etuuksia
        puolisontulotnetto1=q1['puoliso_tulot_netto'] # ilman etuuksia
        puolisontulotnetto2=q2['puoliso_tulot_netto'] # ilman etuuksia
        if laske_tyollistymisveroaste>0:
            tulot['tulotnetto']=omattulotnetto2+puolisontulotnetto2
            tulot['puolisotulotnetto']=puolisontulotnetto2
            tulot['omattulotnetto']=omattulotnetto2
        else:
            tulot['tulotnetto']=omattulotnetto1+puolisontulotnetto1
            tulot['puolisotulotnetto']=puolisontulotnetto1
            tulot['omattulotnetto']=omattulotnetto1
            
        marg['marginaaliveroprosentti']=100-(tulot['kateen2']-tulot['kateen1'])*100/dt 
    
        return tulot,marg
    
    def laske_ja_plottaa(self,p=None,min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,
            figname=None):
            
        netto,eff,tva,osa_tva=self.comp_insentives(p=p,p2=None,min_salary=min_salary,
                                                max_salary=max_salary,step_salary=step_salary,dt=dt)
                
        if plottaa:
            self.plot_insentives(netto,eff,tva,osa_tva,min_salary=min_salary,max_salary=max_salary+1,
                step_salary=step_salary,
                basenetto=basenetto,baseeff=baseeff,basetva=basetva,baseosatva=baseosatva,
                dt=dt,otsikko=otsikko,otsikkobase=otsikkobase,selite=selite,
                plot_tva=plot_tva,plot_eff=plot_eff,plot_netto=plot_netto,plot_osaeff=plot_osaeff,
                figname=figname)
        
        return netto,eff,tva,osa_tva
        
    def plot_insentives(self,netto,eff,tva,osa_tva,
            min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=False,
            figname=None):
            
        x=np.arange(min_salary,max_salary,step_salary)
        if plot_netto:
            fig, axs = plt.subplots()
            if basenetto is not None:
                axs.plot(x,basenetto,label=otsikkobase)
                axs.plot(x,netto,label=otsikko)
                if selite:
                    axs.legend(loc='upper right')
            else:
                axs.plot(x,netto)        
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel('Käteen (e/kk)')
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            if figname is not None:
                plt.savefig(figname+'_netto.eps', format='eps')
            plt.show()

        if plot_eff:
            fig, axs = plt.subplots()
            if baseeff is not None:
                axs.plot(x,baseeff,label=otsikkobase)
                axs.plot(x,eff,label=otsikko)
                if selite:
                    axs.legend(loc='upper right')
            else:
                axs.plot(x,eff)        
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel(self.labels['effective'])
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            if figname is not None:
                plt.savefig(figname+'_effmarg.eps', format='eps')
            plt.show()

        if plot_tva:
            fig, axs = plt.subplots()
            if basenetto is not None:
                axs.plot(x,basetva,label=otsikkobase)
                axs.plot(x,tva,label=otsikko)
                if selite:
                    axs.legend(loc='upper right')
            else:
                axs.plot(x,tva)
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel('Työllistymisveroaste (%)')
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 120)
            if figname is not None:
                plt.savefig(figname+'_tva.eps', format='eps')
            plt.show()

        if plot_osaeff:
            fig, axs = plt.subplots()
            if baseosatva is not None:
                axs.plot(x,baseosatva,label=otsikkobase)
                axs.plot(x,osa_tva,label=otsikko)
                if selite:
                    axs.legend(loc='upper right')
            else:
                axs.plot(x,osa_tva) 
                       
            axs.set_xlabel('Osatyön palkka (e/kk)')
            axs.set_ylabel('Osatyöstä kokotyöhön siirtymisen eff.marg.vero (%)')
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            if figname is not None:
                plt.savefig(figname+'_osatva.eps', format='eps')
            plt.show()    
        
    def comp_insentives(self,p=None,p2=None,min_salary=0,max_salary=6000,step_salary=1,dt=100):
        n_salary=int((max_salary+step_salary-min_salary)/step_salary)
        netto=np.zeros(n_salary)
        palkka=np.zeros(n_salary)
        tva=np.zeros(n_salary)
        osa_tva=np.zeros(n_salary)
        eff=np.zeros(n_salary)
        
        if p is None:
            p=self.get_default_parameter()

        if p2 is None:
            p2=p.copy()
            p2['t']=0 # palkka
        p3=p.copy()
        n0,q0=self.laske_tulot(p2)
        k=0
        for t in np.arange(0,max_salary+step_salary,step_salary):
            p3['t']=t # palkka
            n1,q1=self.laske_tulot(p3)
            p3['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p3)
            p3['t']=2*t # palkka
            n3,q3=self.laske_tulot(p3)
            netto[k]=n1
            palkka[k]=t
            eff[k]=(1-(n2-n1)/dt)*100
            if t>0:
                tva[k]=(1-(n1-n0)/t)*100
                osa_tva[k]=(1-(n3-n1)/t)*100
            else:
                tva[k]=0
                osa_tva[k]=0
            k=k+1
            
        return netto,eff,tva,osa_tva
        
    def laske_ja_plottaa_marginaalit(self,p=None,min_salary=0,max_salary=6000,
                basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,
                otsikko="Vaihtoehto",otsikkobase="Perustapaus",selite=True,ret=False,
                plot_tva=True,plot_eff=True,plot_netto=True,figname=None,grayscale=False,
                incl_perustulo=False,incl_elake=True,fig=None,ax=None):
        netto=np.zeros(max_salary+1)
        palkka=np.zeros(max_salary+1)
        tva=np.zeros(max_salary+1)
        eff=np.zeros(max_salary+1)
        asumistuki=np.zeros(max_salary+1)
        toimeentulotuki=np.zeros(max_salary+1)
        ansiopvraha=np.zeros(max_salary+1)
        nettotulot=np.zeros(max_salary+1)
        lapsilisa=np.zeros(max_salary+1)
        elake=np.zeros(max_salary+1)    
        elatustuki=np.zeros(max_salary+1)
        perustulo=np.zeros(max_salary+1)
        margasumistuki=np.zeros(max_salary+1)
        margtoimeentulotuki=np.zeros(max_salary+1)
        margansiopvraha=np.zeros(max_salary+1)
        margverot=np.zeros(max_salary+1)    
        margelake=np.zeros(max_salary+1)    
        margpvhoito=np.zeros(max_salary+1)        
        margyht=np.zeros(max_salary+1)        
        margyht2=np.zeros(max_salary+1)    
        margperustulo=np.zeros(max_salary+1)    
        tva_asumistuki=np.zeros(max_salary+1)
        tva_toimeentulotuki=np.zeros(max_salary+1)
        tva_ansiopvraha=np.zeros(max_salary+1)
        tva_verot=np.zeros(max_salary+1)        
        tva_elake=np.zeros(max_salary+1)        
        tva_pvhoito=np.zeros(max_salary+1)        
        tva_perustulo=np.zeros(max_salary+1)        
        tva_yht=np.zeros(max_salary+1)        
        tva_yht2=np.zeros(max_salary+1)        
        
        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            reverse=True
        else:
            pal=sns.color_palette()
        
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
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            tulot2,tvat=self.laske_marginaalit(q0,q1,t,laske_tyollistymisveroaste=1)
            netto[t]=n1
            palkka[t]=t
            margasumistuki[t]=marg['asumistuki']
            margtoimeentulotuki[t]=marg['toimtuki']
            margverot[t]=marg['verot']
            margelake[t]=marg['elake']
            margansiopvraha[t]=marg['ansiopvraha']
            margpvhoito[t]=marg['pvhoito']
            margperustulo[t]=marg['perustulo']
            margyht[t]=marg['marginaali']
            margyht2[t]=marg['marginaaliveroprosentti']
            elake[t]=q1['kokoelake_netto']
            asumistuki[t]=q1['asumistuki']
            toimeentulotuki[t]=q1['toimtuki']
            ansiopvraha[t]=q1['ansiopvraha_nettonetto']+q1['puoliso_ansiopvraha_nettonetto']
            lapsilisa[t]=q1['lapsilisa']
            perustulo[t]=q1['perustulo_nettonetto']+q1['puoliso_perustulo_nettonetto']
            nettotulot[t]=tulot['tulotnetto']
            tva_asumistuki[t]=tvat['asumistuki']
            tva_toimeentulotuki[t]=tvat['toimtuki']
            tva_verot[t]=tvat['verot']
            tva_elake[t]=tvat['elake']
            tva_perustulo[t]=tvat['perustulo']
            tva_ansiopvraha[t]=tvat['ansiopvraha']
            tva_pvhoito[t]=tvat['pvhoito']
            tva_yht[t]=tvat['marginaali']
            tva_yht2[t]=tvat['marginaaliveroprosentti']

            eff[t]=(1-(n2-n1)/dt)*100
            if t>0:
                tva[t]=(1-(n1-n0)/t)*100
            else:
                tva[t]=0
                
        if plot_eff:
            sns.set()
            if fig is None:
                figi,axs = plt.subplots()
            else:
                figi=fig
                axs=ax
            if incl_perustulo:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margperustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],'Perustulo'),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito']),
                        colors=pal)
                        
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel(self.labels['effective'])
            axs.grid(True,color='lightgray')
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 120)
            if selite:
                #axs.legend(loc='upper right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
            if figname is not None:
                plt.savefig(figname+'_eff.png')
            plt.show()
        
        if plot_netto:
            if fig is None:
                figi,axs = plt.subplots()
            else:
                figi=fig
                axs=ax
            sns.set()
            if incl_perustulo:
                axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elake,perustulo,
                    labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elake'],'Perustulo'),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elake,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elake'],),
                        colors=pal)
                else:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä'),
                        colors=pal)
            
            #axs.plot(netto)
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel('Käteen (e/kk)')
            axs.grid(True,color='lightgray')
            axs.set_xlim(0, max_salary)
            if selite:        
                #axs.legend(loc='lower right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='lower right')
                
            if figname is not None:
                plt.savefig(figname+'_netto.png')
            plt.show()

        if plot_tva:
            if fig is None:
                figi,axs = plt.subplots()
            else:
                figi=fig
                axs=ax
            sns.set()
            if incl_perustulo:
                axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,tva_perustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],'Perustulo'),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito']),
                        colors=pal)

            axs.plot(tva,label='Vaihtoehto')
            #axs.plot(tva_yht,label='Vaihtoehto2')
            #axs.plot(tva_yht2,label='Vaihtoehto3')
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel('Työllistymisveroaste (%)')
            axs.grid(True,color='lightgray')
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 120)
            if selite:
                #axs.legend(loc='upper right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
                
            if figname is not None:
                plt.savefig(figname+'_tva.png')
            plt.show()
               
        if ret: 
            return netto,eff,tva   

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
            margpuolisonverot[t]=marg['puoliso_verot']
            tyotvakmaksu[t]=q1['tyotvakmaksu']
            sairausvakuutus[t]=q1['sairausvakuutus']
            ptel[t]=q1['ptel']
            kunnallisvero[t]=q1['kunnallisvero']
            valtionvero[t]=q1['valtionvero']
            puolisonverot[t]=0 #q1['puolisoverot']
                            
        fig,axs = plt.subplots()
        axs.stackplot(palkka,margvaltionvero,margkunnallisvero,margptel,margsairausvakuutus,margtyotvakmaksu,margpuolisonverot,
            #labels=('Valtionvero','Kunnallisvero','PTEL','sairausvakuutus','työttömyysvakuutusmaksu','puolison verot'))
            labels=('State tax','Municipal tax','Employee pension premium','sairausvakuutus','työttömyysvakuutusmaksu','puolison verot'))
        axs.plot(margverot,label='Yht')
        #axs.plot(margyht,label='Vaihtoehto2')
        #axs.plot(margyht2,label='Vaihtoehto3')
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel(self.labels['effective'])
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        axs.set_ylim(-50, 120)
        if selite:
            axs.legend(loc='upper left')
        plt.show()
        
        fig,axs = plt.subplots()
        axs.stackplot(palkka,tyotvakmaksu,sairausvakuutus,ptel,kunnallisvero,valtionvero,puolisonverot,
            labels=('tyotvakmaksu','sairausvakuutus','ptel','kunnallisvero','valtionvero','puolisonverot'))
        #axs.plot(netto)
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel('Verot yhteensä (e/kk)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        if selite:        
            axs.legend(loc='lower right')
        plt.show()

    def laske_ja_plottaa_hila(self,min_salary=0,max_salary=6000,type='eff',dt=100):
        fig,axs = plt.subplots(10,3)
        for k in range(1,31):
            ax=plt.subplot(10,3,k)
            p,_=perheparametrit(k)
            self.lp_marginaalit_apu(ax,otsikko='Tapaus '+str(k),p=p,min_salary=min_salary,max_salary=max_salary,type=type,dt=dt)

        plt.show()

    def lp_marginaalit_apu(self,axs,otsikko='',p=None,min_salary=0,max_salary=6000,type='eff',dt=100,selite=False,include_perustulo=False):
        netto=np.zeros(max_salary+1)
        palkka=np.zeros(max_salary+1)
        tva=np.zeros(max_salary+1)
        eff=np.zeros(max_salary+1)
        elake=np.zeros(max_salary+1)
        asumistuki=np.zeros(max_salary+1)
        toimeentulotuki=np.zeros(max_salary+1)
        kokoelake=np.zeros(max_salary+1)
        ansiopvraha=np.zeros(max_salary+1)
        nettotulot=np.zeros(max_salary+1)
        lapsilisa=np.zeros(max_salary+1)
        perustulo=np.zeros(max_salary+1)
        elatustuki=np.zeros(max_salary+1)
        margasumistuki=np.zeros(max_salary+1)
        margtoimeentulotuki=np.zeros(max_salary+1)
        margansiopvraha=np.zeros(max_salary+1)
        margperustulo=np.zeros(max_salary+1)    
        margverot=np.zeros(max_salary+1)   
        margelake=np.zeros(max_salary+1)   
        margpvhoito=np.zeros(max_salary+1)        
        margyht=np.zeros(max_salary+1)        
        margyht2=np.zeros(max_salary+1)        
        tva_asumistuki=np.zeros(max_salary+1)
        tva_elake=np.zeros(max_salary+1)
        tva_toimeentulotuki=np.zeros(max_salary+1)
        tva_ansiopvraha=np.zeros(max_salary+1)
        tva_verot=np.zeros(max_salary+1)        
        tva_pvhoito=np.zeros(max_salary+1)        
        tva_yht=np.zeros(max_salary+1)        
        tva_yht2=np.zeros(max_salary+1)        
        tva_perustulo=np.zeros(max_salary+1)        

        if p is None:
            p=self.get_default_parameter()
            
        p2=p.copy()

        p2['t']=0 # palkka
        n0,q0=self.laske_tulot(p2) #,elake=0)
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1,q1=self.laske_tulot(p2) #,,elake=0)
            p2['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p2) #,,elake=0)
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            netto[t]=n1
            palkka[t]=t
            margasumistuki[t]=marg['asumistuki']
            margtoimeentulotuki[t]=marg['toimtuki']
            margverot[t]=marg['verot']
            margansiopvraha[t]=marg['ansiopvraha']
            margpvhoito[t]=marg['pvhoito']
            margelake[t]=marg['pvhoito']
            margyht[t]=marg['marginaali']
            margyht2[t]=marg['marginaaliveroprosentti']
            margperustulo[t]=marg['perustulo']
            perustulo[t]=q1['perustulo_nettonetto']+q1['puoliso_perustulo_nettonetto']
            asumistuki[t]=q1['asumistuki']
            elake[t]=q1['kokoelake_netto']
            toimeentulotuki[t]=q1['toimtuki']
            ansiopvraha[t]=q1['ansiopvraha_nettonetto']+q1['puoliso_ansiopvraha_nettonetto']
            lapsilisa[t]=q1['lapsilisa']
            nettotulot[t]=tulot['tulotnetto']
            if type=='tva':
                tulot2,tvat=self.laske_marginaalit(q0,q1,t,laske_tyollistymisveroaste=1)
                tva_asumistuki[t]=tvat['asumistuki']
                tva_perustulo[t]=tvat['perustulo']
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
                
        if type=='eff':
            #fig,axs = plt.subplots()
            if include_perustulo:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margperustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],'Perustulo'))
            else:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake']))
            self.labels['valtionvero']='Valtionvero'
            self.labels['kunnallisvero']='Kunnallisvero'
            self.labels['telp']='TEL-P'
            self.labels['sairausvakuutus']='sairausvakuutus'
            self.labels['työttömyysvakuutusmaksu']='työttömyysvakuutusmaksu'
            self.labels['puolison verot']='puolison verot'
            self.labels['taxes']='verot'
            self.labels['asumistuki']='asumistuki'
            self.labels['toimeentulotuki']='toimeentulotuki'
            self.labels['tyottomyysturva']='työttömyystuki'
            self.labels['paivahoito']='päivähoito'
            self.labels['elake']='eläke'
            
            axs.plot(eff)
            #axs.plot(margyht,label='Vaihtoehto2')
            #axs.plot(margyht2,label='Vaihtoehto3')
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel(self.labels['effective'])
            axs.grid(True)
            axs.title.set_text(otsikko)
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 120)
            if selite:
                axs.legend(loc='upper right')
            #plt.show()
        elif type=='tva':
            #fig,axs = plt.subplots()
            if include_perustulo:
                axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_perustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],'Työttömyysturva',self.labels['paivahoito'],'Perustulo'))
            else:
                axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],'Työttömyysturva',self.labels['paivahoito']))
            
            axs.title.set_text(otsikko)
            if self.language=='Finnish':
                axs.plot(tva,label='Vaihtoehto')
                #axs.plot(tva_yht,label='Vaihtoehto2')
                #axs.plot(tva_yht2,label='Vaihtoehto3')
                axs.set_xlabel(self.labels['wage'])
                axs.set_ylabel('Työllistymisveroaste (%)')
            else:
                axs.plot(tva,label='Vaihtoehto')
                #axs.plot(tva_yht,label='Vaihtoehto2')
                #axs.plot(tva_yht2,label='Vaihtoehto3')
                axs.set_xlabel('Wage (e/m)')
                axs.set_ylabel('Työllistymisveroaste (%)')
            
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 120)
            if selite:
                axs.legend(loc='upper right')
        else:
            if include_perustulo:
                axs.stackplot(palkka,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,elake,perustulo,
                    labels=(self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Palkka','Lapsilisä',self.labels['elake'],'Perustulo'))
            else:
                axs.stackplot(palkka,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,elake,
                    labels=(self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Palkka','Lapsilisä',self.labels['elake']))
                            
            axs.plot(netto)
            axs.title.set_text(otsikko)
            if self.language=='Finnish':
                axs.set_xlabel(self.labels['wage'])
                axs.set_ylabel('Käteen (e/kk)')
            else:
                axs.set_xlabel('Wage (e/m)')
                axs.set_ylabel('Net income (e/m)')
            
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            if selite:
                axs.legend(loc='lower right')
                
        #return netto,eff,tva        
        
    # valitaan oikeat funktiot vuoden mukaan
    def set_year(self,vuosi):
        '''
        korvataan etuusfunktiot oikeiden vuosien etuusfunktioilla
        '''
        if vuosi==2019:
            self.laske_kansanelake=self.laske_kansanelake2019
            self.laske_takuuelake=self.laske_takuuelake2019
            self.aitiysraha=self.aitiysraha2019
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2019
            self.veroparam=self.veroparam2019          
            self.valtionvero_asteikko=self.valtionvero_asteikko_2019
            self.laske_ylevero=self.laske_ylevero2019
            self.elaketulovahennys=self.elaketulovahennys2019
            self.tyotulovahennys=self.tyotulovahennys2019
            self.ansiotulovahennys=self.ansiotulovahennys2019
            self.perusvahennys=self.perusvahennys2019
            self.lapsilisa=self.lapsilisa2019
            self.asumistuki=self.asumistuki2019
            self.kotihoidontuki=self.kotihoidontuki2019
            self.paivahoitomenot=self.paivahoitomenot2019
            self.sairauspaivaraha=self.sairauspaivaraha2019
            self.toimeentulotuki_param=self.toimeentulotuki_param2019
        elif vuosi==2020:
            self.laske_kansanelake=self.laske_kansanelake2020
            self.laske_takuuelake=self.laske_takuuelake2020
            self.aitiysraha=self.aitiysraha2020
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2020
            self.valtionvero_asteikko=self.valtionvero_asteikko_2020
            self.laske_ylevero=self.laske_ylevero2020
            self.elaketulovahennys=self.elaketulovahennys2020
            self.tyotulovahennys=self.tyotulovahennys2020
            self.perusvahennys=self.perusvahennys2020
            self.ansiotulovahennys=self.ansiotulovahennys2020
            self.veroparam=self.veroparam2020
            self.lapsilisa=self.lapsilisa2020
            self.asumistuki=self.asumistuki2020
            self.kotihoidontuki=self.kotihoidontuki2020
            self.paivahoitomenot=self.paivahoitomenot2020
            self.sairauspaivaraha=self.sairauspaivaraha2020
            self.toimeentulotuki_param=self.toimeentulotuki_param2020
        elif vuosi==2021:
            self.laske_kansanelake=self.laske_kansanelake2021
            self.laske_takuuelake=self.laske_takuuelake2021
            self.aitiysraha=self.aitiysraha2021
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2021
            self.valtionvero_asteikko=self.valtionvero_asteikko_2021
            self.laske_ylevero=self.laske_ylevero2021
            self.elaketulovahennys=self.elaketulovahennys2021
            self.tyotulovahennys=self.tyotulovahennys2021
            self.perusvahennys=self.perusvahennys2021
            self.ansiotulovahennys=self.ansiotulovahennys2021
            self.veroparam=self.veroparam2021
            self.lapsilisa=self.lapsilisa2021
            self.asumistuki=self.asumistuki2021
            self.kotihoidontuki=self.kotihoidontuki2021
            self.paivahoitomenot=self.paivahoitomenot2021
            self.sairauspaivaraha=self.sairauspaivaraha2021
            self.toimeentulotuki_param=self.toimeentulotuki_param2021
        elif vuosi==2018:
            self.laske_kansanelake=self.laske_kansanelake2018
            self.laske_takuuelake=self.laske_takuuelake2018
            self.aitiysraha=self.aitiysraha2019
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2018
            self.veroparam=self.veroparam2018            
            self.elaketulovahennys=self.elaketulovahennys2018
            self.tyotulovahennys=self.tyotulovahennys2018
            self.perusvahennys=self.perusvahennys2018
            self.ansiotulovahennys=self.ansiotulovahennys2018
            self.valtionvero_asteikko=self.valtionvero_asteikko_2018
            self.laske_ylevero=self.laske_ylevero2018
            self.lapsilisa=self.lapsilisa2018
            self.asumistuki=self.asumistuki2018
            self.kotihoidontuki=self.kotihoidontuki2018
            self.paivahoitomenot=self.paivahoitomenot2018
            self.sairauspaivaraha=self.sairauspaivaraha2018
            self.toimeentulotuki_param=self.toimeentulotuki_param2018            
        else:
            print('Vuoden {v} aineisto puuttuu'.format(v=vuosi))
    
