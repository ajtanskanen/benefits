"""

    benefits
    
    implements social security and social insurance benefits in the Finnish social security schemes


"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite
from .labels import Labels
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager

class Benefits():
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
            elif key=='additional_vat':
                if value is not None:
                    self.additional_vat=value
            elif key=='vaihtuva_tyelmaksu':
                if value is not None:
                    self.vaihtuva_tyelmaksu=value
            elif key=='tyel_perusvuosi':
                if value is not None:
                    self.tyel_perusvuosi=value                    
            elif key=='extra_ppr':
                if value is not None:
                    self.use_extra_ppr=True
                    self.extra_ppr_factor+=value
    
        # choose the correct set of benefit functions for computations
        self.set_year(self.year)
        self.lab=Labels()
        self.labels=self.lab.ben_labels(self.language)
        
        if self.vaihtuva_tyelmaksu:
            self.get_tyelpremium()
        
    def explain(self,p=None):
        #self.tee_selite()
        if p is None:
            print('Ei parametrejä')
        else:
            selite=tee_selite(p)
            print(selite)
            
    def laske_vaihtuva_tyoelakemaksu(self,ika):
        vuosi=int(self.floor(self.tyel_perusvuosi+ika)) # alkuvuonna 18
        
        # prosenttia palkoista, vuodesta 2017 alkaen, jatkettu päätepisteen tasolla vuoden 2085 jälkeen
        self.tyontekijan_maksu=self.data_ptel[vuosi]
        if vuosi<2017:
            self.tyontekijan_maksu_52=self.tyontekijan_maksu*19/15
        else:
            self.tyontekijan_maksu_52=self.tyontekijan_maksu+0.015
            
        self.koko_tyel_maksu=self.data_tyel_kokomaksu[vuosi]
        self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu
    
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
        
    def toimeentulotuki_param2022(self):
        min_etuoikeutettuosa=150
        lapsi1=324.34     # e/kk     alle 10v lapsi
        lapsi2=298.60     # e/kk
        lapsi3=272.85     # e/kk
        yksinhuoltaja=586.89     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=437.60
        yksinasuva=514.82
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
        
        if False: # lain mukainen tiukka tulkinta
            omaetuoikeutettuosa=min(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
            puolison_etuoikeutettuosa=min(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
        else: # Kelan tulkinta: aina 150e
            omaetuoikeutettuosa=min_etuoikeutettuosa
            puolison_etuoikeutettuosa=min_etuoikeutettuosa
            
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
            
        if self.use_extra_ppr:
            tuki1=tuki1*self.extra_ppr_factor
        
        tuki=max(0,tuki1+menot-max(0,omabruttopalkka-omaetuoikeutettuosa-omapalkkavero)\
                -max(0,puolison_bruttopalkka-puolison_etuoikeutettuosa-puolison_palkkavero)-verot-muuttulot)

        if p['toimeentulotuki_vahennys']>0: # vähennetään 20%
            tuki=tuki*0.8
                
        if tuki<10:
            tuki=0    
            
        return tuki
        
    def perheparametrit(self,perhetyyppi=10,tulosta=False):
        return perheparametrit(perhetyyppi=perhetyyppi,tulosta=tulosta)
        
    def print_examples(self):
        return print_examples()
        
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
        
        if self.use_extra_ppr:
            pvraha=21.5*(32.40+lisa)*self.extra_ppr_factor
        else:
            pvraha=21.5*(32.40+lisa) #*self.extra_ppr_factor
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
        
        if self.use_extra_ppr:
            pvraha=21.5*(32.40+lisa)*self.extra_ppr_factor
        else:
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
        
        if self.use_extra_ppr:
            pvraha=21.5*(33.66+lisa)*self.extra_ppr_factor
        else:
            pvraha=21.5*(33.66+lisa)
        tuki=max(0,pvraha)    
    
        return tuki

    # tmtuki samankokoinen
    def peruspaivaraha2021(self,lapsia):
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.30     # e/pv
        elif lapsia==2:
            lisa=7.78     # e/pv
        else:
            lisa=10.03     # e/pv 
        
        if self.use_extra_ppr:
            pvraha=21.5*(33.78+lisa)*self.extra_ppr_factor
        else:
            pvraha=21.5*(33.78+lisa)
        tuki=max(0,pvraha)    
    
        return tuki

    def peruspaivaraha2022(self,lapsia):
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.41     # e/pv
        elif lapsia==2:
            lisa=7.95     # e/pv
        else:
            lisa=10.25     # e/pv 
        
        if self.use_extra_ppr:
            pvraha=21.5*(34.50+lisa)*self.extra_ppr_factor
        else:
            pvraha=21.5*(34.50+lisa)
        tuki=max(0,pvraha)    
    
        return tuki
                
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
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                taite=3078.60   
                            
            if saa_ansiopaivarahaa>0: # & (kesto<400.0): # ei keston tarkastusta!
                #print(f'tyoton {tyoton} vakiintunutpalkka {vakiintunutpalkka} lapsia {lapsia} tyotaikaisettulot {tyotaikaisettulot} saa_ansiopaivarahaa {saa_ansiopaivarahaa} kesto {kesto} ansiokerroin {ansiokerroin} omavastuukerroin {omavastuukerroin}')
            
                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-self.sotumaksu)     
                #print(f'vakpalkka {vakpalkka}')
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
                soviteltuperus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,soviteltuperus)  

                tuki=ansiopaivarahamaara    
                tuki=omavastuukerroin*max(soviteltuperus,tuki)     # voi tulla vastaan pienillä tasoilla4
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

    def elaketulovahennys2022(self,elaketulot,tulot):
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
        
    def veroparam2018(self):
        self.kunnallisvero_pros=max(0,max(0,0.1984+self.additional_kunnallisvero)) # Viitamäen raportista 19,84; verotuloilla painotettu k.a. 19,86
        self.tyottomyysvakuutusmaksu=0.0190 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,max(0,0.0635+self.additional_tyel_premium)) # PTEL
            self.tyontekijan_maksu_52=max(0,max(0,0.0785+self.additional_tyel_premium)) # PTEL
            self.koko_tyel_maksu=max(0,max(0,0.2440+self.additional_tyel_premium))
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0086
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0142 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0070 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0
        self.sairaanhoitomaksu_etuus=0.0147 # muut
        
        self.paivarahamaksu_pros=0.0153 # palkka
        self.paivarahamaksu_raja=14020/self.kk_jakaja    
        
        self.elakemaksu_alaraja=58.27
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2019(self):
        self.kunnallisvero_pros=max(0,0.1988+self.additional_kunnallisvero) # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0125 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0077
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0142 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0070 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0
        self.sairaanhoitomaksu_etuus=0.0161 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=14282/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2020(self):
        self.kunnallisvero_pros=max(0,0.1997+self.additional_kunnallisvero) # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0125 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0134
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0142 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0070 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0068
        self.sairaanhoitomaksu_etuus=0.0161 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=14574/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2021(self):
        self.kunnallisvero_pros=max(0,0.2002+self.additional_kunnallisvero) # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0140 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0153
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0142 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0070 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0066
        self.sairaanhoitomaksu_etuus=0.0165 # muut
        
        self.paivarahamaksu_pros=0.0136 # palkka
        self.paivarahamaksu_raja=14766/self.kk_jakaja    
        
        self.elakemaksu_alaraja=61.37
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2022(self):
        self.kunnallisvero_pros=max(0,0.2002+self.additional_kunnallisvero) # Viitamäen raportista
        self.tyottomyysvakuutusmaksu=0.0140 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0153
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0142 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0070 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0053
        self.sairaanhoitomaksu_etuus=0.0150 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=15128/self.kk_jakaja    
        
        self.elakemaksu_alaraja=61.37
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
        
#         if np.abs(d2-d1)>1e-6:
#             print('verotus',d2-d1)

        return netto,peritytverot,valtionvero,kunnallisvero,kunnallisveronperuste,\
               valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
               tyotulovahennys_kunnallisveroon,ptel,sairausvakuutusmaksu,tyotvakmaksu,koko_tyoelakemaksu,ylevero

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
    
    def kotihoidontuki2021(self,lapsia,allekolmev,alle_kouluikaisia):
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=343.95 # e/kk
            seuraavat_alle_3v=102.67 # e/kk
            yli_3v=65.97 #e_kk
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
    
    def kotihoidontuki2022(self,lapsia,allekolmev,alle_kouluikaisia):
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=350.27 # e/kk
            seuraavat_alle_3v=104.86 # e/kk
            yli_3v=67.38 #e_kk
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
            lapsilisat += 53.3
            
        return lapsilisat
    
    def lapsilisa2021(self,yksinhuoltajakorotus=False):
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 63.3
            
        return lapsilisat
    
    def lapsilisa2022(self,yksinhuoltajakorotus=False):
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 63.3
            
        return lapsilisat
    
    def laske_lapsilisa(self,lapsia,yksinhuoltajakorotus=0):
        lapsilisat=self.lapsilisa(yksinhuoltajakorotus=yksinhuoltajakorotus)

        if lapsia==0:
            tuki=0
        elif lapsia==1:
            tuki=lapsilisat[0]
        elif lapsia==2:
            tuki=sum(lapsilisat[0:2])
        elif lapsia==3:
            tuki=sum(lapsilisat[0:3])
        elif lapsia==4:
            tuki=sum(lapsilisat[0:4])
        elif lapsia==5:
            tuki=sum(lapsilisat[0:5])
        elif lapsia>5:
            tuki=sum(lapsilisat[0:5])+(lapsia-5)*lapsilisat[4]
        else:
            print('error(1))')
        
        return tuki
        
    def opintoraha(self,palkka,p):
        '''
        18-vuotias itsellisesti asuva opiskelija
        '''
        if p['lapsia']>0:
            if self.year==2018:
                tuki=350.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2019:
                tuki=350.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2020:
                tuki=350.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2021:
                tuki=355.05# +650*0.4 = opintolainahyvitys mukana?
        else:
            if self.year==2018:
                tuki=250.28 #+650*0.4 # opintolainahyvitys mukana
            elif self.year==2019:
                tuki=250.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2020:
                tuki=250.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2021:
                tuki=253.69 # +650*0.4 = opintolainahyvitys mukana?
            
        if self.year==2018:
            raja=696
        elif self.year==2019:
            raja=667
        elif self.year==2020:
            raja=667
        elif self.year==2021:
            raja=696

        if palkka>raja: #+222/12: # oletetaan että täysiaikainen opiskelija
            tuki=0
            
        return tuki
        
    def check_p(self,p):
        if 'toimeentulotuki_vahennys' not in p:
            p['toimeentulotuki_vahennys']=0
        if 'lapsikorotus_lapsia' not in p:
            p['lapsikorotus_lapsia']=p['lapsia']
        for alku in set(['omat_','puoliso_','']):
            if alku+'alive' not in p:
                p[alku+'alive']=1
            if alku+'elake_maksussa' not in p:
                p[alku+'elake_maksussa']=0
            if alku+'opiskelija' not in p:
                p[alku+'opiskelija']=0
            if alku+'elakkeella' not in p:
                p[alku+'elakkeella']=0
            if alku+'tyoelake' not in p:
                p[alku+'tyoelake']=0
            if alku+'kansanelake' not in p:
                p[alku+'kansanelake']=0
            if alku+'sairauspaivarahalla' not in p:
                p[alku+'sairauspaivarahalla']=0
            if alku+'disabled' not in p:
                p[alku+'disabled']=0
            if alku+'saa_elatustukea' not in p:
                p[alku+'saa_elatustukea']=0
        return p

    def laske_tulot(self,p,tt_alennus=0,include_takuuelake=True,legacy=True):
        q={} # tulokset tänne
        p=self.check_p(p)
        q['perustulo']=0
        q['puoliso_perustulo']=0
        q['puhdas_tyoelake']=0
        q['multiplier']=1
        q['kotihoidontuki']=0
        q['kotihoidontuki_netto']=0
        q['puoliso_opintotuki']=0
        q['puoliso_kotihoidontuki']=0
        q['puoliso_kotihoidontuki_netto']=0
        q['puoliso_ansiopvraha_netto']=0
        q['puoliso_kotihoidontuki_netto']=0
        q['puoliso_opintotuki_netto']=0
        if p['elakkeella']>0: # vanhuuseläkkeellä
            p['tyoton']=0
            q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
            q['elake_maksussa']=p['tyoelake']
            q['elake_tuleva']=0
            p['saa_ansiopaivarahaa']=0
            # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
            if (p['aikuisia']>1):
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,disability=p['disabled'])
                q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'],yksin=0)
            else:
                q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,disability=p['disabled'])
                q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'],yksin=1)

            q['ansiopvraha'],q['puhdasansiopvraha'],q['peruspvraha']=(0,0,0)
            #oletetaan että myös puoliso eläkkeellä
            q['puoliso_ansiopvraha']=0
            q['opintotuki']=0
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
                    q['puoliso_kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
                elif p['puoliso_tyoton']>0:
                    q['puoliso_ansiopvraha'],q['puoliso_puhdasansiopvraha'],q['puoliso_peruspvraha']=self.ansiopaivaraha(p['puoliso_tyoton'],p['puoliso_vakiintunutpalkka'],p['lapsia'],p['puoliso_tulot'],p['puoliso_saa_ansiopaivarahaa'],p['puoliso_tyottomyyden_kesto'],p)
            
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q['verot'],q['valtionvero'],q['kunnallisvero'],q['kunnallisveronperuste'],q['valtionveroperuste'],\
            q['ansiotulovahennys'],q['perusvahennys'],q['tyotulovahennys'],q['tyotulovahennys_kunnallisveroon'],\
            q['ptel'],q['sairausvakuutusmaksu'],q['tyotvakmaksu'],q['tyel_kokomaksu'],q['ylevero']=self.verotus(p['t'],
                q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
                q['kokoelake'],p['lapsia'],p)
        _,q['verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p)

        if (p['aikuisia']>1):
            _,q['puoliso_verot'],_,_,_,_,_,_,_,_,q['puoliso_ptel'],q['puoliso_sairausvakuutusmaksu'],\
                q['puoliso_tyotvakmaksu'],q['puoliso_tyel_kokomaksu'],q['puoliso_ylevero']\
                =self.verotus(p['puoliso_tulot'],q['puoliso_ansiopvraha']+q['puoliso_aitiyspaivaraha']+q['puoliso_isyyspaivaraha']+q['puoliso_kotihoidontuki']+q['puoliso_sairauspaivaraha']+q['puoliso_opintotuki'],
                    q['puoliso_kokoelake'],p['lapsia'],p)
            _,q['puoliso_verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puoliso_tulot'],0,0,0,p)
        else:
            q['puoliso_verot_ilman_etuuksia']=0
            q['puoliso_verot']=0
            q['puoliso_ptel']=0
            q['puoliso_sairausvakuutusmaksu']=0
            q['puoliso_tyotvakmaksu']=0
    
        if p['aikuisia']==1 and p['saa_elatustukea']>0:
            q['elatustuki']=self.laske_elatustuki(p['lapsia'],p['aikuisia'])
        else:
            q['elatustuki']=0
        
        if p['elakkeella']>0:
            q['asumistuki']=self.elakkeensaajan_asumistuki(p['puoliso_tulot']+p['t'],q['kokoelake'],p['asumismenot_asumistuki'],p)
        else:
            q['asumistuki']=self.asumistuki(p['puoliso_tulot']+p['t'],q['ansiopvraha']+q['puoliso_ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],p['asumismenot_asumistuki'],p)
            
        if p['lapsia']>0:
            q['pvhoito']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['puoliso_ansiopvraha']+q['sairauspaivaraha'],p)
            if (p['lapsia_kotihoidontuella']>0):
                alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
                q['pvhoito']=0 #max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
            q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['elatustuki'],p)
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
            q['puoliso_ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
            
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
            q['ansiopvraha_netto']=q['ansiopvraha']-(q['verot']-q['verot_ilman_etuuksia'])
            
        if p['aikuisia']>1:
            if p['puoliso_tyoton']>0: # vanhuuseläkkeellä
                q['puoliso_ansiopvraha_netto']=q['puoliso_ansiopvraha']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
            elif p['puoliso_opiskelija']>0:
                q['puoliso_opintotuki_netto']=q['puoliso_opintotuki']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
            elif p['puoliso_kotihoidontuella']>0:
                q['puoliso_kotihoidontuki_netto']=q['puoliso_kotihoidontuki']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia']) 
        else:
            q['puoliso_ansiopvraha_netto']=0
        #print('ptyötön',q['puoliso_ansiopvraha_netto'],q['puoliso_ansiopvraha'],q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
            
        if (p['isyysvapaalla']>0 or p['aitiysvapaalla']>0) and p['tyoton']>0:
            print('error: vanhempainvapaalla & työtön ei toteutettu')
    
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
            q['toimeentulotuki']=0
        else:
            # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
            q['toimeentulotuki']=self.toimeentulotuki(p['t'],q['verot_ilman_etuuksia'],p['puoliso_tulot'],q['puoliso_verot_ilman_etuuksia'],\
                q['elatustuki']+q['opintotuki_netto']+q['puoliso_opintotuki_netto']+q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto']+q['puoliso_kotihoidontuki_netto'],\
                0,p['asumismenot_toimeentulo'],q['pvhoito'],p)

        kateen=q['opintotuki']+q['kokoelake']+p['puoliso_tulot']+p['t']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
            +q['ansiopvraha']+q['puoliso_ansiopvraha']+q['elatustuki']-q['puoliso_verot']-q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']
        omanetto=q['opintotuki']+q['kokoelake']+p['t']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
            +q['ansiopvraha']+q['elatustuki']-q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']
            
        q['kateen']=kateen # tulot yhteensä perheessä
        q['perhetulot_netto']=p['puoliso_tulot']+p['t']-q['verot_ilman_etuuksia']-q['puoliso_verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['omattulot_netto']=p['t']-q['verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
        q['etuustulo_netto']=q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['opintotuki']\
            +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimeentulotuki']-(q['pvhoito_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'])
        q['etuustulo_brutto']=q['ansiopvraha']+q['puoliso_ansiopvraha']+q['opintotuki']\
            +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimeentulotuki']+q['kokoelake']
        q['brutto']=q['etuustulo_brutto']+p['t']
            
        #if p['aikuisia']>1 and False:
        #    asumismeno=0.5*p['asumismenot_asumistuki']
        #else:
        asumismeno=p['asumismenot_asumistuki']
            
        q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        
        # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
        q['netto']=max(0,kateen-q['alv'])
        #q['netto']=max(0,omanetto-q['alv']-asumismeno)
        
        if not legacy:
            kateen=q['netto']
        
        q['palkkatulot']=p['t']
        if p['elakkeella']<1:
            q['palkkatulot_eielakkeella']=p['t']
        else:
            q['palkkatulot_eielakkeella']=0
            
        q['puoliso_palkkatulot']=p['puoliso_tulot']
        q['puoliso_tulot_netto']=p['puoliso_tulot']-q['puoliso_verot_ilman_etuuksia']
        q['perustulo']=0
        q['puoliso_perustulo']=0
        q['perustulo_netto']=0
        q['puoliso_perustulo_netto']=0
        q['perustulo_nettonetto']=0
        q['puoliso_perustulo_nettonetto']=0

        return kateen,q
        
    def setup_puoliso_q(self,p,q,puoliso='puoliso_',alku='puoliso_',include_takuuelake=True):
        q[puoliso+'multiplier']=1
        q[puoliso+'perustulo']=0
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
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
                else:
                    q[puoliso+'opintotuki']=self.opintoraha(0,p)
            else: # ei eläkkeellä     
                q[puoliso+'kokoelake']=p[alku+'tyoelake']
                q[puoliso+'opintotuki']=0
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'tyoelake']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                q[puoliso+'ansiopvraha'],q[puoliso+'puhdasansiopvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'sairauspaivarahalla']>0:
                    q[puoliso+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'vakiintunutpalkka'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
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
            if p[alku+'aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p[alku+'isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
            elif p[alku+'kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            else:
                q[omat+'opintotuki']=self.opintoraha(0,p)
        else: # ei eläkkeellä     
            q[omat+'opintotuki']=0
            q[omat+'elake_maksussa']=p[alku+'elake_maksussa']
            q[omat+'kokoelake']=p[alku+'tyoelake']
            q[omat+'tyoelake']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            if p[alku+'aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p[alku+'isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'vakiintunutpalkka'])
            elif p[alku+'sairauspaivarahalla']>0:
                q[omat+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'vakiintunutpalkka'])
            elif p[alku+'kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            elif p['tyoton']>0:
                if alku+'omavastuukerroin' in p:
                    omavastuukerroin=p[alku+'omavastuukerroin']
                else:
                    omavastuukerroin=1.0
                q[omat+'ansiopvraha'],q[omat+'puhdasansiopvraha'],q[omat+'peruspvraha']=\
                    self.ansiopaivaraha(p[alku+'tyoton'],p[alku+'vakiintunutpalkka'],p['lapsikorotus_lapsia'],p[alku+'t'],
                        p[alku+'saa_ansiopaivarahaa'],p[alku+'tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin,alku=omat)
        return q        
        
    def summaa_q(self,p,q,omat='omat_',puoliso='puoliso_'):
        if p['aikuisia']>1:
            q['verot']=q[omat+'verot']+q[puoliso+'verot']
            q['ptel']=q[omat+'ptel']+q[puoliso+'ptel']
            q['kunnallisvero']=q[omat+'kunnallisvero']+q[puoliso+'kunnallisvero']
            q['valtionvero']=q[omat+'valtionvero']+q[puoliso+'valtionvero']
            q['verot_ilman_etuuksia']=q[omat+'verot_ilman_etuuksia']+q[puoliso+'verot_ilman_etuuksia']
            q['tyotvakmaksu']=q[omat+'tyotvakmaksu']+q[puoliso+'tyotvakmaksu']
            q['ansiopvraha']=q[puoliso+'ansiopvraha']+q[omat+'ansiopvraha']
            q['puhdasansiopvraha']=q[puoliso+'puhdasansiopvraha']+q[omat+'puhdasansiopvraha']
            q['peruspvraha']=q[puoliso+'peruspvraha']+q[omat+'peruspvraha']
            q['elake_maksussa']=q[puoliso+'elake_maksussa']+q[omat+'elake_maksussa']
            q['opintotuki']=q[puoliso+'opintotuki']+q[omat+'opintotuki']
            q['palkkatulot']=q[omat+'palkkatulot']+q[puoliso+'palkkatulot']
            q['kokoelake']=q[puoliso+'kokoelake']+q[omat+'kokoelake']
            q['kotihoidontuki']=q[puoliso+'kotihoidontuki']+q[omat+'kotihoidontuki']
            q['aitiyspaivaraha']=q[puoliso+'aitiyspaivaraha']+q[omat+'aitiyspaivaraha']
            q['isyyspaivaraha']=q[puoliso+'isyyspaivaraha']+q[omat+'isyyspaivaraha']
            q['sairauspaivaraha']=q[puoliso+'sairauspaivaraha']+q[omat+'sairauspaivaraha']
            q['tyel_kokomaksu']=q[puoliso+'tyel_kokomaksu']+q[omat+'tyel_kokomaksu']
            q['sairausvakuutusmaksu']=q[puoliso+'sairausvakuutusmaksu']+q[omat+'sairausvakuutusmaksu']
            q['ylevero']=q[puoliso+'ylevero']+q[omat+'ylevero'] # onko kotitalouskohtainen??
            q['elatustuki']=q[omat+'elatustuki']+q[puoliso+'elatustuki']
            q['perustulo']=q[omat+'perustulo']+q[puoliso+'perustulo']
            q['palkkatulot_eielakkeella']=q[puoliso+'palkkatulot_eielakkeella']+q[omat+'palkkatulot_eielakkeella']
            q['perustulo_netto']=q[omat+'perustulo_netto']+q[puoliso+'perustulo_netto']
            q['perustulo_nettonetto']=q[omat+'perustulo_nettonetto']+q[puoliso+'perustulo_nettonetto']
        else:
            q['verot']=q[omat+'verot']
            q['ptel']=q[omat+'ptel']
            q['kunnallisvero']=q[omat+'kunnallisvero']
            q['valtionvero']=q[omat+'valtionvero']
            q['verot_ilman_etuuksia']=q[omat+'verot_ilman_etuuksia']
            q['tyotvakmaksu']=q[omat+'tyotvakmaksu']
            q['ansiopvraha']=q[omat+'ansiopvraha']
            q['puhdasansiopvraha']=q[omat+'puhdasansiopvraha']
            q['peruspvraha']=q[omat+'peruspvraha']
            q['elake_maksussa']=q[omat+'elake_maksussa']
            q['opintotuki']=q[omat+'opintotuki']
            q['kokoelake']=q[omat+'kokoelake']
            q['kotihoidontuki']=q[omat+'kotihoidontuki']
            q['aitiyspaivaraha']=q[omat+'aitiyspaivaraha']
            q['isyyspaivaraha']=q[omat+'isyyspaivaraha']
            q['sairauspaivaraha']=q[omat+'sairauspaivaraha']
            q['tyel_kokomaksu']=q[omat+'tyel_kokomaksu']
            q['sairausvakuutusmaksu']=q[omat+'sairausvakuutusmaksu']
            q['ylevero']=q[omat+'ylevero']
            q['palkkatulot']=q[omat+'palkkatulot']
            q['elatustuki']=q[omat+'elatustuki']
            q['perustulo']=q[omat+'perustulo']
            q['palkkatulot_eielakkeella']=q[omat+'palkkatulot_eielakkeella']
            q['perustulo_netto']=q[omat+'perustulo_netto']
            q['perustulo_nettonetto']=q[omat+'perustulo_nettonetto']
        
        return q
        
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
            self.verotus(q[omat+'palkkatulot'],q[omat+'ansiopvraha']+q[omat+'aitiyspaivaraha']+q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+q[omat+'sairauspaivaraha']+q[omat+'opintotuki'],
                q[omat+'kokoelake'],p['lapsia'],p,alku=omatalku)
        _,q[omat+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p,alku=omatalku)

        if p['aikuisia']>1 and p[puoliso+'alive']>0:
            _,q[puoliso+'verot'],q[puoliso+'valtionvero'],q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveronperuste'],q[puoliso+'valtionveroperuste'],\
            q[puoliso+'ansiotulovahennys'],q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon'],\
            q[puoliso+'ptel'],q[puoliso+'sairausvakuutusmaksu'],q[puoliso+'tyotvakmaksu'],q[puoliso+'tyel_kokomaksu'],q[puoliso+'ylevero']=\
                self.verotus(q[puoliso+'palkkatulot'],
                    q[puoliso+'ansiopvraha']+q[puoliso+'aitiyspaivaraha']+q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'sairauspaivaraha']+q[puoliso+'opintotuki'],
                    q[puoliso+'kokoelake'],0,p,alku=puoliso) # onko oikein että lapsia 0 tässä????
            _,q[puoliso+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],0,0,0,p,alku=puoliso)
        else:
            q[puoliso+'verot_ilman_etuuksia'],q[puoliso+'verot'],q[puoliso+'valtionvero']=0,0,0
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
            q['asumistuki']=self.asumistuki(q['palkkatulot'],q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']
                                            +q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
                                            p['asumismenot_asumistuki'],p)
#             print(q['palkkatulot'],q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']
#                                             +q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
#                                             p['asumismenot_asumistuki'])
            
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
            else:
                # kuukausi lomalla, jolloin ei päivähoitoa
                q['pvhoito']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['sairauspaivaraha'],p)
                if (p['lapsia_kotihoidontuella']>0):
                    alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
                    q['pvhoito']=max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
                q['pvhoito_ilman_etuuksia']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],p[puolisoalku+'t']+p[omatalku+'t']+q['elatustuki'],p)
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
            q['lapsilisa']=0
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
            q[puoliso+'ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
        q[omat+'kokoelake_netto'],q[omat+'isyyspaivaraha_netto'],q[omat+'ansiopvraha_netto'],q[omat+'aitiyspaivaraha_netto'],q[omat+'sairauspaivaraha_netto'],\
            q[omat+'opintotuki_netto'],q[omat+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
        q[puoliso+'kokoelake_netto'],q[puoliso+'isyyspaivaraha_netto'],q[puoliso+'ansiopvraha_netto'],q[puoliso+'aitiyspaivaraha_netto'],q[puoliso+'sairauspaivaraha_netto'],\
            q[puoliso+'opintotuki_netto'],q[puoliso+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
            
        if p[omatalku+'elakkeella']>0:
            q[omat+'kokoelake_netto']=q[omat+'kokoelake']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
        elif p[omatalku+'opiskelija']>0:
            q[omat+'opintotuki_netto']=q[omat+'opintotuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
        elif p[omatalku+'aitiysvapaalla']>0:
            q[omat+'aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        elif p[omatalku+'isyysvapaalla']>0:
            q[omat+'isyyspaivaraha_netto']=q[omat+'isyyspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        elif p[omatalku+'kotihoidontuella']>0:
            q[omat+'kotihoidontuki_netto']=q[omat+'kotihoidontuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        elif p[omatalku+'sairauspaivarahalla']>0:
            q[omat+'sairauspaivaraha_netto']=q[omat+'sairauspaivaraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia']) 
        else:
            q[omat+'ansiopvraha_netto']=q[omat+'ansiopvraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])

        if p[puolisoalku+'elakkeella']>0:
            q[puoliso+'kokoelake_netto']=q[puoliso+'kokoelake']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
        elif p[puolisoalku+'opiskelija']>0:
            q[puoliso+'opintotuki_netto']=q[puoliso+'opintotuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
        elif p[puolisoalku+'aitiysvapaalla']>0:
            q[puoliso+'aitiyspaivaraha_netto']=q[puoliso+'aitiyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        elif p[puolisoalku+'isyysvapaalla']>0:
            q[puoliso+'isyyspaivaraha_netto']=q[puoliso+'isyyspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        elif p[puolisoalku+'kotihoidontuella']>0:
            q[puoliso+'kotihoidontuki_netto']=q[puoliso+'kotihoidontuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        elif p[puolisoalku+'sairauspaivarahalla']>0:
            q[puoliso+'sairauspaivaraha_netto']=q[puoliso+'sairauspaivaraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia']) 
        else:
            q[puoliso+'ansiopvraha_netto']=q[puoliso+'ansiopvraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])

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

        if q['ansiopvraha_netto']>0:
            if p['aikuisia']>1:
                if p[omatalku+'alive']>0 and p[puolisoalku+'alive']>0:
                    suhde=max(0,q[omat+'ansiopvraha_netto']/q['ansiopvraha_netto'])
                    q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                    q[puoliso+'ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                elif p[omatalku+'alive']>0:
                    q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                    q[puoliso+'ansiopvraha_nettonetto']=0
                elif p[puolisoalku+'alive']>0:
                    q[puoliso+'ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                    q[omat+'ansiopvraha_nettonetto']=0
                else:
                    q[omat+'ansiopvraha_nettonetto']=0
                    q[puoliso+'ansiopvraha_nettonetto']=0
            else:
                q[omat+'ansiopvraha_nettonetto']=q[omat+'ansiopvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                q[puoliso+'ansiopvraha_nettonetto']=0
                
            q['ansiopvraha_nettonetto']=q[puoliso+'ansiopvraha_nettonetto']+q[omat+'ansiopvraha_nettonetto']
        else:
            q[omat+'ansiopvraha_nettonetto']=0
            q[puoliso+'ansiopvraha_nettonetto']=0
            q['ansiopvraha_nettonetto']=0

        if p['aikuisia']<2:
            if p[omatalku+'opiskelija']>0 or p[omatalku+'alive']<1:
                q['toimeentulotuki']=0
            else:
                # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
                q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],0,0,\
                    q['elatustuki']+q['opintotuki_netto']+q['ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                    +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
                    0,p['asumismenot_toimeentulo'],q['pvhoito'],p)
                #print(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],0,0,\
                #    q['elatustuki']+q['opintotuki']+q['ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                #    +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki'],\
                #    0,p['asumismenot_toimeentulo'],q['pvhoito'])
                #print(q['elatustuki'],q['opintotuki'],q['ansiopvraha_netto'],q['asumistuki'],q['sairauspaivaraha_netto'])
                #print(q['lapsilisa'],q['kokoelake_netto'],q['aitiyspaivaraha_netto'],q['isyyspaivaraha_netto'],q['kotihoidontuki'])
                #print('*',q['ansiopvraha_netto'],q['asumistuki'],q['lapsilisa'],q['kokoelake_netto'],q['elatustuki'])
        else:
            if p[omatalku+'opiskelija']>0 and p[puolisoalku+'opiskelija']>0:
                q['toimeentulotuki']=0
            else:
                # Hmm, meneekö sairauspäiväraha, äitiyspäiväraha ja isyyspäiväraha oikein?
                q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],p[puolisoalku+'t'],q[puoliso+'verot_ilman_etuuksia'],\
                    q['elatustuki']+q['opintotuki_netto']+q['ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                    +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
                    0,p['asumismenot_toimeentulo'],q['pvhoito'],p)

        # sisältää sekä omat että puolison tulot ja menot
        kateen=q['opintotuki']+q['kokoelake']+q['palkkatulot']+q['aitiyspaivaraha']+q['isyyspaivaraha']\
            +q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']+q['ansiopvraha']+q['elatustuki']\
            -q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']

        brutto_omat=q[omat+'opintotuki']+q[omat+'kokoelake']+q[omat+'palkkatulot']+q[omat+'aitiyspaivaraha']\
            +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+\
            +q[omat+'ansiopvraha']+q[omat+'elatustuki']+q[omat+'sairauspaivaraha']
        kateen_omat=brutto_omat-q[omat+'verot']
        etuusnetto_omat=brutto_omat-q[omat+'palkkatulot']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
                    
        q['kateen']=kateen # tulot yhteensä perheessä
        q['etuustulo_netto']=q['ansiopvraha_netto']+q['opintotuki']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimeentulotuki']+q['kokoelake']+q['elatustuki']+q['lapsilisa']\
            -(q['pvhoito']-q['pvhoito_ilman_etuuksia'])-(q['verot']-q['verot_ilman_etuuksia'])
            
        asumismeno=p['asumismenot_asumistuki']
            
        q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        
        # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
        q['netto']=max(0,kateen-q['alv'])
        
        if p['aikuisia']>1:
            brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
                +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                +q[puoliso+'ansiopvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']
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
            
            etuusnetto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])*suhde
            kateen_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])*suhde
            brutto_omat+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
            q[omat+'toimeentulotuki']=q['toimeentulotuki']*suhde
            q[omat+'asumistuki']=q['asumistuki']*suhde
            q[omat+'pvhoito']=q['pvhoito']*suhde
            q[omat+'lapsilisa']=q['lapsilisa']*suhde
            q[omat+'alv']=q['alv']*suhde
            
            etuusnetto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])*(1-suhde)
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
            etuusnetto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito']
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

        #q[omat+'etuustulo_brutto']=brutto_omat
        #q[puoliso+'etuustulo_brutto']=brutto_puoliso
        
        q[omat+'etuustulo_brutto']=q[omat+'ansiopvraha']+q[omat+'opintotuki']+q[omat+'aitiyspaivaraha']\
            +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+q[omat+'asumistuki']\
            +q[omat+'toimeentulotuki']+q[omat+'kokoelake']+q[omat+'elatustuki']+q[omat+'lapsilisa'] # + sairauspaivaraha
        q[puoliso+'etuustulo_brutto']=q[puoliso+'ansiopvraha']+q[puoliso+'opintotuki']+q[puoliso+'aitiyspaivaraha']\
            +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'asumistuki']\
            +q[puoliso+'toimeentulotuki']+q[puoliso+'kokoelake']+q[puoliso+'elatustuki']+q[puoliso+'lapsilisa']
        q['etuustulo_brutto']=q[omat+'etuustulo_brutto']+q[puoliso+'etuustulo_brutto'] # + sairauspaivaraha
        
        kateen=q['netto']
        
        # check that omat, puoliso split is ok
        #self.check_q_netto(q,p['aikuisia'],omat,puoliso)

        return kateen,q
        
    def add_q(self,benefitq1,benefitq2):
        q= { k: benefitq1.get(k, 0) + benefitq2.get(k, 0) for k in set(benefitq1) }
        
        return q
        
    def check_q_netto(self,q,aikuisia,omat,puoliso):
        if aikuisia>1:
            s=[omat,puoliso]
            d=q['netto']-q[omat+'netto']-q[puoliso+'netto']
            if np.abs(d)>1e-6:
                print('netto2',d,puoliso)
            d=q['palkkatulot']-q[omat+'palkkatulot']-q[puoliso+'palkkatulot']
            if np.abs(d)>1e-6:
                print('palkkatulot2',d,puoliso)
        else:
            s=[omat]
            for ss in set(['etuustulo_brutto','palkkatulot','netto','opintotuki','kokoelake','palkkatulot','aitiyspaivaraha','isyyspaivaraha','kotihoidontuki','ansiopvraha','verot','pvhoito']):
                d=q[ss]-q[omat+ss]
                if np.abs(d)>1e-6:
                    print('1',ss,omat,d)
                    print('b',ss,q['omat_'+ss])
            
        for alku in set(s):
            d1=q[alku+'palkkatulot']+q[alku+'etuustulo_brutto']-q[alku+'verot']-q[alku+'alv']-q[alku+'pvhoito']
            d2=q[alku+'netto']
            
            if np.abs(d2-d1)>1e-6:
                print('12',alku,d2-d1,puoliso)
        
    

    def laske_alv(self,kateen):
        # kulutusmenoista maksetaan noin 24% alvia (lähde: TK, https://www.stat.fi/tietotrendit/artikkelit/2019/arvonlisavero-haivyttaa-progression-vaikutuksen-pienituloisimmilta/)
        alv=(0.24+self.additional_vat)/(1.24+self.additional_vat)
        if self.year==2022:
            return alv*kateen
        elif self.year==2021:
            return alv*kateen
        elif self.year==2020:
            return alv*kateen
        elif self.year==2019:
            return alv*kateen
        elif self.year==2018:
            return alv*kateen
        
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
        max_menot=np.array([[508, 492, 411, 362],[735, 706, 600, 527],[937, 890, 761, 675],[1095, 1038, 901, 804]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3

        max_meno=max_menot[min(3,p['aikuisia']+p['lapsia']-1),p['kuntaryhma']]+max(0,p['aikuisia']+p['lapsia']-4)*max_lisa[p['kuntaryhma']]

        prosentti=0.8 # vastaa 80 %
        suojaosa=300*p['aikuisia']
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
        suojaosa=300*p['aikuisia']
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
        suojaosa=300*p['aikuisia']
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
    
    def elakkeensaajan_asumistuki_2018(self,palkkatulot,muuttulot,vuokra,p):
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        max_menot=np.array([8_613,7_921,6_949])
        max_meno=max_menot[max(0,p['kuntaryhma']-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if p['aikuisia']<2:
            tuloraja=9_534/12
        else:
            tuloraja=15_565/12
            #if puolisolla_oikeus:
            #    tuloraja=15_565/12
            #else:
            #    tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if p['aikuisia']>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        

        
    def elakkeensaajan_asumistuki_2019(self,palkkatulot,muuttulot,vuokra,p):
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        # e/kk    IIII kuntaryhmä,
        # e/kk
        # 1    508    492    411    362
        # 2    735    706    600    527
        # 3    937    890    761    675
        max_menot=np.array([8_243,7_581,6_651])
        max_meno=max_menot[max(0,p['kuntaryhma']-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if p['aikuisia']<2:
            tuloraja=9_534/12
        else:
            tuloraja=15_565/12
            #if puolisolla_oikeus:
            #    tuloraja=15_565/12
            #else:
            #    tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if p['aikuisia']>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        


    def elakkeensaajan_asumistuki_2020(self,palkkatulot,muuttulot,vuokra,p):
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        # e/kk    IIII kuntaryhmä,
        # e/kk
        # 1    508    492    411    362
        # 2    735    706    600    527
        # 3    937    890    761    675
        max_menot=np.array([8_360,7_688,6_745])
        max_meno=max_menot[max(0,p['kuntaryhma']-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if p['aikuisia']<2:
            tuloraja=9_534/12
        else:
            tuloraja=15_565/12
            #if puolisolla_oikeus:
            #    tuloraja=15_565/12
            #else:
            #    tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if p['aikuisia']>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        

        
    def elakkeensaajan_asumistuki_2021(self,palkkatulot,muuttulot,vuokra,p):
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        max_menot=np.array([8_613,7_921,6_949])
        max_meno=max_menot[max(0,p['kuntaryhma']-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if p['aikuisia']<2:
            tuloraja=9_534/12
        else:
            tuloraja=15_565/12
            #if puolisolla_oikeus:
            #    tuloraja=15_565/12
            #else:
            #    tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if p['aikuisia']>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        

        
    def elakkeensaajan_asumistuki_2022(self,palkkatulot,muuttulot,vuokra,p,puolisolla_oikeus=False):
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        #
        max_menot=np.array([8_433,7_755,6_804])
        max_meno=max_menot[max(0,p['kuntaryhma']-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if p['aikuisia']<2:
            tuloraja=9_534/12
        else:
            tuloraja=15_565/12
            #if puolisolla_oikeus:
            #    tuloraja=15_565/12
            #else:
            #    tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if p['aikuisia']>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
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
                alaraja=2136
                prosentti=prosentti1
            elif vakea==2:
                alaraja=2136
                prosentti=prosentti1
            elif vakea==3:
                alaraja=2756
                prosentti=prosentti1
            elif vakea==4:
                alaraja=3129
                prosentti=prosentti1
            elif vakea==5:
                alaraja=3502
                prosentti=prosentti1
            elif vakea==6:
                alaraja=3874
                prosentti=prosentti1
            else:
                alaraja=3874+138*(vakea-6)
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
        
    def paivahoitomenot2021(self,hoidossa,tulot,p,prosentti1=None,prosentti2=None,prosentti3=None,maksimimaksu=None):
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
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        return maksu        
        
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
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        return maksu                
    
    def laske_kansanelake2018(self,ika,tyoelake,yksin,disability=False,lapsia=0):
        if yksin>0:
            maara=628.85
        else:
            maara=557.79
            
        if lapsia>0:
            maara += 22.23*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-55.54))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-55.54))/2)
            else:
                maara=0
            
        if maara<6.92:
            maara=0
            
        return maara
            
    def laske_kansanelake2019(self,ika,tyoelake,yksin,disability=False,lapsia=0):
        if yksin>0:
            maara=628.85
        else:
            maara=557.79
        if lapsia>0:
            maara += 22.23*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-55.54))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-55.54))/2)
            else:
                maara=0
            
        if maara<6.92:
            maara=0
            
        return maara
        
    def laske_kansanelake2020(self,ika,tyoelake,yksin,disability=False,lapsia=0):
        if yksin>0:
            maara=662.86
        else:
            maara=591.79
        if lapsia>0:
            maara += 22.23*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-55.54))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-55.54))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-55.54))/2)
            else:
                maara=0
            
        if maara<6.92:
            maara=0
            
        return maara
        
    def laske_kansanelake2021(self,ika,tyoelake,yksin,disability=False,lapsia=0):
        if yksin>0:
            maara=665.29
        else:
            maara=593.97
        if lapsia>0:
            maara += 22.23*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-56.29))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-56.29))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-56.29))/2)
            else:
                maara=0
            
        if maara<6.92:
            maara=0
            
        return maara
        
    def laske_kansanelake2022(self,ika,tyoelake,yksin,disability=False,lapsia=0):
        if yksin>0:
            maara=679.50
        else:
            maara=606.65
        if lapsia>0:
            maara += 22.71*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-57.45))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-57.45))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-57.45))/2)
            else:
                maara=0
                
        if maara<6.92:
            maara=0
            
        return maara
        
    def laske_takuuelake2018(self,ika,muuelake,disability=False,lapsia=0):
        if ika<63 and not disability:
            return 0
        
        lapsikorotus=22.23*lapsia
        if muuelake<777.84+lapsikorotus:
            elake=784.52+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<6.92:
            elake=0

        return elake
    
    def laske_takuuelake2019(self,ika,muuelake,disability=False,lapsia=0):
        if ika<63 and not disability:
            return 0
        
        lapsikorotus=22.23*lapsia
        if muuelake<777.84+lapsikorotus:
            elake=784.52+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<6.92:
            elake=0

        return elake
    
    def laske_takuuelake2020(self,ika,muuelake,disability=False,lapsia=0):
        if ika<63 and not disability:
            return 0
        
        lapsikorotus=22.23*lapsia
        if muuelake<834.52+lapsikorotus:
            elake=834.52+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<6.92:
            elake=0

        return elake
        
    def laske_takuuelake2021(self,ika,muuelake,disability=False,lapsia=0):
        if ika<63 and not disability:
            return 0
            
        lapsikorotus=22.23*lapsia
        
        if muuelake<837.59+lapsikorotus:
            elake=837.59+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<6.92:
            elake=0

        return elake
        
    def laske_takuuelake2022(self,ika,muuelake,disability=False,lapsia=0):
        if ika<63 and not disability:
            return 0
            
        lapsikorotus=22.71*lapsia
        
        if muuelake<855.48+lapsikorotus:
            elake=855.48+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<6.92:
            elake=0

        return elake        
        
    def laske_puhdas_tyoelake(self,ika,elake,disability=False,yksin=1,lapsia=0):
         '''
         Vähentää työeläkkeestä kansaneläkkeen ja takuueläkkeen
         '''
         if self.irr_vain_tyoelake:
             return elake 
         else:
             kansanelake=self.laske_kansanelake(ika,0,yksin,disability=disability,lapsia=0)
             elakeindeksi=(0*1+1.0*1.0/1.016) #**0.25
             indeksi=elakeindeksi**max(0,ika-65)
             if ika>=63 or disability:
                 return max(0,elake-self.laske_takuuelake(ika,0,disability=disability)-kansanelake*indeksi)
                 #return max(0,elake-self.laske_takuuelake(ika,0,disability=disability))
             else:
                 return max(0,elake-self.laske_kansanelake(ika,0,1)*indeksi)
                 
    def laske_puhdas_tyoelake_v2(self,ika,tyoelake,kansanelake,disability=False,yksin=1,lapsia=0):
        '''
        Vähentää työeläkkeestä kansaneläkkeen ja takuueläkkeen
        '''
        kansanelake_taysi=self.laske_kansanelake(ika,0,yksin,disability=disability,lapsia=lapsia)
        elakeindeksi=(0*1+1.0*1.0/1.016)
        indeksi=elakeindeksi**max(0,ika-65)

        # tyoeläkkeestä vähennetään takuueläke ja se osa kansaneläkettä, jonka työeläke on leikannut (kansaneläke sisältyy elake:seen)
        vahennys1=max(0,(kansanelake_taysi-kansanelake)*indeksi)
            
        if ika>=63 or disability:
            vahennys2=max(0,self.laske_takuuelake(ika,kansanelake_taysi,disability=disability,lapsia=lapsia)-self.laske_takuuelake(ika,tyoelake+kansanelake,disability=disability,lapsia=lapsia))
            return max(0,tyoelake-vahennys1-vahennys2)
        else:
            return max(0,tyoelake-vahennys1)
    
    def laske_kokonaiselake(self,ika,muuelake,yksin=1,include_takuuelake=True,include_kansanelake=False,disability=False,lapsia=0):
        '''
        by default, kansaneläke is not included, since this function is called annually
        kansaneläke sisältyy muuelake-muuttujaan
        '''
        if include_kansanelake:
            kansanelake=self.laske_kansanelake(ika,muuelake,yksin,disability=disability,lapsia=lapsia)
            muuelake=muuelake+kansanelake
            
        if include_takuuelake:
            takuuelake=self.laske_takuuelake(ika,muuelake,disability=disability,lapsia=lapsia)
            kokoelake=takuuelake+muuelake
        else:
            kokoelake=muuelake
    
        return kokoelake
        
    def laske_kokonaiselake_v2(self,ika,muuelake,kansanelake,yksin=1,include_takuuelake=True,include_kansanelake=False,disability=False,lapsia=0):
        '''
        by default, kansaneläke is not included, since this function is called annually
        kansaneläke lasketaan erikseen
        '''
        if include_kansanelake:
            muuelake=muuelake+kansanelake
            
        if include_takuuelake:
            takuuelake=self.laske_takuuelake(ika,muuelake,disability=disability,lapsia=lapsia)
            kokoelake=takuuelake+muuelake
        else:
            kokoelake=muuelake
    
        return kokoelake

    def isyysraha_perus(self,vakiintunutpalkka):
        if self.year==2018:
            minimi=27.86*25
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2019:
            minimi=27.86*25
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2020:
            minimi=28.94*25
            taite1=37_861/12  
            taite2=58_252/12  
        elif self.year==2021:
            minimi=29.05*25
            taite1=39_144/12  
            taite2=60_225/12  
        elif self.year==2022:
            minimi=29.67*25
            taite1=39_144/12  
            taite2=60_225/12  
        elif self.year==2023:
            minimi=29.67*25
            taite1=39_144/12  
            taite2=60_225/12  

        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
        raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def aitiysraha2019(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=0
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            minimi=27.86*25
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def aitiysraha2020(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=0
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            minimi=28.94*25
            taite1=37_861/12  
            taite2=58_252/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def aitiysraha2021(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=0
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            minimi=29.05*25
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def aitiysraha2022(self,vakiintunutpalkka,kesto):
        if kesto<56/260:
            minimi=0
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            minimi=29.67*25
            taite1=39_144/12  
            taite2=60_225/12 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return raha
        
    def sairauspaivaraha2018(self,vakiintunutpalkka):
        minimi=24.64*25
        taite1=30_394/12
        taite2=58_252/12
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))

        return raha
        
    def sairauspaivaraha2019(self,vakiintunutpalkka):
        minimi=27.86*25
        taite1=30_394/12
        taite2=57_183/12
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    

        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))

        return raha

    def sairauspaivaraha2020(self,vakiintunutpalkka):
        minimi=28.94*25
        taite1=31_595/12  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return raha
        
    def sairauspaivaraha2021(self,vakiintunutpalkka):
        minimi=29.05*25
        taite1=32_011/12  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return raha
        
    def sairauspaivaraha2022(self,vakiintunutpalkka):
        minimi=29.67*25
        taite1=32_011/12  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return raha
        
    def laske_marginaalit(self,q1,q2,dt,laske_tyollistymisveroaste=0):
    
        if dt<1:
            dt=1

        # lasketaan marginaalit
        marg={}        
        marg['asumistuki']=(-q2['asumistuki']+q1['asumistuki'])*100/dt
        marg['kotihoidontuki']=(-q2['kotihoidontuki_netto']+q1['kotihoidontuki_netto'])*100/dt
        marg['ansiopvraha']=(+q1['ansiopvraha_netto']-q2['ansiopvraha_netto']+q1['puoliso_ansiopvraha_netto']-q2['puoliso_ansiopvraha_netto'])*100/dt 
        marg['pvhoito']=(-q1['pvhoito']+q2['pvhoito'])*100/dt
        marg['toimeentulotuki']=(+q1['toimeentulotuki']-q2['toimeentulotuki'])*100/dt
        marg['palkkaverot']=(-q1['verot_ilman_etuuksia']+q2['verot_ilman_etuuksia']-q1['puoliso_verot_ilman_etuuksia']+q2['puoliso_verot_ilman_etuuksia'])*100/dt
        marg['valtionvero']=(-q1['valtionvero']+q2['valtionvero'])*100/dt
        marg['alv']=(-q1['alv']+q2['alv'])*100/dt
        marg['elake']=(q1['kokoelake_netto']-q2['kokoelake_netto'])*100/dt
        marg['opintotuki']=(q1['opintotuki_netto']-q2['opintotuki_netto'])*100/dt
        marg['kunnallisvero']=(-q1['kunnallisvero']+q2['kunnallisvero'])*100/dt
        #marg['ansiotulovah']=(+q1['ansiotulovahennys']-q2['ansiotulovahennys'])*100/dt
        #marg['tyotulovahennys']=(+q1['tyotulovahennys']-q2['tyotulovahennys'])*100/dt
        #marg['perusvahennys']=(+q1['perusvahennys']-q2['perusvahennys'])*100/dt
        #marg['tyotulovahennys_kunnallisveroon']=(+q1['tyotulovahennys_kunnallisveroon']-q2['tyotulovahennys_kunnallisveroon'])*100/dt
        marg['ptel']=(-q1['ptel']+q2['ptel']-q1['puoliso_ptel']+q2['puoliso_ptel'])*100/dt
        marg['sairausvakuutusmaksu']=(-q1['sairausvakuutusmaksu']+q2['sairausvakuutusmaksu']-q1['puoliso_sairausvakuutusmaksu']+q2['puoliso_sairausvakuutusmaksu'])*100/dt
        marg['tyotvakmaksu']=(-q1['tyotvakmaksu']+q2['tyotvakmaksu']-q1['puoliso_tyotvakmaksu']+q2['puoliso_tyotvakmaksu'])*100/dt
        marg['puoliso_verot']=(-q1['puoliso_verot']+q2['puoliso_verot'])*100/dt
        marg['perustulo']=(-q2['perustulo_netto']+q1['perustulo_netto']-q2['puoliso_perustulo_netto']+q1['puoliso_perustulo_netto'])*100/dt
    
        marg['sivukulut']=marg['tyotvakmaksu']+marg['sairausvakuutusmaksu']+marg['ptel'] # sisältyvät jo veroihin
        marg['etuudet']=marg['ansiopvraha']+marg['asumistuki']+marg['toimeentulotuki']+marg['kotihoidontuki']
        marg['verot']=marg['palkkaverot'] # sisältää sivukulut
        marg['ansioverot']=marg['palkkaverot']+marg['elake'] # sisältää sivukulut
        marg['marginaali']=marg['pvhoito']+marg['etuudet']+marg['verot']+marg['elake']
    
        # ja käteen jää
        tulot={}
        tulot['kateen1']=q1['kateen']
        tulot['kateen2']=q2['kateen']
    
        if 'omattulot_netto' in q1: # v1
            omattulotnetto1=q1['omattulot_netto'] # ilman etuuksia
            omattulotnetto2=q2['omattulot_netto'] # ilman etuuksia
            puolisontulotnetto1=q1['puoliso_tulot_netto'] # ilman etuuksia
            puolisontulotnetto2=q2['puoliso_tulot_netto'] # ilman etuuksia
        else:
            omattulotnetto1=q1['omat_netto'] # ilman etuuksia
            omattulotnetto2=q2['omat_netto'] # ilman etuuksia
            puolisontulotnetto1=q1['puoliso_netto'] # ilman etuuksia
            puolisontulotnetto2=q2['puoliso_netto'] # ilman etuuksia

        if laske_tyollistymisveroaste>0:
            tulot['tulotnetto']=omattulotnetto2+puolisontulotnetto2
            #tulot['puolisotulotnetto']=puolisontulotnetto2
            #tulot['omattulotnetto']=omattulotnetto2
        else:
            tulot['tulotnetto']=omattulotnetto1+puolisontulotnetto1
            #tulot['puolisotulotnetto']=puolisontulotnetto1
            #tulot['omattulotnetto']=omattulotnetto1
            
        marg['marginaaliveroprosentti']=100-(tulot['kateen2']-tulot['kateen1'])*100/dt 
    
        return tulot,marg
    
    def laske_ja_plottaa(self,p=None,p0=None,min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,
            figname=None,grayscale=None,source='Lähde: EK',header=True):
            
        netto,eff,tva,osa_tva=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,
                                                max_salary=max_salary,step_salary=step_salary,dt=dt)
                
        if header:
            head_text=tee_selite(p,short=True)
        else:
            head_text=None
                
        if plottaa:
            self.plot_insentives(netto,eff,tva,osa_tva,min_salary=min_salary,max_salary=max_salary+1,
                step_salary=step_salary,
                basenetto=basenetto,baseeff=baseeff,basetva=basetva,baseosatva=baseosatva,
                dt=dt,otsikko=otsikko,otsikkobase=otsikkobase,selite=selite,
                plot_tva=plot_tva,plot_eff=plot_eff,plot_netto=plot_netto,plot_osaeff=plot_osaeff,
                figname=figname,grayscale=grayscale,source=source,header=head_text)
        
        return netto,eff,tva,osa_tva

    def get_palette_EK(self):
        colors1=['#003326','#05283d','#ff9d6a','#599956']
        colors2=['#295247','#2c495a','#fdaf89','#7cae79']
        colors3=['#88b2eb','#ffcb21','#e85c03']
        
        colors=['#295247','#7cae79','#ffcb21','#e85c03','#88b2eb','#2c495a','#fdaf89']
        
        return sns.color_palette(colors)
        
    def get_style_EK(self):
        axes={'axes.facecolor': 'white',
         'axes.edgecolor': 'black',
         'axes.grid': False,
         'axes.axisbelow': 'line',
         'axes.labelcolor': 'black',
         'figure.facecolor': 'white',
         'grid.color': '#b0b0b0',
         'grid.linestyle': '-',
         'text.color': 'black',
         'xtick.color': 'black',
         'ytick.color': 'black',
         'xtick.direction': 'out',
         'ytick.direction': 'out',
         'lines.solid_capstyle': 'projecting',
         'patch.edgecolor': 'black',
         'patch.force_edgecolor': False,
         'image.cmap': 'viridis',
         'font.family': ['sans-serif'],
         'font.sans-serif': ['IBM Plex Sans',
          'DejaVu Sans',
          'Bitstream Vera Sans',
          'Computer Modern Sans Serif',
          'Lucida Grande',
          'Verdana',
          'Geneva',
          'Lucid',
          'Arial',
          'Helvetica',
          'Avant Garde',
          'sans-serif'],
         'xtick.bottom': True,
         'xtick.top': False,
         'ytick.left': True,
         'ytick.right': False,
         'axes.spines.left': False,
         'axes.spines.bottom': True,
         'axes.spines.right': False,
         'axes.spines.top': False}
         
        return axes
        
    def laske_ja_selita(self,p=None,p0=None,min_salary=0,max_salary=3000,step_salary=1500,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,
            figname=None,grayscale=None,source='Lähde: EK',header=True):
            
        head_text=tee_selite(p,short=False)

        if p0 is None:
            netto,eff,tva,osa_tva=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,
                                                    max_salary=max_salary,step_salary=step_salary,dt=dt)
                
            tyottomana_base=basenetto[0]
            tyottomana_vaihtoehto=netto[0]
            tyottomana_ero=tyottomana_vaihtoehto-tyottomana_base
            tyossa_base=basenetto[2]
            tyossa_vaihtoehto=netto[2]
            tyossa_ero=tyossa_vaihtoehto-tyossa_base
            osatyossa_base=basenetto[1]
            osatyossa_vaihtoehto=netto[1]
            osatyossa_ero=osatyossa_vaihtoehto-osatyossa_base
        else:
            netto,eff,tva,osa_tva,basenetto=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,
                                                    max_salary=max_salary,step_salary=step_salary,dt=dt)
            tyottomana_base=basenetto[0]
            tyottomana_vaihtoehto=netto[0]
            tyottomana_ero=tyottomana_vaihtoehto-tyottomana_base
            tyossa_base=basenetto[2]
            tyossa_vaihtoehto=netto[2]
            tyossa_ero=tyossa_vaihtoehto-tyossa_base
            osatyossa_base=basenetto[1]
            osatyossa_vaihtoehto=netto[1]
            osatyossa_ero=osatyossa_vaihtoehto-osatyossa_base
        

        if header:
            print(head_text)
        print(f'Nettotulot työttömänä {tyottomana_vaihtoehto:.2f} perus {tyottomana_base:.2f}  ero {tyottomana_ero:.2f}')
        print(f'Nettotulot työssä (palkka {max_salary:.2f} e/kk) {tyossa_vaihtoehto:.2f} perus {tyossa_base:.2f}  ero {tyossa_ero:.2f} tva {tva[2]:.3f}%')
        print(f'Nettotulot 50% osa-aikatyössä (palkka {max_salary/2:.2f} e/k) {osatyossa_vaihtoehto:.2f} perus {osatyossa_base:.2f} ero {osatyossa_ero:.2f}  tva {tva[1]:.3f}%')
        
        return netto,eff,tva,osa_tva

        
    def plot_insentives(self,netto,eff,tva,osa_tva,
            min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=False,
            figname=None,grayscale=False,source=None,header=None):
            
        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            reverse=True
        else:
            pal=sns.color_palette()            
            
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
            axs.set_ylabel(self.labels['net income'])
            axs.grid(False)
            axs.set_xlim(0, max_salary)
            if source is not None:
                self.add_source(source)
            
            if header is not None:
                axs.title.set_text(header)
                
            if figname is not None:
                plt.savefig(figname+'_netto.eps', format='eps')
                plt.savefig(figname+'_netto.png', format='png',dpi=300)
                
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
            if source is not None:
                self.add_source(source)
            
            if header is not None:
                axs.title.set_text(header)
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
            if source is not None:
                self.add_source(source)
            
            if header is not None:
                axs.title.set_text(header)
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
            axs.set_ylabel('Osatyöstä kokotyöhön siirtymisen eff.rajavero (%)')
            axs.grid(True)
            axs.set_xlim(0, max_salary)
            if source is not None:
                self.add_source(source)
            if header is not None:
                axs.title.set_text(header)
            if figname is not None:
                plt.savefig(figname+'_osatva.eps', format='eps')
            plt.show()    
        
    def comp_insentives(self,p=None,p0=None,min_salary=0,max_salary=6000,step_salary=1,dt=100):
    
        n_salary=int((max_salary+step_salary-min_salary)/step_salary)
        netto=np.zeros(n_salary)
        basenetto=np.zeros(n_salary)
        palkka=np.zeros(n_salary)
        tva=np.zeros(n_salary)
        osa_tva=np.zeros(n_salary)
        eff=np.zeros(n_salary)
        
        if p is None:
            p,selite=self.get_default_parameter()

        if p0 is None:
            p2b=p.copy()
        else:
            p2b=p0.copy()
        
        p3=p.copy()
            
        n0,q0=self.laske_tulot(p2b)
        basenetto[0]
        k=0
        for t in np.arange(min_salary,max_salary+step_salary,step_salary):
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
            p2b['t']=t # palkka
            basenetto[k],_=self.laske_tulot(p2b)

            k=k+1
            
        if p0 is not None:
            return netto,eff,tva,osa_tva,basenetto
        else:
            return netto,eff,tva,osa_tva
        
    def comp_taxes(self,p=None,p2=None,min_salary=0,max_salary=6000,step_salary=1,dt=100):
        n_salary=int((max_salary+step_salary-min_salary)/step_salary)+1
        netto=np.zeros(n_salary)
        palkka=np.zeros(n_salary)
        taxes=np.zeros(n_salary)
        contributions=np.zeros(n_salary)
        eff=np.zeros(n_salary)
        
        if p is None:
            p,selite=self.get_default_parameter()

        if p2 is None:
            p2=p.copy()
            p2['t']=0 # palkka
        p3=p.copy()
        n0,q0=self.laske_tulot(p2)
        k=0
        wages=np.arange(min_salary,max_salary+step_salary,step_salary)
        for t in wages:
            p3['t']=t # palkka
            n1,q1=self.laske_tulot(p3)
            p3['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p3)
            netto[k]=n1
            palkka[k]=t
            eff[k]=(1-(n2-n1)/dt)*100
            taxes[k]=q1['verot']
            
            #print(f"{t:.2f},{q1['verot']:.2f},{q1['valtionvero']:.2f},{q1['kunnallisvero']:.2f}")
            #print(f"sv:{q1['ptel']:.2f},{q1['sairausvakuutusmaksu']:.2f},{q1['tyotvakmaksu']:.2f},{q1['tyel_kokomaksu']:.2f},{q1['ylevero']}")
            #print(f"vä:{q1['ansiotulovahennys']:.2f},{q1['perusvahennys']:.2f},{q1['tyotulovahennys']:.2f},{q1['tyotulovahennys_kunnallisveroon']}")
            #print(f"pe:{t:.2f},{q1['kunnallisveronperuste']:.2f},{q1['valtionveroperuste']:.2f}")

            k=k+1
            
        return wages,netto,eff,taxes
        
    def comp_top_marginaali(self,p=None):
    
        if p==None:
            p,selite=perheparametrit(perhetyyppi=1)
        salary=150_000/12.5
        n,eff,_,_=self.comp_insentives(p=p,min_salary=salary,max_salary=salary+1,step_salary=1,dt=100)
        #print(n,eff)
        
        return eff[0]
        
    def laske_ja_plottaa_marginaalit(self,p=None,p2=None,min_salary=0,max_salary=6000,
                basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,
                otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=True,ret=False,
                plot_tva=True,plot_eff=True,plot_netto=True,figname=None,grayscale=False,
                incl_perustulo=False,incl_elake=True,fig=None,ax=None,incl_opintotuki=False,
                incl_alv=False,
                plot_kotihoidontuki=False,
                plot_osatva=True,header=True,source='Lähde: EK',palette=None,palette_EK=True,square=False):
        netto=np.zeros(max_salary+1)
        palkka=np.zeros(max_salary+1)
        tva=np.zeros(max_salary+1)
        osatva=np.zeros(max_salary+1)
        eff=np.zeros(max_salary+1)
        asumistuki=np.zeros(max_salary+1)
        toimeentulotuki=np.zeros(max_salary+1)
        ansiopvraha=np.zeros(max_salary+1)
        nettotulot=np.zeros(max_salary+1)
        lapsilisa=np.zeros(max_salary+1)
        elake=np.zeros(max_salary+1)    
        elatustuki=np.zeros(max_salary+1)
        perustulo=np.zeros(max_salary+1)
        opintotuki=np.zeros(max_salary+1)        
        kotihoidontuki=np.zeros(max_salary+1)    
        margasumistuki=np.zeros(max_salary+1)
        margtoimeentulotuki=np.zeros(max_salary+1)
        margansiopvraha=np.zeros(max_salary+1)
        margverot=np.zeros(max_salary+1)    
        margalv=np.zeros(max_salary+1)    
        margelake=np.zeros(max_salary+1)    
        margpvhoito=np.zeros(max_salary+1)        
        margyht=np.zeros(max_salary+1)        
        margyht2=np.zeros(max_salary+1)    
        margperustulo=np.zeros(max_salary+1)    
        margopintotuki=np.zeros(max_salary+1)    
        margkotihoidontuki=np.zeros(max_salary+1)    
        tva_asumistuki=np.zeros(max_salary+1)
        tva_kotihoidontuki=np.zeros(max_salary+1)    
        tva_toimeentulotuki=np.zeros(max_salary+1)
        tva_ansiopvraha=np.zeros(max_salary+1)
        tva_verot=np.zeros(max_salary+1)        
        tva_alv=np.zeros(max_salary+1)    
        tva_elake=np.zeros(max_salary+1)        
        tva_pvhoito=np.zeros(max_salary+1)        
        tva_perustulo=np.zeros(max_salary+1)        
        tva_opintotuki=np.zeros(max_salary+1)        
        tva_yht=np.zeros(max_salary+1)        
        tva_yht2=np.zeros(max_salary+1)        
        osatva_asumistuki=np.zeros(max_salary+1)
        osatva_kotihoidontuki=np.zeros(max_salary+1)    
        osatva_toimeentulotuki=np.zeros(max_salary+1)
        osatva_ansiopvraha=np.zeros(max_salary+1)
        osatva_verot=np.zeros(max_salary+1)        
        osatva_alv=np.zeros(max_salary+1)    
        osatva_elake=np.zeros(max_salary+1)        
        osatva_pvhoito=np.zeros(max_salary+1)        
        osatva_perustulo=np.zeros(max_salary+1)        
        osatva_opintotuki=np.zeros(max_salary+1)        
        osatva_yht=np.zeros(max_salary+1)        
        osatva_yht2=np.zeros(max_salary+1)        
        
        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            plt.grid(b=False)
            reverse=True
        else:
            pal=sns.color_palette()

        if palette is not None:
            pal=sns.color_palette(palette, 12)
            
        if palette_EK:
            pal=self.get_palette_EK()
            #csfont = {'fontname':'Comic Sans MS'}
            fontname='IBM Plex Sans'
            csfont = {'fontname':fontname}
            #fontprop = font_manager.FontProperties(family=fontname,weight='normal',style='normal', size=12)
            custom_params = {"axes.spines.right": False, "axes.spines.top": False, "axes.spines.left": False, 'ytick.left': False}
            sns.set_theme(style="ticks", font=fontname,rc=custom_params)
        else:
            csfont = {}

        if p is None:
            p,selite=self.get_default_parameter()
            
        if header:
            head_text=tee_selite(p,p2=p2,short=False)
        else:
            head_text=None
            
        if p2 is None:
            p1=p.copy()
            p2=p.copy()
            p3=p.copy()
        else:
            p1=p.copy()
            p3=p2.copy()
            plot_eff=False

        p1['t']=0 # palkka
        n0,q0=self.laske_tulot(p1)
        brutto0=q0['brutto']
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1,q1=self.laske_tulot(p2)
            brutto1=q1['brutto']
            p2['t']=t+dt # palkka
            n2,q2=self.laske_tulot(p2)
            deltat=t
            brutto2=q2['brutto']
            p3['t']=t+deltat # palkka
            n3,q3=self.laske_tulot(p3)
            brutto3=q1['brutto']
            
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            d_brutto=brutto2-brutto0
            #tulot2,tvat=self.laske_marginaalit(q0,q1,d_brutto,laske_tyollistymisveroaste=1)
            tulot2,tvat=self.laske_marginaalit(q0,q1,t,laske_tyollistymisveroaste=1)
            tulot3,osatvat=self.laske_marginaalit(q2,q3,deltat)
            netto[t]=n1
            palkka[t]=t
            margasumistuki[t]=marg['asumistuki']
            margtoimeentulotuki[t]=marg['toimeentulotuki']
            margverot[t]=marg['verot']
            margalv[t]=marg['alv']
            margelake[t]=marg['elake']
            margansiopvraha[t]=marg['ansiopvraha']
            margpvhoito[t]=marg['pvhoito']
            margperustulo[t]=marg['perustulo']
            margkotihoidontuki[t]=marg['kotihoidontuki']
            margopintotuki[t]=marg['opintotuki']
            margyht[t]=marg['marginaali']
            margyht2[t]=marg['marginaaliveroprosentti']
            elake[t]=q1['kokoelake_netto']
            asumistuki[t]=q1['asumistuki']
            toimeentulotuki[t]=q1['toimeentulotuki']
            opintotuki[t]=q1['opintotuki']
            ansiopvraha[t]=q1['ansiopvraha_nettonetto']+q1['puoliso_ansiopvraha_nettonetto']
            lapsilisa[t]=q1['lapsilisa']
            perustulo[t]=q1['perustulo_nettonetto']+q1['puoliso_perustulo_nettonetto']
            elatustuki[t]=q1['elatustuki']
            nettotulot[t]=tulot['tulotnetto']
            kotihoidontuki[t]=q1['kotihoidontuki_netto']
            tva_asumistuki[t]=tvat['asumistuki']
            tva_kotihoidontuki[t]=tvat['kotihoidontuki']
            tva_toimeentulotuki[t]=tvat['toimeentulotuki']
            tva_verot[t]=tvat['verot']
            tva_alv[t]=tvat['alv']
            tva_elake[t]=tvat['elake']
            tva_perustulo[t]=tvat['perustulo']
            tva_ansiopvraha[t]=tvat['ansiopvraha']
            tva_opintotuki[t]=tvat['opintotuki']
            tva_pvhoito[t]=tvat['pvhoito']
            tva_yht[t]=tvat['marginaali']
            tva_yht2[t]=tvat['marginaaliveroprosentti']
            osatva_asumistuki[t]=osatvat['asumistuki']
            osatva_kotihoidontuki[t]=osatvat['kotihoidontuki']
            osatva_toimeentulotuki[t]=osatvat['toimeentulotuki']
            osatva_verot[t]=osatvat['verot']
            osatva_alv[t]=osatvat['alv']
            osatva_elake[t]=osatvat['elake']
            osatva_perustulo[t]=osatvat['perustulo']
            osatva_ansiopvraha[t]=osatvat['ansiopvraha']
            osatva_opintotuki[t]=osatvat['opintotuki']
            osatva_pvhoito[t]=osatvat['pvhoito']
            osatva_yht[t]=osatvat['marginaali']
            osatva_yht2[t]=osatvat['marginaaliveroprosentti']

            eff[t]=(1-(n2-n1)/dt)*100
            if t>0:
                tva[t]=(1-(n1-n0)/t)*100
            else:
                tva[t]=0
                
            if deltat>0:
                osatva[t]=(1-(n3-n1)/deltat)*100
            else:
                osatva[t]=0
                
        if plot_eff and plottaa:
            if fig is None:
                figi,axs = plt.subplots()
            else:
                figi=fig
                axs=ax
            #sns.set_theme()
            axs.set_axisbelow(False)
            if incl_perustulo:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo'],self.labels['alv']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['alv']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margopintotuki,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['opintotuki'],self.labels['alv']),
                        colors=pal)
                elif plot_kotihoidontuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margpvhoito,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['paivahoito'],self.labels['alv']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,#margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito']),#self.labels['alv']),
                        colors=pal)
                        
            axs.set_xlabel(self.labels['wage'],)
            axs.set_ylabel(self.labels['effective'])
            plt.yticks(**csfont)
            plt.xticks(**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(min_salary, max_salary)
            axs.set_ylim(0, 120)
            if legend:
                #axs.legend(loc='upper right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
            if source is not None:
                self.add_source(source)
            if header is not None:
                axs.title.set_text(head_text)
                
            if figname is not None:
                plt.savefig(figname+'_eff.png')
            plt.show()
        
        if plot_netto and plottaa:
            if fig is None:
                figi,axs = plt.subplots()
            else:
                figi=fig
                axs=ax
            #sns.set_theme(**csfont)
            axs.set_axisbelow(False)
            if incl_perustulo:
                axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elake,opintotuki,elatustuki,kotihoidontuki,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['kotihoidontuki']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,opintotuki,elatustuki,kotihoidontuki,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['opintotuki'],self.labels['elatustuki'],self.labels['kotihoidontuki']),
                        colors=pal)
                elif plot_kotihoidontuki:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,lapsilisa,elatustuki,kotihoidontuki,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],'Lapsilisä',self.labels['elatustuki'],self.labels['kotihoidontuki']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elatustuki,kotihoidontuki,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elatustuki'],self.labels['kotihoidontuki']),
                        colors=pal)
            
            axs.plot(netto)
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel(self.labels['net income'])
            plt.yticks(**csfont)
            plt.xticks(**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_facecolor('white')
            axs.set_xlim(min_salary, max_salary)
            if legend:        
                #axs.legend(loc='lower right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='lower right')
            if source is not None:
                self.add_source(source)
            if header is not None:
                axs.title.set_text(head_text)
                
            if figname is not None:
                plt.savefig(figname+'_netto.png')
            plt.show()

        if plot_tva and plottaa:
            if fig is None:
                figi,axs = plt.subplots()
            else:
                figi=fig
                axs=ax
            #sns.set_theme(**csfont)
            axs.set_axisbelow(False)
            if incl_perustulo:
                axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_kotihoidontuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['kotihoidontuki']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_opintotuki,tva_kotihoidontuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['opintotuki'],self.labels['kotihoidontuki']),
                        colors=pal)
                elif plot_kotihoidontuki:
                    axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_pvhoito,tva_kotihoidontuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['paivahoito'],self.labels['kotihoidontuki']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,#tva_kotihoidontuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito']),#self.labels['kotihoidontuki']),
                        colors=pal)

            #axs.plot(tva,label='Vaihtoehto')
            #axs.plot(tva_yht,label='Vaihtoehto2')
            #axs.plot(tva_yht2,label='Vaihtoehto3')
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel('Työllistymisveroaste (%)')
            plt.yticks(**csfont)
            plt.xticks(**csfont)
            axs.grid(False)#,color='lightgray',fillstyle='top')
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_facecolor('white')
            axs.set_xlim(min_salary, max_salary)
            axs.set_ylim(0, 120)
            if legend:
                #axs.legend(loc='upper right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
            if source is not None:
                self.add_source(source)
            if header is not None:
                axs.title.set_text(head_text)
                
            if figname is not None:
                plt.savefig(figname+'_tva.png',dpi=200)
            plt.show()
            
        if plot_osatva and plottaa:
            if fig is None:
                figi,axs = plt.subplots()
            else:
                figi=fig
                axs=ax
            #sns.set_theme(**csfont)
            axs.set_axisbelow(False)
            if incl_perustulo:
                axs.stackplot(palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_pvhoito,osatva_opintotuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['opintotuki']),
                        colors=pal)
                elif plot_kotihoidontuki:
                    axs.stackplot(palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_pvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['paivahoito']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_pvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito']),
                        colors=pal)

            #axs.plot(tva,label='Vaihtoehto')
            #axs.plot(tva_yht,label='Vaihtoehto2')
            #axs.plot(tva_yht2,label='Vaihtoehto3')
            axs.set_xlabel(self.labels['parttimewage'])
            axs.set_ylabel('Eff. rajaveroaste osa-aikatyöstä kokoaikatyöhön (%)')
            plt.yticks(**csfont)
            plt.xticks(**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_facecolor('white')
            axs.set_xlim(min_salary, max_salary)
            axs.set_ylim(0, 100)
            if legend:
                #axs.legend(loc='upper right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
            if source is not None:
                self.add_source(source)
            if header is not None:
                axs.title.set_text(head_text)
                
            if figname is not None:
                plt.savefig(figname+'_osatva.png',dpi=200)
            if fig is None:
                plt.show()            
               
        if ret: 
            return netto,eff,tva,osatva
            
    def add_source(self,source):
        plt.annotate(source, xy=(0.88,-0.1), xytext=(0,0), fontsize=12, xycoords='axes fraction', textcoords='offset points', va='top')

    def laske_ja_plottaa_veromarginaalit(self,p=None,min_salary=0,max_salary=6000,basenetto=None,baseeff=None,
            basetva=None,dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",selite=True):
        palkka=np.zeros(max_salary+1)
        margtyotvakmaksu=np.zeros(max_salary+1)        
        margsairausvakuutusmaksu=np.zeros(max_salary+1)
        margptel=np.zeros(max_salary+1)
        margtyotulovah=np.zeros(max_salary+1)
        margansiotulovah=np.zeros(max_salary+1)        
        margverot=np.zeros(max_salary+1)        
        margkunnallisvero=np.zeros(max_salary+1)        
        margvaltionvero=np.zeros(max_salary+1)  
        margperusvahennys=np.zeros(max_salary+1)  
        margpuolisonverot=np.zeros(max_salary+1)  
        tyotvakmaksu=np.zeros(max_salary+1)        
        sairausvakuutusmaksu=np.zeros(max_salary+1)
        ptel=np.zeros(max_salary+1)
        tyotulovah=np.zeros(max_salary+1)
        ansiotulovah=np.zeros(max_salary+1)        
        verot=np.zeros(max_salary+1)        
        kunnallisvero=np.zeros(max_salary+1)        
        valtionvero=np.zeros(max_salary+1)  
        perusvahennys=np.zeros(max_salary+1)  
        puolisonverot=np.zeros(max_salary+1)  
        brutto=np.zeros(max_salary+1)  
        
        if p is None:
            p,selite=self.get_default_parameter()
            
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
            margsairausvakuutusmaksu[t]=marg['sairausvakuutusmaksu']
            margtyotvakmaksu[t]=marg['tyotvakmaksu']
            margpuolisonverot[t]=marg['puoliso_verot']
            tyotvakmaksu[t]=q1['tyotvakmaksu']
            sairausvakuutusmaksu[t]=q1['sairausvakuutusmaksu']
            ptel[t]=q1['ptel']
            kunnallisvero[t]=q1['kunnallisvero']
            valtionvero[t]=q1['valtionvero']
            puolisonverot[t]=0 #q1['puolisoverot']
            brutto[t]=q1['bruttotulot']
                            
        fig,axs = plt.subplots()
        axs.stackplot(palkka,margvaltionvero,margkunnallisvero,margptel,margsairausvakuutusmaksu,margtyotvakmaksu,margpuolisonverot,
            #labels=('Valtionvero','Kunnallisvero','PTEL','sairausvakuutusmaksu','työttömyysvakuutusmaksu','puolison verot'))
            labels=('State tax','Municipal tax','Employee pension premium','sairausvakuutusmaksu','työttömyysvakuutusmaksu','puolison verot'))
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
        axs.stackplot(palkka,tyotvakmaksu,sairausvakuutusmaksu,ptel,kunnallisvero,valtionvero,puolisonverot,
            labels=('tyotvakmaksu','sairausvakuutusmaksu','ptel','kunnallisvero','valtionvero','puolisonverot'))
        #axs.plot(netto)
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel('Verot yhteensä (e/kk)')
        axs.grid(True)
        axs.set_xlim(0, max_salary)
        if selite:        
            axs.legend(loc='lower right')
        plt.show()

    def laske_ja_plottaa_hila(self,min_salary=0,max_salary=6000,type='eff',dt=100,maxn=None,dire=None,grayscale=False):
        if maxn is None:
            maxn=36
        fig,axs = plt.subplots(int(maxn/5),5,sharex=True,sharey=True)
        for k in range(1,maxn):
            x=(k-1) % 5
            y=int(np.floor((k-1)/5))
            #ax=plt.subplot(10,3,k)
            p,_=perheparametrit(k)
            self.lp_marginaalit_apu(axs[y,x],otsikko='Tapaus '+str(k),p=p,min_salary=min_salary,
                max_salary=max_salary,type=type,dt=dt,grayscale=grayscale)

        if dire is not None:
            fig.savefig(dire+'multiple_'+type+'.eps',bbox_inches='tight')
            fig.savefig(dire+'multiple_'+type+'.png',bbox_inches='tight')

        plt.show()

    def lp_marginaalit_apu(self,axs,otsikko='',p=None,min_salary=0,max_salary=6000,type='eff',dt=100,selite=False,
                            include_perustulo=False,include_opintotuki=False,include_elake=False,grayscale=False):
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
        opintotuki=np.zeros(max_salary+1)
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
        
        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            reverse=True
        else:
            pal=sns.color_palette()            
            
        if p is None:
            p,selite=self.get_default_parameter()
            
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
            margtoimeentulotuki[t]=marg['toimeentulotuki']
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
            toimeentulotuki[t]=q1['toimeentulotuki']
            ansiopvraha[t]=q1['ansiopvraha_nettonetto']+q1['puoliso_ansiopvraha_nettonetto']
            lapsilisa[t]=q1['lapsilisa']
            opintotuki[t]=q1['opintotuki']
            elatustuki[t]=q1['elatustuki']
            nettotulot[t]=tulot['tulotnetto']
            if type=='tva':
                tulot2,tvat=self.laske_marginaalit(q0,q1,t,laske_tyollistymisveroaste=1)
                tva_asumistuki[t]=tvat['asumistuki']
                tva_perustulo[t]=tvat['perustulo']
                tva_toimeentulotuki[t]=tvat['toimeentulotuki']
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
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['perustulo']))
            else:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake']))
            
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
                axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,tva_perustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['perustulo']))
            else:
                axs.stackplot(palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake']))
            
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
                axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),
                    colors=pal)
            else:
                if include_elake:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elake,opintotuki,elatustuki,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki']),
                        colors=pal)
                elif include_opintotuki:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,opintotuki,elatustuki,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['opintotuki'],self.labels['elatustuki']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,nettotulot,asumistuki,toimeentulotuki,ansiopvraha,lapsilisa,elatustuki,
                        labels=('Nettopalkka',self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],'Lapsilisä',self.labels['elatustuki']),
                        colors=pal)
#         
#             if include_perustulo:
#                 axs.stackplot(palkka,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,elake,opintotuki,perustulo,
#                     labels=(self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['pure wage'],'Lapsilisä',self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo']))
#             else:
#                 axs.stackplot(palkka,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,elake,opintotuki,
#                     labels=(self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['pure wage'],'Lapsilisä',self.labels['elake'],self.labels['opintotuki']))
                            
            axs.plot(netto)
            axs.title.set_text(otsikko)
            axs.set_xlabel(self.labels['wage'])
            axs.set_ylabel(self.labels['net income'])
            
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
            self.raippavero=self.raippavero2019
            self.laske_ylevero=self.laske_ylevero2019
            self.elaketulovahennys=self.elaketulovahennys2019
            self.tyotulovahennys=self.tyotulovahennys2019
            self.ansiotulovahennys=self.ansiotulovahennys2019
            self.perusvahennys=self.perusvahennys2019
            self.lapsilisa=self.lapsilisa2019
            self.asumistuki=self.asumistuki2019
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2019
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
            self.raippavero=self.raippavero2020
            self.laske_ylevero=self.laske_ylevero2020
            self.elaketulovahennys=self.elaketulovahennys2020
            self.tyotulovahennys=self.tyotulovahennys2020
            self.perusvahennys=self.perusvahennys2020
            self.ansiotulovahennys=self.ansiotulovahennys2020
            self.veroparam=self.veroparam2020
            self.lapsilisa=self.lapsilisa2020
            self.asumistuki=self.asumistuki2020
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2020
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
            self.raippavero=self.raippavero2021
            self.laske_ylevero=self.laske_ylevero2021
            self.elaketulovahennys=self.elaketulovahennys2021
            self.tyotulovahennys=self.tyotulovahennys2021
            self.perusvahennys=self.perusvahennys2021
            self.ansiotulovahennys=self.ansiotulovahennys2021
            self.veroparam=self.veroparam2021
            self.lapsilisa=self.lapsilisa2021
            self.asumistuki=self.asumistuki2021
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2021
            self.kotihoidontuki=self.kotihoidontuki2021
            self.paivahoitomenot=self.paivahoitomenot2021
            self.sairauspaivaraha=self.sairauspaivaraha2021
            self.toimeentulotuki_param=self.toimeentulotuki_param2021
        elif vuosi==2022:
            self.laske_kansanelake=self.laske_kansanelake2022
            self.laske_takuuelake=self.laske_takuuelake2022
            self.aitiysraha=self.aitiysraha2022
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2022
            self.valtionvero_asteikko=self.valtionvero_asteikko_2022
            self.raippavero=self.raippavero2022
            self.laske_ylevero=self.laske_ylevero2022
            self.elaketulovahennys=self.elaketulovahennys2022
            self.tyotulovahennys=self.tyotulovahennys2022
            self.perusvahennys=self.perusvahennys2022
            self.ansiotulovahennys=self.ansiotulovahennys2022
            self.veroparam=self.veroparam2022
            self.lapsilisa=self.lapsilisa2022
            self.asumistuki=self.asumistuki2022
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2022
            self.kotihoidontuki=self.kotihoidontuki2022
            self.paivahoitomenot=self.paivahoitomenot2022
            self.sairauspaivaraha=self.sairauspaivaraha2022
            self.toimeentulotuki_param=self.toimeentulotuki_param2022
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
            self.raippavero=self.raippavero2018
            self.laske_ylevero=self.laske_ylevero2018
            self.lapsilisa=self.lapsilisa2018
            self.asumistuki=self.asumistuki2018
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2018
            self.kotihoidontuki=self.kotihoidontuki2018
            self.paivahoitomenot=self.paivahoitomenot2018
            self.sairauspaivaraha=self.sairauspaivaraha2018
            self.toimeentulotuki_param=self.toimeentulotuki_param2018            
        else:
            print('Vuoden {v} aineisto puuttuu'.format(v=vuosi))
            
        self.sotumaksu=self.laske_sotumaksu(vuosi)

            
    def get_tyelpremium(self):
        tyel_kokomaksu=np.zeros((2100,5))
        # data
        self.data_tyel_kokomaksu[1962:2022]=[5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.15,5.15,5.65,6.1,6.4,6.9,7.9,9.9,12.0,10.0,11.7,13.3,13.3,12.4,11.1,11.1,11.5,12.2,13.0,13.8,14.9,16.9,16.9,14.4,18.5,18.6,20.6,21.1,21.2,21.5,21.5,21.5,21.1,21.1,21.4,21.4,21.6,21.2,21.1,21.1,21.3,21.6,22.1,22.8,22.8,23.6,24.0,24.0,24.4,24.4,24.4,24.4,24.4,24.4]
        # ETK
        self.data_tyel_kokomaksu[2023:2085]=np.array([24.4,24.5,24.5,24.6,24.6,24.7,24.8,24.8,24.9,24.9,25.0,24.9,24.9,24.9,24.9,24.8,24.8,24.7,24.7,24.6,24.6,24.6,24.6,24.6,24.7,24.8,24.8,24.9,25.1,25.2,25.4,25.6,25.8,26.0,26.2,26.5,26.7,27.0,27.2,27.5,27.7,27.9,28.1,28.3,28.5,28.7,28.9,29.1,29.2,29.4,29.5,29.7,29.8,29.9,30.1,30.2,30.3,30.3,30.4,30.4,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5])/100
        self.data_ptel=0.5*(self.data_tyel_kokomaksu-self.data_tyel_kokomaksu[2017])+0.0615 # vuonna 2017 ptel oli 6,15 %
        self.data_ptel[1962:1993]=0
        
        return tyel_kokomaksu
