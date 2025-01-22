'''

    labels.py

'''

class Labels():
    def get_labels(self,language='English'):
        labels={}
        #print('labels, language:',language)
        if language=='English':
            labels['ero määrissä']='Difference in numbers'
            labels['osuus tilassa x']='Proportion in state {} [%]'
            labels['age']='Age [y]'
            labels['diff osuus']='diff in proportions'
            labels['diff määrissä']='diff in numbers'            
            labels['ratio']='Proportion [%]'
            labels['unemp duration']='Length of unemployment [y]'
            labels['scaled freq']='Scaled frequency'
            labels['probability']='probability'
            labels['telp']='Employee pension premium'
            labels['sairausvakuutus']='Health insurance'
            labels['työttömyysvakuutusmaksu']='Unemployment insurance'
            labels['puolison verot']='Partners taxes'
            labels['taxes']='Taxes'
            labels['asumistuki']='Housing benefit'
            labels['toimeentulotuki']='Supplementary benefit'
            labels['tyottomyysturva']='Unemployment benefit'
            labels['paivahoito']='Daycare'
            labels['elake']='Pension'
            labels['tyollisyysaste']='Employment rate'
            labels['Työllisyysaste [%]']='Employment rate [%]'
            labels['Työttömyysaste [%]']='Unemployment rate [%]'
            labels['tyottomien osuus']='Proportion unemployed'
            labels['Työttömien osuus [%]']='Proportion unemployed [%]'
            labels['havainto']='Observation'
            labels['tyottomyysaste']='Unemployment rate [%]'
            labels['tyottomien osuus']='Proportion unemployed [%]'
            labels['tyollisyysaste %']='Employment rate [%]'
            labels['ero osuuksissa']='Difference in proportions [%]'
            labels['osuus']='Proportion'
            labels['osuus %']='Proportion [%]'
            labels['lkm']='Number'
            labels['havainto, naiset']='data, women'
            labels['havainto, miehet']='data, men'
            labels['palkkasumma']='Wage sum [euros]'
            labels['wage']='Wages [euros]'
            labels['spouse state']='employment state of spouse'
            labels['Verokiila %']='Tax wedge [%]'
            labels['Työnteko [hlö/htv]']='Työnteko [hlö/htv]'
            labels['Työnteko [htv]']='Työnteko [htv]'
            labels['Työnteko [hlö]']='Työnteko [hlö]'
            labels['Työnteko [miljoonaa hlö/htv]']='Työnteko [miljoonaa hlö/htv]'
            labels['Työnteko [miljoonaa htv]']='Työnteko [miljoonaa htv]'
            labels['Työnteko [miljoonaa hlö]']='Työnteko [miljoonaa hlö]'
            labels['Osatyönteko [%-yks]']='Part-time work [pp]'
            labels['Muut tulot [euroa]']='Other income [euros]'
            labels['Henkilöitä']='Persons'
            labels['työsuhteen pituus [v]']='duration of employment [y]'
            labels['ika']='Age [y]'
            labels['Lukumäärä']='#'
            labels['Poikkeama työllisyydessä [htv]']='Difference in employment [py]'
            labels['Poikkeama työllisyydessä [henkilöä]']='Difference in employment [p]'
            labels['Hajonta työllisyysasteessa [%]']='Std employment [%]'
            labels['Palkkio']='Reward'
            labels['työttömyysjakson pituus [v]']='duration of unemployment spell [y]'
            labels['työllistyneiden osuus']='proportion employed'
            labels['pois siirtyneiden osuus']='proportion of those moved away'
            labels['Naiset']='Women'
            labels['Miehet']='Men'
            labels['Verot [euroa]']='Taxes [euroa]'
            labels['Verot [[miljardia euroa]']='Taxes [billion euros]'
            labels['Verokertymä [euroa]']='Sum of taxes [euros]'
            labels['Verokertymä [miljardia euroa]']='Sum of taxes [billion euros]'
            labels['Muut tarvittavat tulot [euroa]']='Other income [euros]'
            labels['Muut tarvittavat tulot [miljardia euroa]']='Other income [billion euros]'
            labels['malli']='Life cycle model'
            labels['lapsia']='Children'
            labels['spouses']='Spouses'
            labels['työvoima %']='Workforce %'
            labels['Menetetty palkkasumma']='Lost wages [euros]'
            labels['Menetetty palkkasumma %']='Lost wages [%]'
            labels['Työaika [h]']='Work time [h]'
            labels['Työttömyys [%]']='Unemployment [%]'
            labels['Osatyön osuus %']='Part-time work [%]'
        else:
            labels['Menetetty palkkasumma']='Menetetty palkkasumma [euroa]'
            labels['Menetetty palkkasumma %']='Menetetty palkkasumma [%]'
            labels['ero määrissä']='Ero määrissä'
            labels['osuus tilassa x']='Osuus tilassa {} [%]'
            labels['age']='Ikä [v]'
            labels['diff osuus']='ero osuuksissa'
            labels['diff määrissä']='ero määrissä'            
            labels['ratio']='Osuus tilassa [%]'
            labels['unemp duration']='työttömyysjakson pituus [v]'
            labels['scaled freq']='skaalattu taajuus'
            labels['probability']='todennäköisyys'
            labels['telp']='TEL-P'
            labels['sairausvakuutus']='Sairausvakuutus'
            labels['työttömyysvakuutusmaksu']='Työttömyysvakuutusmaksu'
            labels['puolison verot']='puolison verot'
            labels['taxes']='Verot'
            labels['asumistuki']='Asumistuki'
            labels['toimeentulotuki']='Toimeentulotuki'
            labels['tyottomyysturva']='Työttömyysturva'
            labels['wage']='Wages [euros]'
            labels['spouse state']='Puolison tila'
            labels['ika']='Ikä [v]'
            labels['paivahoito']='Päivähoito'
            labels['elake']='Eläke'
            labels['tyollisyysaste']='työllisyysaste'
            labels['Työllisyysaste [%]']='Työllisyysaste [%]'
            labels['Työttömyysaste [%]']='Työttömyysaste [%]'
            labels['tyottomien osuus']='työttömien osuus'
            labels['Työttömien osuus [%]']='Työttömien osuus [%]'
            labels['havainto']='havainto'
            labels['tyottomyysaste']='Työttömyysaste [%]'
            labels['tyottomien osuus']='Työttömien osuus väestöstö [%]'
            labels['tyollisyysaste %']='Työllisyysaste [%]'
            labels['ero osuuksissa']='Ero osuuksissa [%]'
            labels['osuus']='Osuus'
            labels['osuus %']='Osuus [%]'
            labels['lkm']='Lukumäärä'
            labels['Lukumäärä']='Lukumäärä'
            labels['Poikkeama työllisyydessä [htv]']='Poikkeama työllisyydessä [htv]'
            labels['Poikkeama työllisyydessä [henkilöä]']='Poikkeama työllisyydessä [henkilöä]'
            labels['Hajonta työllisyysasteessa [%]']='Hajonta työllisyysasteessa [%]'
            labels['Palkkio']='Palkkio'
            labels['työttömyysjakson pituus [v]']='työttömyysjakson pituus [v]'
            labels['työllistyneiden osuus']='työllistyneiden osuus'
            labels['pois siirtyneiden osuus']='pois siirtyneiden osuus'
            labels['Naiset']='Naiset'
            labels['Miehet']='Miehet'
            labels['työsuhteen pituus [v]']='työsuhteen pituus [v]'
            labels['havainto, naiset']='havainto, naiset'
            labels['havainto, miehet']='havainto, miehet'
            labels['palkkasumma']='Palkkasumma [euroa]'
            labels['Verokiila %']='Verokiila [%]'
            labels['Työnteko [hlö/htv]']='Työnteko [hlö/htv]'
            labels['Työnteko [htv]']='Työnteko [htv]'
            labels['Työnteko [hlö]']='Työnteko [hlö]'
            labels['Työnteko [miljoonaa hlö/htv]']='Työnteko [miljoonaa hlö/htv]'
            labels['Työnteko [miljoonaa htv]']='Työnteko [miljoonaa htv]'
            labels['Työnteko [miljoonaa hlö]']='Työnteko [miljoonaa hlö]'
            labels['Osatyönteko [%-yks]']='Osa-aikatyössä [%-yks]'
            labels['Muut tulot [euroa]']='Muut tulot [euroa]'
            labels['Henkilöitä']='Henkilöitä'
            labels['Verot [euroa]']='Verot [euroa]'
            labels['Verot [[miljardia euroa]']='Verot [[miljardia euroa]'
            labels['Verokertymä [euroa]']='Verokertymä [euroa]'
            labels['Verokertymä [miljardia euroa]']='Verokertymä [miljardia euroa]'
            labels['Muut tarvittavat tulot [euroa]']='Muut tarvittavat tulot [euroa]'
            labels['Muut tarvittavat tulot [miljardia euroa]']='Muut tarvittavat tulot [miljardia euroa]'
            labels['malli']='elinkaarimalli'
            labels['lapsia']='Lapsia'
            labels['spouses']='Spouses'
            labels['työvoima %']='Työvoima %'
            labels['Työaika [h]']='Työaika [h]'
            labels['Työttömyys [%]']='Työttömyys [%]'
            labels['Osatyön osuus %']='Osatyön osuus työnteosta [%]'

        return labels
        
    def ben_labels(self,language='English'):
        labels={}
        if language=='English':
            labels['wage']='Wage (e/m)'
            labels['parttimewage']='Part-time wage (e/m)'
            labels['pure wage']='Wage'
            labels['effective']='Eff.marg.tax (%)'
            labels['valtionvero']='State tax'
            labels['kunnallisvero']='Municipal tax'
            labels['telp']='Employee pension premium'
            labels['sairausvakuutusmaksu']='Health insurance contribution'
            labels['työttömyysvakuutusmaksu']='Unemployment insurance contribution'
            labels['puolison verot']="Spouse's taxes"
            labels['taxes']='Taxes'
            labels['asumistuki']='Housing benefit'
            labels['toimeentulotuki']='Supplementary benefit'
            labels['tyottomyysturva']='Unemployment benefit'
            labels['paivahoito']='Daycare'
            labels['elake']='Pension'
            labels['perustulo']='Universal basic income'
            labels['opintotuki']='Student allowance'
            labels['lapsilisa']='Child benefit'
            labels['elatustuki']='Alimony'
            labels['net income']='Net income (e/m)'
            labels['brutto income']='Brutto income (e/m)' 
            labels['alv']='VAT'
            labels['valtionvero']='State tax'
            labels['kunnallisvero']='Municipal tax'
            labels['telp']='TEL-P'
            labels['kotihoidontuki']='Child home care allowance'
        else:
            labels['wage']='Palkka (e/kk)'
            labels['parttimewage']='Osa-aikatyön palkka (e/kk)'
            labels['pure wage']='Palkka'
            labels['effective']='Ef.rajaveroaste (%)'
            labels['valtionvero']='Valtionvero'
            labels['kunnallisvero']='Kunnallisvero'
            labels['telp']='TEL-P'
            labels['puolison verot']='puolison verot'
            labels['taxes']='Verot'
            labels['asumistuki']='Asumistuki'
            labels['toimeentulotuki']='Toimeentulotuki'
            labels['tyottomyysturva']='Työttömyysturva'
            labels['paivahoito']='Päivähoito'
            labels['elake']='Elake'
            labels['perustulo']='Perustulo'
            labels['opintotuki']='Opintotuki'
            labels['lapsilisa']='Lapsilisa'
            labels['elatustuki']='Elatustuki'
            labels['net income']='Nettotulot (e/kk)'        
            labels['brutto income']='Bruttotulot (e/kk)'        
            labels['alv']='ALV'
            labels['valtionvero']='Valtionvero'
            labels['kunnallisvero']='Kunnallisvero'
            labels['telp']='TEL-P'
            labels['sairausvakuutusmaksu']='Sairausvakuutusmaksu'
            labels['työttömyysvakuutusmaksu']='Työttömyysvakuutusmaksu'
            labels['kotihoidontuki']='Kotihoidontuki'
            
        return labels

    def get_output_labels(self,language='English'):
        labels={}
        if language=='English':
            labels['työllisiä']='Employed'
            labels['työikäisiä 18-62']='Employed 18-62'
            labels['työllisiä 18-62']='Employed 18-62'
            labels['työssä ja eläkkeellä']='Employed & retired'
            labels['työssä 63+']='Employed 63+'
            labels['palkansaajia']='Employees'
            labels['ansiosidonnaisella']='Unemployed ER'
            labels['tmtuella']='Unemployed non-ER'
            labels['työkyvyttömyyseläke']='Disabled'
            labels['isyysvapaalla']='Father leave'
            labels['kotihoidontuella']='Child home care'
            labels['vanhempainvapaalla']='Parental leave'
            labels['yhteensä']='Total'
            labels['aikuisia']='Adults'
            labels['lapsia']='Children'
            labels['ovella']='OVE'
            labels['opiskelijoita']='Students'
            labels['lapsiperheitä']='Families with children'
            labels['pareja']='Couples'
            labels['tyotulosumma']='wage sum'
            labels['tyotulosumma opiskelijat']='wage sum, students'
            labels['tyotulosumma eielakkeella']='wage sum, not retired'
            labels['tyotulosumma osa-aika']='wage sum, parttime'
            labels['tyotulosumma kokoaika']='wage sum, fulltime'
            labels['muut tulot v2']='income, other v2'
            labels['tulot_netto_v2']='income, netto v2'
            labels['etuusmeno_v2']='benefit expenditure, v2'
            labels['verot+maksut_v2']='tax+contrib, v2'
            labels['eläkkeellä']='retired'
            labels['vanhuuseläkkeellä']='retired'
            labels['osaaikatyössä']='part-time work'
            labels['kokoaikatyössä']='full-time work'
            labels['ta_maksut_elake']='Employer contribution, pensions'
            labels['ta_maksut_muut']='Employer contribution, other'
            labels['ta_maksut']='Employer contribution'
            labels['etuusmeno']='Benefit sum'
            labels['verot+maksut']='taxes+contribution'
            labels['verot+maksut+alv']='taxes+contribution+vat'
            labels['verot+maksut+alv+ta']='taxes+contribution+vat+employer contribution'
            labels['valtionvero']='State tax'
            labels['kunnallisvero']='Municipal tax'
            labels['ptel']='Employees pension premium'
            labels['tyoelakemaksu']='Pension premium'
            labels['tyottomyysvakuutusmaksu']='Unemployment insurance premium'
            labels['sairausvakuutusmaksu']='Health insurance premium'
            labels['ylevero']='YLE tax'
            labels['ansiopvraha']='Unemployment ER benefit'
            labels['peruspvraha']='Unemployment non-ER benefit'
            labels['asumistuki']='Housing benefit'
            labels['tyoelakemeno']='Pension expenditure'
            labels['kansanelakemeno']='Basic pension expenditure'
            labels['takuuelakemeno']='Guaranteed pension expenditure'
            labels['kokoelakemeno']='Total pension expenditure'
            labels['elatustuki']='Alimony'
            labels['lapsilisa']='Child benefit'
            labels['opintotuki']='Student allowance'
            labels['isyyspaivaraha']='Father leave benefit'
            labels['aitiyspaivaraha']='Mother leave benefit'
            labels['kotihoidontuki']='Child home care allowance'
            labels['sairauspaivaraha']='Sickness benefit'
            labels['svpäiväraha']='sickness benefit'
            labels['toimeentulotuki']='Social assistance'
            labels['perustulo']='UBI'
            labels['pvhoitomaksu']='Daycare fee'
            labels['alv']='VAT'
            labels['tyottomyyspvraha']='Unemployment benefit'
            labels['verotettava etuusmeno']='Taxable benefit sum'
            labels['palkkaverot+maksut']='Wage tax+contribution'
            labels['nettotulot']='Net income'
            labels['muut tulot']='Other income'
            labels['julkinen talous, netto']='Public finances, net'
            labels['toteuma (htv)']='realized (py)'
            labels['diff (htv)']='diff (py)'
            labels['diff osuus']='diff in proportions'
            labels['toteuma (#)']='realized (#)'
            labels['diff (#)']='diff (#)'
            labels['Työaika [h]']='Work time [h]'
            labels['Työttömyys [%]']='Unemployment [%]'
            labels['Osatyön osuus %']='Part-time work [%]'
        else:
            labels['työllisiä']='Työllisiä'
            labels['työikäisiä 18-62']='työikäisiä 18-62'
            labels['työllisiä 18-62']='työikäisiä 18-62'
            labels['työssä ja eläkkeellä']='työssä ja eläkkeellä'
            labels['työssä 63+']='työssä 63+'
            labels['palkansaajia']='palkansaajia'
            labels['ansiosidonnaisella']='ansiosidonnaisella'
            labels['tmtuella']='tm-tuella'
            labels['työkyvyttömyyseläke']='työkyvyttömyyseläkkeellä'
            labels['isyysvapaalla']='isyysvapaalla'
            labels['kotihoidontuella']='kotihoidontuella'
            labels['vanhempainvapaalla']='vanhempainvapaalla'
            labels['yhteensä']='yhteensä'
            labels['aikuisia']='aikuisia'
            labels['lapsia']='lapsia'
            labels['ovella']='ove:lla'
            labels['opiskelijoita']='opiskelijoita'
            labels['lapsiperheitä']='lapsiperheitä'
            labels['pareja']='pareja'
            labels['tyotulosumma']='tyotulosumma'
            labels['tyotulosumma opiskelijat']='tyotulosumma, opiskelijat'
            labels['tyotulosumma osa-aika']='tyotulosumma, osa-aika'
            labels['tyotulosumma kokoaika']='tyotulosumma, kokoaika'
            labels['muut tulot v2']='tulot, muut v2'
            labels['tulot_netto_v2']='tulot, netto v2'
            labels['etuusmeno_v2']='etuusmeno, v2'
            labels['verot+maksut_v2']='verot+maksut, v2'
            labels['ta_maksut_elake']='ta-maksut, elake'
            labels['ta_maksut_muut']='ta-maksut, muut'
            labels['ta_maksut']='ta-maksut'
            labels['eläkkeellä']='eläkkeellä'
            labels['vanhuuseläkkeellä']='vanhuuseläkkeellä'
            labels['osaaikatyössä']='osaaikatyössä'
            labels['kokoaikatyössä']='kokoaikatyössä'
            labels['tyotulosumma eielakkeella']='tyotulosumma ei-elakkeella'
            labels['etuusmeno']='etuusmeno'
            labels['verot+maksut']='verot+maksut'
            labels['verot+maksut+alv']='verot+maksut+alv'
            labels['verot+maksut+alv+ta']='verot+maksut+alv+ta'
            labels['valtionvero']='valtionvero'
            labels['kunnallisvero']='kunnallisvero'
            labels['ptel']='P-TEL'
            labels['tyoelakemaksu']='tyoelakemaksu'
            labels['tyottomyysvakuutusmaksu']='tyottomyysvakuutusmaksu'
            labels['sairausvakuutusmaksu']='sairausvakuutusmaksu'
            labels['ylevero']='yle-vero'
            labels['ansiopvraha']='ansiopäiväraha'
            labels['peruspvraha']='peruspvraha'
            labels['asumistuki']='asumistuki'
            labels['tyoelakemeno']='tyoelakemeno'
            labels['kansanelakemeno']='kansanelakemeno'
            labels['takuuelakemeno']='takuuelakemeno'
            labels['kokoelakemeno']='kokoelakemeno'
            labels['elatustuki']='elatustuki'
            labels['lapsilisa']='lapsilisa'
            labels['opintotuki']='opintotuki'
            labels['isyyspaivaraha']='isyyspaivaraha'
            labels['aitiyspaivaraha']='aitiyspaivaraha'
            labels['kotihoidontuki']='kotihoidontuki'
            labels['sairauspaivaraha']='sairauspaivaraha'
            labels['svpäiväraha']='svpäiväraha'
            labels['toimeentulotuki']='toimeentulotuki'
            labels['perustulo']='perustulo'
            labels['pvhoitomaksu']='pvhoitomaksu'
            labels['alv']='alv'
            labels['tyottomyyspvraha']='tyottomyyspvraha'
            labels['verotettava etuusmeno']='verotettava etuusmeno'
            labels['palkkaverot+maksut']='palkkaverot+maksut'
            labels['nettotulot']='nettotulot'
            labels['muut tulot']='muut tulot'
            labels['julkinen talous, netto']='julkinen talous, netto'
            labels['toteuma (htv)']='toteuma (htv)'
            labels['diff (htv)']='diff (htv)'
            labels['diff osuus']='ero osuuksissa'
            labels['toteuma (#)']='toteuma (#)'
            labels['diff (#)']='diff (#)'
            labels['Työaika [h]']='Työaika [h]'
            labels['Työttömyys [%]']='Työttömyys [%]'
            labels['Osatyön osuus %']='Osatyön osuus työnteosta [%]'
            
        return labels        
            