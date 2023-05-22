# haetaan tarpeelliset kirjastot
from .parameters import perheparametrit
from .benefits import Benefits
from .marginals_v2 import Marginals

import numpy as np 

class Bentest():
    # TESTS

    def __init__(self):
        self.year=2023
        self.kk_jakaja=12
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Benefits sisältää etuuskoodin
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')

        self.run_tests(p)

    def run_tests(self,p):
        self.test_tyotulovahennys2023()
        self.test_elaketulovahennys2023()
        self.test_ansiotulovahennys()
        self.test_perusvahennys2023()
        self.test_ylevero2023()
        self.test_valtionvero2023_tyo(p)
        self.test_valtionvero2023_elake(p)
        self.test_marg_tyo(p)

    def check_return(self,val,expected,decimals=2):
        prod=10**decimals
        if np.abs(val-expected)*prod<1:
            print('Passed')
            return True
        else:
            print('Failed')
            return False

    def test_tyotulovahennys2023(self):
        val=self.ben.laske_tyotulovahennys2023_2024(42510/12,42510/12,55)*12
        expected=1613.65
        print(f'työtulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_ansiotulovahennys(self):
        # for year 2023
        puhdas_ansiotulo=16_840
        palkkatulot_puhdas=puhdas_ansiotulo
        val=self.ben.laske_ansiotulovahennys(puhdas_ansiotulo/12,palkkatulot_puhdas/12)*12
        expected=3_442.20
        print(f'ansiotulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_elaketulovahennys2023(self):
        v,k=self.ben.elaketulovahennys2023(18000/12,18000/12)
        v=v*12
        k=k*12
        expected=6403.20
        print(f'elaketulovahennys2023 computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_perusvahennys2023(self):
        puhdas_ansiotulo=18_000-6403.20
        elake=18_000
        tulot=puhdas_ansiotulo
        v=self.ben.laske_perusvahennys(puhdas_ansiotulo/12,puhdas_ansiotulo/12)
        v=v*12
        expected=2_479.18
        print(f'perusvahennys2023 computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_ylevero2023(self):
        v=self.ben.laske_ylevero2023(15_900/12)*12
        expected=47.50
        print(f'ylevero2023 computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2022_tyo(self,p):
        valtionveroperuste=82_900
        v=self.ben.laske_valtionvero2018_2022(valtionveroperuste/12,p)*12
        expected=11_351.50
        print(f'valtionvero2023_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2023_tyo(self,p):
        valtionveroperuste=85_800
        v=self.ben.laske_valtionvero2023_2024(valtionveroperuste/12,p)*12
        expected=22_727.61
        print(f'valtionvero2023_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2023_elake(self,p):
        valtionveroperuste=54_000
        v = self.ben.raippavero2023(valtionveroperuste/12)*12

        expected=409.50
        print(f'raippavero eläke computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_marg_tyo(self,p):
        peruste=(15_000,16_000,17_000,18_000,19_000,20_000,30_000,50_000,100_000,200_000,1_000_000)
        vero=(8.7,10.2,10.3,10.9,12.3,13.5,21.8,31.6,42.1,50.4,56.5)
        marg=(11.2,12.5,12.5,37.0,37.0,37.0,43.6,49.5,59.2,58.0,58.0)
        p2=p.copy()
        p2['asumismenot_asumistuki']=0
        p2['asumismenot_toimeentulotuki']=0
        p2['ei_toimeentulotukea']=1

        print('efektiivinen marginaali ja veroaste -testi')
        for i,per in enumerate(peruste):
            eff,tva = self.marg.comp_test_margs(p2,salary=per/12)

            expected_marg=marg[i]
            print(f'marg @ {per} computed {eff} expected {expected_marg} ',end='')
            r1=self.check_return(eff,expected_marg,decimals=1)

            expected_tva=vero[i]
            print(f'vero @ {per} computed {tva} expected {expected_tva} ',end='')
            r2=self.check_return(tva,expected_tva,decimals=1)
