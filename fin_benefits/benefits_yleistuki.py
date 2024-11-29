"""

    benefits
    
    implements social security benefits and taxation in the Finnish social security schemes

    Yleistukimalli, joka perustuu Orpon hallituksen hallitusohjelmaan
    - rakennettu HO-mallin päälle

"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite
from .labels import Labels
from .ben_utils import print_q, compare_q_print
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
from .benefits_HO import BenefitsHO

class BenefitsYleistuki(BenefitsHO):
    """
    Description:
        The Finnish Earnings-related Social Security

    Source:
        Antti J. Tanskanen

    """
    
    def __init__(self,**kwargs):
        self.setup_YTU()
        super().__init__(**kwargs)
        print('Yleistuki 2023 BENEFITS')

    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_YTU()

    def setup_YTU(self,vaihe=4):        
        self.asumistuki=self.asumistuki2023
        self.tyotulovahennys=self.tyotulovahennys2023
        self.valtionvero_asteikko=self.valtionvero_asteikko_2023
        self.lapsilisa=self.lapsilisa2023
        self.veroparam=self.veroparam2023
        if vaihe==1: # peruspäiväraha ja toimeentulotuki yhteen 
            # do nothing
            a=1
        elif vaihe==2 or vaihe==3: # totu ja asumistuki yhteen
            self.asumistuki=self.asumistuki2023_YTU_stub
            self.toimeentulotuki=self.toimeentulotuki_YTU
            self.toimeentulotuki_param2023=self.toimeentulotuki_param2023_YTU
        elif vaihe==4: # korvataan ansiosidonnainen päiväraha svpäivärahalla ja se kohdistuu kaikkiin
            self.asumistuki = self.asumistuki2023_YTU_stub
            self.toimeentulotuki = self.toimeentulotuki_YTU
            self.toimeentulotuki_param2023=self.toimeentulotuki_param2023_YTU
            self.ansiopaivaraha = self.ansiopaivaraha_porrastus_YTU

    def explain(self,p: dict =None):
        if p is None:
            print('Ei parametrejä')
        else:
            print(tee_selite(p))

    #def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,aikuisia,lapsia,kuntaryhma,p,omavastuuprosentti=0.05):        
    #    return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,aikuisia,lapsia,kuntaryhma,p,omavastuuprosentti=omavastuuprosentti)

    def asumistuki2023_YTU_stub(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
        '''
        Ei tukea, koska yhdistetty totuun
        '''

        return 0

    def asumistuki2023_YTU(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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
        #print('YTU')
        # enimmaismenot kuntaryhmittain kun hloita 1-4
        max_menot=np.array([[563, 563, 447, 394],[808, 808, 652, 574],[1_019, 1_019, 828, 734],[1_188, 1_188, 981, 875]])
        max_lisa=np.array([148, 148, 134, 129])

        # kuntaryhma=3
        max_menot[:,0]=max_menot[:,1]
        max_lisa[0]=max_lisa[1]

        max_meno=max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti=0.7 # vastaa 80 %
        suojaosa=0 #p['asumistuki_suojaosa']*p['aikuisia']
        yhteensovitus=1.0
        yhteensovitus_tyotulo=1.0
        lapsiparam=246 # FIXME 270?
        perusomavastuu_nollatulot = - (667+111*aikuisia+lapsiparam*lapsia)
        perusomavastuu=max(0,
            0.50*(max(0,yhteensovitus_tyotulo*palkkatulot1-suojaosa)
                +max(0,yhteensovitus_tyotulo*palkkatulot2-suojaosa)
                +yhteensovitus*muuttulot
                +perusomavastuu_nollatulot))
        if perusomavastuu<10:
            perusomavastuu=0
        #if p['aikuisia']==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and p['lapsia']==0:
        #    perusomavastuu=0
            
        tuki = max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
        tuki0 = max(0,(min(max_meno,vuokra))*prosentti)

        if self.use_extra_ppr:
            tuki=tuki*self.extra_ppr_factor
            
        if tuki<30:
            tuki=0
    
        return tuki,tuki0,perusomavastuu_nollatulot    

    def toimeentulotuki_param2023_YTU(self) -> (float,float,float,float,float,float,float,float,float):
        '''
        Päivitä
        '''
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        kerroin_lapsi = 1.05
        kerroin_aikuinen = 1.0
        kerroin_yksinhuoltaja = 1.0
        lapsi1=383.03 * kerroin_lapsi    # e/kk     alle 10v lapsi
        lapsi2=355.27 * kerroin_lapsi     # e/kk
        lapsi3=327.51 * kerroin_lapsi     # e/kk
        yksinhuoltaja=632.83 * kerroin_yksinhuoltaja    # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot
        muu=471.84 * kerroin_aikuinen
        yksinasuva=555.11 * kerroin_aikuinen
        # Helsinki: 694 869 993 1089 122
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])
        max_lisa=np.array([122, 99, 96, 96])

        return min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa        

    def toimeentulotuki_YTU(self,omabruttopalkka: float,omapalkkavero: float,puolison_bruttopalkka: float,puolison_palkkavero: float,
                        muuttulot: float,verot: float,asumismenot: float,muutmenot: float,aikuisia: int, lapsia: int,kuntaryhma: int,
                        p: dict,omavastuuprosentti: float=0.0,alennus: int=0,asumistuki: float=None,muut_tulot_asumistuki: float=None):
        '''
        asumistuki tässä eläkeläisen asumistuki
        - se poistettava! FIXME
        '''
        min_etuoikeutettuosa,lapsi1,lapsi2,lapsi3,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_asumislisa=self.toimeentulotuki_param()
        max_asumismeno=max_asumismenot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_asumislisa[kuntaryhma]

        asumismenot = min(asumismenot,max_asumismeno)            
        menot = muutmenot

        elakelaisen_asumistuki = asumistuki

        #print(asumistuki,muuttulot)

        #asumistuki = self.asumistuki2023_YTU(omabruttopalkka,puolison_bruttopalkka,muuttulot,asumismenot,aikuisia,lapsia,kuntaryhma,p)
        asumistuki,asumistuki_nollatulot,perusomavastuu_nollatulot = self.asumistuki2023_YTU(omabruttopalkka,puolison_bruttopalkka,muut_tulot_asumistuki,asumismenot,aikuisia,lapsia,kuntaryhma,p)

        #print(asumistuki,asumistuki_nollatulot,perusomavastuu_nollatulot)
        #menot=asumismenot+muutmenot    
        bruttopalkka=omabruttopalkka+puolison_bruttopalkka    
        palkkavero=omapalkkavero+puolison_palkkavero    
        palkkatulot=bruttopalkka-palkkavero    
        
        if False:   
            omaetuoikeutettuosa = max(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
            puolison_etuoikeutettuosa = max(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
        else:        
            if aikuisia==1:
                omaetuoikeutettuosa = 0.2*omabruttopalkka # min(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
                puolison_etuoikeutettuosa = 0.2*puolison_bruttopalkka # min(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
            else:        
                omaetuoikeutettuosa = 0.2*omabruttopalkka # min(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
                puolison_etuoikeutettuosa = 0.2*puolison_bruttopalkka # min(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
            
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
        #    tuki=max(0,tuki1+menot-max(0,bruttopalkka-etuoikeutettuosa-palkkavero)-verot-muuttulot)    
        #else 
        #    verot2=palkkavero+verot-max(0,(bruttopalkka-etuoikeutettuosa))    
        #    tuki=max(0,tuki1+menot-muuttulot+verot2)    
        #end
        
        if alennus>0:
            tuki1=tuki1*(1-alennus)
            
        if self.use_extra_ppr:
            tuki1=tuki1*self.extra_ppr_factor
        
        palkkakerroin = 1.0
        asu_vero = max(0,min(asumistuki_nollatulot,0.7*0.5*(max(0,palkkakerroin*omabruttopalkka+palkkakerroin*puolison_bruttopalkka+muut_tulot_asumistuki+elakelaisen_asumistuki+perusomavastuu_nollatulot))))
        asu_osa = max(0,asumistuki_nollatulot-asu_vero)

        if omabruttopalkka>0:
            if puolison_bruttopalkka>0:
                asu_vero_puoliso = asu_vero * puolison_bruttopalkka / (omabruttopalkka+puolison_bruttopalkka)
                asu_vero_oma = asu_vero - asu_vero_puoliso
            else:
                asu_vero_puoliso = 0
                asu_vero_oma = asu_vero
        else:
            asu_vero_oma = 0
            if puolison_bruttopalkka>0:
                asu_vero_puoliso = asu_vero
            else:
                asu_vero_puoliso = 0

        totu_osa = max(0,tuki1+menot-max(0,omabruttopalkka-omaetuoikeutettuosa-omapalkkavero-asu_vero_oma)\
                                    -max(0,puolison_bruttopalkka-puolison_etuoikeutettuosa-puolison_palkkavero-asu_vero_puoliso)-verot-muuttulot)        

        #print(f'omabruttopalkka {omabruttopalkka:.2f} muuttulot {muuttulot:.2f} totu_osa {totu_osa:.2f} asu_osa {asu_osa:.2f} asumistuki {asumistuki:.2f} ast0 {asumistuki_nollatulot:.2f} po0 {perusomavastuu_nollatulot:.2f}')

        tuki = totu_osa + asu_osa

        if p['toimeentulotuki_vahennys']>0: # vähennetään 20%
            tuki=tuki*0.8
            if p['toimeentulotuki_vahennys']>99: # vähennetään 100%
                tuki=0.0
                
        if tuki<10:
            tuki=0    
            
        return tuki 

    def ansiopaivaraha_ylaraja_YTU(self,ansiopaivarahamaara: float,tyotaikaisettulot: float,vakpalkka: float,vakiintunutpalkka: float,peruspvraha: float) -> float:
        if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
            #return max(0,vakpalkka-tyotaikaisettulot) 
            return ansiopaivarahamaara - 0.5 * max(0,ansiopaivarahamaara+tyotaikaisettulot - vakpalkka) 
           
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

    def ansiopaivaraha_porrastus_YTU(self,tyoton: int,vakiintunutpalkka,lapsia: int,tyotaikaisettulot: float,saa_ansiopaivarahaa: int,
                       kesto: float,p: dict,ansiokerroin: float=None,omavastuukerroin: float=1.0,alku: str='',korotettu: bool=False):
        ansiopvrahan_suojaosa=0
        lapsikorotus=0
    
        if tyoton>0 and p[alku+'elakkeella']<1:
                            
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

                perus = self.sairauspaivaraha2023_YTU(0,0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                tuki2 = self.sairauspaivaraha2023_YTU(0,vakiintunutpalkka) * ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa = 0 #self.tyottomyysturva_suojaosa(ansiopvrahan_suojaosa,p) 
        
                perus = self.sairauspaivaraha2023_YTU(0,0)     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana

                #vakpalkka=vakiintunutpalkka*(1-self.sotumaksu)     
                #if tuki2>.9*vakpalkka:
                #    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavat_tulot=max(0,tyotaikaisettulot-suojaosa)
                ansiopaivarahamaara=max(0,tuki2-0.5*vahentavat_tulot)
                ansiopaivarahamaara = self.ansiopaivaraha_sovittelu(tuki2,tyotaikaisettulot,suojaosa)
                soviteltuperus=self.soviteltu_peruspaivaraha_YTU(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                #ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,soviteltuperus)  
                ansiopaivarahamaara=self.ansiopaivaraha_ylaraja_YTU(ansiopaivarahamaara,tyotaikaisettulot,vakiintunutpalkka,vakiintunutpalkka,soviteltuperus)  

                perus=max(0,soviteltuperus-ansiopaivarahamaara)
                tuki=omavastuukerroin*max(soviteltuperus,ansiopaivarahamaara)     # voi tulla vastaan pienillä tasoilla4
            else:
                if True: #p[alku+'peruspaivarahalla']>0:
                    ansiopaivarahamaara=0
                    perus=self.soviteltu_peruspaivaraha_YTU(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
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

    def soviteltu_peruspaivaraha_YTU(self,lapsia: int,tyotaikaisettulot: float,ansiopvrahan_suojaosa: int,p: dict) -> float:
        suojaosa=0
        pvraha=self.sairauspaivaraha2023_YTU(0,0)
        vahentavattulo=max(0,tyotaikaisettulot-suojaosa)
        tuki=max(0,pvraha-0.5*vahentavattulo)
    
        return tuki

    def sairauspaivaraha2023_YTU(self,palkka: float,vakiintunutpalkka: float):
        minimi=31.99*25 # = peruspäiväraha
        taite1=32_797/self.kk_jakaja  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)
