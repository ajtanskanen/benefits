"""

    benefits
    
    implements social security benefits and taxation in the Finnish social security schemes


"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite
from .labels import Labels
from .ben_utils import print_q, compare_q_print
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager

class Benefits():
    """
    Description:
        The Finnish Earnings-related Social Security

    Source:
        Antti J. Tanskanen

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
        self.include_kirkollisvero=False
        self.include_joustavahoitoraha=False
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
            elif key=='include_kirkollisvero': # language for plotting
                if value is not None:
                    self.include_kirkollisvero=value
            elif key=='include_joustavahoitoraha': # language for plotting
                if value is not None:
                    self.include_joustavahoitoraha=value
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
        
    def explain(self,p: dict =None):
        if p is None:
            print('Ei parametrejä')
        else:
            print(tee_selite(p))
            
    def laske_vaihtuva_tyoelakemaksu(self,ika: int):
        vuosi=int(self.floor(self.tyel_perusvuosi+ika)) # alkuvuonna 18
        
        # prosenttia palkoista, vuodesta 2017 alkaen, jatkettu päätepisteen tasolla vuoden 2085 jälkeen
        self.tyontekijan_maksu=self.data_ptel[vuosi]
        if vuosi<2017:
            self.tyontekijan_maksu_52=self.tyontekijan_maksu*19/15
        else:
            self.tyontekijan_maksu_52=self.tyontekijan_maksu+0.015
            
        self.koko_tyel_maksu=self.data_tyel_kokomaksu[vuosi]
        self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu
    
    def toimeentulotuki_param2018(self) -> (float,float,float,float,float,float,float,float,float):
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=305.87     # e/kk     alle 10v lapsi
        lapsi2=281.59     # e/kk
        lapsi3=257.32     # e/kk
        yksinhuoltaja=534.05     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=412.68    
        yksinasuva=485.50
        # Helsinki: 694 869 993 1089
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])*1948/2017
        max_lisa=np.array([122, 99, 96, 96])*1948/2017
        
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa
    
    def toimeentulotuki_param2019(self) -> (float,float,float,float,float,float,float,float,float):
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=313.29     # e/kk     alle 10v lapsi
        lapsi2=288.43     # e/kk
        lapsi3=263.56     # e/kk
        yksinhuoltaja=547.02     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=422.70    
        yksinasuva=497.29
        # Helsinki: 694 869 993 1089
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])*1968/2017
        max_lisa=np.array([122, 99, 96, 96])*1968/2017
        
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa

    def toimeentulotuki_param2020(self) -> (float,float,float,float,float,float,float,float,float):
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=317.56     # e/kk     alle 10v lapsi
        lapsi2=292.35     # e/kk
        lapsi3=267.15     # e/kk
        yksinhuoltaja=572.52     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=412.68    
        yksinasuva=502.21
        # Helsinki: 694 869 993 1089
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])*1974/2017
        max_lisa=np.array([122, 99, 96, 96])*1974/2017
        
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa
        
    def toimeentulotuki_param2021(self) -> (float,float,float,float,float,float,float,float,float):
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=317.56     # e/kk     alle 10v lapsi
        lapsi2=292.35     # e/kk
        lapsi3=267.15     # e/kk
        yksinhuoltaja=574.63     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=428.45
        yksinasuva=504.16
        # Helsinki: 694 869 993 1089 122
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])
        max_lisa=np.array([122, 99, 96, 96])
        
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa
        
    def toimeentulotuki_param2022(self) -> (float,float,float,float,float,float,float,float,float):
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=324.34     # e/kk     alle 10v lapsi
        lapsi2=298.60     # e/kk
        lapsi3=272.85     # e/kk
        yksinhuoltaja=586.89     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=437.60
        yksinasuva=514.82
        # Helsinki: 694 869 993 1089
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])
        max_lisa=np.array([122, 99, 96, 96])
        
        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa

    def toimeentulotuki_param2023(self) -> (float,float,float,float,float,float,float,float,float):
        '''
        Päivitä
        '''
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=383.03     # e/kk     alle 10v lapsi
        lapsi2=355.27     # e/kk
        lapsi3=327.51     # e/kk
        yksinhuoltaja=632.83     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=471.84
        yksinasuva=555.11
        # Helsinki: 694 869 993 1089 122
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])
        max_lisa=np.array([122, 99, 96, 96])

        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa
        
    def toimeentulotuki_param2024(self) -> (float,float,float,float,float,float,float,float,float):
        '''
        Päivitä
        '''
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=383.03     # e/kk     alle 10v lapsi
        lapsi2=355.27     # e/kk
        lapsi3=327.51     # e/kk
        yksinhuoltaja=669.99     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=499.55
        yksinasuva=587.71
        # Helsinki: 694 869 993 1089 122
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[715, 507, 418, 363],[895, 652, 574, 463],[1023, 784, 709, 596],[1122, 793, 746, 617]])
        max_lisa=np.array([122, 99, 96, 96])

        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa  

    def toimeentulotuki_param2025(self) -> (float,float,float,float,float,float,float,float,float):
        '''
        Päivitä
        '''
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        lapsi1=383.03     # e/kk     alle 10v lapsi
        lapsi2=355.27     # e/kk
        lapsi3=327.51     # e/kk
        yksinhuoltaja=669.99     # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot 412,68
        muu=499.55
        yksinasuva=587.71
        # Helsinki: 694 869 993 1089 122
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[715, 507, 418, 363],[895, 652, 574, 463],[1023, 784, 709, 596],[1122, 793, 746, 617]])
        max_lisa=np.array([122, 99, 96, 96])

        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa           

    def laske_paivarahamaksu(self,peruste: float,ika: float):
        if peruste>self.paivarahamaksu_raja and ika<68:
            paivarahamaksu = peruste*self.paivarahamaksu_pros
        else:
            paivarahamaksu=0        
        return paivarahamaksu

    def setup_tmtuki_param(self,vuosi: int):
        if vuosi==2018:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2019:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2020:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2021:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2022:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2023:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2024:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2025:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2026:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        elif vuosi==2027:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        else:
            self.tmtuki_suojaosa_perheellinen=800
            self.tmtuki_puoliso_suojaosa=560
            self.tmtuki_lisa=106
            self.tmtuki_suojaosa_yksin=211
        
    def toimeentulotuki(self,omabruttopalkka: float,omapalkkavero: float,puolison_bruttopalkka: float,puolison_palkkavero: float,
                             muuttulot: float,verot: float,asumismenot: float,muutmenot: float,aikuisia: int, lapsia: int,kuntaryhma: int,
                             p: dict,omavastuuprosentti: float=0.0,alennus: int=0):

        min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_asumislisa=self.toimeentulotuki_param()
        max_asumismeno=max_asumismenot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_asumislisa[kuntaryhma]

        asumismenot = min(asumismenot,max_asumismeno)
        if omavastuuprosentti is None:
            omavastuuprosentti = self.toimeentulotuki_omavastuuprosentti
            
        omavastuu=omavastuuprosentti*asumismenot
        menot=max(0,asumismenot-omavastuu)+muutmenot
        
        #menot=asumismenot+muutmenot    
        bruttopalkka=omabruttopalkka+puolison_bruttopalkka    
        palkkavero=omapalkkavero+puolison_palkkavero    
        palkkatulot=bruttopalkka-palkkavero    
        
        if True: # lain mukainen tiukka tulkinta
            omaetuoikeutettuosa=min(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
            puolison_etuoikeutettuosa=min(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
        else: # Kelan tulkinta: aina 150e
            if False:
                omaetuoikeutettuosa=min_etuoikeutettuosa
                puolison_etuoikeutettuosa=min_etuoikeutettuosa
            else: # kokeilu
                omaetuoikeutettuosa=min(min_etuoikeutettuosa,0.35*omabruttopalkka)
                puolison_etuoikeutettuosa=min(min_etuoikeutettuosa,0.35*omabruttopalkka)
            
        etuoikeutettuosa=omaetuoikeutettuosa+puolison_etuoikeutettuosa    

        if aikuisia<2:
            if lapsia<1: 
                tuki1=yksinasuva     # yksinasuva 485,50
            elif lapsia==1:
                tuki1=yksinhuoltaja+lapsi1     # yksinhuoltaja 534,05
            elif lapsia==2:
                tuki1=yksinhuoltaja+lapsi1+lapsi2     # yksinhuoltaja 534,05
            else:
                tuki1=yksinhuoltaja+lapsi1+lapsi2+lapsi3*(lapsia-2)     # yksinhuoltaja 534,05
        else:
            if lapsia<1:
                tuki1=muu*aikuisia
            elif lapsia==1:
                tuki1=muu*aikuisia+lapsi1     # yksinhuoltaja 534,05
            elif lapsia==2:
                tuki1=muu*aikuisia+lapsi1+lapsi2     # yksinhuoltaja 534,05
            else:
                tuki1=muu*aikuisia+lapsi1+lapsi2+lapsi3*(lapsia-2)     # yksinhuoltaja 534,05

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
            if p['toimeentulotuki_vahennys']>99: # vähennetään 100%
                tuki=0.0
                
        if tuki<10:
            tuki=0    
            
        return tuki
        
    def perheparametrit(self,perhetyyppi: int =10,tulosta: bool =False):
        return perheparametrit(perhetyyppi=perhetyyppi,tulosta=tulosta)
        
    def print_examples(self):
        return print_examples()
        
    def get_default_parameter(self):
        return perheparametrit(perhetyyppi=1)
    
    def perustulo(self):
        return 0
    
    # tmtuki samankokoinen
    def peruspaivaraha2018(self,lapsia: int) -> float:
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
    def peruspaivaraha2019(self,lapsia: int) -> float:
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
    def peruspaivaraha2020(self,lapsia: int) -> float:
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
    def peruspaivaraha2021(self,lapsia: int) -> float:
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

    def peruspaivaraha2022(self,lapsia: int) -> float:
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.41     # e/pv
        elif lapsia==2:
            lisa=7.95     # e/pv
        else:
            lisa=10.25     # e/pv 
        
        if self.use_extra_ppr:
            pvraha=21.5*(35.72+lisa)*self.extra_ppr_factor
        else:
            pvraha=21.5*(35.72+lisa)
        tuki=max(0,pvraha)    
    
        return tuki

    def peruspaivaraha2023(self,lapsia: int) -> float:
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=7.01     # e/pv
        elif lapsia==2:
            lisa=10.29     # e/pv
        else:
            lisa=13.26     # e/pv 
        
        if self.use_extra_ppr:
            pvraha=21.5*(37.21+lisa)*self.extra_ppr_factor
        else:
            pvraha=21.5*(37.21+lisa)
        tuki=max(0,pvraha)    
    
        return tuki
        
    def peruspaivaraha2024(self,lapsia: int) -> float:
        if self.use_extra_ppr:
            pvraha=21.5*37.21*self.extra_ppr_factor
        else:
            pvraha=21.5*37.21
        tuki=max(0,pvraha)    

        return tuki

    def peruspaivaraha2025(self,lapsia: int) -> float:
        if self.use_extra_ppr:
            pvraha=21.5*37.21*self.extra_ppr_factor
        else:
            pvraha=21.5*37.21
        tuki=max(0,pvraha)    

        return tuki

    def peruspaivaraha2026(self,lapsia: int) -> float:
        if self.use_extra_ppr:
            pvraha=21.5*37.21*self.extra_ppr_factor
        else:
            pvraha=21.5*37.21
        tuki=max(0,pvraha)    

        return tuki

    def peruspaivaraha2027(self,lapsia: int) -> float:
        if lapsia==0:
            lisa=0    
        elif lapsia==1:
            lisa=5.84     # e/pv
        elif lapsia==2:
            lisa=8.57     # e/pv
        else:
            lisa=11.05    # e/pv 

        if self.use_extra_ppr:
            pvraha=21.5*37.21*self.extra_ppr_factor
        else:
            pvraha=21.5*37.21
        tuki=max(0,pvraha)    

        return tuki                        

    def ansiopaivaraha_ylaraja(self,ansiopaivarahamaara: float,tyotaikaisettulot: float,vakpalkka: float,vakiintunutpalkka: float,peruspvraha: float) -> float:
        if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
            return max(0,vakpalkka-tyotaikaisettulot) 
           
        return ansiopaivarahamaara   
        
    def laske_sotumaksu(self,vuosi: int):
        '''
        '''
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
        elif vuosi==2023:
            sotumaksu=0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2024:
            sotumaksu=0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2025:
            sotumaksu=0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2026:
            sotumaksu=0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2027:
            sotumaksu=0.0434+0.6*self.additional_tyel_premium
        else:
            sotumaksu=0.0448+0.6*self.additional_tyel_premium
            
        return sotumaksu

    def ansiopaivaraha_porrastus(self,tyoton: int,vakiintunutpalkka,lapsia: int,tyotaikaisettulot: float,saa_ansiopaivarahaa: int,
                       kesto: float,p: dict,ansiokerroin: float=None,omavastuukerroin: float=1.0,alku: str='',korotettu: bool=False):
        ansiopvrahan_suojaosa=0
        lapsikorotus=0
    
        if tyoton>0 and p[alku+'elakkeella']<1:
            if self.year==2018:
                taite=3078.60    
            elif self.year==2019:
                taite=3078.60    
            elif self.year==2020:
                taite=3197.70    
            elif self.year==2021:
                taite=3209.10    
            elif self.year==2022:
                taite=3277.50    
            elif self.year==2023:
                taite=3534.95
            elif self.year==2024:
                taite=3534.95*1.03
            elif self.year==2025:
                taite=3534.95*1.03
            elif self.year==2026:
                taite=3534.95*1.03
            elif self.year==2027:
                taite=3534.95*1.03
            else:
                taite=3078.60   
                            
            if saa_ansiopaivarahaa>0: # & (kesto<400.0): # ei keston tarkastusta!
                #print(f'tyoton {tyoton} vakiintunutpalkka {vakiintunutpalkka} lapsia {lapsia} tyotaikaisettulot {tyotaikaisettulot} saa_ansiopaivarahaa {saa_ansiopaivarahaa} kesto {kesto} ansiokerroin {ansiokerroin} omavastuukerroin {omavastuukerroin}')
            
                # porrastetaan ansio-osa keston mukaan
                # 2 kk -> 80%
                # 34 vko -> 75%
                if ansiokerroin is None:
                    if kesto>34/52*12*21.5:
                        ansiokerroin=0.75
                    elif kesto>2*21.5:
                        ansiokerroin=0.80
                    else:
                        ansiokerroin=1.00 # =1-2/3/21.5

                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-self.sotumaksu)     
                
                #print(f'vakpalkka {vakpalkka}')
                if korotettu and (kesto<200.0):
                    if vakpalkka>taite:
                        tuki2=0.25*max(0,vakpalkka-taite)+0.55*max(0,taite-perus)+perus    
                    else:
                        tuki2=0.55*max(0,vakpalkka-perus)+perus
                else:
                    if vakpalkka>taite:
                        tuki2=0.2*max(0,vakpalkka-taite)+0.45*max(0,taite-perus)+perus    
                    else:
                        tuki2=0.45*max(0,vakpalkka-perus)+perus
                        

                tuki2=tuki2
                tuki2=tuki2*ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa=0 #self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p) 
        
                perus=self.peruspaivaraha(lapsia)     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana
                if tuki2>.9*vakpalkka:
                    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavat_tulot=max(0,tyotaikaisettulot-suojaosa)
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavat_tulot)
                ansiopaivarahamaara = self.ansiopaivaraha_sovittelu(tuki2,tyotaikaisettulot,suojaosa)
                soviteltuperus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,soviteltuperus)  

                perus=max(0,soviteltuperus-ansiopaivarahamaara)
                tuki=omavastuukerroin*max(soviteltuperus,ansiopaivarahamaara)     # voi tulla vastaan pienillä tasoilla4
            else:
                if True: #p[alku+'peruspaivarahalla']>0:
                    ansiopaivarahamaara=0
                    perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                    tuki=omavastuukerroin*perus
                else: # tm-tuki
                    ansiopaivarahamaara=0
                    perus=self.soviteltu_tmtuki(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p) 
                    tuki=omavastuukerroin*perus
        else:
            perus=0    
            tuki=0    
            ansiopaivarahamaara=0   

        return tuki,ansiopaivarahamaara,perus

    def ansiopaivaraha_perus(self,tyoton: int,vakiintunutpalkka,lapsia: int,tyotaikaisettulot: float,saa_ansiopaivarahaa: int,
                       kesto: float,p: dict,ansiokerroin: float=1.0,omavastuukerroin: float=1.0,alku: str='',korotettu: bool=False):
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
            elif self.year==2023:
                lapsikorotus=np.array([0,7.01,10.29,13.26])*21.5
                taite=3534.95
            elif self.year==2024:
                lapsikorotus=np.array([0,0,0,0])*21.5
                taite=3534.95*1.03
            elif self.year==2025:
                lapsikorotus=np.array([0,0,0,0])*21.5
                taite=3534.95*1.03
            elif self.year==2026:
                lapsikorotus=np.array([0,0,0,0])*21.5
                taite=3534.95*1.03
            elif self.year==2027:
                lapsikorotus=np.array([0,0,0,0])*21.5
                taite=3534.95*1.03
            else:
                lapsikorotus=np.array([0,5.23,7.68,9.90])*21.5    
                taite=3078.60   
                            
            if saa_ansiopaivarahaa>0: # & (kesto<400.0): # ei keston tarkastusta!
                #print(f'tyoton {tyoton} vakiintunutpalkka {vakiintunutpalkka} lapsia {lapsia} tyotaikaisettulot {tyotaikaisettulot} saa_ansiopaivarahaa {saa_ansiopaivarahaa} kesto {kesto} ansiokerroin {ansiokerroin} omavastuukerroin {omavastuukerroin}')
            
                perus=self.peruspaivaraha(0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                vakpalkka=vakiintunutpalkka*(1-self.sotumaksu)     
                
                #print(f'vakpalkka {vakpalkka}')
                if korotettu and (kesto<200.0):
                    if vakpalkka>taite:
                        tuki2=0.25*max(0,vakpalkka-taite)+0.55*max(0,taite-perus)+perus    
                    else:
                        tuki2=0.55*max(0,vakpalkka-perus)+perus
                else:
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
        
                vahentavat_tulot=max(0,tyotaikaisettulot-suojaosa)
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavat_tulot)
                ansiopaivarahamaara = self.ansiopaivaraha_sovittelu(tuki2,tyotaikaisettulot,suojaosa)
                soviteltuperus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,soviteltuperus)  

                tuki=ansiopaivarahamaara    
                perus=max(0,soviteltuperus-ansiopaivarahamaara)
                tuki=omavastuukerroin*max(soviteltuperus,tuki)     # voi tulla vastaan pienillä tasoilla4
            else:
                if True: #p[alku+'peruspaivarahalla']>0:
                    ansiopaivarahamaara=0
                    perus=self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                    tuki=omavastuukerroin*perus
                else: # tm-tuki
                    ansiopaivarahamaara=0
                    perus=self.soviteltu_tmtuki(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p) 
                    tuki=omavastuukerroin*perus
        else:
            perus=0    
            tuki=0    
            ansiopaivarahamaara=0   

        return tuki,ansiopaivarahamaara,perus

    def ansiopaivaraha_sovittelu(self,tuki2: float,tyotaikaisettulot: float,suojaosa: float):
        vahentavat_tulot=max(0,tyotaikaisettulot-suojaosa)
        ansiopaivarahamaara=max(0,tuki2-0.5*vahentavat_tulot)

        return ansiopaivarahamaara

    def soviteltu_peruspaivaraha(self,lapsia: int,tyotaikaisettulot: float,ansiopvrahan_suojaosa: int,p: dict) -> float:
        suojaosa=self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p)
        pvraha=self.peruspaivaraha(lapsia)
        if True:
            vahentavattulo=max(0,tyotaikaisettulot-suojaosa)
            tuki=max(0,pvraha-0.5*vahentavattulo)
        else: # testejä varten
            vahentavattulo1=max(0,min(500,tyotaikaisettulot-suojaosa))
            vahentavattulo2=max(0,tyotaikaisettulot-suojaosa-500)
            tuki=max(0,pvraha - 0.5*vahentavattulo2 - 0.25*vahentavattulo1)
    
        return tuki
        
    def tmtuki_suojaosa(self,lapsia: int,p: dict) -> float:
        if lapsia>0:
            suojaosa=self.tmtuki_suojaosa_perheellinen+lapsia*self.tmtuki_lisa
        else:
            suojaosa=self.tmtuki_suojaosa_yksin
            
        return suojaosa
        
    def tmtuki_vahentavatulo(self,lapsia: int,tyotaikaisettulot: float,ansiopvrahan_suojaosa: int,p: dict) -> float:
        if p['aikuisia']>1:
            puoliso=True
        else:
            puoliso=False
        
        if lapsia>0 or puoliso:
            suojaosa=self.tmtuki_suojaosa_perheellinen+lapsia*self.tmtuki_lisa
        else:
            suojaosa=self.tmtuki_suojaosa_yksin
        
        if puoliso:
            # Henkilölle, joka on saanut työttömyyspäivärahaa enimmäisajan, työmarkkinatuki
            # maksetaan ilman tarveharkintaa 180 ensimmäisen työttömyyspäivän ajalta. 
            # Myös jos ikä >= 55 ja toe täyttynyt työttömäksi joutuessa, 
            if p['ika']>=55:
                vahentavattulo=max(0,tyotaikaisettulot-suojaosa)
            else:
                vahentavattulo=max(0,max(p['puoliso_tulot']-self.tmtuki_puoliso_suojaosa,0)+tyotaikaisettulot-suojaosa)
        else:
            vahentavattulo=max(0,tyotaikaisettulot-suojaosa)
            
        return vahentavattulo
        
    def soviteltu_tmtuki(self,lapsia: int,tyotaikaisettulot: float,ansiopvrahan_suojaosa: int,p: dict) -> float:
        if True: # ei tarveharkintaa, koska tarveharkinta kohdistuu vain pääomatuloihin yms. ove pitäisi tarveharkita
            return self.soviteltu_peruspaivaraha(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)
        else:
            suojaosa=self.tmtuki_suojaosa(lapsia,p)

            pvraha=self.peruspaivaraha(lapsia)
            vahentavattulo=self.tmtuki_vahentavatulo(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)

            if p['aikuisia']>1:
                puoliso=True
            else:
                puoliso=False

            if lapsia>0 or puoliso:
                tuki=max(0,pvraha-0.5*vahentavattulo)
            else:
                #tuki=max(0,pvraha-0.75*vahentavattulo)
                tuki=max(0,pvraha-0.5*vahentavattulo)
    
            return tuki

    ### Verotus
        
    def elaketulovahennys2018(self,elaketulot: float,tulot: float):
        max_elaketulovahennys_valtio=11560/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9040/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2019(self,elaketulot: float,tulot: float):
        max_elaketulovahennys_valtio=11590/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9050/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2020(self,elaketulot: float,tulot: float):
        max_elaketulovahennys_valtio=11540/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9230/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2021(self,elaketulot: float,tulot: float):
        max_elaketulovahennys_valtio=11150/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9270/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2022(self,elaketulot: float,tulot: float):
        max_elaketulovahennys_valtio=11190/self.kk_jakaja
        elaketulovahennys_valtio=max(0,min(elaketulot,max_elaketulovahennys_valtio-0.38*max(0,tulot-max_elaketulovahennys_valtio)))
        max_elaketulovahennys_kunnallis=9500/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,max_elaketulovahennys_kunnallis-0.51*max(0,tulot-max_elaketulovahennys_kunnallis))))
        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2023(self,elaketulot: float,puhdas_ansiotulo: float):
        raja1_elaketulovahennys_kunnallis=10_320/self.kk_jakaja
        raja2_elaketulovahennys_kunnallis=22_500/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,raja1_elaketulovahennys_kunnallis
            -0.51*max(0,min(puhdas_ansiotulo,raja2_elaketulovahennys_kunnallis)-raja1_elaketulovahennys_kunnallis)
            -0.15*max(0,puhdas_ansiotulo-raja2_elaketulovahennys_kunnallis)))
        )
        elaketulovahennys_valtio=elaketulovahennys_kunnallis

        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2024(self,elaketulot: float,puhdas_ansiotulo: float):
        raja1_elaketulovahennys_kunnallis=10_320/self.kk_jakaja
        raja2_elaketulovahennys_kunnallis=22_500/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,raja1_elaketulovahennys_kunnallis
            -0.51*max(0,min(puhdas_ansiotulo,raja2_elaketulovahennys_kunnallis)-raja1_elaketulovahennys_kunnallis)
            -0.15*max(0,puhdas_ansiotulo-raja2_elaketulovahennys_kunnallis)))
        )
        elaketulovahennys_valtio=elaketulovahennys_kunnallis

        return elaketulovahennys_valtio,elaketulovahennys_kunnallis

    def elaketulovahennys2025(self,elaketulot: float,puhdas_ansiotulo: float):
        raja1_elaketulovahennys_kunnallis=10_320/self.kk_jakaja
        raja2_elaketulovahennys_kunnallis=22_500/self.kk_jakaja
        elaketulovahennys_kunnallis=max(0,min(elaketulot,max(0,raja1_elaketulovahennys_kunnallis
            -0.51*max(0,min(puhdas_ansiotulo,raja2_elaketulovahennys_kunnallis)-raja1_elaketulovahennys_kunnallis)
            -0.15*max(0,puhdas_ansiotulo-raja2_elaketulovahennys_kunnallis)))
        )
        elaketulovahennys_valtio=elaketulovahennys_kunnallis

        return elaketulovahennys_valtio,elaketulovahennys_kunnallis
    def tyotulovahennys2018(self):
        max_tyotulovahennys=1540/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127_000])/self.kk_jakaja
        ttulopros=np.array([0.120,0.0165,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2019(self):
        max_tyotulovahennys=1630/self.kk_jakaja
        ttulorajat=np.array([2500,33000,127_800])/self.kk_jakaja
        ttulopros=np.array([0.120,0.0172,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2020(self):
        max_tyotulovahennys=1770/self.kk_jakaja
        ttulorajat=np.array([2500,33000,129_800])/self.kk_jakaja 
        ttulopros=np.array([0.125,0.0184,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2021(self):
        max_tyotulovahennys=1840/self.kk_jakaja
        ttulorajat=np.array([2500,33000,130_400])/self.kk_jakaja 
        ttulopros=np.array([0.127,0.0189,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2022(self):
        max_tyotulovahennys=1930/self.kk_jakaja
        ttulorajat=np.array([2500,33000,132_200])/self.kk_jakaja 
        ttulopros=np.array([0.13,0.0196,0])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2023(self,ika: float,lapsia: int):
        if ika>=60:
            if ika>=62:
                max_tyotulovahennys=2430/self.kk_jakaja
            elif ika>=65:
                max_tyotulovahennys=2630/self.kk_jakaja
            else:
                max_tyotulovahennys=2230/self.kk_jakaja
        else:
            max_tyotulovahennys=2030/self.kk_jakaja
        ttulorajat=np.array([0,22000,70000])/self.kk_jakaja 
        ttulopros=np.array([0.13,0.0203,0.0121])
        return max_tyotulovahennys,ttulorajat,ttulopros

    def tyotulovahennys2024(self,ika: float,lapsia: int):
        if ika>=65:
            max_tyotulovahennys=3340/self.kk_jakaja
        else:
            max_tyotulovahennys=2140/self.kk_jakaja
        ttulorajat=np.array([0,22000,77000])/self.kk_jakaja*1.032 # 127000??
        ttulopros=np.array([0.13,0.0203,0.121])
        return max_tyotulovahennys,ttulorajat,ttulopros
        
    def tyotulovahennys2025(self,ika: float,lapsia: int):
        if ika>=65:
            max_tyotulovahennys=3340/self.kk_jakaja
        else:
            max_tyotulovahennys=2140/self.kk_jakaja
        ttulorajat=np.array([0,22000,77000])/self.kk_jakaja*1.032 # 127000??
        ttulopros=np.array([0.13,0.0203,0.121])
        return max_tyotulovahennys,ttulorajat,ttulopros
        
    def laske_tyotulovahennys2018_2022(self,puhdas_ansiotulo: float,palkkatulot_puhdas: float,ika: float, lapsia: int):
        '''
        Vuosille 2018-2022
        '''
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

        if puhdas_ansiotulo>ttulorajat[1]: # puhdas_ansiotulo vai puhdas_palkkatulo ??
            if puhdas_ansiotulo>ttulorajat[2]:
                tyotulovahennys=0
            else:
                tyotulovahennys=max(0,tyotulovahennys-ttulopros[1]*max(0,puhdas_ansiotulo-ttulorajat[1]))    
                
        return tyotulovahennys
        
    def laske_tyotulovahennys2023_2025(self,puhdas_ansiotulo: float,palkkatulot_puhdas: float,ika: float,lapsia: float):
        '''
        Vuosille 2023-
        '''
        max_tyotulovahennys,ttulorajat,ttulopros=self.tyotulovahennys(ika,lapsia)
    
        tyotulovahennys=min(max_tyotulovahennys,max(0,ttulopros[0]*max(0,palkkatulot_puhdas-ttulorajat[0])))
        tyotulovahennys=max(0,tyotulovahennys-ttulopros[1]*max(0,min(ttulorajat[2],puhdas_ansiotulo)-ttulorajat[1])-ttulopros[2]*max(0,puhdas_ansiotulo-ttulorajat[2]))    
                
        return tyotulovahennys        

    def laske_ansiotulovahennys(self,puhdas_ansiotulo: float,palkkatulot_puhdas: float):
        '''
        '''
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

        return ansiotulovahennys

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
        
    def ansiotulovahennys2022(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah

    def ansiotulovahennys2023(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah

    def ansiotulovahennys2024(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah
        
    def ansiotulovahennys2025(self):
        rajat=np.array([2500,7230,14000])/self.kk_jakaja
        maxvahennys=3570/self.kk_jakaja
        ansvah=np.array([0.51,0.28,0.045])
        return rajat,maxvahennys,ansvah

    def veroparam2018(self):
        self.kunnallisvero_pros=max(0,max(0,0.1984+self.additional_kunnallisvero)) # Viitamäen raportista 19,84; verotuloilla painotettu k.a. 19,86
        self.kirkollisvero_pros=0.0139
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
        self.sairaanhoitomaksu_etuus=0.0153 # muut
        
        self.paivarahamaksu_pros=0.0153 # palkka
        self.paivarahamaksu_raja=14_020/self.kk_jakaja    
        
        self.elakemaksu_alaraja=58.27
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2019(self):
        self.kunnallisvero_pros=max(0,0.1988+self.additional_kunnallisvero) # Viitamäen raportista
        self.kirkollisvero_pros=0.0139
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
        
        self.paivarahamaksu_pros=0.0154 # palkka
        self.paivarahamaksu_raja=14282/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2020(self):
        self.kunnallisvero_pros=max(0,0.1997+self.additional_kunnallisvero) # Viitamäen raportista
        self.kirkollisvero_pros=0.0139
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
        self.sairaanhoitomaksu_etuus=0.0165 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=14_574/self.kk_jakaja    
        
        self.elakemaksu_alaraja=60.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2021(self):
        self.kunnallisvero_pros=max(0,0.2002+self.additional_kunnallisvero) # Viitamäen raportista
        self.kirkollisvero_pros=0.0139
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
    
        self.sairaanhoitomaksu=0.0068
        self.sairaanhoitomaksu_etuus=0.0165 # muut
        
        self.paivarahamaksu_pros=0.0136 # palkka
        self.paivarahamaksu_raja=14_766/self.kk_jakaja    
        
        self.elakemaksu_alaraja=61.37
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2022(self):
        '''
        Päivitä
        '''
        self.kunnallisvero_pros=max(0,0.2001+self.additional_kunnallisvero) 
        self.kirkollisvero_pros=0.0139
        self.tyottomyysvakuutusmaksu=0.0150 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0134
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0151 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0070 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0053
        self.sairaanhoitomaksu_etuus=0.0150 # muut
        
        self.paivarahamaksu_pros=0.0118 # palkka
        self.paivarahamaksu_raja=15_128/self.kk_jakaja    
        
        self.elakemaksu_alaraja=62.88
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2023(self):
        '''
        Päivitetty 6.5.2023
        '''
        self.kunnallisvero_pros=max(0,0.0746+self.additional_kunnallisvero) # +0.0135) 
        self.kirkollisvero_pros=0.0138
        self.tyottomyysvakuutusmaksu=0.0150 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0153
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0154 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0057 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0060
        self.sairaanhoitomaksu_etuus=0.0157 # muut
        
        self.paivarahamaksu_pros=0.0136 # palkka
        self.paivarahamaksu_raja=15_703/self.kk_jakaja    
        
        self.elakemaksu_alaraja=65.26
        self.tulonhankkimisvahennys=750/self.kk_jakaja
        
    def veroparam2024(self):
        '''
        Päivitetty 6.5.2024
        '''
        self.kunnallisvero_pros=max(0,0.0761+self.additional_kunnallisvero) # Viitamäen raportista
        self.kirkollisvero_pros=0.0139
        self.tyottomyysvakuutusmaksu=0.0079 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0116
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0082 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0057 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0051
        self.sairaanhoitomaksu_etuus=0.0148 # muut
        
        self.paivarahamaksu_pros=0.0101 # palkka
        self.paivarahamaksu_raja=16_499/self.kk_jakaja    
        
        self.elakemaksu_alaraja=68.57
        self.tulonhankkimisvahennys=750/self.kk_jakaja

    def veroparam2025(self):
        '''
        Päivitetty 21.9.2022
        '''
        self.kunnallisvero_pros=max(0,0.0761+self.additional_kunnallisvero) # Viitamäen raportista
        self.kirkollisvero_pros=0.0139
        self.tyottomyysvakuutusmaksu=0.0079 #
        if self.vaihtuva_tyelmaksu:
            self.laske_vaihtuva_tyoelakemaksu(p['ika'])
        else:
            self.tyontekijan_maksu=max(0,0.0715+self.additional_tyel_premium) # PTEL
            self.tyontekijan_maksu_52=max(0,0.0865+self.additional_tyel_premium) # PTEL
            self.koko_tyel_maksu=max(0,0.2440+self.additional_tyel_premium) # PTEL
            self.tyonantajan_tyel=self.koko_tyel_maksu-self.tyontekijan_maksu

        self.tyonantajan_sairausvakuutusmaksu=0.0116
        self.tyonantajan_tyottomyysvakuutusmaksu=0.0082 # keskimäärin
        self.tyonantajan_ryhmahenkivakuutusmaksu=0.0006
        self.tyonantajan_tytalmaksu=0.0057 # työtapaturma- ja ammattitautimaksu, keskimäärin
        self.tyonantajan_sivukulut=max(0,self.tyonantajan_ryhmahenkivakuutusmaksu
            +self.tyonantajan_tyel+self.tyonantajan_sairausvakuutusmaksu+self.tyonantajan_tytalmaksu)
    
        self.sairaanhoitomaksu=0.0055
        self.sairaanhoitomaksu_etuus=0.0157 # muut
        
        self.paivarahamaksu_pros=0.0101 # palkka
        self.paivarahamaksu_raja=16_499/self.kk_jakaja    
        
        self.elakemaksu_alaraja=62.88
        self.tulonhankkimisvahennys=750/self.kk_jakaja

    def laske_ylevero2018(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14750/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2019(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14750/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2020(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2021(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    

    def laske_ylevero2022(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero

    def laske_ylevero2023(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    
        
    def laske_ylevero2024(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero    
        
    def laske_ylevero2025(self,puhdas_ansiotulo: float):
        yleveropros=0.025
        min_ylevero=0/self.kk_jakaja
        max_ylevero=163/self.kk_jakaja
        ylevero_alaraja=14000/self.kk_jakaja
    
        ylevero=min(max_ylevero,yleveropros*max(0,puhdas_ansiotulo-ylevero_alaraja))
    
        if ylevero<min_ylevero:
            ylevero=0
            
        return ylevero  

    def laske_perusvahennys(self,puhdas_ansiotulo: float):
        perusvahennys_pros,max_perusvahennys=self.perusvahennys()
        peruste=max(0,puhdas_ansiotulo)
        if peruste<max_perusvahennys:
            perusvahennys=peruste
        else:
            perusvahennys=max(0,max_perusvahennys-perusvahennys_pros*max(0,puhdas_ansiotulo-max_perusvahennys))

        return perusvahennys

    def perusvahennys2018(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3100/self.kk_jakaja
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
    
    def perusvahennys2023(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3870/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2024(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3980/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def perusvahennys2025(self):
        perusvahennys_pros=0.18
        max_perusvahennys=3980/self.kk_jakaja
        return perusvahennys_pros,max_perusvahennys
    
    def verotus(self,palkkatulot: float,muuttulot: float,elaketulot: float,lapsia: int,p: dict,alku: str=''):
        lapsivahennys=0 # poistui 2018
    
        peritytverot=0
        
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
        
        paivarahamaksu=self.laske_paivarahamaksu(palkkatulot,p['ika'])
        #print('paivarahamaksu',paivarahamaksu,palkkatulot*12,self.paivarahamaksu_raja*12)

        peritytverot += paivarahamaksu + ptel + tyotvakmaksu
    
        # tulonhankkimisvähennys pienentää ansiotuloa    
        palkkatulot_puhdas=max(0,palkkatulot-self.tulonhankkimisvahennys) # puhdas palkkatulo
        
        # eläketulovähennys
        puhdas_ansiotulo = palkkatulot_puhdas+muuttulot+elaketulot
        
        elaketulovahennys_valtio,elaketulovahennys_kunnallis = self.elaketulovahennys(elaketulot,puhdas_ansiotulo)
        elaketulot_valtio = max(0,elaketulot-elaketulovahennys_valtio)
        elaketulot_kunnallis = max(0,elaketulot-elaketulovahennys_kunnallis)

        tulot_valtio = puhdas_ansiotulo + elaketulot_valtio - elaketulot -paivarahamaksu-ptel-tyotvakmaksu 
        tulot_kunnallis = puhdas_ansiotulo + elaketulot_kunnallis - elaketulot -paivarahamaksu-ptel-tyotvakmaksu 
    
        # ylevero
    
        ylevero = self.laske_ylevero(puhdas_ansiotulo)
        peritytverot += ylevero

        # työtulovähennys vähennetään valtionveroista

        tyotulovahennys=self.laske_tyotulovahennys(puhdas_ansiotulo,palkkatulot_puhdas,p['ika'],lapsia)

        # perusvähennys
        if self.year>=2023:
            ansiotulovahennys_valtio=self.laske_ansiotulovahennys(puhdas_ansiotulo,palkkatulot_puhdas)
            peruste=max(0,tulot_valtio-ansiotulovahennys_valtio)
            perusvahennys_valtio=self.laske_perusvahennys(peruste)
        else:
            perusvahennys_valtio=0
            ansiotulovahennys_valtio=0
                    
        # valtioverotus
        # varsinainen verotus
        valtionveroperuste = max(0,tulot_valtio - perusvahennys_valtio - ansiotulovahennys_valtio)

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

        # kunnallisverotus
        if self.year>=2023:
            ansiotulovahennys = ansiotulovahennys_valtio
            perusvahennys = perusvahennys_valtio
            kunnallisveroperuste = valtionveroperuste # max(0,tulot_kunnallis - perusvahennys - ansiotulovahennys)
        else:
            ansiotulovahennys=self.laske_ansiotulovahennys(puhdas_ansiotulo,palkkatulot_puhdas)
            # perusvähennys
            peruste=max(0,tulot_kunnallis-ansiotulovahennys)
            perusvahennys=self.laske_perusvahennys(peruste)
        
            # Yhteensä
            kunnallisveroperuste=max(0,peruste-perusvahennys)
        
        kunnallis_verotettava_palkkatulo=max(0,kunnallisveroperuste-elaketulot_kunnallis-muuttulot)
        peritty_sairaanhoitomaksu=max(0,kunnallis_verotettava_palkkatulo)*self.sairaanhoitomaksu+max(0,kunnallisveroperuste-kunnallis_verotettava_palkkatulo)*self.sairaanhoitomaksu_etuus
        
        if tyotulovahennys_kunnallisveroon>0:
            kunnallisvero_0=kunnallisveroperuste*self.kunnallisvero_pros
            kirkollisvero_0=kunnallisveroperuste*self.kirkollisvero_pros
            a=peritty_sairaanhoitomaksu+kunnallisvero_0+kirkollisvero_0
            if a > 0:
                osuus_0 = tyotulovahennys_kunnallisveroon/a
                kvhen = kunnallisvero_0 * osuus_0
                kihen = kirkollisvero_0 * osuus_0
                svhen = peritty_sairaanhoitomaksu * osuus_0
            else:
                kvhen=0
                kihen=0
                svhen=0

            kunnallisvero=max(0,kunnallisveroperuste*self.kunnallisvero_pros-kvhen)
            kirkollisvero=max(0,kunnallisveroperuste*self.kirkollisvero_pros-kihen)
            peritty_sairaanhoitomaksu=max(0,peritty_sairaanhoitomaksu-svhen)
        else:
            kunnallisvero=kunnallisveroperuste*self.kunnallisvero_pros
            kirkollisvero=kunnallisveroperuste*self.kirkollisvero_pros
            
        sairausvakuutusmaksu = paivarahamaksu + peritty_sairaanhoitomaksu
        
        # perityst verot sis kaikki työntekijän osuudet, ilman työnantajan osuutta
        peritytverot += peritty_sairaanhoitomaksu + kunnallisvero
        if self.include_kirkollisvero:
            peritytverot += kirkollisvero

        # yhteensä
        netto=tulot-peritytverot

        return netto,peritytverot,valtionvero,kunnallisvero,kunnallisveroperuste,\
               valtionveroperuste,ansiotulovahennys,perusvahennys,tyotulovahennys,\
               tyotulovahennys_kunnallisveroon,ptel,sairausvakuutusmaksu,tyotvakmaksu,koko_tyoelakemaksu,ylevero
        
    def raippavero2018(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2019(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2020(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2021(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2022(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
    
    def raippavero2023(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero

    def raippavero2024(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
        pros=0.0585
        vero=max(elaketulo-alaraja,0)*pros
        return vero
        
    def raippavero2025(self,elaketulo: float):
        alaraja=47_000/self.kk_jakaja
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
        
    def valtionvero_asteikko_2023(self):
        rajat=np.array([0,19900,29700,49000,85800])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.1264,0.19,0.3025,0.34,0.44+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.44+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros
        
    def valtionvero_asteikko_2024(self):
        rajat=np.array([0,20_500,30_500,50_400,88_200,150_000])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.1264,0.19,0.3025,0.34,0.42,0.44+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.44+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros               

    def valtionvero_asteikko_2025(self):
        rajat=np.array([0,20_500,30_500,50_400,88_200,150_000])/self.kk_jakaja
        pros=np.maximum(0,np.array([0.1264,0.19,0.3025,0.34,0.42,0.44+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.44+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros               

### Hoitolisä

    def hoitolisa2018(self,perheentulot: float,perhekoko: int):
        '''
        '''
        perustuki=181.07
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.095)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

    def hoitolisa2019(self,perheentulot: float,perhekoko: int):
        '''
        '''
        perustuki=181.07
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.095)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

    def hoitolisa2020(self,perheentulot: float,perhekoko: int):
        '''
        '''
        perustuki=182.86
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.095)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

    def hoitolisa2021(self,perheentulot: float,perhekoko: int):
        '''
        '''
        perustuki=182.86
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.095)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

    def hoitolisa2022(self,perheentulot: float,perhekoko: int):
        '''
        '''
        perustuki=187.45
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.095)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

    def hoitolisa2023(self,perheentulot: float,perhekoko: int):
        '''
        '''
        perustuki=202.12
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.094)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

    def hoitolisa2024(self,perheentulot: float,perhekoko: int):
        '''
        Vuoden 2023 tasossa
        '''
        perustuki=202.12
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.094)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

    def hoitolisa2025(self,perheentulot: float,perhekoko: int):
        '''
        Vuoden 2023 tasossa
        '''
        perustuki=202.12
        if perhekoko==2:
            tuki=max(0,perustuki-max(0,perheentulot-1160)*0.115)
        elif perhekoko==3:
            tuki=max(0,perustuki-max(0,perheentulot-1430)*0.094)
        elif perhekoko>3:
            tuki=max(0,perustuki-max(0,perheentulot-1700)*0.079)
        else:
            tuki=0
        
        return tuki

# joustava hoitoraha

    def joustavahoitoraha(self,työaika: float,allekolmev: int):
        if allekolmev<1:
            tuki=0
        else:
            if self.year==2018:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2019:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2020:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2021:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2022:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2023:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2024:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2025:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2026:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            elif self.year==2027:
                osatuki=179.49 # e/kk
                täysituki=269.24 # e/kk
            else:
                print('unknown year',self.year)
                
            if työaika<=30/40:
                if työaika<22.5/40:
                    tuki=täysituki
                else:
                    tuki=osatuki
            else:
                tuki=0
        
        return tuki

# kotihoidontuki
        
    def kotihoidontuki2018(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int):
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
    
    def kotihoidontuki2019(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int):
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
    
    def kotihoidontuki2020(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int):
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
    
    def kotihoidontuki2021(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int):
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
    
    def kotihoidontuki2022(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int) -> float:
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=362.61 # e/kk
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

    def kotihoidontuki2023(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int) -> float:
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=377.68 # e/kk
            seuraavat_alle_3v=113.07 # e/kk
            yli_3v=72.66 #e_kk
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
        
    def kotihoidontuki2024(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int) -> float:
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=377.68 # e/kk
            seuraavat_alle_3v=113.07 # e/kk
            yli_3v=72.66 #e_kk
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

    def kotihoidontuki2025(self,lapsia: int,allekolmev: int,alle_kouluikaisia: int) -> float:
        if lapsia<1:
            arvo=0
        else:
            tuki_alle_3v=377.68 # e/kk
            seuraavat_alle_3v=113.07 # e/kk
            yli_3v=72.66 #e_kk
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
        
    def laske_elatustuki(self,lapsia: int,aikuisia: int):
        if self.year==2018:
            elatustuki=156.39*lapsia
        elif self.year==2019:
            elatustuki=158.74*lapsia
        elif self.year==2020:
            elatustuki=167.35*lapsia
        elif self.year==2021:
            elatustuki=167.35*lapsia
        elif self.year==2022:
            elatustuki=172.59*lapsia
        elif self.year==2023:
            elatustuki=186.97*lapsia
        elif self.year==2024:
            elatustuki=196.02*lapsia
        elif self.year==2025:
            elatustuki=196.02*lapsia*1.02
        elif self.year==2026:
            elatustuki=196.02*lapsia*1.02**2
        elif self.year==2027:
            elatustuki=196.02*lapsia*1.02**3
        else:
            error()
        
        return elatustuki

    def laske_valtionvero2018_2022(self,tulot: float,p: dict) -> float:
        '''
        Vanha valtionvero vuosille 2018-2022
        '''
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

    def laske_valtionvero2023(self,tulot: float,p: dict) -> float:
        '''
        Sote-alueiden vuoksi kunnallisveroa siirrettiin valtionveroon. Rakennemuutos
        '''
        rajat,pros=self.valtionvero_asteikko()

        vero=0

        for k in range(0,4):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[4]:
            vero=vero+(tulot-rajat[4])*pros[4]
        
        return vero

    def laske_valtionvero2024(self,tulot: float,p: dict) -> float:
        '''
        Sote-alueiden vuoksi kunnallisveroa siirrettiin valtionveroon. Rakennemuutos
        '''
        rajat,pros=self.valtionvero_asteikko()

        vero=0

        for k in range(0,5):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[5]:
            vero=vero+(tulot-rajat[5])*pros[5]
        
        return vero      

    def laske_valtionvero2025(self,tulot: float,p: dict) -> float:
        '''
        Sote-alueiden vuoksi kunnallisveroa siirrettiin valtionveroon. Rakennemuutos
        '''
        rajat,pros=self.valtionvero_asteikko()

        vero=0

        for k in range(0,5):
            vero=vero+max(0,min(rajat[k+1],tulot)-rajat[k])*pros[k]

        if tulot>rajat[5]:
            vero=vero+(tulot-rajat[5])*pros[5]
        
        return vero                

    def tyottomyysturva_suojaosa(self,suojaosamalli: int,p: dict=None):
        if suojaosamalli==2:
            suojaosa=0
        elif suojaosamalli==3:
            suojaosa=400
        elif suojaosamalli==4:
            suojaosa=500
        elif suojaosamalli==5:
            suojaosa=600
        elif suojaosamalli==10:
            suojaosa=p['tyottomyysturva_suojaosa_taso']
        else: # perusmallis
            if self.year in set([2018,2019,2021,2022,2023]):
                suojaosa=300
            elif self.year in set([2020]):
                suojaosa=500
            elif self.year in set([2024,2025]):
                suojaosa=0
        
        return suojaosa
        
    def lapsilisa2018(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([95.75,105.80,135.01,154.64,174.27])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 53.3

        return lapsilisat
    
    def lapsilisa2019(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,153.24,172.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 53.3
            
        return lapsilisat
    
    def lapsilisa2020(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 53.3
            
        return lapsilisat
    
    def lapsilisa2021(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 63.3
            
        return lapsilisat
    
    def lapsilisa2022(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 63.3
            
        return lapsilisat
    
    def lapsilisa2023(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 68.3
            
        return lapsilisat
    
    def lapsilisa2024(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,173.24,192.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 73.3
            
        return lapsilisat
    
    def lapsilisa2025(self,yksinhuoltajakorotus: bool=False) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,173.24,192.69])
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 73.3
            
        return lapsilisat

    def laske_lapsilisa(self,lapsia: int,yksinhuoltajakorotus: float=0) -> float:
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
        
    def opintoraha(self,palkka: float,lapsia: int):
        '''
        18-vuotias itsellisesti asuva opiskelija
        '''
        if lapsia>0:
            if self.year==2018:
                tuki=350.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2019:
                tuki=350.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2020:
                tuki=350.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2021:
                tuki=355.05# +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2022:
                tuki=375.40# +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2023:
                tuki=385.40# +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2024:
                tuki=385.40# +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2025:
                tuki=385.40# +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2026:
                tuki=385.40# +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2027:
                tuki=385.40# +650*0.4 = opintolainahyvitys mukana?
        else:
            if self.year==2018:
                tuki=250.28 #+650*0.4 # opintolainahyvitys mukana
            elif self.year==2019:
                tuki=250.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2020:
                tuki=250.28 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2021:
                tuki=253.69 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2022:
                tuki=268.23 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2023:
                tuki=268.23 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2024:
                tuki=268.23 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2025:
                tuki=268.23 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2026:
                tuki=268.23 # +650*0.4 = opintolainahyvitys mukana?
            elif self.year==2027:
                tuki=268.23 # +650*0.4 = opintolainahyvitys mukana?
            
        if self.year==2018:
            raja=696
        elif self.year==2019:
            raja=667
        elif self.year==2020:
            raja=667
        elif self.year==2021:
            raja=696
        elif self.year==2022:
            raja=696
        elif self.year==2023:
            raja=696*1.5
        elif self.year==2024:
            raja=696*1.5
        elif self.year==2025:
            raja=696*1.5
        elif self.year==2026:
            raja=696*1.5
        elif self.year==2027:
            raja=696*1.5
        else:
            print('error')

        if palkka>raja: #+222/12: # oletetaan että täysiaikainen opiskelija
            tuki=0
            
        return tuki

    def check_p(self,p: dict):
        if 'toimeentulotuki_vahennys' not in p:
            p['toimeentulotuki_vahennys']=0
        if 'lapsikorotus_lapsia' not in p:
            p['lapsikorotus_lapsia']=p['lapsia']
        if 'osaaikainen_paivahoito' not in p:
            p['osaaikainen_paivahoito']=0
        if 'ei_toimeentulotukea' not in p:
            p['ei_toimeentulotukea']=0
        if 'asumistuki_suojaosa' not in p:
            self.default_asumistuki_suojaosa(p)
        
        for alku in set(['omat_','puoliso_','']):
            if alku+'alive' not in p:
                p[alku+'alive']=1
            if alku+'peruspaivarahalla' not in p:
                p[alku+'peruspaivarahalla']=0
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
            if alku+'tyoaika' not in p:
                p[alku+'tyoaika']=0
            if alku+'isyysvapaa_kesto' not in p:
                p[alku+'isyysvapaa_kesto']=0

    # def laske_tulot(self,p: dict,tt_alennus=0,include_takuuelake: bool=True,legacy: bool=True):
    #     q={} # tulokset tänne
        
    #     self.check_p(p)
    #     q['perustulo']=0
    #     q['puoliso_perustulo']=0
    #     q['puhdas_tyoelake']=0
    #     q['multiplier']=1
    #     q['kotihoidontuki']=0
    #     q['kotihoidontuki_netto']=0
    #     q['puoliso_opintotuki']=0
    #     q['puoliso_kotihoidontuki']=0
    #     q['puoliso_kotihoidontuki_netto']=0
    #     q['puoliso_ansiopvraha_netto']=0
    #     q['puoliso_opintotuki_netto']=0
    #     if p['elakkeella']>0: # vanhuuseläkkeellä
    #         p['tyoton']=0
    #         q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
    #         q['elake_maksussa']=p['tyoelake']
    #         q['elake_tuleva']=0
    #         p['saa_ansiopaivarahaa']=0
    #         # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
    #         if (p['aikuisia']>1):
    #             q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,disability=p['disabled'])
    #             q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'],yksin=0)
    #         else:
    #             q['kokoelake']=self.laske_kokonaiselake(p['ika'],q['elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,disability=p['disabled'])
    #             q['puhdas_tyoelake']=self.laske_puhdas_tyoelake(p['ika'],p['tyoelake'],disability=p['disabled'],yksin=1)

    #         q['ansiopvraha'],q['tyotpvraha'],q['peruspvraha']=(0,0,0)
    #         #oletetaan että myös puoliso eläkkeellä
    #         q['puoliso_ansiopvraha']=0
    #         q['opintotuki']=0
    #     elif p['opiskelija']>0:
    #         q['elake_maksussa']=p['tyoelake']
    #         q['kokoelake']=p['tyoelake']
    #         q['elake_tuleva']=0
    #         q['puoliso_ansiopvraha']=0
    #         q['ansiopvraha'],q['tyotpvraha'],q['peruspvraha']=(0,0,0)
    #         q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
    #         q['opintotuki']=0
    #         if p['aitiysvapaalla']>0:
    #             q['aitiyspaivaraha']=self.aitiysraha(0,p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
    #         elif p['isyysvapaalla']>0:
    #             q['isyyspaivaraha']=self.isyysraha(0,p['vakiintunutpalkka'])
    #         elif p['kotihoidontuella']>0:
    #             q['kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
    #         else:
    #             q['opintotuki']=self.opintoraha(0,p)
    #     else: # ei eläkkeellä     
    #         q['opintotuki']=0
    #         q['elake_maksussa']=p['tyoelake']
    #         q['kokoelake']=p['tyoelake']
    #         q['elake_tuleva']=0
    #         q['puoliso_ansiopvraha']=0
    #         q['ansiopvraha'],q['tyotpvraha'],q['peruspvraha']=(0,0,0)
    #         q['isyyspaivaraha'],q['aitiyspaivaraha'],q['kotihoidontuki'],q['sairauspaivaraha']=(0,0,0,0)
    #         if p['aitiysvapaalla']>0:
    #             q['aitiyspaivaraha']=self.aitiysraha(0,p['vakiintunutpalkka'],p['aitiysvapaa_kesto'])
    #         elif p['isyysvapaalla']>0:
    #             q['isyyspaivaraha']=self.isyysraha(0,p['vakiintunutpalkka'])
    #         elif p['sairauspaivarahalla']>0:
    #             q['sairauspaivaraha']=self.sairauspaivaraha(0,p['vakiintunutpalkka'])
    #         elif p['kotihoidontuella']>0:
    #             q['kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
    #         elif p['tyoton']>0:
    #             if 'omavastuukerroin' in p:
    #                 omavastuukerroin=p['omavastuukerroin']
    #             else:
    #                 omavastuukerroin=1.0
    #             q['ansiopvraha'],q['tyotpvraha'],q['peruspvraha']=self.ansiopaivaraha(p['tyoton'],p['vakiintunutpalkka'],p['lapsia'],p['t'],p['saa_ansiopaivarahaa'],p['tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin)
                
    #     if p['aikuisia']>1:
    #         if p['puoliso_elakkeella']>0: # vanhuuseläkkeellä
    #             p['puoliso_tyoton']=0
    #             q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
    #             q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
    #             q['puoliso_elake_tuleva']=0
    #             p['puoliso_saa_ansiopaivarahaa']=0
    #             # huomioi takuueläkkeen, kansaneläke sisältyy eläke_maksussa-osaan
    #             q['puoliso_kokoelake']=self.laske_kokonaiselake(p['puoliso_ika'],q['puoliso_elake_maksussa'],yksin=0)
    #             q['puoliso_ansiopvraha'],q['puoliso_tyotpvraha'],q['puoliso_peruspvraha']=(0,0,0)
    #             q['puoliso_opintotuki']=0
    #         elif p['puoliso_opiskelija']>0:
    #             q['puoliso_kokoelake']=0
    #             q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
    #             q['puoliso_elake_tuleva']=0
    #             q['puoliso_ansiopvraha'],q['puoliso_tyotpvraha'],q['puoliso_peruspvraha']=(0,0,0)
    #             q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
    #             q['puoliso_opintotuki']=0
    #             if p['puoliso_aitiysvapaalla']>0:
    #                 q['puoliso_aitiyspaivaraha']=self.aitiysraha(0,p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
    #             elif p['puoliso_isyysvapaalla']>0:
    #                 q['puoliso_isyyspaivaraha']=self.isyysraha(0,p['puoliso_vakiintunutpalkka'])
    #             elif p['puoliso_kotihoidontuella']>0:
    #                 q['puoliso_kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
    #             else:
    #                 q['puoliso_opintotuki']=self.opintoraha(0,p)
    #         else: # ei eläkkeellä     
    #             q['puoliso_kokoelake']=0
    #             q['puoliso_opintotuki']=0
    #             q['puoliso_elake_maksussa']=p['puoliso_tyoelake']
    #             q['puoliso_elake_tuleva']=0
    #             q['puoliso_puolison_ansiopvraha']=0
    #             q['puoliso_ansiopvraha'],q['puoliso_tyotpvraha'],q['puoliso_peruspvraha']=(0,0,0)
    #             q['puoliso_isyyspaivaraha'],q['puoliso_aitiyspaivaraha'],q['puoliso_kotihoidontuki'],q['puoliso_sairauspaivaraha']=(0,0,0,0)
    #             if p['puoliso_aitiysvapaalla']>0:
    #                 q['puoliso_aitiyspaivaraha']=self.aitiysraha(0,p['puoliso_vakiintunutpalkka'],p['puoliso_aitiysvapaa_kesto'])
    #             elif p['puoliso_isyysvapaalla']>0:
    #                 q['puoliso_isyyspaivaraha']=self.isyysraha(0,p['puoliso_vakiintunutpalkka'])
    #             elif p['puoliso_sairauspaivarahalla']>0:
    #                 q['puoliso_sairauspaivaraha']=self.sairauspaivaraha(0,p['puoliso_vakiintunutpalkka'])
    #             elif p['puoliso_kotihoidontuella']>0:
    #                 q['puoliso_kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
    #             elif p['puoliso_tyoton']>0:
    #                 q['puoliso_ansiopvraha'],q['puoliso_tyotpvraha'],q['puoliso_peruspvraha']=self.ansiopaivaraha(p['puoliso_tyoton'],p['puoliso_vakiintunutpalkka'],p['lapsia'],p['puoliso_tulot'],p['puoliso_saa_ansiopaivarahaa'],p['puoliso_tyottomyyden_kesto'],p)
            
    #     # q['verot] sisältää kaikki veronluonteiset maksut
    #     _,q['verot'],q['valtionvero'],q['kunnallisvero'],q['kunnallisveroperuste'],q['valtionveroperuste'],\
    #         q['ansiotulovahennys'],q['perusvahennys'],q['tyotulovahennys'],q['tyotulovahennys_kunnallisveroon'],\
    #         q['ptel'],q['sairausvakuutusmaksu'],q['tyotvakmaksu'],q['tyel_kokomaksu'],q['ylevero']=self.verotus(p['t'],
    #             q['ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
    #             q['kokoelake'],p['lapsia'],p)
    #     _,q['verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,p['lapsia'],p)

    #     if (p['aikuisia']>1):
    #         _,q['puoliso_verot'],_,_,_,_,_,_,_,_,q['puoliso_ptel'],q['puoliso_sairausvakuutusmaksu'],\
    #             q['puoliso_tyotvakmaksu'],q['puoliso_tyel_kokomaksu'],q['puoliso_ylevero']\
    #             =self.verotus(p['puoliso_tulot'],q['puoliso_ansiopvraha']+q['puoliso_aitiyspaivaraha']+q['puoliso_isyyspaivaraha']+q['puoliso_kotihoidontuki']+q['puoliso_sairauspaivaraha']+q['puoliso_opintotuki'],
    #                 q['puoliso_kokoelake'],p['lapsia'],p)
    #         _,q['puoliso_verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['puoliso_tulot'],0,0,0,p)
    #     else:
    #         q['puoliso_verot_ilman_etuuksia']=0
    #         q['puoliso_verot']=0
    #         q['puoliso_ptel']=0
    #         q['puoliso_sairausvakuutusmaksu']=0
    #         q['puoliso_tyotvakmaksu']=0
    
    #     if p['aikuisia']==1 and p['saa_elatustukea']>0:
    #         q['elatustuki']=self.laske_elatustuki(p['lapsia'],p['aikuisia'])
    #     else:
    #         q['elatustuki']=0
        
    #     if p['elakkeella']>0:
    #         q['asumistuki']=self.elakkeensaajan_asumistuki(p['t']+p['puoliso_tulot'],q['kokoelake'],p['asumismenot_asumistuki'],p['aikuisia'],p['kuntaryhma'],p)
    #     else:
    #         q['asumistuki']=self.asumistuki(p[t],p['puoliso_tulot'],q['ansiopvraha']+q['puoliso_ansiopvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
    #               p['asumismenot_asumistuki'],p['aikuisia'],p['lapsia'],p['kuntaryhma'],p)
            
    #     if p['lapsia']>0:
    #         q['pvhoito']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['kokoelake']+q['elatustuki']+q['ansiopvraha']+q['puoliso_ansiopvraha']+q['sairauspaivaraha'],p)
    #         if (p['lapsia_kotihoidontuella']>0):
    #             alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
    #             q['pvhoito']=0 #max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
    #         q['pvhoito_ilman_etuuksia']=self.paivahoitomenot(p['lapsia_paivahoidossa'],p['puoliso_tulot']+p['t']+q['elatustuki'],p)
    #         if p['aikuisia']==1:
    #             yksinhuoltajakorotus=1
    #         else:
    #             yksinhuoltajakorotus=0
    #         q['lapsilisa']=self.laske_lapsilisa(p['lapsia'],yksinhuoltajakorotus=yksinhuoltajakorotus)
    #     else:
    #         q['pvhoito']=0
    #         q['pvhoito_ilman_etuuksia']=0
    #         q['lapsilisa']=0
    
    #     # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
    #     q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['ansiopvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
    #         q['puoliso_ansiopvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
            
    #     if p['elakkeella']>0:
    #         q['kokoelake_netto']=q['kokoelake']-(q['verot']-q['verot_ilman_etuuksia'])
    #     elif p['opiskelija']>0:
    #         q['opintotuki_netto']=q['opintotuki']-(q['verot']-q['verot_ilman_etuuksia'])
    #     elif p['aitiysvapaalla']>0:
    #         q['aitiyspaivaraha_netto']=q['aitiyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
    #     elif p['isyysvapaalla']>0:
    #         q['isyyspaivaraha_netto']=q['isyyspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
    #     elif p['kotihoidontuella']>0:
    #         q['kotihoidontuki_netto']=q['kotihoidontuki']-(q['verot']-q['verot_ilman_etuuksia']) 
    #     elif p['sairauspaivarahalla']>0:
    #         q['sairauspaivaraha_netto']=q['sairauspaivaraha']-(q['verot']-q['verot_ilman_etuuksia']) 
    #     else:
    #         q['ansiopvraha_netto']=q['ansiopvraha']-(q['verot']-q['verot_ilman_etuuksia'])
            
    #     if p['aikuisia']>1:
    #         if p['puoliso_tyoton']>0: # vanhuuseläkkeellä
    #             q['puoliso_ansiopvraha_netto']=q['puoliso_ansiopvraha']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
    #         elif p['puoliso_opiskelija']>0:
    #             q['puoliso_opintotuki_netto']=q['puoliso_opintotuki']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
    #         elif p['puoliso_kotihoidontuella']>0:
    #             q['puoliso_kotihoidontuki_netto']=q['puoliso_kotihoidontuki']-(q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia']) 
    #     else:
    #         q['puoliso_ansiopvraha_netto']=0
    #     #print('ptyötön',q['puoliso_ansiopvraha_netto'],q['puoliso_ansiopvraha'],q['puoliso_verot']-q['puoliso_verot_ilman_etuuksia'])
            
    #     if (p['isyysvapaalla']>0 or p['aitiysvapaalla']>0) and p['tyoton']>0:
    #         print('error: vanhempainvapaalla & työtön ei toteutettu')
    
    #     # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
    #     # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
    #     # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia

    #     if q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']>0:
    #         suhde=max(0,q['ansiopvraha_netto']/(q['puoliso_ansiopvraha_netto']+q['ansiopvraha_netto']))
    #         q['ansiopvraha_nettonetto']=q['ansiopvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
    #         q['puoliso_ansiopvraha_nettonetto']=q['puoliso_ansiopvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
    #     else:
    #         q['ansiopvraha_nettonetto']=0
    #         q['puoliso_ansiopvraha_nettonetto']=0

    #     if p['opiskelija']>0 or p['ei_toimeentulotukea']>0:
    #         q['toimeentulotuki']=0
    #     else:
    #         q['toimeentulotuki']=self.toimeentulotuki(p['t'],q['verot_ilman_etuuksia'],p['puoliso_tulot'],q['puoliso_verot_ilman_etuuksia'],\
    #             q['elatustuki']+q['opintotuki_netto']+q['puoliso_opintotuki_netto']+q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
    #             +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto']+q['puoliso_kotihoidontuki_netto'],\
    #             0,p['asumismenot_toimeentulo'],q['pvhoito'],p['aikuisia'],p['lapsia'],p['kuntaryhma'],p)

    #     kateen=q['opintotuki']+q['kokoelake']+p['puoliso_tulot']+p['t']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
    #         +q['ansiopvraha']+q['puoliso_ansiopvraha']+q['elatustuki']-q['puoliso_verot']-q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']
    #     omanetto=q['opintotuki']+q['kokoelake']+p['t']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']\
    #         +q['ansiopvraha']+q['elatustuki']-q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']
            
    #     q['kateen']=kateen # tulot yhteensä perheessä
    #     q['perhetulot_netto']=p['puoliso_tulot']+p['t']-q['verot_ilman_etuuksia']-q['puoliso_verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
    #     q['omattulot_netto']=p['t']-q['verot_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'] # ilman etuuksia
    #     q['etuustulo_netto']=q['ansiopvraha_netto']+q['puoliso_ansiopvraha_netto']+q['opintotuki']\
    #         +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
    #         +q['toimeentulotuki']-(q['pvhoito_ilman_etuuksia']-q['pvhoito_ilman_etuuksia'])
    #     q['etuustulo_brutto']=q['ansiopvraha']+q['puoliso_ansiopvraha']+q['opintotuki']\
    #         +q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
    #         +q['toimeentulotuki']+q['kokoelake']
    #     q['brutto']=q['etuustulo_brutto']+p['t']+p['puoliso_tulot']
            
    #     #if p['aikuisia']>1 and False:
    #     #    asumismeno=0.5*p['asumismenot_asumistuki']
    #     #else:
    #     asumismeno=p['asumismenot_asumistuki']
            
    #     q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        
    #     # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
    #     q['netto']=max(0,kateen-q['alv'])
    #     #q['netto']=max(0,omanetto-q['alv']-asumismeno)
        
    #     if not legacy:
    #         kateen=q['netto']
        
    #     q['palkkatulot']=p['t']
    #     if p['elakkeella']<1:
    #         q['palkkatulot_eielakkeella']=p['t']
    #     else:
    #         q['palkkatulot_eielakkeella']=0
            
    #     q['puoliso_palkkatulot']=p['puoliso_tulot']
    #     q['puoliso_tulot_netto']=p['puoliso_tulot']-q['puoliso_verot_ilman_etuuksia']
    #     q['perustulo']=0
    #     q['puoliso_perustulo']=0
    #     q['perustulo_netto']=0
    #     q['puoliso_perustulo_netto']=0
    #     q['perustulo_nettonetto']=0
    #     q['puoliso_perustulo_nettonetto']=0

    #     return kateen,q
        
    def setup_puoliso_q(self,p: dict,q: dict,puoliso: str='puoliso_',alku: str='puoliso_',
                        include_takuuelake: bool=True,add_kansanelake: bool=True) -> dict:
        '''
        add_kansanelake tarkoittaa, että kansaneläke lasketaan maksussa olevan eläkkeen lisäksi
        '''
        q[puoliso+'multiplier']=1
        q[puoliso+'perustulo']=0
        q[puoliso+'puhdas_tyoelake']=0
        q[puoliso+'kansanelake']=0
        q[puoliso+'tyoelake']=0
        q[puoliso+'takuuelake']=0
            
        q[puoliso+'perustulo']=0
        q[puoliso+'perustulo_netto']=0
        q[puoliso+'perustulo_nettonetto']=0
        q[puoliso+'joustava_hoitoraha']=0
        
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
                #q[puoliso+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[puoliso+'elake_maksussa'],include_takuuelake=include_takuuelake,yksin=0,
                #                            disability=p[puoliso+'disabled'],lapsia=p['lapsikorotus_lapsia'],add_kansanelake=add_kansanelake)
                q[puoliso+'kokoelake']=self.laske_kokonaiselake_v2(p['ika'],q[puoliso+'tyoelake'],q[puoliso+'kansanelake'],include_takuuelake=include_takuuelake,yksin=0,
                                            disability=p[puoliso+'disabled'],lapsia=p['lapsikorotus_lapsia'],add_kansanelake=add_kansanelake)
                q[puoliso+'takuuelake']=q[puoliso+'kokoelake']-q[puoliso+'elake_maksussa']
                q[puoliso+'ansiopvraha'],q[puoliso+'tyotpvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'opintotuki']=0
                q[puoliso+'puhdas_tyoelake']=self.laske_puhdas_tyoelake_v2(p['ika'],q[puoliso+'tyoelake'],q[puoliso+'kansanelake'],disability=p[alku+'disabled'],yksin=0,lapsia=p['lapsia'])
            elif p[alku+'opiskelija']>0:
                q[puoliso+'kokoelake']=p[alku+'tyoelake']
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'tyoelake']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                q[puoliso+'ansiopvraha'],q[puoliso+'tyotpvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                q[puoliso+'opintotuki']=0
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'isyysvapaa_kesto'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
                else:
                    q[puoliso+'opintotuki']=self.opintoraha(0,p['lapsia'])
            else: # ei eläkkeellä     
                q[puoliso+'kokoelake']=p[alku+'tyoelake']
                q[puoliso+'opintotuki']=0
                q[puoliso+'elake_maksussa']=p[alku+'tyoelake']
                q[puoliso+'tyoelake']=p[alku+'tyoelake']
                q[puoliso+'elake_tuleva']=0
                q[puoliso+'ansiopvraha'],q[puoliso+'tyotpvraha'],q[puoliso+'peruspvraha']=(0,0,0)
                q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
                if p[alku+'aitiysvapaalla']>0:
                    q[puoliso+'aitiyspaivaraha']=self.aitiysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
                elif p[alku+'isyysvapaalla']>0:
                    q[puoliso+'isyyspaivaraha']=self.isyysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'isyysvapaa_kesto'])
                elif p[alku+'sairauspaivarahalla']>0:
                    q[puoliso+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'t'],p[alku+'vakiintunutpalkka'])
                elif p[alku+'kotihoidontuella']>0:
                    q[puoliso+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
                elif p[alku+'tyoton']>0:
                    q[puoliso+'tyotpvraha'],q[puoliso+'ansiopvraha'],q[puoliso+'peruspvraha']=\
                        self.ansiopaivaraha(p[alku+'tyoton'],p[alku+'vakiintunutpalkka'],p['lapsikorotus_lapsia'],p[alku+'t'],
                            p[alku+'saa_ansiopaivarahaa'],p[alku+'tyottomyyden_kesto'],p,alku=alku)
                else: # työssä
                    if self.include_joustavahoitoraha:
                        q[puoliso+'joustava_hoitoraha']=self.joustavahoitoraha(p[alku+'tyoaika'],p['lapsia_alle_3v'])
        else:
            q[puoliso+'kokoelake']=0
            q[puoliso+'opintotuki']=0
            q[puoliso+'elake_maksussa']=0
            q[puoliso+'tyoelake']=0
            q[puoliso+'elake_tuleva']=0
            q[puoliso+'ansiopvraha'],q[puoliso+'tyotpvraha'],q[puoliso+'peruspvraha']=(0,0,0)
            q[puoliso+'isyyspaivaraha'],q[puoliso+'aitiyspaivaraha'],q[puoliso+'kotihoidontuki'],q[puoliso+'sairauspaivaraha']=(0,0,0,0)
            q[puoliso+'palkkatulot']=0
            q[puoliso+'palkkatulot_eielakkeella']=0
                
        return q
        
    def setup_omat_q(self,p: dict,omat: str='omat_',alku: str='',include_takuuelake: bool=True,add_kansanelake: bool=True):
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
        q[omat+'joustava_hoitoraha']=0
        
        if p[alku+'elakkeella']<1 and p[alku+'alive']>0:
            q[omat+'palkkatulot_eielakkeella']=p[alku+'t']
        else:
            q[omat+'palkkatulot_eielakkeella']=0
            
        if p[alku+'alive']<1:
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'elake_maksussa'],q[omat+'tyoelake'],q[omat+'kansanelake'],q[omat+'elake_tuleva']=0,0,0,0
            q[omat+'ansiopvraha'],q[omat+'tyotpvraha'],q[omat+'peruspvraha']=(0,0,0)
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
                #q[omat+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[omat+'elake_maksussa'],yksin=0,include_takuuelake=include_takuuelake,
                #                            disability=p[alku+'disabled'],lapsia=p['lapsikorotus_lapsia'],add_kansanelake=add_kansanelake)
                q[omat+'kokoelake']=self.laske_kokonaiselake_v2(p['ika'],q[omat+'tyoelake'],q[omat+'kansanelake'],yksin=0,include_takuuelake=include_takuuelake,
                                            disability=p[alku+'disabled'],lapsia=p['lapsikorotus_lapsia'],add_kansanelake=add_kansanelake)
                q[omat+'takuuelake']=q[omat+'kokoelake']-q[omat+'elake_maksussa']
                q[omat+'puhdas_tyoelake']=self.laske_puhdas_tyoelake_v2(p['ika'],q[omat+'tyoelake'],q[omat+'kansanelake'],
                                            disability=p[alku+'disabled'],yksin=0,lapsia=p['lapsia'])
            else:
                #[omat+'kokoelake']=self.laske_kokonaiselake(p['ika'],q[omat+'elake_maksussa'],yksin=1,include_takuuelake=include_takuuelake,
                #                            disability=p[alku+'disabled'],lapsia=p['lapsikorotus_lapsia'],add_kansanelake=add_kansanelake)
                q[omat+'kokoelake']=self.laske_kokonaiselake_v2(p['ika'],q[omat+'tyoelake'],q[omat+'kansanelake'],yksin=1,include_takuuelake=include_takuuelake,
                                            disability=p[alku+'disabled'],lapsia=p['lapsikorotus_lapsia'],add_kansanelake=add_kansanelake)
                q[omat+'takuuelake']=q[omat+'kokoelake']-q[omat+'elake_maksussa']
                q[omat+'puhdas_tyoelake']=self.laske_puhdas_tyoelake_v2(p['ika'],q[omat+'tyoelake'],q[omat+'kansanelake'],
                                            disability=p[alku+'disabled'],yksin=1,lapsia=p['lapsia'])

            q[omat+'ansiopvraha'],q[omat+'tyotpvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'opintotuki']=0
        elif p[alku+'opiskelija']>0:
            q[omat+'elake_maksussa']=p[alku+'elake_maksussa']
            q[omat+'kokoelake']=p[alku+'tyoelake']
            q[omat+'tyoelake']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            q[omat+'ansiopvraha'],q[omat+'tyotpvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            q[omat+'opintotuki']=0
            if p[alku+'aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p[alku+'isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'isyysvapaa_kesto'])
            elif p[alku+'kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            else:
                q[omat+'opintotuki']=self.opintoraha(0,p['lapsia'])
        else: # ei eläkkeellä     
            q[omat+'opintotuki']=0
            q[omat+'elake_maksussa']=p[alku+'elake_maksussa']
            q[omat+'kokoelake']=p[alku+'tyoelake']
            q[omat+'tyoelake']=p[alku+'tyoelake']
            q[omat+'elake_tuleva']=0
            q[omat+'ansiopvraha'],q[omat+'tyotpvraha'],q[omat+'peruspvraha']=(0,0,0)
            q[omat+'isyyspaivaraha'],q[omat+'aitiyspaivaraha'],q[omat+'kotihoidontuki'],q[omat+'sairauspaivaraha']=(0,0,0,0)
            if p[alku+'aitiysvapaalla']>0:
                q[omat+'aitiyspaivaraha']=self.aitiysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'aitiysvapaa_kesto'])
            elif p[alku+'isyysvapaalla']>0:
                q[omat+'isyyspaivaraha']=self.isyysraha(p[alku+'t'],p[alku+'vakiintunutpalkka'],p[alku+'isyysvapaa_kesto'])
            elif p[alku+'sairauspaivarahalla']>0:
                q[omat+'sairauspaivaraha']=self.sairauspaivaraha(p[alku+'t'],p[alku+'vakiintunutpalkka'])
            elif p[alku+'kotihoidontuella']>0:
                q[omat+'kotihoidontuki']=self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],p['lapsia_alle_kouluikaisia'])
            elif p['tyoton']>0:
                if alku+'omavastuukerroin' in p:
                    omavastuukerroin=p[alku+'omavastuukerroin']
                else:
                    omavastuukerroin=1.0
                q[omat+'tyotpvraha'],q[omat+'ansiopvraha'],q[omat+'peruspvraha']=\
                    self.ansiopaivaraha(p[alku+'tyoton'],p[alku+'vakiintunutpalkka'],p['lapsikorotus_lapsia'],p[alku+'t'],
                        p[alku+'saa_ansiopaivarahaa'],p[alku+'tyottomyyden_kesto'],p,omavastuukerroin=omavastuukerroin,alku=omat)
            else: # työssä
                if self.include_joustavahoitoraha:
                    q[omat+'joustava_hoitoraha']=self.joustavahoitoraha(p[alku+'tyoaika'],p['lapsia_alle_3v'])

        return q        
        
    def summaa_q(self,p: dict,q: dict,omat: str='omat_',puoliso: str='puoliso_'):
        if p['aikuisia']>1:
            q['verot']=q[omat+'verot']+q[puoliso+'verot']
            q['ptel']=q[omat+'ptel']+q[puoliso+'ptel']
            q['kunnallisvero']=q[omat+'kunnallisvero']+q[puoliso+'kunnallisvero']
            q['valtionvero']=q[omat+'valtionvero']+q[puoliso+'valtionvero']
            q['verot_ilman_etuuksia']=q[omat+'verot_ilman_etuuksia']+q[puoliso+'verot_ilman_etuuksia']
            q['tyotvakmaksu']=q[omat+'tyotvakmaksu']+q[puoliso+'tyotvakmaksu']
            q['ansiopvraha']=q[puoliso+'ansiopvraha']+q[omat+'ansiopvraha']
            q['tyotpvraha']=q[puoliso+'tyotpvraha']+q[omat+'tyotpvraha']
            q['peruspvraha']=q[puoliso+'peruspvraha']+q[omat+'peruspvraha']
            q['elake_maksussa']=q[puoliso+'elake_maksussa']+q[omat+'elake_maksussa']
            q['opintotuki']=q[puoliso+'opintotuki']+q[omat+'opintotuki']
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
            q['palkkatulot']=q[omat+'palkkatulot']+q[puoliso+'palkkatulot']
            q['palkkatulot_eielakkeella']=q[puoliso+'palkkatulot_eielakkeella']+q[omat+'palkkatulot_eielakkeella']
            q['perustulo_netto']=q[omat+'perustulo_netto']+q[puoliso+'perustulo_netto']
            q['perustulo_nettonetto']=q[omat+'perustulo_nettonetto']+q[puoliso+'perustulo_nettonetto']
            q['ansiotulovahennys']=q[omat+'ansiotulovahennys']+q[puoliso+'ansiotulovahennys']
            q['perusvahennys']=q[omat+'perusvahennys']+q[puoliso+'perusvahennys']
            q['tyotulovahennys']=q[omat+'tyotulovahennys']+q[puoliso+'tyotulovahennys']
            q['kunnallisveroperuste']=q[omat+'kunnallisveroperuste']+q[puoliso+'kunnallisveroperuste']
            q['valtionveroperuste']=q[omat+'valtionveroperuste']+q[puoliso+'valtionveroperuste']
        else:
            q['verot']=q[omat+'verot']
            q['ptel']=q[omat+'ptel']
            q['kunnallisvero']=q[omat+'kunnallisvero']
            q['valtionvero']=q[omat+'valtionvero']
            q['verot_ilman_etuuksia']=q[omat+'verot_ilman_etuuksia']
            q['tyotvakmaksu']=q[omat+'tyotvakmaksu']
            q['ansiopvraha']=q[omat+'ansiopvraha']
            q['tyotpvraha']=q[omat+'tyotpvraha']
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
            q['elatustuki']=q[omat+'elatustuki']
            q['perustulo']=q[omat+'perustulo']
            q['palkkatulot']=q[omat+'palkkatulot']
            q['palkkatulot_eielakkeella']=q[omat+'palkkatulot_eielakkeella']
            q['perustulo_netto']=q[omat+'perustulo_netto']
            q['perustulo_nettonetto']=q[omat+'perustulo_nettonetto']
            q['ansiotulovahennys']=q[omat+'ansiotulovahennys']
            q['perusvahennys']=q[omat+'perusvahennys']
            q['tyotulovahennys']=q[omat+'tyotulovahennys']
            q['kunnallisveroperuste']=q[omat+'kunnallisveroperuste']
            q['valtionveroperuste']=q[omat+'valtionveroperuste']
        
        return q
        
    def laske_tulot_v3(self,p: dict,tt_alennus=0,include_takuuelake: bool=True,omat: str='omat_',omatalku: str='',puoliso: str='puoliso_',puolisoalku: str='puoliso_',
        include_alv: bool=True,split_costs: bool=True,set_equal: bool=False,add_kansanelake: bool=True):
        '''
        v4:ää varten tehty tulonlaskenta
        - eroteltu paremmin omat ja puolison tulot ja etuudet 
        - perusmuuttujat ovat summamuuttujia
        
        - netto -muuttujat ovat verot vähennettynä
        - nettonetto -muuttujista myös pvhoito (ja alv) pois
        '''
        self.check_p(p)

        aikuisia=p['aikuisia']
        lapsia=p['lapsia']

        q=self.setup_omat_q(p,omat=omat,alku=omatalku,include_takuuelake=include_takuuelake,add_kansanelake=add_kansanelake)
        q=self.setup_puoliso_q(p,q,puoliso=puoliso,alku=puolisoalku,include_takuuelake=include_takuuelake,add_kansanelake=add_kansanelake)
        
        # q['verot] sisältää kaikki veronluonteiset maksut
        _,q[omat+'verot'],q[omat+'valtionvero'],q[omat+'kunnallisvero'],q[omat+'kunnallisveroperuste'],q[omat+'valtionveroperuste'],\
            q[omat+'ansiotulovahennys'],q[omat+'perusvahennys'],q[omat+'tyotulovahennys'],q[omat+'tyotulovahennys_kunnallisveroon'],\
            q[omat+'ptel'],q[omat+'sairausvakuutusmaksu'],q[omat+'tyotvakmaksu'],q[omat+'tyel_kokomaksu'],q[omat+'ylevero']=\
            self.verotus(q[omat+'palkkatulot'],q[omat+'tyotpvraha']+q[omat+'aitiyspaivaraha']+q[omat+'isyyspaivaraha']\
                +q[omat+'kotihoidontuki']+q[omat+'sairauspaivaraha']+q[omat+'opintotuki'],
                q[omat+'kokoelake'],lapsia,p,alku=omatalku)
        _,q[omat+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(p['t'],0,0,lapsia,p,alku=omatalku)
        if q[omat+'kokoelake']>0:
            _,q[omat+'verot_vain_elake'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(0,0,q[omat+'kokoelake'],lapsia,p,alku=omatalku)
        else:
            q[omat+'verot_vain_elake']=0

        if aikuisia>1 and p[puoliso+'alive']>0:
            _,q[puoliso+'verot'],q[puoliso+'valtionvero'],q[puoliso+'kunnallisvero'],q[puoliso+'kunnallisveroperuste'],q[puoliso+'valtionveroperuste'],\
            q[puoliso+'ansiotulovahennys'],q[puoliso+'perusvahennys'],q[puoliso+'tyotulovahennys'],q[puoliso+'tyotulovahennys_kunnallisveroon'],\
            q[puoliso+'ptel'],q[puoliso+'sairausvakuutusmaksu'],q[puoliso+'tyotvakmaksu'],q[puoliso+'tyel_kokomaksu'],q[puoliso+'ylevero']=\
                self.verotus(q[puoliso+'palkkatulot'],
                    q[puoliso+'tyotpvraha']+q[puoliso+'aitiyspaivaraha']+q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'sairauspaivaraha']+q[puoliso+'opintotuki'],
                    q[puoliso+'kokoelake'],0,p,alku=puoliso) # onko oikein että lapsia 0 tässä????
            _,q[puoliso+'verot_ilman_etuuksia'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(q[puoliso+'palkkatulot'],0,0,0,p,alku=puoliso)
            if q[puoliso+'kokoelake']>0:
                _,q[puoliso+'verot_vain_elake'],_,_,_,_,_,_,_,_,_,_,_,_,_=self.verotus(0,0,q[puoliso+'kokoelake'],lapsia,p,alku=omatalku)
            else:
                q[puoliso+'verot_vain_elake']=0
        else:
            q[puoliso+'verot_ilman_etuuksia'],q[puoliso+'verot'],q[puoliso+'valtionvero']=0,0,0
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
        if aikuisia==1 and p['saa_elatustukea']>0 and p[omatalku+'alive']>0:
            q[omat+'elatustuki']=self.laske_elatustuki(lapsia,aikuisia)
        else:
            q[omat+'elatustuki']=0
        
        q[puoliso+'elatustuki']=0
        
        q=self.summaa_q(p,q,omat=omat,puoliso=puoliso)
        
        if q['kotihoidontuki']>0:
            hoitol = self.hoitolisa(aikuisia+lapsia,q['palkkatulot']+q['tyotpvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['sairauspaivaraha']+q['opintotuki'])
            q['kotihoidontuki'] += hoitol
            if q[omat+'kotihoidontuki']>0:
                q[omat+'kotihoidontuki'] += hoitol
            else:
                q[puoliso+'kotihoidontuki'] += hoitol

        if q[puoliso+'joustava_hoitoraha']>0:
            q[puoliso+'kotihoidontuki'] += q[puoliso+'joustava_hoitoraha']
            q['kotihoidontuki'] += q[puoliso+'joustava_hoitoraha']
        if q[omat+'joustava_hoitoraha']>0:
            q[omat+'kotihoidontuki'] += q[omat+'joustava_hoitoraha']
            q['kotihoidontuki'] += q[omat+'joustava_hoitoraha']

        if p[puolisoalku+'alive']<1 and p[omatalku+'alive']<1: # asumistuki nolla, jos kumpikaan ei hengissä
            q['asumistuki'] = 0
        elif p[omatalku+'elakkeella']>0 and p[puolisoalku+'elakkeella']>0: # eläkkeensaajan asumistuki vain, jos molemmat eläkkeellä
            q['asumistuki']=self.elakkeensaajan_asumistuki(q['palkkatulot'],q['kokoelake'],p['asumismenot_asumistuki'],aikuisia,p['kuntaryhma'],p,puolisolla_oikeus=False)
        elif p[omatalku+'elakkeella']>0 or p[puolisoalku+'elakkeella']>0: # eläkkeensaajan asumistuki vain, jos toinen eläkkeellä
            q['asumistuki']=self.elakkeensaajan_asumistuki(q['palkkatulot'],q['kokoelake'],p['asumismenot_asumistuki'],aikuisia,p['kuntaryhma'],p,puolisolla_oikeus=True)
        else: # muuten yleinen asumistuki
            q['asumistuki']=self.asumistuki(q[omat+'palkkatulot'],q[puoliso+'palkkatulot'],q['tyotpvraha']+q['aitiyspaivaraha']+q['isyyspaivaraha']
                                            +q['kotihoidontuki']+q['sairauspaivaraha']+q['opintotuki'],
                                            p['asumismenot_asumistuki'],aikuisia,lapsia,p['kuntaryhma'],p)
            
        if lapsia>0:
            if aikuisia>1:
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
                q['pvhoito']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],q['palkkatulot']+q['kokoelake']+q['elatustuki']+q['tyotpvraha']+q['sairauspaivaraha'],aikuisia,lapsia,p)
                #if (p['lapsia_kotihoidontuella']>0):
                #    alle_kouluikaisia=max(0,p['lapsia_kotihoidontuella']-p['lapsia_alle_3v'])
                #    q['pvhoito']=max(0,q['pvhoito']-self.kotihoidontuki(p['lapsia_kotihoidontuella'],p['lapsia_alle_3v'],alle_kouluikaisia)) # ok?
                q['pvhoito_ilman_etuuksia']=11/12*self.paivahoitomenot(p['lapsia_paivahoidossa'],p[puolisoalku+'t']+p[omatalku+'t']+q['elatustuki'],aikuisia,lapsia,p)
                #if p['lapsia_paivahoidossa']>0:
                #    print('pv',q['pvhoito'],'lapsia',p['lapsia_paivahoidossa'],'t',q['palkkatulot'],'etuus',q['kokoelake']+q['elatustuki']+q['tyotpvraha']+q['sairauspaivaraha'])
                
            if aikuisia==1:
                yksinhuoltajakorotus=1
            else:
                yksinhuoltajakorotus=0
            q['lapsilisa']=self.laske_lapsilisa(lapsia,yksinhuoltajakorotus=yksinhuoltajakorotus)
        else:
            q['pvhoito']=0
            q['pvhoito_ilman_etuuksia']=0
            q['lapsilisa']=0
    
        # lasketaan netotettu ansiopäiväraha huomioiden verot (kohdistetaan ansiopvrahaan se osa veroista, joka ei aiheudu palkkatuloista)
        self.update_netto(p,q,omat,puoliso,omatalku,puolisoalku)
            
        if (p[omatalku+'isyysvapaalla']>0 or p[omatalku+'aitiysvapaalla']>0) and p[omatalku+'tyoton']>0:
            print('error: vanhempainvapaalla & työtön ei toteutettu')
        if (p[puolisoalku+'isyysvapaalla']>0 or p[puolisoalku+'aitiysvapaalla']>0) and p[puolisoalku+'tyoton']>0:
            print('error: vanhempainvapaalla & työtön ei toteutettu')
    
        # jaetaan ilman etuuksia laskettu pvhoitomaksu puolisoiden kesken ansiopäivärahan suhteessa
        # eli kohdistetaan päivähoitomaksun korotus ansiopäivärahan mukana
        # ansiopäivärahaan miten huomioitu päivähoitomaksussa, ilman etuuksia

        self.update_toimeentulotuki(p,q,omat,puoliso,omatalku,puolisoalku)

        # sisältää sekä omat että puolison tulot ja menot
        kateen=q['opintotuki']+q['kokoelake']+q['palkkatulot']+q['aitiyspaivaraha']+q['isyyspaivaraha']\
            +q['kotihoidontuki']+q['asumistuki']+q['toimeentulotuki']+q['tyotpvraha']+q['elatustuki']\
            -q['verot']-q['pvhoito']+q['lapsilisa']+q['sairauspaivaraha']

        brutto_omat=q[omat+'opintotuki']+q[omat+'kokoelake']+q[omat+'palkkatulot']+q[omat+'aitiyspaivaraha']\
            +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+\
            +q[omat+'tyotpvraha']+q[omat+'elatustuki']+q[omat+'sairauspaivaraha']
        kateen_omat=brutto_omat-q[omat+'verot']
        etuusnetto_omat=brutto_omat-q[omat+'palkkatulot']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])
                
        if aikuisia>1:
            brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
                +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                +q[puoliso+'tyotpvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']
            kateen_puoliso=brutto_puoliso-q[puoliso+'verot']
            etuusnetto_puoliso=brutto_puoliso-q[puoliso+'palkkatulot']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])
        else:
            brutto_puoliso=0
            kateen_puoliso=0
            etuusnetto_puoliso=0

        q['kateen']=kateen # tulot yhteensä perheessä
        q['etuustulo_netto']=q['tyotpvraha']+q['opintotuki']+q['aitiyspaivaraha']+q['isyyspaivaraha']+q['kotihoidontuki']+q['asumistuki']\
            +q['toimeentulotuki']+q['kokoelake']+q['elatustuki']+q['lapsilisa']+q['sairauspaivaraha']\
            -(q['pvhoito']-q['pvhoito_ilman_etuuksia'])-(q['verot']-q['verot_ilman_etuuksia'])
        #q['etuustulo_nettonetto']=q['etuustulo_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
            
        asumismeno=p['asumismenot_asumistuki']
        q['asumismeno']=asumismeno
            
        if include_alv:
            q['alv']=self.laske_alv(max(0,kateen-asumismeno)) # vuokran ylittävä osuus tuloista menee kulutukseen
        else:
            q['alv']=0
        
        # nettotulo, joka huomioidaan elinkaarimallissa alkaen versiosta 4. sisältää omat tulot ja puolet vuokrasta
        q['netto']=max(0,kateen-q['alv'])
        
        if split_costs: # näitä ei tarvita unemp-moduleihin, vain kannuste-laskelmiin
            self.split_cost_to_wage_unemp(p,q,omat,puoliso,omatalku,puolisoalku)
         
            if aikuisia>1:
                if kateen_puoliso+kateen_omat<1e-6:
                    suhde=0.5
                else: # jaetaan bruttotulojen suhteessa, mutta tasoitetaan eroja
                    suhde = kateen_omat/(kateen_puoliso+kateen_omat)
                    summa = q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito']
                    if summa >= 0: 
                        suhde = 0.5
                    elif (summa < 0) and (summa + kateen_puoliso+kateen_omat > 0):
                        suhde = kateen_omat/(kateen_puoliso+kateen_omat)
                    else:
                        print("ONGELMA: q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'] > kateen_puoliso+kateen_omat",summa, kateen_puoliso+kateen_omat)
                        suhde = 0.5

                    #if kateen_omat>kateen_puoliso:
                    #    if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0: 
                    #        suhde = kateen_puoliso/(kateen_puoliso+kateen_omat)
                    #    else:
                    #        suhde = kateen_omat/(kateen_puoliso+kateen_omat)
                    #else:
                    #    if (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-q['alv']-q['pvhoito'])>0:
                    #        suhde = kateen_puoliso/(kateen_puoliso+kateen_omat)
                    #    else:
                    #        suhde = kateen_omat/(kateen_puoliso+kateen_omat)
                
                etuusnetto_omat += (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
                kateen_omat += (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
                brutto_omat += (q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*suhde
                if kateen_omat>0:
                    r2=etuusnetto_omat/kateen_omat
                else:
                    r2=1
                
                q[omat+'toimeentulotuki'] = q['toimeentulotuki']*suhde
                q[omat+'asumistuki'] = q['asumistuki']*suhde
                q[omat+'lapsilisa'] = q['lapsilisa']*suhde

                if etuusnetto_omat>0:
                    r_t_e=q[omat+'toimeentulotuki']/etuusnetto_omat
                    r_a_e=q[omat+'asumistuki']/etuusnetto_omat
                    r_tt_e=q[omat+'tyotpvraha_nettonetto']/etuusnetto_omat
                    r_tt_l=q[omat+'lapsilisa']/etuusnetto_omat
                    r_tt_ko=q[omat+'kokoelake_netto']/etuusnetto_omat
                    r_tt_op=q[omat+'opintotuki_netto']/etuusnetto_omat
                    r_ko=q[omat+'kotihoidontuki_netto']/etuusnetto_omat
                    r_e=q[omat+'elatustuki']/etuusnetto_omat
                else:
                    r_t_e=0
                    r_a_e=0
                    r_tt_e=0
                    r_tt_l=0
                    r_tt_ko=0
                    r_tt_op=0
                    r_ko=0
                    r_e=0
            
                etuusnetto_omat += (-r2*(q['alv']+q['pvhoito']))*suhde
                kateen_omat += (-q['alv']-q['pvhoito'])*suhde
                q[omat+'palkkatulot_nettonetto'] += -(1-r2)*q['alv']*suhde
                omat_alv = q['alv']*suhde*r2
                q[omat+'toimeentulotuki_nettonetto'] = q[omat+'toimeentulotuki']-r_t_e*omat_alv
                q[omat+'asumistuki_nettonetto'] = q[omat+'asumistuki']-r_a_e*omat_alv
                q[omat+'tyotpvraha_nettonetto'] += -r_tt_e*omat_alv
                q[omat+'opintotuki_nettonetto'] = q[omat+'opintotuki_netto']-r_tt_op*omat_alv
                q[omat+'kokoelake_nettonetto'] = q[omat+'kokoelake_netto']-r_tt_ko*omat_alv
                q[omat+'kotihoidontuki_nettonetto'] = q[omat+'kotihoidontuki_netto']-r_ko*omat_alv
                q[omat+'elatustuki_nettonetto'] = q[omat+'elatustuki']-r_e*omat_alv
                q[omat+'lapsilisa_nettonetto'] = q[omat+'lapsilisa']-r_tt_l*omat_alv
                q[omat+'pvhoito'] = q['pvhoito']*suhde
                q[omat+'alv'] = q['alv']*suhde
            
                etuusnetto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
                kateen_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
                brutto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki'])*(1-suhde)
                if kateen_puoliso>0:
                    r2=etuusnetto_puoliso/kateen_puoliso
                else:
                    r2=1
                
                q[puoliso+'toimeentulotuki'] = q['toimeentulotuki']*(1-suhde)
                q[puoliso+'asumistuki'] = q['asumistuki']*(1-suhde)
                q[puoliso+'lapsilisa'] = q['lapsilisa']*(1-suhde)
                if etuusnetto_puoliso>0:
                    r_t_e = q[puoliso+'toimeentulotuki']/etuusnetto_puoliso
                    r_a_e = q[puoliso+'asumistuki']/etuusnetto_puoliso
                    r_tt_e = q[puoliso+'tyotpvraha_nettonetto']/etuusnetto_puoliso
                    r_tt_l = q[puoliso+'lapsilisa']/etuusnetto_puoliso
                    r_tt_ko = q[puoliso+'kokoelake_netto']/etuusnetto_puoliso
                    r_tt_op = q[puoliso+'opintotuki_netto']/etuusnetto_puoliso
                    r_ko = q[puoliso+'kotihoidontuki_netto']/etuusnetto_puoliso
                    r_e = q[puoliso+'elatustuki']/etuusnetto_puoliso
                else:
                    r_t_e=0
                    r_a_e=0
                    r_tt_e=0
                    r_tt_l=0
                    r_tt_ko=0
                    r_tt_op=0
                    r_ko=0
                    r_e=0

                #etuusnetto_puoliso+=(q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']-r2*(q['alv']+q['pvhoito']))*(1-suhde)
                etuusnetto_puoliso += (-r2*(q['alv']+q['pvhoito']))*(1-suhde)
                kateen_puoliso += (-q['alv']-q['pvhoito'])*(1-suhde)
                puoliso_alv = q['alv']*(1-suhde)*r2
                q[puoliso+'palkkatulot_nettonetto']+=-(1-r2)*q['alv']*(1-suhde)
                q[puoliso+'toimeentulotuki_nettonetto']=q[puoliso+'toimeentulotuki']-r_t_e*puoliso_alv
                q[puoliso+'asumistuki_nettonetto']=q[puoliso+'asumistuki']-r_a_e*puoliso_alv
                q[puoliso+'tyotpvraha_nettonetto']+=-r_tt_e*puoliso_alv
                q[puoliso+'kokoelake_nettonetto']=q[puoliso+'kokoelake_netto']-r_tt_ko*puoliso_alv
                q[puoliso+'opintotuki_nettonetto']=q[puoliso+'opintotuki_netto']-r_tt_op*puoliso_alv
                q[puoliso+'kotihoidontuki_nettonetto']=q[puoliso+'kotihoidontuki_netto']-r_ko*puoliso_alv
                q[puoliso+'elatustuki_nettonetto']=q[puoliso+'elatustuki']-r_e*puoliso_alv
                q[puoliso+'lapsilisa_nettonetto']=q[puoliso+'lapsilisa']-r_tt_l*puoliso_alv
                q[puoliso+'pvhoito']=q['pvhoito']*(1-suhde)
                q[puoliso+'alv']=q['alv']*(1-suhde)

                if set_equal:
                    puolet=0.5*(kateen_omat+kateen_puoliso)
                    kateen_omat=puolet
                    kateen_puoliso=puolet
            
                #if kateen_puoliso<1e-6:
                #    print(kateen_omat,kateen_puoliso)
            else:
                kateen_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                brutto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                etuusnetto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                if kateen_omat>0:
                    r2=etuusnetto_omat/kateen_omat
                else:
                    r2=1
                
                q[omat+'toimeentulotuki']=q['toimeentulotuki']
                q[omat+'asumistuki']=q['asumistuki']
                q[omat+'lapsilisa']=q['lapsilisa']
                q[puoliso+'toimeentulotuki']=0
                q[puoliso+'asumistuki']=0
                q[puoliso+'lapsilisa']=0
                
                kateen_omat += -q['alv']-q['pvhoito']

                if etuusnetto_omat>0:
                    r_t_e=q['toimeentulotuki']/etuusnetto_omat
                    r_a_e=q['asumistuki']/etuusnetto_omat
                    r_tt_e=q['tyotpvraha_nettonetto']/etuusnetto_omat
                    r_tt_l=q['lapsilisa']/etuusnetto_omat
                    r_tt_el=q['elatustuki']/etuusnetto_omat
                    r_tt_op=q['opintotuki']/etuusnetto_omat
                    r_tt_ko=q['kokoelake']/etuusnetto_omat
                    r_ko=q[omat+'kotihoidontuki_netto']/etuusnetto_omat
                    r_e=q[omat+'elatustuki']/etuusnetto_omat
                else:
                    r_t_e=0
                    r_a_e=0
                    r_tt_e=0
                    r_tt_l=0
                    r_tt_el=0
                    r_tt_op=0
                    r_tt_ko=0
                    r_ko=0
                    r_e=0
            
                etuusnetto_omat+=-r2*(q['alv']+q['pvhoito'])
                q[omat+'palkkatulot_nettonetto']+=-(1-r2)*q['alv']
                q[omat+'toimeentulotuki_nettonetto']=q[omat+'toimeentulotuki']-r_t_e*q['alv']*r2
                q[omat+'asumistuki_nettonetto']=q[omat+'asumistuki']-r_a_e*q['alv']*r2
                q[omat+'tyotpvraha_nettonetto']+=-r_tt_e*q['alv']*r2
                q[omat+'opintotuki_nettonetto']=q[omat+'opintotuki_netto']-r_tt_op*q['alv']*r2
                q[omat+'kokoelake_nettonetto']=q[omat+'kokoelake_netto']-r_tt_ko*q['alv']*r2
                q[omat+'elatustuki_nettonetto']=q[omat+'elatustuki']-r_e*q['alv']*r2
                q[omat+'pvhoito']=q['pvhoito']
                q[omat+'kotihoidontuki_nettonetto']=q[omat+'kotihoidontuki_netto']-r_ko*q['alv']*r2
                q[omat+'lapsilisa_nettonetto']=q[omat+'lapsilisa']-r_tt_l*q['alv']*r2            
                q[omat+'alv']=q['alv']
                
                kateen_puoliso=0
                brutto_puoliso=0
                etuusnetto_puoliso=0
                q[puoliso+'palkkatulot_nettonetto']=0
                q[puoliso+'toimeentulotuki_nettonetto']=0
                q[puoliso+'asumistuki_nettonetto']=0
                q[puoliso+'pvhoito']=0
                q[puoliso+'lapsilisa_nettonetto']=0
                q[puoliso+'kokoelake_nettonetto']=0
                q[puoliso+'kotihoidontuki_nettonetto']=0
                q[puoliso+'opintotuki_nettonetto']=0
                q[puoliso+'elatustuki_nettonetto']=0
                q[puoliso+'alv']=0
                
            q['toimeentulotuki_nettonetto']=q[puoliso+'toimeentulotuki_nettonetto']+q[omat+'toimeentulotuki_nettonetto']
            q['asumistuki_nettonetto']=q[puoliso+'asumistuki_nettonetto']+q[omat+'asumistuki_nettonetto']
            q['kokoelake_nettonetto']=q[puoliso+'kokoelake_nettonetto']+q[omat+'kokoelake_nettonetto']
            q['opintotuki_nettonetto']=q[puoliso+'opintotuki_nettonetto']+q[omat+'opintotuki_nettonetto']
            q['lapsilisa_nettonetto']=q[puoliso+'lapsilisa_nettonetto']+q[omat+'lapsilisa_nettonetto']
            q['tyotpvraha_nettonetto']=q[puoliso+'tyotpvraha_nettonetto']+q[omat+'tyotpvraha_nettonetto']
            q['kotihoidontuki_nettonetto']=q[puoliso+'kotihoidontuki_nettonetto']+q[omat+'kotihoidontuki_nettonetto']
            q['elatustuki_nettonetto']=q[puoliso+'elatustuki_nettonetto']+q[omat+'elatustuki_nettonetto']
            #q['etuustulo_netto_v2']=q[puoliso+'etuustulo_netto']+q[omat+'etuustulo_netto']
            q['palkkatulot_nettonetto']=q[puoliso+'palkkatulot_nettonetto']+q[omat+'palkkatulot_nettonetto']
            q['perustulo_nettonetto']=q[puoliso+'perustulo_nettonetto']+q[omat+'perustulo_nettonetto']

        else:
            if aikuisia>1:
                brutto_puoliso=q[puoliso+'opintotuki']+q[puoliso+'kokoelake']+q[puoliso+'palkkatulot']+q[puoliso+'aitiyspaivaraha']\
                    +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']\
                    +q[puoliso+'tyotpvraha']+q[puoliso+'elatustuki']+q[puoliso+'sairauspaivaraha']
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
            else:
                kateen_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                brutto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                etuusnetto_omat+=q['asumistuki']+q['lapsilisa']+q['toimeentulotuki']
                if kateen_omat>0:
                    r2=etuusnetto_omat/kateen_omat
                else:
                    r2=1
                
                q[omat+'toimeentulotuki']=q['toimeentulotuki']
                q[omat+'asumistuki']=q['asumistuki']
                q[omat+'lapsilisa']=q['lapsilisa']
                q[puoliso+'toimeentulotuki']=q['toimeentulotuki']
                q[puoliso+'asumistuki']=q['asumistuki']
                q[puoliso+'lapsilisa']=q['lapsilisa']
            
        q[omat+'netto']=kateen_omat
        q[puoliso+'netto']=kateen_puoliso
        q[omat+'etuustulo_netto']=etuusnetto_omat
        q[puoliso+'etuustulo_netto']=etuusnetto_puoliso
        
        assert(np.abs(q[omat+'netto']+q[puoliso+'netto']-q['netto'])<1e-10)
        
        q[omat+'etuustulo_brutto']=q[omat+'tyotpvraha']+q[omat+'opintotuki']+q[omat+'sairauspaivaraha']+q[omat+'aitiyspaivaraha']\
            +q[omat+'isyyspaivaraha']+q[omat+'kotihoidontuki']+q[omat+'asumistuki']\
            +q[omat+'toimeentulotuki']+q[omat+'kokoelake']+q[omat+'elatustuki']+q[omat+'lapsilisa'] # + sairauspaivaraha
        q[puoliso+'etuustulo_brutto']=q[puoliso+'tyotpvraha']+q[puoliso+'opintotuki']+q[puoliso+'sairauspaivaraha']+q[puoliso+'aitiyspaivaraha']\
            +q[puoliso+'isyyspaivaraha']+q[puoliso+'kotihoidontuki']+q[puoliso+'asumistuki']\
            +q[puoliso+'toimeentulotuki']+q[puoliso+'kokoelake']+q[puoliso+'elatustuki']+q[puoliso+'lapsilisa']
        q['etuustulo_brutto']=q[omat+'etuustulo_brutto']+q[puoliso+'etuustulo_brutto'] # + sairauspaivaraha
        
        q['brutto']=brutto_omat+brutto_puoliso # q['etuustulo_brutto']+p['t'] #+p[puoliso+'t']
        kateen=q['netto']
        
        # check that omat, puoliso split is ok
        #self.check_q_netto(q,p['aikuisia'],omat,puoliso)

        return kateen,q
        
    def update_toimeentulotuki(self,p: dict,q: dict,omat: str,puoliso: str,omatalku: str,puolisoalku: str):
        if p['ei_toimeentulotukea']<1:
            if p['aikuisia']<2:
                if p[omatalku+'opiskelija']>0 or p[omatalku+'alive']<1:
                    q['toimeentulotuki']=0
                else:
                    q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],0,0,\
                        q['elatustuki']+q['opintotuki_netto']+q['tyotpvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                        +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
                        0,p['asumismenot_toimeentulo'],q['pvhoito'],p['aikuisia'],p['lapsia'],p['kuntaryhma'],p)
            else:
                if p[omatalku+'opiskelija']>0 and p[puolisoalku+'opiskelija']>0:
                    q['toimeentulotuki']=0
                else:
                    q['toimeentulotuki']=self.toimeentulotuki(p[omatalku+'t'],q[omat+'verot_ilman_etuuksia'],p[puolisoalku+'t'],q[puoliso+'verot_ilman_etuuksia'],\
                        q['elatustuki']+q['opintotuki_netto']+q['tyotpvraha_netto']+q['asumistuki']+q['sairauspaivaraha_netto']\
                        +q['lapsilisa']+q['kokoelake_netto']+q['aitiyspaivaraha_netto']+q['isyyspaivaraha_netto']+q['kotihoidontuki_netto'],\
                        0,p['asumismenot_toimeentulo'],q['pvhoito'],p['aikuisia'],p['lapsia'],p['kuntaryhma'],p)
        else:
            q['toimeentulotuki']=0
                            
    def update_netto(self,p: dict,q: dict,omat: str,puoliso: str,omatalku: str,puolisoalku: str):
        q['kokoelake_netto'],q['isyyspaivaraha_netto'],q['tyotpvraha_netto'],q['aitiyspaivaraha_netto'],q['sairauspaivaraha_netto'],\
            q[puoliso+'tyotpvraha_netto'],q['opintotuki_netto']=(0,0,0,0,0,0,0)
        q[omat+'kokoelake_netto'],q[omat+'isyyspaivaraha_netto'],q[omat+'tyotpvraha_netto'],q[omat+'aitiyspaivaraha_netto'],q[omat+'sairauspaivaraha_netto'],\
            q[omat+'opintotuki_netto'],q[omat+'kotihoidontuki_netto']=(0,0,0,0,0,0,0)
        q[puoliso+'kokoelake_netto'],q[puoliso+'isyyspaivaraha_netto'],q[puoliso+'tyotpvraha_netto'],q[puoliso+'aitiyspaivaraha_netto'],q[puoliso+'sairauspaivaraha_netto'],\
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
            if q[omat+'kotihoidontuki']>0:
                r=q[omat+'tyotpvraha']/(q[omat+'tyotpvraha']+q[omat+'kotihoidontuki'])
                q[omat+'tyotpvraha_netto']=q[omat+'tyotpvraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])*r
                q[omat+'kotihoidontuki_netto']=q[omat+'kotihoidontuki']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])*(1-r)
            else:
                q[omat+'tyotpvraha_netto']=q[omat+'tyotpvraha']-(q[omat+'verot']-q[omat+'verot_ilman_etuuksia'])

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
            if q[puoliso+'kotihoidontuki']>0:
                r=q[puoliso+'tyotpvraha']/(q[puoliso+'tyotpvraha']+q[puoliso+'kotihoidontuki'])
                q[puoliso+'tyotpvraha_netto']=q[puoliso+'tyotpvraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])*r
                q[puoliso+'kotihoidontuki_netto']=q[puoliso+'kotihoidontuki']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])*(1-r)
            else:
                q[puoliso+'tyotpvraha_netto']=q[puoliso+'tyotpvraha']-(q[puoliso+'verot']-q[puoliso+'verot_ilman_etuuksia'])

        q[puoliso+'palkkatulot_netto']=q[puoliso+'palkkatulot']-q[puoliso+'verot_ilman_etuuksia']
        q[omat+'palkkatulot_netto']=q[omat+'palkkatulot']-q[omat+'verot_ilman_etuuksia']

        q['palkkatulot_netto']=q[omat+'palkkatulot_netto']+q[puoliso+'palkkatulot_netto']
        q['tyotpvraha_netto']=q[omat+'tyotpvraha_netto']+q[puoliso+'tyotpvraha_netto']
        q['kokoelake_netto']=q[omat+'kokoelake_netto']+q[puoliso+'kokoelake_netto']
        q['aitiyspaivaraha_netto']=q[omat+'aitiyspaivaraha_netto']+q[puoliso+'aitiyspaivaraha_netto']
        q['isyyspaivaraha_netto']=q[omat+'isyyspaivaraha_netto']+q[puoliso+'isyyspaivaraha_netto']
        q['kotihoidontuki_netto']=q[omat+'kotihoidontuki_netto']+q[puoliso+'kotihoidontuki_netto']
        q['sairauspaivaraha_netto']=q[omat+'sairauspaivaraha_netto']+q[puoliso+'sairauspaivaraha_netto']
                            
    def split_cost_to_wage_unemp(self,p: dict,q: dict,omat: str,puoliso: str,omatalku: str,puolisoalku: str):
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

        if q['tyotpvraha_netto']>0:
            if p['aikuisia']>1:
                if p[omatalku+'alive']>0 and p[puolisoalku+'alive']>0:
                    suhde=max(0,q[omat+'tyotpvraha_netto']/q['tyotpvraha_netto'])
                    q[omat+'tyotpvraha_nettonetto']=q[omat+'tyotpvraha_netto']-suhde*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                    q[puoliso+'tyotpvraha_nettonetto']=q[puoliso+'tyotpvraha_netto']-(1-suhde)*(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                elif p[omatalku+'alive']>0:
                    q[omat+'tyotpvraha_nettonetto']=q[omat+'tyotpvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                    q[puoliso+'tyotpvraha_nettonetto']=0
                elif p[puolisoalku+'alive']>0:
                    q[puoliso+'tyotpvraha_nettonetto']=q[puoliso+'tyotpvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                    q[omat+'tyotpvraha_nettonetto']=0
                else:
                    q[omat+'tyotpvraha_nettonetto']=0
                    q[puoliso+'tyotpvraha_nettonetto']=0
            else:
                q[omat+'tyotpvraha_nettonetto']=q[omat+'tyotpvraha_netto']-(q['pvhoito']-q['pvhoito_ilman_etuuksia'])
                q[puoliso+'tyotpvraha_nettonetto']=0
                
            q['tyotpvraha_nettonetto']=q[puoliso+'tyotpvraha_nettonetto']+q[omat+'tyotpvraha_nettonetto']
        else:
            q[omat+'tyotpvraha_nettonetto']=0
            q[puoliso+'tyotpvraha_nettonetto']=0
            q['tyotpvraha_nettonetto']=0           
        
    def add_q(self,benefitq1: dict,benefitq2: dict):
        q= { k: benefitq1.get(k, 0) + benefitq2.get(k, 0) for k in set(benefitq1).union(set(benefitq2)) }
        
        return q
        
    def check_q_netto(self,q: dict,aikuisia: int,omat: str,puoliso: str):
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
            for ss in set(['etuustulo_brutto','palkkatulot','netto','opintotuki','kokoelake','palkkatulot','aitiyspaivaraha','isyyspaivaraha','kotihoidontuki','tyotpvraha','verot','pvhoito']):
                d=q[ss]-q[omat+ss]
                if np.abs(d)>1e-6:
                    print('1',ss,omat,d)
                    print('b',ss,q['omat_'+ss])
            
        for alku in set(s):
            d1=q[alku+'palkkatulot']+q[alku+'etuustulo_brutto']-q[alku+'verot']-q[alku+'alv']-q[alku+'pvhoito']
            d2=q[alku+'netto']
            
            if np.abs(d2-d1)>1e-6:
                print('12',alku,'ero',d2-d1,puoliso,'d1',d1,'d2',d2)
                print('palkka',q[alku+'palkkatulot'],'etuus_brutto',q[alku+'etuustulo_brutto'],'verot',q[alku+'verot'],'alv',q[alku+'alv'],'pvhoito',q[alku+'pvhoito'])
        
    def laske_alv(self,kateen: float):
        # kulutusmenoista maksetaan noin 24% alvia (lähde: TK, https://www.stat.fi/tietotrendit/artikkelit/2019/arvonlisavero-haivyttaa-progression-vaikutuksen-pienituloisimmilta/)
        if self.year<2025:
            alv=(0.24+self.additional_vat)/(1.24+self.additional_vat)
        else:
            alv=(0.255+self.additional_vat)/(1.255+self.additional_vat)
            
        return alv*kateen
        
    def default_asumistuki_suojaosa(self,p):
        if self.year >= 2024:
            p['asumistuki_suojaosa']=0
        else:
            p['asumistuki_suojaosa']=300

    def asumistuki2018(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict):
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
        max_menot=np.array([[508, 492, 390, 344],[735, 706, 570, 501],[937, 890, 723, 641],[1095, 1038, 856, 764]])
        max_lisa=np.array([137, 130, 123, 118])
        # kuntaryhma=3

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.8 # vastaa 80 %
        suojaosa=p['asumistuki_suojaosa']*aikuisia
        perusomavastuu=max(0,0.42*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(597+99*aikuisia+221*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
        
        if tuki<30:
            tuki=0
    
        return tuki
        
    def asumistuki2019(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.8 # vastaa 80 %
        suojaosa=p['asumistuki_suojaosa']*aikuisia
        perusomavastuu=max(0,0.42*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(597+99*aikuisia+221*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        if tuki<30:
            tuki=0
    
        return tuki

    def asumistuki2020(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.8 # vastaa 80 %
        suojaosa=p['asumistuki_suojaosa']*aikuisia
        perusomavastuu=max(0,0.42*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(603+100*aikuisia+223*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        if tuki<30:
            tuki=0
    
        return tuki
        
    def asumistuki2021(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.8 # vastaa 80 %
        suojaosa=p['asumistuki_suojaosa']*aikuisia
        perusomavastuu=max(0,0.42*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(606+100*aikuisia+224*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        if tuki<30:
            tuki=0
    
        return tuki
        
    def asumistuki2022(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.8 # vastaa 80 %
        suojaosa=p['asumistuki_suojaosa']*aikuisia
        perusomavastuu=max(0,0.42*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(619+103*aikuisia+228*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<30:
            tuki=0
    
        return tuki
        
    def asumistuki2023(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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
        max_menot=np.array([[582, 563, 447, 394],[843, 808, 652, 574],[1_072, 1_019, 828, 734],[1_253, 1_188, 981, 875]])
        max_lisa=np.array([156, 148, 134, 129])
        # kuntaryhma=3

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.8 # vastaa 80 %
        suojaosa=p['asumistuki_suojaosa']*aikuisia
        perusomavastuu=max(0,0.42*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(667+111*aikuisia+246*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<30:
            tuki=0
    
        return tuki    
        
    def asumistuki2024(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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
        max_menot=np.array([[563, 563, 447, 394],[808, 808, 652, 574],[1_019, 1_019, 828, 734],[1_188, 1_188, 981, 875]])
        max_lisa=np.array([148, 148, 134, 129])
        # kuntaryhma=3

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.7 # vastaa 80 %
        if True:
            suojaosa=0
        else:
            suojaosa=250 #min(250,palkkatulot1*0.5)+min(250,palkkatulot2*0.5)
        perusomavastuu=max(0,0.50*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(667+111*aikuisia+246*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<30:
            tuki=0
    
        return tuki          

    def asumistuki2025(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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
        max_menot=np.array([[605, 585, 465, 410],[840, 840, 678, 597],[1_060, 1_060, 861, 673],[1_235, 1_235, 1_020, 910]])
        max_lisa=np.array([154, 154, 139, 134])
        # kuntaryhma=3

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.7 # vastaa 80 %
        suojaosa=0
        perusomavastuu=max(0,0.50*(max(0,palkkatulot1-suojaosa)+max(0,palkkatulot2-suojaosa)+muuttulot-(667+111*aikuisia+246*lapsia)))
        if perusomavastuu<10:
            perusomavastuu=0
        #if aikuisia==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and lapsia==0:
        #    perusomavastuu=0
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<30:
            tuki=0
    
        return tuki                    

    def elakkeensaajan_asumistuki_2018(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        max_menot=np.array([8_613,7_921,6_949])/12
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if aikuisia<2:
            tuloraja=9_534/12
        else:
            if puolisolla_oikeus:
                tuloraja=15_565/12
            else:
                tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        

        
    def elakkeensaajan_asumistuki_2019(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        # e/kk    IIII kuntaryhmä,
        # e/kk
        # 1    508    492    411    362
        # 2    735    706    600    527
        # 3    937    890    761    675
        max_menot=np.array([8_243,7_581,6_651])/12
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if aikuisia<2:
            tuloraja=9_534/12
        else:
            if puolisolla_oikeus:
                tuloraja=15_565/12
            else:
                tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        


    def elakkeensaajan_asumistuki_2020(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        # e/kk    IIII kuntaryhmä,
        # e/kk
        # 1    508    492    411    362
        # 2    735    706    600    527
        # 3    937    890    761    675
        max_menot=np.array([8_360,7_688,6_745])/12
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if aikuisia<2:
            tuloraja=9_534/12
        else:
            if puolisolla_oikeus:
                tuloraja=15_565/12
            else:
                tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        

        
    def elakkeensaajan_asumistuki_2021(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        max_menot=np.array([8_613,7_921,6_949])/12
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=52.66 # e/kk, 2019
        if aikuisia<2:
            tuloraja=9_534/12
        else:
            if puolisolla_oikeus:
                tuloraja=15_565/12
            else:
                tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        

        
    def elakkeensaajan_asumistuki_2022(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        #
        max_menot=np.array([9_287,8_541,7_493])/12/1.078
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=56.78 # e/kk, 2019
        if aikuisia<2:
            tuloraja=9_534/12
        else:
            if puolisolla_oikeus:
                tuloraja=15_565/12
            else:
                tuloraja=13_676/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki        
        
    def elakkeensaajan_asumistuki_2023(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        #
        max_menot=np.array([9_287,8_541,7_493])/12
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=56.78 # e/kk, 2019
        if aikuisia<2:
            tuloraja=10_280/12
        else:
            if puolisolla_oikeus:
                tuloraja=16_783/12
            else:
                tuloraja=14_746/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<7.46:
                tuki=0
        else:
            if tuki<3.73:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki                
        
    def elakkeensaajan_asumistuki_2024(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        #
        max_menot=np.array([9_287,8_541,7_493])/12*1.03
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=56.78 # e/kk, 2019
        if aikuisia<2:
            tuloraja=10_280/12
        else:
            if puolisolla_oikeus:
                tuloraja=16_783/12
            else:
                tuloraja=14_746/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki  

    def elakkeensaajan_asumistuki_2025(self,palkkatulot: float,muuttulot: float,vuokra: float,aikuisia: int,kuntaryhma: int,p: dict,puolisolla_oikeus: bool=False) -> float:
        # Ruokakunnan koko
        # henkilöä    I kuntaryhmä,
        # e/kk    II kuntaryhmä,
        # e/kk    III kuntaryhmä,
        #
        max_menot=np.array([9_287,8_541,7_493])/12*1.03
        max_meno=max_menot[max(0,kuntaryhma-1)]

        prosentti=0.85 # vastaa 85 %
        perusomavastuu=56.78 # e/kk, 2019
        if aikuisia<2:
            tuloraja=10_280/12
        else:
            if puolisolla_oikeus:
                tuloraja=16_783/12
            else:
                tuloraja=14_746/12 # oletetaan että puolisolla ei oikeutta asumistukeen
            
        lisaomavastuu=0.413*max(0,palkkatulot+muuttulot-tuloraja)
            
        tuki=max(0,(min(max_meno,vuokra)-perusomavastuu-lisaomavastuu)*prosentti)
        
        if aikuisia>1:
            if tuki<6.92:
                tuki=0
        else:
            if tuki<3.46:
                tuki=0
        
        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
    
        return tuki                        

    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot2018(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,
            prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        minimimaksu=10

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.5
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=290

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0
            
        if osaaikainen:
            maksu *= 0.6
        
        return maksu
        
    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot2019(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        minimimaksu=10

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.5
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=290

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0

        if osaaikainen:
            maksu *= 0.6
        
        return maksu
        
    # hallituksen päätöksenmukaiset päivähoitomenot 2018
    def paivahoitomenot2020(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        minimimaksu=10

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.5
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=290

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        if osaaikainen:
            maksu *= 0.6
        
        return maksu
        
    def paivahoitomenot2021(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        '''
        Päivähoitomaksut 1.8.2021
        '''
        minimimaksu=27

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.4
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=288

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        if osaaikainen:
            maksu *= 0.6
        
        return maksu        
        
    def paivahoitomenot2022(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        '''
        Päivähoitomaksut 1.8.2021
        '''
        minimimaksu=27

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.4
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=288

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        if osaaikainen:
            maksu *= 0.6
        
        return maksu                
        
    def paivahoitomenot2023(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        '''
        Päivähoitomaksut 1.8.2021
        '''
        minimimaksu=27

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.4
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=288

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        if osaaikainen:
            maksu *= 0.6
        
        return maksu
        
    def paivahoitomenot2024(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        '''
        Päivähoitomaksut 1.8.2021
        '''
        minimimaksu=27

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.4
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=288

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        if osaaikainen:
            maksu *= 0.6
        
        return maksu

    def paivahoitomenot2025(self,hoidossa: int,tulot: float,aikuisia: int, lapsia: int,p: dict,prosentti1: float=None,prosentti2: float=None,prosentti3: float=None,maksimimaksu: float=None):
        '''
        Päivähoitomaksut 1.8.2021
        '''
        minimimaksu=27

        if p['osaaikainen_paivahoito']>0:
            osaaikainen=True
        else:
            osaaikainen=False

        if prosentti1==None:
            prosentti1=0.107
        if prosentti2==None:
            prosentti2=0.4
        if prosentti3==None:
            prosentti3=0.2
            
        if maksimimaksu==None:
            maksimimaksu=288

        if lapsia>0:
            vakea=lapsia+aikuisia
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
                            kerroin=1+prosentti2+prosentti3*(lapsia-2)
            maksu=kerroin*pmaksu
        else:
            maksu=0
        
        if osaaikainen:
            maksu *= 0.6
        
        return maksu        

    def laske_kansanelake2018(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
        if yksin>0:
            maara=628.85
        else:
            maara=557.79
            
        if lapsia>0:
            maara += 22.23*lapsia
            
        if disability: # ei lykkäystä tai varhennusta
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
            
    def laske_kansanelake2019(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
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
        
    def laske_kansanelake2020(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
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
        
    def laske_kansanelake2021(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
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
        
    def laske_kansanelake2022(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
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
        
    def laske_kansanelake2023(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
        if yksin>0:
            maara=732.67
        else:
            maara=654.13
        if lapsia>0:
            maara += 24.48*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-61.95))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-61.95))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-61.95))/2)
            else:
                maara=0
                
        if maara<7.46:
            maara=0
            
        return maara
        
    def laske_kansanelake2024(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
        '''
        Päivitä
        '''
        if yksin>0:
            maara=775.50
        else:
            maara=692.54

        if lapsia>0:
            maara += 24.48*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-65.62))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-65.62))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-65.62))/2)
            else:
                maara=0
                
        if maara<7.46:
            maara=0
            
        return maara      

    def laske_kansanelake2025(self,ika: int,tyoelake: float,yksin: int,disability: bool=False,lapsia: int=0) -> float:
        '''
        Päivitä
        '''
        if yksin>0:
            maara=775.50
        else:
            maara=692.54

        if lapsia>0:
            maara += 24.48*lapsia
            
        if disability:
            maara = max(0,maara-np.maximum(0,(tyoelake-65.62))/2)
        else:
            if ika>=65:
                maara = max(0,maara*(1.0+0.072*(ika-65))-np.maximum(0,(tyoelake-65.62))/2)
            elif ika>=62: # varhennus
                maara = max(0,maara*(1.0-0.048*(65-ika))-np.maximum(0,(tyoelake-65.62))/2)
            else:
                maara=0
                
        if maara<7.46:
            maara=0
            
        return maara                
        
    def laske_takuuelake2018(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
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
    
    def laske_takuuelake2019(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
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
    
    def laske_takuuelake2020(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
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
        
    def laske_takuuelake2021(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
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
        
    def laske_takuuelake2022(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
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

    def laske_takuuelake2023(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
        if ika<63 and not disability:
            return 0
            
        lapsikorotus=24.48*lapsia
        
        if muuelake<922.42+lapsikorotus:
            elake=922.42+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<7.46:
            elake=0

        return elake        
        
    def laske_takuuelake2024(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
        if ika<63 and not disability:
            return 0
            
        lapsikorotus=24.48*lapsia
        
        if muuelake<976.54+lapsikorotus:
            elake=976.54+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<7.46:
            elake=0

        return elake    

    def laske_takuuelake2025(self,ika: int,muuelake: float,disability: bool=False,lapsia: int=0) -> float:
        if ika<63 and not disability:
            return 0
            
        lapsikorotus=24.48*lapsia
        
        if muuelake<976.54+lapsikorotus:
            elake=976.54+lapsikorotus-muuelake
        else:
            elake=0
        
        if elake<7.46:
            elake=0

        return elake                        
        
    def laske_puhdas_tyoelake(self,ika: int,elake: float,disability: bool=False,yksin: int=1,lapsia: int=0) -> float:
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
                 
    def laske_puhdas_tyoelake_v2(self,ika: int,tyoelake: float,kansanelake: float,disability=False,yksin=1,lapsia=0):
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
    
    def laske_kokonaiselake(self,ika: int,muuelake: float,yksin: int=1,include_takuuelake: bool=True,add_kansanelake: bool=False,disability: bool=False,lapsia: int=0) -> float:
        '''
        by default, kansaneläke is not included, since this function is called annually
        kansaneläke sisältyy muuelake-muuttujaan
        '''
        if add_kansanelake:
            kansanelake = self.laske_kansanelake(ika,muuelake,yksin,disability=disability,lapsia=lapsia)
            muuelake = muuelake+kansanelake
            
        if include_takuuelake:
            takuuelake = self.laske_takuuelake(ika,muuelake,disability=disability,lapsia=lapsia)
            #if takuuelake>0:
            #    print('ika',ika,'muuelake',muuelake,'takuuelake',takuuelake)
            kokoelake = takuuelake+muuelake
        else:
            kokoelake = muuelake
    
        return kokoelake
        
    def laske_kokonaiselake_v2(self,ika: int,omaelake: float,kansanelake: float,yksin: int=1,include_takuuelake: bool=True,add_kansanelake: bool=False,disability: bool=False,lapsia: int=0) -> float:
        '''
        by default, kansaneläke is not included, since this function is called annually
        kansaneläke lasketaan erikseen
        '''
        if add_kansanelake:
            kansanelake = self.laske_kansanelake(ika,omaelake,yksin,disability=disability,lapsia=lapsia)
            muuelake = omaelake + kansanelake
        else:
            muuelake = omaelake + kansanelake
            
        if include_takuuelake:
            takuuelake=self.laske_takuuelake(ika,muuelake,disability=disability,lapsia=lapsia)
            kokoelake = takuuelake+muuelake
            #if takuuelake>0:
            #    print('ika',ika,'tyoelake',omaelake,'kansanelake',kansanelake,'takuuelake',takuuelake)
            #if takuuelake>0 and kansanelake<1e-4:
            #    print('ika',ika,'tyoelake',omaelake,'kansanelake',kansanelake,'takuuelake',takuuelake)
        else:
            kokoelake = muuelake
    
        return kokoelake

    def isyysraha_perus(self,palkka: float,vakiintunutpalkka: float,kesto: float):
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
            minimi=31.99*25
            taite1=40_106/12  
            taite2=61_705/12
        elif self.year==2024:
            minimi=31.99*25
            taite1=40_106/12  
            taite2=61_705/12
        elif self.year==2025:
            minimi=31.99*25
            taite1=40_106/12  
            taite2=61_705/12
        elif self.year==2026:
            minimi=31.99*25
            taite1=40_106/12  
            taite2=61_705/12
        elif self.year==2027:
            minimi=31.99*25
            taite1=40_106/12  
            taite2=61_705/12
        else:
            print('isyysraha: unknown year',year)  

        if self.year<2023:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))
        else: # lisää raskausrahan vastine
            if kesto<56/260:
                vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
            else:
                vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                raha=max(minimi,0.7*min(taite1,vakiintunutpalkka)+0.4*max(min(taite2,vakiintunutpalkka)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(0,raha-palkka)
        
    def aitiysraha2018(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=27.86*25
        taite1=37_861/12  
        taite2=58_252/12 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(0,raha-palkka)
                
    def aitiysraha2019(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=27.86*25
        taite1=37_861/12  
        taite2=58_252/12 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(0,raha-palkka)
        
    def aitiysraha2020(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=28.94*25
        taite1=37_861/12  
        taite2=58_252/12 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(0,raha-palkka)
        
    def aitiysraha2021(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=29.05*25
        taite1=39_144/12  
        taite2=60_225/12 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(0,raha-palkka)
        
    def aitiysraha2022(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=29.67*25
        taite1=39_144/12  
        taite2=60_225/12 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(0,raha-palkka)
        
    def aitiysraha2023(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=31.99*25
        taite1=40_106/12  
        taite2=61_705/12 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(0,raha-palkka)
        
    def aitiysraha2024(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=31.99*25
        taite1=40_106/self.kk_jakaja  
        taite2=61_705/self.kk_jakaja 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(raha,palkka)

    def aitiysraha2025(self,palkka: float,vakiintunutpalkka: float,kesto: float):
        minimi=31.99*25
        taite1=40_106/self.kk_jakaja  
        taite2=61_705/self.kk_jakaja 
        if kesto<56/260:
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.9*min(taite1,vakiintunut)+0.325*max(vakiintunut-taite1,0))
        else: 
            vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
            raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.4*max(vakiintunutpalkka-taite2,0))

        return max(raha,palkka)        

    def sairauspaivaraha2018(self,palkka: float,vakiintunutpalkka: float):
        minimi=24.64*25
        taite1=30_394/self.kk_jakaja
        taite2=58_252/self.kk_jakaja
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))

        return max(0,raha-palkka)
        
    def sairauspaivaraha2019(self,palkka: float,vakiintunutpalkka: float):
        minimi=27.86*25
        taite1=30_394/self.kk_jakaja
        taite2=57_183/self.kk_jakaja
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    

        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.4*max(min(taite2,vakiintunut)-taite1,0)+0.2*max(vakiintunut-taite2,0))

        return max(0,raha-palkka)

    def sairauspaivaraha2020(self,palkka: float,vakiintunutpalkka: float):
        minimi=28.94*25
        taite1=31_595/self.kk_jakaja  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)
        
    def sairauspaivaraha2021(self,palkka: float,vakiintunutpalkka: float):
        minimi=29.05*25
        taite1=32_011/self.kk_jakaja  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)
        
    def sairauspaivaraha2022(self,palkka: float,vakiintunutpalkka: float):
        minimi=30.71*25
        taite1=32_011/self.kk_jakaja  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)

    def sairauspaivaraha2023(self,palkka: float,vakiintunutpalkka: float):
        minimi=31.99*25
        taite1=32_797/self.kk_jakaja  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)

    def sairauspaivaraha2024(self,palkka: float,vakiintunutpalkka: float):
        minimi=31.99*25
        taite1=32_797/self.kk_jakaja
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)

    def sairauspaivaraha2025(self,palkka: float,vakiintunutpalkka: float):
        minimi=31.99*25
        taite1=32_797/self.kk_jakaja
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)        
        
    # valitaan oikeat funktiot vuoden mukaan
    def set_year(self,vuosi: int):
        '''
        korvataan etuusfunktiot oikeiden vuosien etuusfunktioilla
        '''
        debug=False
        if vuosi==2019:
            self.laske_kansanelake=self.laske_kansanelake2019
            self.laske_takuuelake=self.laske_takuuelake2019
            self.aitiysraha=self.aitiysraha2019
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2019
            self.veroparam=self.veroparam2019          
            self.valtionvero_asteikko=self.valtionvero_asteikko_2019
            self.raippavero=self.raippavero2019
            self.laske_valtionvero=self.laske_valtionvero2018_2022
            self.laske_ylevero=self.laske_ylevero2019
            self.elaketulovahennys=self.elaketulovahennys2019
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2018_2022
            self.tyotulovahennys=self.tyotulovahennys2019
            self.ansiotulovahennys=self.ansiotulovahennys2019
            self.perusvahennys=self.perusvahennys2019
            self.lapsilisa=self.lapsilisa2019
            self.asumistuki=self.asumistuki2019
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2019
            self.kotihoidontuki=self.kotihoidontuki2019
            self.hoitolisa=self.hoitolisa2019
            self.paivahoitomenot=self.paivahoitomenot2019
            self.sairauspaivaraha=self.sairauspaivaraha2019
            self.toimeentulotuki_param=self.toimeentulotuki_param2019
            self.ansiopaivaraha=self.ansiopaivaraha_perus
        elif vuosi==2020:
            self.laske_kansanelake=self.laske_kansanelake2020
            self.laske_takuuelake=self.laske_takuuelake2020
            self.aitiysraha=self.aitiysraha2020
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2020
            self.valtionvero_asteikko=self.valtionvero_asteikko_2020
            self.raippavero=self.raippavero2020
            self.laske_valtionvero=self.laske_valtionvero2018_2022
            self.laske_ylevero=self.laske_ylevero2020
            self.elaketulovahennys=self.elaketulovahennys2020
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2018_2022
            self.tyotulovahennys=self.tyotulovahennys2020
            self.perusvahennys=self.perusvahennys2020
            self.ansiotulovahennys=self.ansiotulovahennys2020
            self.veroparam=self.veroparam2020
            self.lapsilisa=self.lapsilisa2020
            self.asumistuki=self.asumistuki2020
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2020
            self.kotihoidontuki=self.kotihoidontuki2020
            self.hoitolisa=self.hoitolisa2020
            self.paivahoitomenot=self.paivahoitomenot2020
            self.sairauspaivaraha=self.sairauspaivaraha2020
            self.toimeentulotuki_param=self.toimeentulotuki_param2020
            self.ansiopaivaraha=self.ansiopaivaraha_perus
        elif vuosi==2021:
            self.laske_kansanelake=self.laske_kansanelake2021
            self.laske_takuuelake=self.laske_takuuelake2021
            self.aitiysraha=self.aitiysraha2021
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2021
            self.valtionvero_asteikko=self.valtionvero_asteikko_2021
            self.raippavero=self.raippavero2021
            self.laske_valtionvero=self.laske_valtionvero2018_2022
            self.laske_ylevero=self.laske_ylevero2021
            self.elaketulovahennys=self.elaketulovahennys2021
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2018_2022
            self.tyotulovahennys=self.tyotulovahennys2021
            self.perusvahennys=self.perusvahennys2021
            self.ansiotulovahennys=self.ansiotulovahennys2021
            self.veroparam=self.veroparam2021
            self.lapsilisa=self.lapsilisa2021
            self.asumistuki=self.asumistuki2021
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2021
            self.kotihoidontuki=self.kotihoidontuki2021
            self.hoitolisa=self.hoitolisa2021
            self.paivahoitomenot=self.paivahoitomenot2021
            self.sairauspaivaraha=self.sairauspaivaraha2021
            self.toimeentulotuki_param=self.toimeentulotuki_param2021
            self.ansiopaivaraha=self.ansiopaivaraha_perus
        elif vuosi==2022:
            self.laske_kansanelake=self.laske_kansanelake2022
            self.laske_takuuelake=self.laske_takuuelake2022
            self.aitiysraha=self.aitiysraha2022
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2022
            self.valtionvero_asteikko=self.valtionvero_asteikko_2022
            self.laske_valtionvero=self.laske_valtionvero2018_2022
            self.raippavero=self.raippavero2022
            self.laske_ylevero=self.laske_ylevero2022
            self.elaketulovahennys=self.elaketulovahennys2022
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2018_2022
            self.tyotulovahennys=self.tyotulovahennys2022
            self.perusvahennys=self.perusvahennys2022
            self.ansiotulovahennys=self.ansiotulovahennys2022
            self.veroparam=self.veroparam2022
            self.lapsilisa=self.lapsilisa2022
            self.asumistuki=self.asumistuki2022
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2022
            self.kotihoidontuki=self.kotihoidontuki2022
            self.hoitolisa=self.hoitolisa2022
            self.paivahoitomenot=self.paivahoitomenot2022
            self.sairauspaivaraha=self.sairauspaivaraha2022
            self.toimeentulotuki_param=self.toimeentulotuki_param2022
            self.ansiopaivaraha=self.ansiopaivaraha_perus
        elif vuosi==2023:
            self.laske_kansanelake=self.laske_kansanelake2023
            self.laske_takuuelake=self.laske_takuuelake2023
            self.aitiysraha=self.aitiysraha2023
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2023
            self.valtionvero_asteikko=self.valtionvero_asteikko_2023
            self.raippavero=self.raippavero2023
            self.laske_valtionvero=self.laske_valtionvero2023
            self.laske_ylevero=self.laske_ylevero2023
            self.elaketulovahennys=self.elaketulovahennys2023
            self.tyotulovahennys=self.tyotulovahennys2023
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2023_2025
            self.perusvahennys=self.perusvahennys2023
            self.ansiotulovahennys=self.ansiotulovahennys2023
            self.veroparam=self.veroparam2023
            self.lapsilisa=self.lapsilisa2023
            self.asumistuki=self.asumistuki2023
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2023
            self.kotihoidontuki=self.kotihoidontuki2023
            self.hoitolisa=self.hoitolisa2023
            self.paivahoitomenot=self.paivahoitomenot2023
            self.sairauspaivaraha=self.sairauspaivaraha2023
            self.toimeentulotuki_param=self.toimeentulotuki_param2023  
            self.ansiopaivaraha=self.ansiopaivaraha_perus          
        elif vuosi==2024:
            self.laske_kansanelake=self.laske_kansanelake2024
            self.laske_takuuelake=self.laske_takuuelake2024
            self.aitiysraha=self.aitiysraha2024
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2024
            self.valtionvero_asteikko=self.valtionvero_asteikko_2024
            self.raippavero=self.raippavero2024
            self.laske_valtionvero=self.laske_valtionvero2024
            self.laske_ylevero=self.laske_ylevero2024
            self.elaketulovahennys=self.elaketulovahennys2024
            self.tyotulovahennys=self.tyotulovahennys2024
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2023_2025
            self.perusvahennys=self.perusvahennys2024
            self.ansiotulovahennys=self.ansiotulovahennys2024
            self.veroparam=self.veroparam2024
            self.lapsilisa=self.lapsilisa2024
            self.asumistuki=self.asumistuki2024
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2024
            self.kotihoidontuki=self.kotihoidontuki2024
            self.hoitolisa=self.hoitolisa2024
            self.paivahoitomenot=self.paivahoitomenot2024
            self.sairauspaivaraha=self.sairauspaivaraha2024
            self.toimeentulotuki_param=self.toimeentulotuki_param2024    
            self.ansiopaivaraha=self.ansiopaivaraha_porrastus       
        elif vuosi==2025:
            self.laske_kansanelake=self.laske_kansanelake2025
            self.laske_takuuelake=self.laske_takuuelake2025
            self.aitiysraha=self.aitiysraha2025
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2025
            self.valtionvero_asteikko=self.valtionvero_asteikko_2025
            self.raippavero=self.raippavero2025
            self.laske_valtionvero=self.laske_valtionvero2025
            self.laske_ylevero=self.laske_ylevero2025
            self.elaketulovahennys=self.elaketulovahennys2025
            self.tyotulovahennys=self.tyotulovahennys2025
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2023_2025
            self.perusvahennys=self.perusvahennys2025
            self.ansiotulovahennys=self.ansiotulovahennys2025
            self.veroparam=self.veroparam2025
            self.lapsilisa=self.lapsilisa2025
            self.asumistuki=self.asumistuki2025
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2025
            self.kotihoidontuki=self.kotihoidontuki2025
            self.hoitolisa=self.hoitolisa2025
            self.paivahoitomenot=self.paivahoitomenot2025
            self.sairauspaivaraha=self.sairauspaivaraha2025
            self.toimeentulotuki_param=self.toimeentulotuki_param2025
            self.ansiopaivaraha=self.ansiopaivaraha_porrastus
        elif vuosi==2026:
            self.laske_kansanelake=self.laske_kansanelake2026
            self.laske_takuuelake=self.laske_takuuelake2026
            self.aitiysraha=self.aitiysraha2026
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2026
            self.valtionvero_asteikko=self.valtionvero_asteikko_2026
            self.raippavero=self.raippavero2026
            self.laske_valtionvero=self.laske_valtionvero2026
            self.laske_ylevero=self.laske_ylevero2026
            self.elaketulovahennys=self.elaketulovahennys2026
            self.tyotulovahennys=self.tyotulovahennys2026
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2023_2026
            self.perusvahennys=self.perusvahennys2026
            self.ansiotulovahennys=self.ansiotulovahennys2026
            self.veroparam=self.veroparam2026
            self.lapsilisa=self.lapsilisa2026
            self.asumistuki=self.asumistuki2026
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2026
            self.kotihoidontuki=self.kotihoidontuki2026
            self.hoitolisa=self.hoitolisa2026
            self.paivahoitomenot=self.paivahoitomenot2026
            self.sairauspaivaraha=self.sairauspaivaraha2026
            self.toimeentulotuki_param=self.toimeentulotuki_param2026   
            self.ansiopaivaraha=self.ansiopaivaraha_porrastus   
        elif vuosi==2027:
            self.laske_kansanelake=self.laske_kansanelake2027
            self.laske_takuuelake=self.laske_takuuelake2027
            self.aitiysraha=self.aitiysraha2027
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2027
            self.valtionvero_asteikko=self.valtionvero_asteikko_2027
            self.raippavero=self.raippavero2027
            self.laske_valtionvero=self.laske_valtionvero2027
            self.laske_ylevero=self.laske_ylevero2027
            self.elaketulovahennys=self.elaketulovahennys2027
            self.tyotulovahennys=self.tyotulovahennys2027
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2023_2027
            self.perusvahennys=self.perusvahennys2027
            self.ansiotulovahennys=self.ansiotulovahennys2027
            self.veroparam=self.veroparam2027
            self.lapsilisa=self.lapsilisa2027
            self.asumistuki=self.asumistuki2027
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2027
            self.kotihoidontuki=self.kotihoidontuki2027
            self.hoitolisa=self.hoitolisa2027
            self.paivahoitomenot=self.paivahoitomenot2027
            self.sairauspaivaraha=self.sairauspaivaraha2027
            self.toimeentulotuki_param=self.toimeentulotuki_param2027                      
            self.ansiopaivaraha=self.ansiopaivaraha_porrastus
        elif vuosi==2018:
            self.laske_kansanelake=self.laske_kansanelake2018
            self.laske_takuuelake=self.laske_takuuelake2018
            self.aitiysraha=self.aitiysraha2018
            self.isyysraha=self.isyysraha_perus
            self.peruspaivaraha=self.peruspaivaraha2018
            self.veroparam=self.veroparam2018            
            self.elaketulovahennys=self.elaketulovahennys2018
            self.laske_tyotulovahennys=self.laske_tyotulovahennys2018_2022
            self.tyotulovahennys=self.tyotulovahennys2018
            self.perusvahennys=self.perusvahennys2018
            self.ansiotulovahennys=self.ansiotulovahennys2018
            self.laske_valtionvero=self.laske_valtionvero2018_2022
            self.valtionvero_asteikko=self.valtionvero_asteikko_2018
            self.raippavero=self.raippavero2018
            self.laske_ylevero=self.laske_ylevero2018
            self.lapsilisa=self.lapsilisa2018
            self.asumistuki=self.asumistuki2018
            self.elakkeensaajan_asumistuki=self.elakkeensaajan_asumistuki_2018
            self.kotihoidontuki=self.kotihoidontuki2018
            self.hoitolisa=self.hoitolisa2018
            self.paivahoitomenot=self.paivahoitomenot2018
            self.sairauspaivaraha=self.sairauspaivaraha2018
            self.toimeentulotuki_param=self.toimeentulotuki_param2018
            self.ansiopaivaraha=self.ansiopaivaraha_perus            
        else:
            print('Vuoden {v} aineisto puuttuu'.format(v=vuosi))
            
        self.sotumaksu=self.laske_sotumaksu(vuosi)
        self.setup_tmtuki_param(vuosi)
        self.veroparam()
            
    def get_tyelpremium(self):
        tyel_kokomaksu=np.zeros((2100,5))
        # data
        self.data_tyel_kokomaksu[1962:2022]=[5.0,5.0,5.0,5.0,5.0,5.0,5.0,5.15,5.15,5.65,6.1,6.4,6.9,7.9,9.9,12.0,10.0,11.7,13.3,13.3,12.4,11.1,11.1,11.5,12.2,13.0,13.8,14.9,16.9,16.9,14.4,18.5,18.6,20.6,21.1,21.2,21.5,21.5,21.5,21.1,21.1,21.4,21.4,21.6,21.2,21.1,21.1,21.3,21.6,22.1,22.8,22.8,23.6,24.0,24.0,24.4,24.4,24.4,24.4,24.4,24.4]
        # ETK
        self.data_tyel_kokomaksu[2023:2085]=np.array([24.4,24.5,24.5,24.6,24.6,24.7,24.8,24.8,24.9,24.9,25.0,24.9,24.9,24.9,24.9,24.8,24.8,24.7,24.7,24.6,24.6,24.6,24.6,24.6,24.7,24.8,24.8,24.9,25.1,25.2,25.4,25.6,25.8,26.0,26.2,26.5,26.7,27.0,27.2,27.5,27.7,27.9,28.1,28.3,28.5,28.7,28.9,29.1,29.2,29.4,29.5,29.7,29.8,29.9,30.1,30.2,30.3,30.3,30.4,30.4,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5,30.5])/100
        self.data_ptel=0.5*(self.data_tyel_kokomaksu-self.data_tyel_kokomaksu[2017])+0.0615 # vuonna 2017 ptel oli 6,15 %
        self.data_ptel[1962:1993]=0
        
        return tyel_kokomaksu

    def compare_q(self,q1,q2):
        compare_q_print(q1,q2)

