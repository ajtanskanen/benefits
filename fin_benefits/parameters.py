import numpy as np

def perheparametrit(perhetyyppi=10,tulosta=False):

	lapsia_kotihoidontuella=0    
	alle3v=0    
	
	p={}
	p['tyoton']=1
	p['ika']=30
	p['saa_ansiopaivarahaa']=1
	p['t']=0
	p['vakiintunutpalkka']=2500
	p['perustulo']=0
	elakkeella=0
	elake=0
	p['asumismenot_toimeentulo']=500
	p['asumismenot_asumistuki']=500
	p['lapsia']=0
	p['paivahoidossa']=0
	p['aikuisia']=1
	p['veromalli']=0
	p['kuntaryhma']=2 # vastaa 3:sta matlabissa
	p['lapsia_kotihoidontuella']=0
	p['alle3v']=0
	p['ansiopvrahan_suojaosa']=1
	p['ansiopvraha_lapsikorotus']=1
	p['puolison_tulot']=0
	p['puoliso_tyoton']=0  
	p['puoliso_vakiintunutpalkka']=0  
	p['puoliso_saa_ansiopaivarahaa']=0
	p['puolison_tulot']=0
	p['puolison_tyottomyyden_kesto']=100
	p['tyottomyyden_kesto']=10
	
	if perhetyyppi==1: # 1+0, töissä
		lapsia=0    
		paivahoidossa=0    
		aikuisia=1    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=0    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==2: # 1+0, työtön ansiopäivärahalla 
		lapsia=0    
		paivahoidossa=0    
		aikuisia=1    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==3: # 1+0, työtön työmarkkinatuella
		lapsia=0    
		paivahoidossa=0    
		aikuisia=1    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==4: # 1+1, 
		lapsia=1    
		paivahoidossa=1    
		aikuisia=1    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==5: # 2+1, molemmat töissä (puoliso osapäivätöissä)
		lapsia=1    
		paivahoidossa=1    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=0    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=1250    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==6: # 2+1, puoliso ansioturvalla
		lapsia=2    
		paivahoidossa=2    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=0    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==7: # 2+1, molemmat ansiopaivarahalla
		lapsia=1    
		paivahoidossa=1    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==8: # 2+2, molemmat töissä
		lapsia=1    
		paivahoidossa=1    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=1    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==9: # 2+3, molemmat töissä
		lapsia=3    
		paivahoidossa=1    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=1    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==10: # 1+1, 
		lapsia=1    
		paivahoidossa=1    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==11: # 1+3, ansiopaivarahalla
		lapsia=3    
		paivahoidossa=2    
		aikuisia=1    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==12: # 2+2, työmarkkinatuella
		lapsia=2    
		paivahoidossa=2    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    
	elif perhetyyppi==13: # 2+2, ansiosidonnaisella
		lapsia=2    
		paivahoidossa=2    
		aikuisia=2    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0            
	elif perhetyyppi==14: # 2+1, puoliso työssä
		lapsia=1    
		paivahoidossa=1    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=1250    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0          
	elif perhetyyppi==16: # 1+2, työmarkkinatuelta töihin, Kaupalle: #1
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=0    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==17: # 2+2, työssä, työllistyvä puolis0 1250e/kk
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=2    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=0    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=2000    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0         
	elif perhetyyppi==18: # 2+2, kotihoidontuella, puolis0 2500e/kk
		lapsia=2    
		paivahoidossa=0    
		lapsia_kotihoidontuella=2    
		alle3v=2    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=0    
		saa_ansiopaivarahaa=0    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==19: # 2+2, kotihoidontuelta työhön, puolis0 2500e/kk
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=2    
		aikuisia=2    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==20: # 1+2, työmarkkinatuelta töihin, Kaupalle: #2
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=0    
		aikuisia=1    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==21: # 1+2, ansiosidonnaiselta töihin, Kaupalle: #3
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=0    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==22: # 1+1, työmarkkinatuelta töihin, Kaupalle: #4
		lapsia=1    
		paivahoidossa=1    
		lapsia_kotihoidontuella=0    
		alle3v=0    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==23: # 2+2, työmarkkinatuelta töihin, Kaupalle: #5
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=0    
		aikuisia=2    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==24: # 2+2, työmarkkinatuelta töihin, puoliso tm-tuella, Viitamäki kuvio: #12 & #13
		lapsia=2    
		paivahoidossa=1    
		lapsia_kotihoidontuella=0    
		alle3v=0    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==25: # 2+2, ansiopäivärahalta töihin, puoliso tm-tuella, Viitamäki kuvio #14 & #15
		lapsia=2    
		paivahoidossa=1    
		lapsia_kotihoidontuella=0    
		alle3v=0    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==26: # 2+2, työmarkkinatuella, päivähoidossa 0
		lapsia=2    
		paivahoidossa=0    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0            
	elif perhetyyppi==27: # 2+2, työmarkkinatuella, päivähoidossa 2
		lapsia=2    
		paivahoidossa=2    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0            
	elif perhetyyppi==28: # 2+2, ei työmarkkinatuella, päivähoidossa 2
		lapsia=2    
		paivahoidossa=2    
		aikuisia=2    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=2500    
		puolison_vakiintunutpalkka=2500    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0            
	elif perhetyyppi==29: # 1+1, työmarkkinatuelta töihin, Viitamäki HS 
		lapsia=1    
		paivahoidossa=1    
		lapsia_kotihoidontuella=0    
		alle3v=1    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=1    
		puoliso_saa_ansiopaivarahaa=0                  
	elif perhetyyppi==30: # 2+1, tmtuki, puoliso osapäivätyössä
		lapsia=1    
		paivahoidossa=1    
		aikuisia=2    
		vakiintunutpalkka=2500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=1250    
		puolison_vakiintunutpalkka=1250    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0       
	elif perhetyyppi==31: # 1+3, työmarkkinatuelta töihin, Viitamäki HS 
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=1    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=0    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0       
	elif perhetyyppi==32: # 1+1, työmarkkinatuelta töihin, Viitamäki HS 
		lapsia=2    
		paivahoidossa=2    
		lapsia_kotihoidontuella=0    
		alle3v=1    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                
	elif perhetyyppi==41: # 1+0, eläkkeellä
		lapsia=0    
		paivahoidossa=0
		lapsia_kotihoidontuella=0    
		alle3v=0
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=0    
		saa_ansiopaivarahaa=0
		elakkeella=1
		elake=1500
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                
	elif perhetyyppi==42: # 1+0, töissä
		lapsia=0    
		paivahoidossa=0
		lapsia_kotihoidontuella=0    
		alle3v=0
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=0    
		saa_ansiopaivarahaa=0
		elakkeella=0
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0                
	else: # 1+0
		lapsia=0    
		paivahoidossa=0    
		aikuisia=1    
		vakiintunutpalkka=1500    
		tyoton=1    
		saa_ansiopaivarahaa=1    
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0   
		
	# perhekoko          1   2   3   4    5
	# luvut peräisin Viitamäeltä
	vuokra_toimeentulo=np.array([440,660,850,980,1150]) # helsinki 675 800 919 1008 +115/hlo
	vuokra_asumistuki =np.array([411,600,761,901,1024])
	vuokra_yhdistetty =vuokra_toimeentulo    

	asumismenot_toimeentulo=vuokra_toimeentulo[lapsia+aikuisia-1]
	asumismenot_asumistuki=vuokra_asumistuki[lapsia+aikuisia-1]
	asumismenot_yhdistetty=vuokra_yhdistetty[lapsia+aikuisia-1]
	
	if (aikuisia<2):
		puolison_tulot=0    
		puolison_vakiintunutpalkka=0    
		puoliso_tyoton=0    
		puoliso_saa_ansiopaivarahaa=0    

	if (puoliso_tyoton>0):
		puolison_tulot=0    

	if (paivahoidossa>lapsia):
		paivahoidossa=lapsia   
		
	p['lapsia']=lapsia
	p['elakkeella']=elakkeella
	p['tyoelake']=elake
	p['aitiysvapaalla']=0
	p['isyysvapaalla']=0
	p['kotihoidontuella']=0
	p['paivahoidossa']=paivahoidossa
	p['aikuisia']=aikuisia
	p['vakiintunutpalkka']=vakiintunutpalkka
	p['tyoton']=tyoton
	p['saa_ansiopaivarahaa']=saa_ansiopaivarahaa
	p['puolison_tulot']=puolison_tulot
	p['puolison_vakiintunutpalkka']=puolison_vakiintunutpalkka
	p['puoliso_tyoton']=puoliso_tyoton
	p['puoliso_saa_ansiopaivarahaa']=puoliso_saa_ansiopaivarahaa
	p['asumismenot_toimeentulo']=asumismenot_toimeentulo
	p['asumismenot_asumistuki']=asumismenot_asumistuki
	p['asumismenot_yhdistetty']=asumismenot_yhdistetty
	p['lapsia_kotihoidontuella']=lapsia_kotihoidontuella
	p['alle3v']=alle3v
	
	#return lapsia,paivahoidossa,lapsia_kotihoidontuella,aikuisia,vakiintunutpalkka,tyoton,saa_ansiopaivarahaa, \
	#puolison_tulot,puolison_vakiintunutpalkka,puoliso_tyoton,puoliso_saa_ansiopaivarahaa, \
	#asumismenot_asumistuki,asumismenot_toimeentulo,alle3v,asumismenot_yhdistetty 
	
	selite=tee_selite(p)
	
	if tulosta:
		print(selite)
	
	return p,selite

