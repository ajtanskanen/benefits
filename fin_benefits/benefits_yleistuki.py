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
from .benefits import Benefits

class BenefitsYleistuki(Benefits):
    """
    Description:
        The Finnish Social Security as a Gym Module
        Universal Credit

    Source:
        Antti J. Tanskanen

    """
    
    def __init__(self,**kwargs):
        self.vaihe = 2
        super().__init__(**kwargs)
        self.set_year(self.year)
        self.yhteensovitus_tyotulo = 0.8 # asumistuki
        self.asumistuki_korvausaste = 0.7
        super().__init__(**kwargs)
        #self.setup_YTU()
        self.set_year(self.year)
        print(f'Yleistuki {self.year} BENEFITS')

    def set_yhteensovitus_tyotulo(self,prosentti):
        self.yhteensovitus_tyotulo = prosentti

    def set_asumistuki_korvausaste(self,prosentti):
        self.asumistuki_korvausaste = prosentti

    def set_vaihe(self,vaihe):
        self.vaihe = vaihe
        self.setup_YTU()

    def set_year(self,vuosi):
        super().set_year(vuosi)
        self.setup_YTU()

    def setup_YTU(self):
        self.asumistuki = self.asumistuki2023
        if self.vaihe ==1: # peruspäiväraha ja toimeentulotuki yhteen 
            #print('Vaihe 1')
            # do nothing
            a = 1
        elif self.vaihe==2 or self.vaihe==3: # totu ja asumistuki yhteen
            #print('Vaihe 2')
            self.asumistuki = self.asumistuki_YTU_stub
            self.toimeentulotuki = self.toimeentulotuki_YTU
            self.toimeentulotuki_param2023 = self.toimeentulotuki_param2023_YTU
            self.toimeentulotuki_param2025 = self.toimeentulotuki_param2025_YTU
        elif self.vaihe==4: # korvataan ansiosidonnainen päiväraha svpäivärahalla ja se kohdistuu kaikkiin
            #print('Vaihe 4')
            self.asumistuki = self.asumistuki_YTU_stub
            self.toimeentulotuki = self.toimeentulotuki_YTU
            self.toimeentulotuki_param2023 = self.toimeentulotuki_param2023_YTU
            self.toimeentulotuki_param2025 = self.toimeentulotuki_param2025_YTU
            self.ansiopaivaraha = self.ansiopaivaraha_porrastus_YTU

        if self.year==2023:
            self.toimeentulotuki_param = self.toimeentulotuki_param2023
            self.valtionvero_asteikko = self.valtionvero_asteikko_2023_HO
            self.lapsilisa = self.lapsilisa2023_HO
            self.tyotulovahennys=self.tyotulovahennys2023_HO
            self.veroparam=self.veroparam2023_HO
            self.sairauspaivaraha=self.sairauspaivaraha2023_YTU
            #self.ansiopaivaraha=self.ansiopaivaraha_HO
        elif self.year==2025:
            self.toimeentulotuki_param = self.toimeentulotuki_param2025
            self.tyotulovahennys = self.tyotulovahennys2025
            self.valtionvero_asteikko = self.valtionvero_asteikko_2025
            self.lapsilisa = self.lapsilisa2025
            self.veroparam = self.veroparam2025
            self.sairauspaivaraha=self.sairauspaivaraha2025_YTU
        else:
            print(f'year {self.year} not supported in yleistuki')

    def explain(self,p: dict =None):
        if p is None:
            print('Ei parametrejä')
        else:
            print(tee_selite(p))

    #def toimeentulotuki(self,omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,aikuisia,lapsia,kuntaryhma,p,omavastuuprosentti=0.05):        
    #    return super().toimeentulotuki(omabruttopalkka,omapalkkavero,puolison_bruttopalkka,puolison_palkkavero,muuttulot,verot,asumismenot,muutmenot,aikuisia,lapsia,kuntaryhma,p,omavastuuprosentti=omavastuuprosentti)

    def asumistuki_YTU_stub(self,palkkatulot1: float,palkkatulot2: float,muuttulot: float,vuokra: float,aikuisia: int,lapsia: int,kuntaryhma: int,p: dict) -> float:
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
        max_menot =np.array([[563, 563, 447, 394],[808, 808, 652, 574],[1_019, 1_019, 828, 734],[1_188, 1_188, 981, 875]])
        max_lisa =np.array([148, 148, 134, 129])

        # kuntaryhma=3
        max_menot[:,0] =max_menot[:,1]
        max_lisa[0] =max_lisa[1]

        max_meno =max_menot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_lisa[kuntaryhma]

        prosentti = 0.7 # vastaa 80 %
        suojaosa = 0 #p['asumistuki_suojaosa']*p['aikuisia']
        prosentti = self.asumistuki_korvausaste # 0.7 # vastaa 70 %
        
        yhteensovitus_tyotulo= self.yhteensovitus_tyotulo #1.0
        yhteensovitus_muut = 1.0
        lapsiparam = 246*1.05
        perusomavastuu_nollatulot = max(0,-0.50*(667+111*aikuisia+lapsiparam*lapsia))
        perusomavastuu = max(0,
            0.50*(max(0,yhteensovitus_tyotulo*palkkatulot1-suojaosa)
                 +max(0,yhteensovitus_tyotulo*palkkatulot2-suojaosa)
                 +yhteensovitus_muut*muuttulot
                 -(667+111*aikuisia+lapsiparam*lapsia)))
        if perusomavastuu<10:
            perusomavastuu = 0
        #if p['aikuisia']==1 and p['tyoton']==1 and p['saa_ansiopaivarahaa']==0 and palkkatulot<1 and p['lapsia']==0:
        #    perusomavastuu=0
            
        # lasketaan tuet ml. työskentely ja muut tuet
        tuki = max(0,(min(max_meno,vuokra)-perusomavastuu)*prosentti)
        # lasketaan tuet ilman työskentelyä ja muita tukia
        tuki0 = max(0,(min(max_meno,vuokra)-perusomavastuu_nollatulot)*prosentti)
            
        if tuki<30:
            tuki = 0
            
        if tuki0<30:
            tuki0 = 0

        # yhteensovituksen vaikutus        
        asu_vero = tuki0 - tuki

        #asu_vero1 = max(0,min(asumistuki_nollatulot,0.7*0.5*(max(0,palkkakerroin*omabruttopalkka+palkkakerroin*puolison_bruttopalkka+muut_tulot_asumistuki+elakelaisen_asumistuki+perusomavastuu_nollatulot))))
        #asu_vero1 = max(0,min(tuki0,prosentti*0.5*(max(0,yhteensovitus_tyotulo*palkkatulot1+yhteensovitus_tyotulo*palkkatulot2+muuttulot-perusomavastuu_nollatulot))))
        #print('palkkatulot1',palkkatulot1,'asu_vero',asu_vero,'asu_vero1',asu_vero1,'tuki',tuki,'tuki0',tuki0)

        #if self.use_extra_ppr:
        #    tuki=tuki*self.extra_ppr_factor
    
        return tuki,tuki0,perusomavastuu_nollatulot,asu_vero

    def toimeentulotuki_param2023_YTU(self) -> (float,float,float,float,float,float,float,float,float):
        '''
        '''
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150

        kerroin = 640 / 593.55
        yksinasuva = 555.11 * kerroin

        lapsi_kerroin_alle10_1 = 0.75
        lapsi_kerroin_alle10_2 = 0.70
        lapsi_kerroin_alle10_3 = 0.65
        lapsi_kerroin_alle18_1 = 0.75
        lapsi_kerroin_alle18_2 = 0.70 
        lapsi_kerroin_alle18_3 = 0.65
        lapsi_kerroin_18 = 0.75
        aikuinen_kerroin = 0.85
        yksinhuoltaja_kerroin = 1.14

        lapsiparam = np.zeros((3,3))

        lapsiparam[0,0] = yksinasuva * lapsi_kerroin_alle10_1     # e/kk     alle 10v lapsi
        lapsiparam[0,1] = yksinasuva * lapsi_kerroin_alle10_2    # e/kk
        lapsiparam[0,2] = yksinasuva * lapsi_kerroin_alle10_3      # e/kk

        lapsiparam[1,0] = yksinasuva * lapsi_kerroin_alle18_1     # e/kk   10-17 v lapsi
        lapsiparam[1,1] = yksinasuva * lapsi_kerroin_alle18_2    # e/kk
        lapsiparam[1,2] = yksinasuva * lapsi_kerroin_alle18_3      # e/kk

        lapsiparam[2,0] = yksinasuva * lapsi_kerroin_18     # e/kk  18+ lapsi
        lapsiparam[2,1] = yksinasuva * lapsi_kerroin_18    # e/kk
        lapsiparam[2,2] = yksinasuva * lapsi_kerroin_18      # e/kk

        yksinhuoltaja = yksinasuva * yksinhuoltaja_kerroin    # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot
        muu = yksinasuva * aikuinen_kerroin
        
        # Helsinki: 694 869 993 1089 122
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot = np.array([[694, 492, 398, 352],[869, 621, 557, 463],[993, 747, 675, 568],[1089, 793, 746, 617]])
        max_lisa = np.array([122, 99, 96, 96])

        return min_etuoikeutettuosa,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa,lapsiparam

    def toimeentulotuki_param2025_YTU(self) -> (float,float,float,float,float,float,float,float,float):
        '''
        Päivitetty 10.12.2024
        '''
        self.toimeentulotuki_omavastuuprosentti = 0.0
        min_etuoikeutettuosa=150
        
        kerroin = 640 / 593.55
        yksinasuva = 593.55 * kerroin


        lapsi_kerroin_alle10_1 = 0.75
        lapsi_kerroin_alle10_2 = 0.70
        lapsi_kerroin_alle10_3 = 0.65
        lapsi_kerroin_alle18_1 = 0.75
        lapsi_kerroin_alle18_2 = 0.70
        lapsi_kerroin_alle18_3 = 0.65
        lapsi_kerroin_18 = 0.75
        aikuinen_kerroin = 0.85
        yksinhuoltaja_kerroin = 1.14
        
        lapsiparam = np.zeros((3,3))

        lapsiparam[0,0] = yksinasuva * lapsi_kerroin_alle10_1     # e/kk     alle 10v lapsi
        lapsiparam[0,1] = yksinasuva * lapsi_kerroin_alle10_2    # e/kk
        lapsiparam[0,2] = yksinasuva * lapsi_kerroin_alle10_3      # e/kk

        lapsiparam[1,0] = yksinasuva * lapsi_kerroin_alle18_1     # e/kk   10-17 v lapsi
        lapsiparam[1,1] = yksinasuva * lapsi_kerroin_alle18_2    # e/kk
        lapsiparam[1,2] = yksinasuva * lapsi_kerroin_alle18_3      # e/kk

        lapsiparam[2,0] = yksinasuva * lapsi_kerroin_18     # e/kk  18+ lapsi
        lapsiparam[2,1] = yksinasuva * lapsi_kerroin_18    # e/kk
        lapsiparam[2,2] = yksinasuva * lapsi_kerroin_18      # e/kk

        lapsi1 = yksinasuva * lapsi_kerroin_alle10_1     # e/kk     alle 10v lapsi
        lapsi2 = yksinasuva * lapsi_kerroin_alle10_2    # e/kk
        lapsi3 = yksinasuva * lapsi_kerroin_alle10_3      # e/kk

        lapsi1_10_17 = yksinasuva * lapsi_kerroin_alle18_1     # e/kk  
        lapsi2_10_17 = yksinasuva * lapsi_kerroin_alle18_2    # e/kk
        lapsi3_10_17 = yksinasuva * lapsi_kerroin_alle18_3      # e/kk

        yksinhuoltaja = yksinasuva * yksinhuoltaja_kerroin    # e/kk
        # muu 18v täyttänyt ja avio- ja avopuolisot
        muu = yksinasuva * aikuinen_kerroin

        # Helsinki: 715 507 993 1089 122
        # Kangasala: 492 621 747 793 99
        # Heinola: 398 557 675 746 96
        # Kihniö: 352 463 568 617 96
        max_asumismenot=np.array([[715, 507, 418, 363],[895, 652, 574, 463],[1023, 784, 709, 596],[1122, 793, 746, 617]])
        max_lisa=np.array([122, 99, 96, 96])

        return min_etuoikeutettuosa,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_lisa,lapsiparam

    def toimeentulotuki_YTU(self,omabruttopalkka: float,omapalkkavero: float,puolison_bruttopalkka: float,puolison_palkkavero: float,
                        muuttulot: float,verot: float,asumismenot: float,muutmenot: float,aikuisia: int, lapsia: int,kuntaryhma: int,
                        p: dict,omavastuuprosentti: float=0.0,alennus: int=0,asumistuki: float=None,muut_tulot_asumistuki: float=None):
        '''
        '''
        min_etuoikeutettuosa,yksinhuoltaja,muu,yksinasuva,max_asumismenot,max_asumislisa,lapsiparam = self.toimeentulotuki_param()
        max_asumismeno = max_asumismenot[min(3,aikuisia+lapsia-1),kuntaryhma]+max(0,aikuisia+lapsia-4)*max_asumislisa[kuntaryhma]

        asumismenot = min(asumismenot,max_asumismeno)            
        menot = muutmenot # ei huomioida asumismenoja

        elakelaisen_asumistuki = asumistuki

        if p['aikuisia']>1 and p['puoliso_alive']>0:
            if p['elakkeella']>0 and p['puoliso_elakkeella']>0:
                asumistuki,asumistuki_nollatulot,perusomavastuu_nollatulot,asu_vero = 0,0,0,0
            else:
                asumistuki,asumistuki_nollatulot,perusomavastuu_nollatulot,asu_vero = self.asumistuki2023_YTU(omabruttopalkka,puolison_bruttopalkka,muut_tulot_asumistuki,asumismenot,aikuisia,lapsia,kuntaryhma,p)
        else:
            if p['elakkeella']>0:
                asumistuki,asumistuki_nollatulot,perusomavastuu_nollatulot,asu_vero = 0,0,0,0
            else:
                asumistuki,asumistuki_nollatulot,perusomavastuu_nollatulot,asu_vero = self.asumistuki2023_YTU(omabruttopalkka,puolison_bruttopalkka,muut_tulot_asumistuki,asumismenot,aikuisia,lapsia,kuntaryhma,p)

        #print(asumistuki,asumistuki_nollatulot,perusomavastuu_nollatulot)
        #menot = asumismenot+muutmenot    
        bruttopalkka = omabruttopalkka+puolison_bruttopalkka    
        palkkavero = omapalkkavero+puolison_palkkavero    
        palkkatulot = bruttopalkka-palkkavero    
        
        if False:   
            omaetuoikeutettuosa = max(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
            puolison_etuoikeutettuosa = max(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
        else:        
            omaetuoikeutettuosa = 0.25*omabruttopalkka # min(min_etuoikeutettuosa,0.2*omabruttopalkka)     # etuoikeutettu osa edunsaajakohtainen 1.1.2015 alkaen
            puolison_etuoikeutettuosa = 0.25*puolison_bruttopalkka # min(min_etuoikeutettuosa,0.2*puolison_bruttopalkka)    
            
        etuoikeutettuosa = omaetuoikeutettuosa+puolison_etuoikeutettuosa    

        if aikuisia<2:
            if lapsia<1: 
                tuki1 = yksinasuva     # yksinasuva 485,50
            elif lapsia>0:
                lapset_alle10 = p['lapsia_alle_kouluikaisia']
                lapset_10_17 = lapsia - lapset_alle10
                lapset_18 = 0 # näitä ei mukana simulaatiossa
                tuki1 = yksinhuoltaja + self.toimeentulotuki_lapsiosuus(lapset_alle10,lapset_10_17,lapset_18,lapsiparam)
        else:
            lapset_alle10 = p['lapsia_alle_kouluikaisia']
            lapset_10_17 = lapsia - lapset_alle10
            lapset_18 = 0 # näitä ei mukana simulaatiossa
            tuki1 = muu*aikuisia + self.toimeentulotuki_lapsiosuus(lapset_alle10,lapset_10_17,lapset_18,lapsiparam)

        # if (bruttopalkka-etuoikeutettuosa>palkkavero)
        #    tuki = max(0,tuki1+menot-max(0,bruttopalkka-etuoikeutettuosa-palkkavero)-verot-muuttulot)    
        #else 
        #    verot2 = palkkavero+verot-max(0,(bruttopalkka-etuoikeutettuosa))    
        #    tuki = max(0,tuki1+menot-muuttulot+verot2)    
        #end
        
        if alennus>0:
            tuki1 = tuki1*(1-alennus)
            
        #if self.use_extra_ppr:
        #    tuki1 = tuki1*self.extra_ppr_factor
        
        #palkkakerroin = 1.0
        #asu_vero1 = max(0,min(asumistuki_nollatulot,0.7*0.5*(max(0,palkkakerroin*omabruttopalkka+palkkakerroin*puolison_bruttopalkka+muut_tulot_asumistuki+elakelaisen_asumistuki+perusomavastuu_nollatulot))))
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

        # asumisosan vähennys tulojen mukaan huomioidaan yhteensovituksessa, tulojen yhteensovitus ei voi olla yli 80 % (etuoikeutettu osa 20%)
        totu_osa = max(0,tuki1+menot-max(0,omabruttopalkka-omaetuoikeutettuosa-omapalkkavero-asu_vero_oma)\
                                    -max(0,puolison_bruttopalkka-puolison_etuoikeutettuosa-puolison_palkkavero-asu_vero_puoliso)-max(0,verot-palkkavero)-muuttulot)        

        #print(f'omabruttopalkka {omabruttopalkka:.2f} muuttulot {muuttulot:.2f} totu_osa {totu_osa:.2f} asu_osa {asu_osa:.2f} asumistuki {asumistuki:.2f} ast0 {asumistuki_nollatulot:.2f} po0 {perusomavastuu_nollatulot:.2f}')

        tuki = totu_osa + asu_osa

        if p['toimeentulotuki_vahennys']>0: # vähennetään 20%
            tuki = tuki*0.8
            if p['toimeentulotuki_vahennys']>99: # vähennetään 100%
                tuki = 0.0
                
        if tuki<10:
            tuki = 0    
            
        return tuki 

    def ansiopaivaraha_ylaraja_YTU(self,ansiopaivarahamaara: float,tyotaikaisettulot: float,vakpalkka: float,vakiintunutpalkka: float,peruspvraha: float) -> float:
        if vakpalkka<ansiopaivarahamaara+tyotaikaisettulot:
            #return max(0,vakpalkka-tyotaikaisettulot) 
            return ansiopaivarahamaara - 0.5 * max(0,ansiopaivarahamaara+tyotaikaisettulot - vakpalkka) 
            #return ansiopaivarahamaara - 0.0 * max(0,ansiopaivarahamaara+tyotaikaisettulot - vakpalkka) 
           
        return ansiopaivarahamaara   
        
    def laske_sotumaksu(self,vuosi: int):
        '''
        '''
        if vuosi==2018:
            sotumaksu = 0.0448+0.6*self.additional_tyel_premium
        elif vuosi==2019:
            sotumaksu = 0.0448+0.6*self.additional_tyel_premium
        elif vuosi==2020:
            sotumaksu = 0.0414+0.6*self.additional_tyel_premium
        elif vuosi==2021:
            sotumaksu = 0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2022:
            sotumaksu = 0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2023:
            sotumaksu = 0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2024:
            sotumaksu = 0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2025:
            sotumaksu = 0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2026:
            sotumaksu = 0.0434+0.6*self.additional_tyel_premium
        elif vuosi==2027:
            sotumaksu = 0.0434+0.6*self.additional_tyel_premium
        else:
            sotumaksu=0.0448+0.6*self.additional_tyel_premium
            
        return sotumaksu

    def ansiopaivaraha_porrastus_YTU(self,tyoton: int,vakiintunutpalkka,lapsia: int,tyotaikaisettulot: float,saa_ansiopaivarahaa: int,
                       kesto: float,p: dict,ansiokerroin: float=None,omavastuukerroin: float=1.0,alku: str='',korotettu: bool=False):
        ansiopvrahan_suojaosa = 0
        lapsikorotus = 0

        if tyoton>0 and p[alku+'elakkeella']<1:
                            
            if saa_ansiopaivarahaa>0: # & (kesto<400.0): # ei keston tarkastusta!
                #print(f'tyoton {tyoton} vakiintunutpalkka {vakiintunutpalkka} lapsia {lapsia} tyotaikaisettulot {tyotaikaisettulot} saa_ansiopaivarahaa {saa_ansiopaivarahaa} kesto {kesto} ansiokerroin {ansiokerroin} omavastuukerroin {omavastuukerroin}')
            
                # porrastetaan ansio-osa keston mukaan
                # 2 kk -> 80%
                # 34 vko -> 75%
                if ansiokerroin is None:
                    if kesto>34/52*12*21.5:
                        ansiokerroin = 0.75
                    elif kesto>2*21.5:
                        ansiokerroin = 0.80
                    else:
                        ansiokerroin = 1.00 # =1-2/3/21.5

                perus = self.sairauspaivaraha2023_YTU(0,0)     # peruspäiväraha lasketaan tässä kohdassa ilman lapsikorotusta
                tuki2 = self.sairauspaivaraha2023_YTU(0,vakiintunutpalkka) * ansiokerroin # mahdollinen porrastus tehdään tämän avulla
                suojaosa = 0 
        
                #perus = self.sairauspaivaraha2023_YTU(0,0)     # peruspäiväraha lasketaan tässä kohdassa lapsikorotukset mukana

                # luovutaan rajasta
                #vakpalkka=vakiintunutpalkka*(1-self.sotumaksu)     
                #if tuki2>.9*vakpalkka:
                #    tuki2=max(.9*vakpalkka,perus)    
        
                vahentavat_tulot = max(0,tyotaikaisettulot-suojaosa)
                ansiopaivarahamaara = max(0,tuki2-0.5*vahentavat_tulot)
                #ansiopaivarahamaara = self.ansiopaivaraha_sovittelu(tuki2,tyotaikaisettulot,suojaosa)
                soviteltuperus=self.soviteltu_peruspaivaraha_YTU(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                #ansiopaivarahamaara=self.ansiopaivaraha_ylaraja(ansiopaivarahamaara,tyotaikaisettulot,vakpalkka,vakiintunutpalkka,soviteltuperus)  
                ansiopaivarahamaara = self.ansiopaivaraha_ylaraja_YTU(ansiopaivarahamaara,tyotaikaisettulot,vakiintunutpalkka,vakiintunutpalkka,soviteltuperus)  

                perus = max(0,soviteltuperus-ansiopaivarahamaara)
                tuki = omavastuukerroin*max(soviteltuperus,ansiopaivarahamaara)     # voi tulla vastaan pienillä tasoilla4
            else:
                ansiopaivarahamaara = 0
                perus = self.soviteltu_peruspaivaraha_YTU(lapsia,tyotaikaisettulot,ansiopvrahan_suojaosa,p)    
                tuki = omavastuukerroin*perus
        else:
            perus = 0    
            tuki = 0    
            ansiopaivarahamaara = 0   

        return tuki,ansiopaivarahamaara,perus

    def ansiopaivaraha_sovittelu_YTU(self,tuki2: float,tyotaikaisettulot: float,suojaosa: float):
        vahentavat_tulot = max(0,tyotaikaisettulot-suojaosa)
        ansiopaivarahamaara = max(0,tuki2-0.5*vahentavat_tulot)

        return ansiopaivarahamaara

    def soviteltu_peruspaivaraha_YTU(self,lapsia: int,tyotaikaisettulot: float,ansiopvrahan_suojaosa: int,p: dict) -> float:
        suojaosa = 0
        if self.year==2023:
            pvraha = self.sairauspaivaraha2023_YTU(0,0)
        elif self.year==2025:
            pvraha = self.sairauspaivaraha2025_YTU(0,0)
        vahentavattulo = max(0,tyotaikaisettulot-suojaosa)
        tuki = max(0,pvraha-0.5*vahentavattulo)
    
        return tuki

    def sairauspaivaraha2023_YTU(self,palkka: float,vakiintunutpalkka: float):
        minimi = 31.99*25 #  =  peruspäiväraha
        taite1 = 32_797/self.kk_jakaja  
        vakiintunut = (1-0.0858)*vakiintunutpalkka                    
                    
        raha = max(minimi,0.7*min(taite1,vakiintunut)+0.15*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)

    def sairauspaivaraha2023(self,palkka: float,vakiintunutpalkka: float):
        minimi=31.99*25
        taite1=32_797/self.kk_jakaja  
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)

    def sairauspaivaraha2025_YTU(self,palkka: float,vakiintunutpalkka: float):
        if True: # "neutraali"
            minimi = 31.99*25 #  =  peruspäiväraha
            taite1 = 35_500 # (1-0.0858)*32_797/self.kk_jakaja # = 29983
            vakiintunut = vakiintunutpalkka
            kerroin1 = 0.64 # (1-0.0858)*0.7 # = 0.63994
            kerroin2 = 0.19 # (1-0.0858)*0.15 # = 0.13713
        else: # nykytila ilman pros.vähennyksiä
            minimi = 31.99*25 #  =  peruspäiväraha
            taite1 = 35_500 # (1-0.0858)*32_797/self.kk_jakaja # = 29983
            vakiintunut = vakiintunutpalkka
            kerroin1 = 0.64 # (1-0.0858)*0.7 # = 0.63994
            kerroin2 = 0.15 # (1-0.0858)*0.15 # = 0.13713
                    
        raha = max(minimi,kerroin1*min(taite1,vakiintunut)+kerroin2*max(vakiintunut-taite1,0))

        return max(0,raha-palkka)
    
    def sairauspaivaraha2025(self,palkka: float,vakiintunutpalkka: float):
        minimi=31.99*25
        taite1=28_241/self.kk_jakaja
        vakiintunut=(1-self.sotumaksu)*vakiintunutpalkka                    
                    
        raha=max(minimi,0.7*min(taite1,vakiintunut)+0.15*max(vakiintunut-taite1,0))

        return max(0,raha-palkka) 

    def ansiopaivaraha_HO(self,tyoton,vakiintunutpalkka,lapsia,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p,ansiokerroin=1.0,omavastuukerroin=1.0,alku=''):
        # porrastetaan ansio-osa keston mukaan
        # 2 kk -> 80%
        # 34 vko -> 75%
        if self.porrastus:
            if kesto>34/52*12*21.5:
                kerroin=0.75
            elif kesto>2*21.5:
                kerroin=0.80
            else:
                kerroin=1.00 # =1-2/3/21.5
        else:
            if kesto<3*21.5:
                kerroin=1.00 # =1-2/3/21.5
            else:
                kerroin=1.00 # =1-2/3/21.5
            
        p2=p.copy()

        p2['tyottomyysturva_suojaosa_taso']=0
        p2['ansiopvrahan_suojaosa']=0
        p2['ansiopvraha_lapsikorotus']=0
        lapsia = 0

        # kutsutaan alkuperäistä ansiopäivärahaa kertoimella
        return super().ansiopaivaraha_porrastus(tyoton,vakiintunutpalkka,0,tyotaikaisettulot,saa_ansiopaivarahaa,kesto,p2,ansiokerroin=kerroin,omavastuukerroin=omavastuukerroin,alku=alku)

    def veroparam2023_HO(self):
        '''
        Päivitetty 6.5.2023
        '''
        super().veroparam2023()
        self.tyottomyysvakuutusmaksu=0.0150 - 0.002 # vastaa VM:n arviota rakenteellisesta maksun muutoksesta 
 
    def valtionvero_asteikko_2023_HO(self):
        rajat=np.array([0,19_900,29_700,49_000,150_000])/self.kk_jakaja
        pros=(1-100/20000)*np.maximum(0,np.array([0.1264,0.19,0.3025,0.34,0.44+self.additional_income_tax_high])+self.additional_income_tax)
        pros=np.maximum(0,np.minimum(pros,0.44+self.additional_income_tax_high+self.additional_income_tax))
        return rajat,pros

    def lapsilisa2023_HO(self,yksinhuoltajakorotus: bool=False,alle3v: int=0) -> float:
        lapsilisat=np.array([94.88,104.84,133.79,163.24,182.69]) + 2.0
        if yksinhuoltajakorotus:
            # yksinhuoltajakorotus 53,30 e/lapsi
            lapsilisat += 68.3 + 10.0
            
        return lapsilisat

    def tyotulovahennys2023_HO(self,ika: float,lapsia: int):
        if ika>=65:
            max_tyotulovahennys=3230/self.kk_jakaja
        else:
            max_tyotulovahennys=2030/self.kk_jakaja
        ttulorajat=np.array([0,22000,77000])/self.kk_jakaja # 127000??
        ttulopros=np.array([0.13,0.0203,0.121])
        return max_tyotulovahennys,ttulorajat,ttulopros
