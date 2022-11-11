'''

    labels.py

'''

class Labels():
    def get_labels(self,language='English'):
        labels={}
        if language=='English':
            labels['osuus tilassa x']='Proportion in state {} [%]'
            labels['age']='Age [y]'
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
            labels['tyottomien osuus']='Proportion of unemployed'
            labels['havainto']='Observation'
            labels['tyottomyysaste']='Unemployment rate [%]'
            labels['tyottomien osuus']='Proportion of unemployed [%]'
            labels['tyollisyysaste %']='Employment rate [%]'
            labels['ero osuuksissa']='Difference in proportions [%]'
            labels['osuus']='proportion'
            labels['havainto, naiset']='data, women'
            labels['havainto, miehet']='data, men'
            labels['palkkasumma']='Palkkasumma [euroa]'
            labels['wage']='Wages [euros]'
            labels['spouse state']='Puolison tila'
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
            labels['ika']='Age [y]'
            labels['Naiset']='Women'
            labels['Miehet']='Men'
            labels['Verot [euroa]']='Verot [euroa]'
            labels['Verot [[miljardia euroa]']='Verot [[miljardia euroa]'
            labels['Verokertymä [euroa]']='Verokertymä [euroa]'
            labels['Verokertymä [miljardia euroa]']='Verokertymä [miljardia euroa]'
            labels['Muut tarvittavat tulot [euroa]']='Muut tarvittavat tulot [euroa]'
            labels['Muut tarvittavat tulot [miljardia euroa]']='Muut tarvittavat tulot [miljardia euroa]'
            labels['malli']='Life cycle model'
            labels['lapsia']='Children'
            labels['spouses']='Spouses'
            labels['työvoima %']='Workforce %'
        else:
            labels['osuus tilassa x']='Osuus tilassa {} [%]'
            labels['age']='Ikä [v]'
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
            labels['tyottomien osuus']='työttömien osuus'
            labels['havainto']='havainto'
            labels['tyottomyysaste']='Työttömyysaste [%]'
            labels['tyottomien osuus']='Työttömien osuus väestöstö [%]'
            labels['tyollisyysaste %']='Työllisyysaste [%]'
            labels['ero osuuksissa']='Ero osuuksissa [%]'
            labels['osuus']='Osuus'
            labels['Naiset']='Naiset'
            labels['Miehet']='Miehet'
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
            labels['sairausvakuutusmaksu']='Health insurance'
            labels['työttömyysvakuutusmaksu']='työttömyysvakuutusmaksu'
            labels['puolison verot']='puolison verot'
            labels['taxes']='Taxes'
            labels['asumistuki']='Housing benefit'
            labels['toimeentulotuki']='Supplementary benefit'
            labels['tyottomyysturva']='Unemployment benefit'
            labels['paivahoito']='Daycare'
            labels['elake']='Pension'
            labels['perustulo']='Universal basic income'
            labels['opintotuki']='Opintotuki'
            labels['lapsilisa']='Child benefit'
            labels['elatustuki']='Alimony'
            labels['net income']='Net income (e/m)'
            labels['brutto income']='Brutto income (e/m)' 
            labels['alv']='VAT'
            labels['valtionvero']='Valtionvero'
            labels['kunnallisvero']='Kunnallisvero'
            labels['telp']='TEL-P'
            labels['sairausvakuutusmaksu']='sairausvakuutusmaksu'
            labels['työttömyysvakuutusmaksu']='työttömyysvakuutusmaksu'
            labels['puolison verot']='puolison verot'
            labels['taxes']='verot'
            labels['kotihoidontuki']='Kotihoidontuki'
        else:
            labels['wage']='Palkka (e/kk)'
            labels['parttimewage']='Osa-aikatyön palkka (e/kk)'
            labels['pure wage']='Palkka'
            labels['effective']='Eff.rajaveroaste (%)'
            labels['valtionvero']='Valtionvero'
            labels['kunnallisvero']='Kunnallisvero'
            labels['telp']='TEL-P'
            labels['sairausvakuutusmaksu']='sairausvakuutusmaksu'
            labels['työttömyysvakuutusmaksu']='Työttömyysvakuutusmaksu'
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
            labels['sairausvakuutusmaksu']='sairausvakuutusmaksu'
            labels['työttömyysvakuutusmaksu']='työttömyysvakuutusmaksu'
            labels['puolison verot']='puolison verot'
            labels['kotihoidontuki']='Kotihoidontuki'
            
        return labels
            