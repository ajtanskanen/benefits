# Benefits - Python module that makes analysis of social security easy

Benefits implements Finnish social security and taxation as a Python module. It enables analysis of benefits and incentives via example cases.
The aim is to enable analysis of any social security scheme easily.

For example, the module enables computation of net income at various levels given the current state of a person-

<p>
<img src='kuvat/verkkoon_netto.png'><br>
Figure 1. Net income as a function of wage taking into account social security benefits and taxation.

Incentive to work more is often considered via the effective tax rate.

<p>
<img src='kuvat/verkkoon_eff.png'><br>
Figure 2. Effective marginal tax rate as a function of wage taking into account social security benefits and taxation.

Incentive to work at all is often considered via the participation tax rate.

<p>
<img src='kuvat/verkkoon_ptr.png'><br>
Figure 3. Participation marginal tax rate as a function of wage taking into account social security benefits and taxation.

Further, the code is implemented in a modular way to enable embedding in a more complex model, such as <a href='https://github.com/ajtanskanen/lifecycle-rl'>a life cycle model</a>.

Social security reform
----

The module also implements universal basic income, which can be analyzed.

To see an executable example, see <a href='https://colab.research.google.com/drive/1mn6e3EEulFXpQppHKbphRGaA4ujTAx-J#scrollTo=J9Z67ShBbdy8'>Google Colab workbook</a>.

## References

	@misc{fin_benefits,
	  author = {Antti J. Tanskanen},
	  title = {Benefits - Python module that makes analysis of social security easy},
	  year = {2019},
	  publisher = {GitHub},
	  journal = {GitHub repository},
	  howpublished = {\url{https://github.com/ajtanskanen/benefits}},
	}
	
The library is described and used in articles
    
    @article{tanskanen202,
      title={Deep reinforced learning enables solving rich discrete-choice life cycle models to analyze social security reforms},
      author={Tanskanen, Antti J},
      journal={Social Sciences & Humanities Open},
      volume={5},
      pages={100263},
      year={2022}
    }
    
    @article{tanskanen2020,
      title={Ty{\"o}llisyysvaikutuksien arviointia teko{\"a}lyll{\"a}: Unelmoivatko robotit ansiosidonnaisesta sosiaaliturvasta},
      author={Tanskanen, Antti J},
      journal={Kansantaloudellinen aikakauskirja},
      volume={2},
      pages={292--321},
      year={2020}
    }    