def tee_selite(p):
	selite="Perhe, jossa {aikuisia} aikuista".format(aikuisia=p['aikuisia'])
	if p['lapsia']>0:
		selite+=" ja {lapsia} lasta.".format(lapsia=p['lapsia'])
		if p['paivahoidossa']>0:
			selite+=" Lapsista {paiva} on päivähoidossa.".format(paiva=p['paivahoidossa'])
		if p['alle3v']>0:
			selite+=" Lapsista {alle3v}".format(alle3v=p['alle3v'])
		selite
	else:
		selite=selite+", ei lapsia."
		
	if p['elakkeella']<1:
		if p['tyoton']>0:
			selite+=" Työtön"
			if p['saa_ansiopaivarahaa']>0:
				selite+=" (ansiopaivaraha, vakiintunut ansio {v} e/kk)".format(v=p['vakiintunutpalkka'])
			else:
				selite+=" (työmarkkinatuki)"
		else:
			selite+=" Töissä"
	else:
		selite+=" Vanhuuseläkkeellä (työeläke {e} e/kk)".format(e=p['tyoelake'])
		
	if p['aikuisia']>1:
		if p['puoliso_tyoton']>0:
			selite+=", puoliso työtön"
			if p['puoliso_saa_ansiopaivarahaa']>0:
				selite+=" (ansiopaivaraha, vakiintunut ansio {v} e/kk).".format(v=p['puolison_vakiintunutpalkka'])
			else:
				selite+=" (työmarkkinatuki)."
		else:
			selite+=", puoliso töissä"
			selite+=" (palkka {p} e/kk).".format(p=p['puolison_tulot'])
	else:
		selite+=", ei puolisoa."
		
	selite+=" Asumismenot asumistuessa {a} e/kk".format(a=p['asumismenot_toimeentulo'])
			
	return selite
