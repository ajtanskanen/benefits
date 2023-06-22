# haetaan tarpeelliset kirjastot
from .parameters import perheparametrit,tee_selite
from .benefits import Benefits
from .marginals_v2 import Marginals

import numpy as np 

class Bentest():
    # TESTS

    def __init__(self):
        self.kk_jakaja=12

        self.run_tests_2018()
        self.run_tests_2019()
        self.run_tests_2020()
        self.run_tests_2021()
        self.run_tests_2022()
        self.run_tests_2023()
        #self.run_tests_2024()

    def run_tests_2018(self):
        # Luokka Benefits sisältää etuuskoodin
        self.year=2018
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')

        print('\nRunning tests on 2018')
        self.test_tyotulovahennys2018()
        self.test_elaketulovahennys2018()
        self.test_ansiotulovahennys2018()
        self.test_perusvahennys2018()
        self.test_ylevero2018()
        self.test_valtionvero2018_tyo(p)
        self.test_valtionvero2018_elake(p)
        #self.test_marg_tyo2018(p)

    def run_tests_2019(self):
        # Luokka Benefits sisältää etuuskoodin
        self.year=2019
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')

        print('\nRunning tests on 2019')
        self.test_tyotulovahennys2019()
        self.test_elaketulovahennys2019()
        self.test_ansiotulovahennys2019()
        self.test_perusvahennys2019()
        self.test_ylevero2019()
        self.test_valtionvero2019_tyo(p)
        self.test_valtionvero2019_elake(p)
        #self.test_marg_tyo2019(p)

    def run_tests_2020(self):
        # Luokka Benefits sisältää etuuskoodin
        self.year=2020
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')

        print('\nRunning tests on 2020')
        self.test_tyotulovahennys2020()
        self.test_elaketulovahennys2020()
        self.test_ansiotulovahennys2020()
        self.test_perusvahennys2020()
        self.test_ylevero2020()
        self.test_valtionvero2020_tyo(p)
        self.test_valtionvero2020_elake(p)
        #self.test_marg_tyo2020(p)

    def run_tests_2021(self):
        # Luokka Benefits sisältää etuuskoodin
        self.year=2021
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')

        print('\nRunning tests on 2021')
        self.test_tyotulovahennys2021()
        self.test_elaketulovahennys2021()
        self.test_ansiotulovahennys2021()
        self.test_perusvahennys2021()
        self.test_ylevero2021()
        self.test_paivarahamaksu2021()
        self.test_valtionvero2021_tyo(p)
        self.test_valtionvero2021_elake(p)
        self.test_marg_tyo2021(p)

    def run_tests_2022(self):
        # Luokka Benefits sisältää etuuskoodin
        self.year=2022
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')

        print('\nRunning tests on 2022')
        self.test_tyotulovahennys2022()
        self.test_elaketulovahennys2022()
        self.test_ansiotulovahennys2022()
        self.test_perusvahennys2022()
        self.test_ylevero2022()
        self.test_valtionvero2022_tyo(p)
        self.test_valtionvero2022_elake(p)
        self.test_marg_tyo2022(p)

    def run_tests_2023(self):
        # Luokka Benefits sisältää etuuskoodin
        self.year=2023
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)
        p2,selite2=perheparametrit(perhetyyppi=58,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')

        print('\nRunning tests on 2023')
        self.test_tyotulovahennys2023()
        self.test_elaketulovahennys2023()
        self.test_ansiotulovahennys2023()
        self.test_perusvahennys2023()
        self.test_ylevero2023()
        self.test_valtionvero2023_tyo(p)
        self.test_valtionvero2023_elake(p)
        self.test_marg_tyo2023(p)
        self.test_marg_elake2023(p2)

    def run_tests_2024(self):
        # Luokka Benefits sisältää etuuskoodin
        self.year=2024
        self.ben=Benefits(year=self.year,include_kirkollisvero=True)
        p,selite=perheparametrit(perhetyyppi=1,kuntaryhmä=1,vuosi=self.year,tulosta=False)
        p2,selite=perheparametrit(perhetyyppi=58,kuntaryhmä=1,vuosi=self.year,tulosta=False)

        # Luokka Marginals sisältää marginaalien plottausfunktiot
        self.marg=Marginals(self.ben,year=self.year,incl_alv=False,lang='eng')
        print('Running tests on 2024')
        self.test_tyotulovahennys2024()
        self.test_elaketulovahennys2024()
        self.test_ansiotulovahennys2024()
        self.test_perusvahennys2024()
        self.test_ylevero2024()
        self.test_valtionvero2024_tyo(p)
        self.test_valtionvero2024_elake(p)
        self.test_marg_tyo2024(p)

    def check_return(self,val,expected,decimals=2):
        prod=10**decimals
        if np.abs(val-expected)*prod<1:
            print('Passed')
            return True
        else:
            print('Failed')
            return False

    def test_tyotulovahennys2018(self):
        val=self.ben.laske_tyotulovahennys2018_2022(42510/12,42510/12,55)*12
        expected=1383.08
        print(f'työtulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_tyotulovahennys2019(self):
        val=self.ben.laske_tyotulovahennys2018_2022(42510/12,42510/12,55)*12
        expected=1466.43
        print(f'työtulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_tyotulovahennys2020(self):
        val=self.ben.laske_tyotulovahennys2018_2022(42510/12,42510/12,55)*12
        expected=1595.02
        print(f'työtulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_tyotulovahennys2021(self):
        val=self.ben.laske_tyotulovahennys2018_2022(42510/12,42510/12,55)*12
        expected=1660.26
        print(f'työtulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_tyotulovahennys2022(self):
        val=self.ben.laske_tyotulovahennys2018_2022(42510/12,42510/12,55)*12
        expected=1743.60
        print(f'työtulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_tyotulovahennys2023(self):
        val=self.ben.laske_tyotulovahennys2023_2024(42510/12,42510/12,55)*12
        expected=1613.65
        print(f'työtulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_ansiotulovahennys2018(self):
        # for year 2023
        puhdas_ansiotulo=15_840
        palkkatulot_puhdas=puhdas_ansiotulo
        val=self.ben.laske_ansiotulovahennys(puhdas_ansiotulo/12,palkkatulot_puhdas/12)*12
        expected=3487.20
        print(f'ansiotulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_ansiotulovahennys2019(self):
        # for year 2023
        puhdas_ansiotulo=15_840
        palkkatulot_puhdas=puhdas_ansiotulo
        val=self.ben.laske_ansiotulovahennys(puhdas_ansiotulo/12,palkkatulot_puhdas/12)*12
        expected=3487.20
        print(f'ansiotulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_ansiotulovahennys2020(self):
        # for year 2023
        puhdas_ansiotulo=15_840
        palkkatulot_puhdas=puhdas_ansiotulo
        val=self.ben.laske_ansiotulovahennys(puhdas_ansiotulo/12,palkkatulot_puhdas/12)*12
        expected=3487.20
        print(f'ansiotulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)
        
    def test_ansiotulovahennys2021(self):
        # for year 2023
        puhdas_ansiotulo=15_840
        palkkatulot_puhdas=puhdas_ansiotulo
        val=self.ben.laske_ansiotulovahennys(puhdas_ansiotulo/12,palkkatulot_puhdas/12)*12
        expected=3487.20
        print(f'ansiotulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_ansiotulovahennys2022(self):
        # for year 2022
        puhdas_ansiotulo=15_840
        palkkatulot_puhdas=puhdas_ansiotulo
        val=self.ben.laske_ansiotulovahennys(puhdas_ansiotulo/12,palkkatulot_puhdas/12)*12
        expected=3487.20
        print(f'ansiotulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_ansiotulovahennys2023(self):
        # for year 2023
        puhdas_ansiotulo=16_840
        palkkatulot_puhdas=puhdas_ansiotulo
        val=self.ben.laske_ansiotulovahennys(puhdas_ansiotulo/12,palkkatulot_puhdas/12)*12
        expected=3_442.20
        print(f'ansiotulovähennys computed {val} expected {expected} ',end='')
        return self.check_return(val,expected)

    def test_elaketulovahennys2018(self):
        v,k=self.ben.elaketulovahennys2023(18000/12,18000/12)
        v=v*12
        k=k*12
        expected=6403.20
        print(f'elaketulovahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_elaketulovahennys2019(self):
        v,k=self.ben.elaketulovahennys2023(18000/12,18000/12)
        v=v*12
        k=k*12
        expected=6403.20
        print(f'elaketulovahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_elaketulovahennys2020(self):
        v,k=self.ben.elaketulovahennys2023(18000/12,18000/12)
        v=v*12
        k=k*12
        expected=6403.20
        print(f'elaketulovahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_elaketulovahennys2021(self):
        v,k=self.ben.elaketulovahennys2023(18000/12,18000/12)
        v=v*12
        k=k*12
        expected=6403.20
        print(f'elaketulovahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_elaketulovahennys2022(self):
        v,k=self.ben.elaketulovahennys2023(18000/12,18000/12)
        v=v*12
        k=k*12
        expected=6403.20
        print(f'elaketulovahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_elaketulovahennys2023(self):
        v,k=self.ben.elaketulovahennys2023(18000/12,18000/12)
        v=v*12
        k=k*12
        expected=6403.20
        print(f'elaketulovahennys2023 computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_perusvahennys2018(self):
        puhdas_ansiotulo=18_000-4470.40
        elake=18_000
        tulot=puhdas_ansiotulo
        v=self.ben.laske_perusvahennys(puhdas_ansiotulo/12)
        v=v*12
        expected=1222.67
        print(f'perusvahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_perusvahennys2019(self):
        puhdas_ansiotulo=18_000-4485.50
        elake=18_000
        tulot=puhdas_ansiotulo
        v=self.ben.laske_perusvahennys(puhdas_ansiotulo/12)
        v=v*12
        expected=1_467.29
        print(f'perusvahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_perusvahennys2020(self):
        puhdas_ansiotulo=18_000-4757.30
        elake=18_000
        tulot=puhdas_ansiotulo
        v=self.ben.laske_perusvahennys(puhdas_ansiotulo/12)
        v=v*12
        expected=1_793.51
        print(f'perusvahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_perusvahennys2021(self):
        puhdas_ansiotulo=18_000-4817.70
        elake=18_000
        tulot=puhdas_ansiotulo
        v=self.ben.laske_perusvahennys(puhdas_ansiotulo/12)
        v=v*12
        expected=1910.59
        print(f'perusvahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)                        

    def test_perusvahennys2022(self):
        # kunnallisveron perusvähennys
        puhdas_ansiotulo=18_000-5_165
        elake=18_000
        tulot=puhdas_ansiotulo
        v=self.ben.laske_perusvahennys(puhdas_ansiotulo/12)
        v=v*12
        expected=2_102.90
        print(f'perusvahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_perusvahennys2023(self):
        puhdas_ansiotulo=18_000-6403.20
        elake=18_000
        tulot=puhdas_ansiotulo
        v=self.ben.laske_perusvahennys(puhdas_ansiotulo/12)
        v=v*12
        expected=2_479.18
        print(f'perusvahennys{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_ylevero2018(self):
        v=self.ben.laske_ylevero2023(15_900/12)*12
        expected=47.50
        print(f'ylevero{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_ylevero2019(self):
        v=self.ben.laske_ylevero2023(15_900/12)*12
        expected=47.50
        print(f'ylevero{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_ylevero2020(self):
        v=self.ben.laske_ylevero2023(15_900/12)*12
        expected=47.50
        print(f'ylevero{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_ylevero2021(self):
        v=self.ben.laske_ylevero2023(15_900/12)*12
        expected=47.50
        print(f'ylevero{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_ylevero2022(self):
        v=self.ben.laske_ylevero2023(15_900/12)*12
        expected=47.50
        print(f'ylevero{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_ylevero2023(self):
        v=self.ben.laske_ylevero2023(15_900/12)*12
        expected=47.50
        print(f'ylevero{self.year} computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2018_tyo(self,p):
        valtionveroperuste=74_200
        v=self.ben.laske_valtionvero2018_2022(valtionveroperuste/12,p)*12
        expected=10156.25
        print(f'valtionvero{self.year}_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2018_elake(self,p):
        valtionveroperuste=54_000
        v = self.ben.raippavero2023(valtionveroperuste/12)*12

        expected=409.50
        print(f'raippavero eläke computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2019_tyo(self,p):
        valtionveroperuste=76_100
        v=self.ben.laske_valtionvero2018_2022(valtionveroperuste/12,p)*12
        expected=10413.25
        print(f'valtionvero{self.year}_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2019_elake(self,p):
        valtionveroperuste=54_000
        v = self.ben.raippavero2023(valtionveroperuste/12)*12

        expected=409.50
        print(f'raippavero eläke computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2020_tyo(self,p):
        valtionveroperuste=78_500
        v=self.ben.laske_valtionvero2018_2022(valtionveroperuste/12,p)*12
        expected=10_751.25
        print(f'valtionvero{self.year}_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2020_elake(self,p):
        valtionveroperuste=54_000
        v = self.ben.raippavero2023(valtionveroperuste/12)*12

        expected=409.50
        print(f'raippavero eläke computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2021_tyo(self,p):
        valtionveroperuste=80_500
        v=self.ben.laske_valtionvero2018_2022(valtionveroperuste/12,p)*12
        expected=11023.50
        print(f'valtionvero{self.year}_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2021_elake(self,p):
        valtionveroperuste=54_000
        v = self.ben.raippavero2023(valtionveroperuste/12)*12

        expected=409.50
        print(f'raippavero eläke computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2022_tyo(self,p):
        valtionveroperuste=82_900
        v=self.ben.laske_valtionvero2018_2022(valtionveroperuste/12,p)*12
        expected=11_351.50
        print(f'valtionvero{self.year}_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2022_elake(self,p):
        valtionveroperuste=54_000
        v = self.ben.raippavero2023(valtionveroperuste/12)*12

        expected=409.50
        print(f'raippavero eläke computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2023_tyo(self,p):
        valtionveroperuste=85_800
        v=self.ben.laske_valtionvero2023_2024(valtionveroperuste/12,p)*12
        expected=22_727.61
        print(f'valtionvero{self.year}_tyo computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_valtionvero2023_elake(self,p):
        valtionveroperuste=54_000
        v = self.ben.raippavero2023(valtionveroperuste/12)*12
        expected=409.50
        print(f'raippavero eläke computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_paivarahamaksu2021(self):
        peruste = 30_000
        v = self.ben.laske_paivarahamaksu(peruste,50)
        expected = 408
        print(f'päivärahamaksu computed {v} expected {expected} ',end='')
        return self.check_return(v,expected)

    def test_marg_tyo2023(self,p):
        peruste=(15_000,16_000,17_000,18_000,19_000,20_000,30_000,40_000,50_000,60_000,70_000,80_000,90_000,100_000,150_000,200_000,1_000_000)
        vero=(8.7,10.2,10.3,10.9,12.3,13.5,21.8,27.2,31.6,34.8,37.4,39.2,40.7,42.1,47.8,50.4,56.5)
        marg=(11.2,12.5,12.5,37.0,37.0,37.0,43.6,49.5,49.5,53,53,52.2,52.2,59.2,59.2,58.0,58.0,58.0)
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

    def test_marg_tyo2018(self,p):
        peruste=(15_000,16_000,17_000,18_000,19_000,20_000,30_000,40_000,50_000,60_000,70_000,80_000,90_000,100_000,150_000,200_000,1_000_000)
        vero=(8.7,10.2,10.3,10.9,12.3,13.5,21.8,27.2,31.6,34.8,37.4,39.2,40.7,42.1,47.8,50.4,56.5)
        marg=(11.2,12.5,12.5,37.0,37.0,37.0,43.6,47.1,49.5,53,53,52.2,52.2,59.2,59.2,58.0,58.0,58.0)
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

    def test_marg_tyo2019(self,p):
        peruste=(15_000,16_000,17_000,18_000,19_000,20_000,30_000,40_000,50_000,60_000,70_000,80_000,90_000,100_000,150_000,200_000,1_000_000)
        vero=(8.7,10.0,10.3,11.5,12.8,14.0,22.4,28.0,32.1,35.1,37.5,39.3,40.7,42.4,47.9,50.4,56.3)
        marg=(11.1,12.3,23.8,36.8,36.8,36.8,39.7,48.1,48.1,51.7,51.7,51.7,51.7,59.7,57.8,57.8,57.8)
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

    def test_marg_tyo2020(self,p):
        peruste=(15_000,16_000,17_000,18_000,19_000,20_000,30_000,40_000,50_000,60_000,70_000,80_000,90_000,100_000,150_000,200_000,1_000_000)
        vero=(8.7,10.0,10.3,11.5,12.8,14.0,22.4,28.0,32.1,35.1,37.5,39.3,40.7,42.4,47.9,50.4,56.3)
        marg=(11.1,12.3,23.8,36.8,36.8,36.8,39.7,48.1,48.1,51.7,51.7,51.7,51.7,59.7,57.8,57.8,57.8)
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

    def test_marg_tyo2021(self,p):
        peruste=(13_000,14_000,15_000,16_000,17_000,18_000,19_000,20_000,30_000,40_000,50_000,60_000,70_000,80_000,90_000,100_000,150_000,200_000,1_000_000)
        vero=(8.6,8.6,10.0,10.1,10.9,12.3,13.6,14.8,23.1,28.8,32.7,35.7,38.0,39.8,41.1,43.0,48.4,50.8,56.5)
        marg=(8.6,8.6,12.4,15.1,37.1,37.1,37.1,37.1,40.0,48.2,48.2,51.8,51.8,51.8,59.0,59.9,58.0,58.0,58.0)
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

    def test_marg_tyo2022(self,p):
        peruste=(13_000,14_000,15_000,16_000,17_000,18_000,19_000,20_000,30_000,40_000,50_000,60_000,70_000,80_000,90_000,100_000,150_000,200_000,1_000_000)
        vero=(8.7,8.7,8.7,10.0,10.3,11.5,12.8,14.0,22.4,28.0,32.1,35.1,37.5,39.3,40.7,42.4,47.9,50.4,56.3)
        marg=(8.7,8.7,11.1,12.3,23.8,36.8,36.8,36.8,39.7,48.1,48.1,51.7,51.7,51.7,51.7,59.7,57.8,57.8,57.8)
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

    def test_marg_tyo2024(self,p):
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


    def test_marg_elake2023(self,p):
        peruste=(5_000,10_000,15_000,16_000,17_000,18_000,19_000,20_000,30_000,40_000,50_000,60_000,70_000,80_000,90_000,100_000,150_000,200_000)
        vero=   (0,    0,     5.9,   8.3,   10.3,  12.2,  13.8,  15.2,  22.7,  28.0,  32.1,  35.1,  37.3,  38.9,  40.6,  42.6,   48.4,   51.4)
        marg=   (0,    0,     43.4,  43.4,  43.4,  43.4,  43.4,  43.4,  33.7,  46.7,  50.2,  50.2,  50.2,  50.2,  60.2,  60.2,   60.2,   60.2)
        p2=p.copy()
        p2['asumismenot_asumistuki']=0
        p2['asumismenot_toimeentulotuki']=0
        p2['ei_toimeentulotukea']=1
        p2['elakkeella']=1
        p2['tyoelake']=0
        p2['ika']=75

        print('\n 2023 vanhuuseläkeläisen efektiivinen marginaali ja veroaste -testi (ilman kansaneläke & takuueläke)')
        for i,per in enumerate(peruste):
            eff,tva = self.marg.comp_test_margs(p2,pension=per/12,include_kansanelake=False,include_takuuelake=False)

            expected_marg=marg[i]
            print(f'marg @ {per} computed {eff} expected {expected_marg} ',end='')
            r1=self.check_return(eff,expected_marg,decimals=1)

            expected_tva=vero[i]
            print(f'vero @ {per} computed {tva} expected {expected_tva} ',end='')
            r2=self.check_return(tva,expected_tva,decimals=1)