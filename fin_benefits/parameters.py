import numpy as np

def perheparametrit(perhetyyppi=10,tulosta=False):

    lapsia_kotihoidontuella=0    
    alle3v=0
    opiskelija=0
    
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
    p['lapsia_paivahoidossa']=0
    p['aikuisia']=1
    p['veromalli']=0
    p['kuntaryhma']=2 # vastaa 3:sta matlabissa
    p['lapsia_kotihoidontuella']=0
    p['alle3v']=0
    p['ansiopvrahan_suojaosa']=1
    p['ansiopvraha_lapsikorotus']=1
    p['puoliso_tulot']=0
    p['puoliso_tyoton']=0  
    p['puoliso_vakiintunutpalkka']=0  
    p['puoliso_saa_ansiopaivarahaa']=0
    p['puoliso_tyottomyyden_kesto']=100
    p['tyottomyyden_kesto']=10
    p['saa_elatustukea']=0
    
    kotihoidontuella=0
    
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
        saa_ansiopaivarahaa=0
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
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0        
    elif perhetyyppi==18: # 2+2, kotihoidontuella, puolis0 2500e/kk
        lapsia=2
        paivahoidossa=0    
        lapsia_kotihoidontuella=2 
        kotihoidontuella=1
        alle3v=1
        aikuisia=2    
        vakiintunutpalkka=3000    
        tyoton=0
        saa_ansiopaivarahaa=1
        puolison_tulot=4500    
        puolison_vakiintunutpalkka=3000    
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0
    elif perhetyyppi==19: # 2+2, kotihoidontuelta työhön, puolis0 2500e/kk
        lapsia=2
        paivahoidossa=2
        lapsia_kotihoidontuella=0    
        kotihoidontuella=0
        alle3v=1
        aikuisia=2    
        vakiintunutpalkka=3000    
        tyoton=0
        saa_ansiopaivarahaa=1
        puolison_tulot=4500    
        puolison_vakiintunutpalkka=3000    
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
    elif perhetyyppi==33: # 1+0, eläkkeellä
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
    elif perhetyyppi==34: # 1+0, töissä
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
    elif perhetyyppi==35: # opiskelija, asuu yksin
        lapsia=0    
        paivahoidossa=0
        lapsia_kotihoidontuella=0    
        alle3v=0
        aikuisia=1    
        vakiintunutpalkka=0
        opiskelija=1
        tyoton=0    
        saa_ansiopaivarahaa=0
        elakkeella=0
        puolison_tulot=0    
        puolison_vakiintunutpalkka=0    
        puoliso_tyoton=0    
        puoliso_saa_ansiopaivarahaa=0  
    elif perhetyyppi==36: # 2+2, kotihoidontuelta työhön, puolis0 3500e/kk
        lapsia=2    
        paivahoidossa=2    
        lapsia_kotihoidontuella=0    
        alle3v=2    
        aikuisia=2    
        vakiintunutpalkka=1500    
        tyoton=1    
        saa_ansiopaivarahaa=0    
        puolison_tulot=3500    
        puolison_vakiintunutpalkka=2500    
        puoliso_tyoton=0    
        puoliso_saa_ansiopaivarahaa=0                          
    elif perhetyyppi==37: # 2+3, työmarkkinatuelta työhön, puoliso 1500e/kk
        lapsia=3
        paivahoidossa=2
        lapsia_kotihoidontuella=0    
        alle3v=2
        aikuisia=2    
        vakiintunutpalkka=1500    
        tyoton=1    
        saa_ansiopaivarahaa=0    
        puolison_tulot=1500    
        puolison_vakiintunutpalkka=1500    
        puoliso_tyoton=0    
        puoliso_saa_ansiopaivarahaa=0                          
    elif perhetyyppi==38: # 2+3, työmarkkinatuelta työhön, puoliso 1500e/kk
        lapsia=4
        paivahoidossa=2
        lapsia_kotihoidontuella=0    
        alle3v=2
        aikuisia=2    
        vakiintunutpalkka=1500    
        tyoton=1    
        saa_ansiopaivarahaa=0    
        puolison_tulot=1500    
        puolison_vakiintunutpalkka=1500    
        puoliso_tyoton=0    
        puoliso_saa_ansiopaivarahaa=0                          
    elif perhetyyppi==39: # 2+3, työmarkkinatuelta työhön, puoliso 1500e/kk
        lapsia=3
        paivahoidossa=2
        lapsia_kotihoidontuella=0    
        alle3v=2
        aikuisia=2    
        vakiintunutpalkka=1500    
        tyoton=1    
        saa_ansiopaivarahaa=1  
        puolison_tulot=1500    
        puolison_vakiintunutpalkka=1500    
        puoliso_tyoton=0    
        puoliso_saa_ansiopaivarahaa=0                          
    elif perhetyyppi==40: # 1+2, 
        lapsia=1   
        paivahoidossa=0
        lapsia_kotihoidontuella=1
        kotihoidontuella=1
        alle3v=1
        aikuisia=1
        vakiintunutpalkka=2500    
        tyoton=0
        saa_ansiopaivarahaa=1    
        puolison_tulot=0    
        puolison_vakiintunutpalkka=0
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0                  
    elif perhetyyppi==41: # 1+2, 
        lapsia=1   
        paivahoidossa=1
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=1
        aikuisia=1
        vakiintunutpalkka=2500    
        tyoton=0
        saa_ansiopaivarahaa=1    
        puolison_tulot=0    
        puolison_vakiintunutpalkka=0
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0                  
    elif perhetyyppi==42: # 2+1, 
        lapsia=1
        paivahoidossa=0
        lapsia_kotihoidontuella=1
        kotihoidontuella=1
        alle3v=1
        aikuisia=2
        vakiintunutpalkka=2500    
        tyoton=0
        saa_ansiopaivarahaa=1    
        puolison_tulot=0    
        puolison_vakiintunutpalkka=2500
        puoliso_tyoton=1
        puoliso_saa_ansiopaivarahaa=1
    elif perhetyyppi==43: # 2+1, 
        lapsia=1
        paivahoidossa=1
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=1
        aikuisia=2
        vakiintunutpalkka=2500    
        tyoton=0
        saa_ansiopaivarahaa=1    
        puolison_tulot=0    
        puolison_vakiintunutpalkka=2500
        puoliso_tyoton=1
        puoliso_saa_ansiopaivarahaa=1    
    elif perhetyyppi==44: # 2+4
        lapsia=4
        paivahoidossa=4
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=2
        aikuisia=2
        vakiintunutpalkka=3500    
        tyoton=1
        saa_ansiopaivarahaa=0
        puolison_tulot=1000
        puolison_vakiintunutpalkka=3500
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0
    elif perhetyyppi==45: # 2+4
        lapsia=4
        paivahoidossa=4
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=2
        aikuisia=1
        vakiintunutpalkka=1500    
        tyoton=1
        saa_ansiopaivarahaa=0
        puolison_tulot=0    
        puolison_vakiintunutpalkka=3500
        puoliso_tyoton=1
        puoliso_saa_ansiopaivarahaa=0
    elif perhetyyppi==46: # 2+3
        lapsia=2
        paivahoidossa=2
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=2
        aikuisia=2
        vakiintunutpalkka=1500
        tyoton=1
        saa_ansiopaivarahaa=0
        puolison_tulot=1000
        puolison_vakiintunutpalkka=2500
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0
    elif perhetyyppi==47: # 2+3
        lapsia=0
        paivahoidossa=0
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=0
        aikuisia=1
        vakiintunutpalkka=4000
        tyoton=1
        saa_ansiopaivarahaa=1
        puolison_tulot=0
        puolison_vakiintunutpalkka=0
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0
    elif perhetyyppi==48: # 2+3
        lapsia=0
        paivahoidossa=0
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=0
        aikuisia=1
        vakiintunutpalkka=4000
        tyoton=0
        saa_ansiopaivarahaa=0
        puolison_tulot=0
        puolison_vakiintunutpalkka=0
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0
    elif perhetyyppi==49: # 2+2
        lapsia=2
        paivahoidossa=2
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=2
        aikuisia=2
        vakiintunutpalkka=2500
        tyoton=1
        saa_ansiopaivarahaa=1
        puolison_tulot=1000
        puolison_vakiintunutpalkka=1000
        puoliso_tyoton=0
        puoliso_saa_ansiopaivarahaa=0
    elif perhetyyppi==50: # 2+2
        lapsia=2
        paivahoidossa=2
        lapsia_kotihoidontuella=0
        kotihoidontuella=0
        alle3v=2
        aikuisia=2
        vakiintunutpalkka=2500
        tyoton=0
        saa_ansiopaivarahaa=0
        puolison_tulot=1000
        puolison_vakiintunutpalkka=1000
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
        
    if lapsia>0 and aikuisia==1:
        p['saa_elatustukea']=1
        
    # perhekoko          1   2   3   4    5
    # luvut peräisin Viitamäeltä
    vuokra_toimeentulo=np.array([440,660,850,980,1150]) # helsinki 675 800 919 1008 +115/hlo
    vuokra_asumistuki =np.array([411,600,761,901,1024])
    vuokra_yhdistetty =vuokra_toimeentulo    

    ind=lapsia+aikuisia-1
    if ind<5:
        asumismenot_toimeentulo=vuokra_toimeentulo[ind]
        asumismenot_asumistuki=vuokra_asumistuki[ind]
        asumismenot_yhdistetty=vuokra_yhdistetty[ind]
    else:
        asumismenot_toimeentulo=vuokra_toimeentulo[4]+115*(ind-4)
        asumismenot_asumistuki=vuokra_asumistuki[4]+115*(ind-4)
        asumismenot_yhdistetty=vuokra_yhdistetty[4]+115*(ind-4)
    
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
    p['opiskelija']=opiskelija
    p['aitiysvapaalla']=0
    p['isyysvapaalla']=0
    p['kotihoidontuella']=kotihoidontuella
    p['lapsia_paivahoidossa']=paivahoidossa
    p['aikuisia']=aikuisia
    p['vakiintunutpalkka']=vakiintunutpalkka
    p['tyoton']=tyoton
    p['saa_ansiopaivarahaa']=saa_ansiopaivarahaa
    p['puoliso_tulot']=puolison_tulot
    p['puoliso_t']=puolison_tulot
    p['puoliso_vakiintunutpalkka']=puolison_vakiintunutpalkka
    p['puoliso_tyoton']=puoliso_tyoton
    p['puoliso_saa_ansiopaivarahaa']=puoliso_saa_ansiopaivarahaa
    p['asumismenot_toimeentulo']=asumismenot_toimeentulo
    p['asumismenot_asumistuki']=asumismenot_asumistuki
    p['asumismenot_yhdistetty']=asumismenot_yhdistetty
    p['lapsia_kotihoidontuella']=lapsia_kotihoidontuella
    p['lapsia_alle_3v']=alle3v
    p['lapsia_alle_kouluikaisia']=lapsia
    p['puoliso_elakkeella']=0
    p['puoliso_opiskelija']=0
    p['puoliso_tyoelake']=0
    p['puoliso_aitiysvapaalla']=0
    p['puoliso_isyysvapaalla']=0
    p['puoliso_sairauspaivarahalla']=0
    p['puoliso_kotihoidontuella']=0
    
    #return lapsia,paivahoidossa,lapsia_kotihoidontuella,aikuisia,vakiintunutpalkka,tyoton,saa_ansiopaivarahaa, \
    #puolison_tulot,puolison_vakiintunutpalkka,puoliso_tyoton,puoliso_saa_ansiopaivarahaa, \
    #asumismenot_asumistuki,asumismenot_toimeentulo,alle3v,asumismenot_yhdistetty 
    
    selite=tee_selite(p)
    
    if tulosta:
        print(selite)
    
    return p,selite

def tee_selite(p,p2=None,short=False):
    if p['aikuisia']>1:
        selite="{aikuisia} aikuista".format(aikuisia=p['aikuisia'])
    elif p['aikuisia']>0:
        selite="{aikuisia} aikuinen".format(aikuisia=p['aikuisia'])
    else:
        selite="Perhe, jossa ei aikuisia"
        
    if not short and False:
        if p['lapsia']>0:
            pvhoito=''
            if p['lapsia']<2:
                if p['lapsia_paivahoidossa']>0:
                    pvhoito=" (päivähoidossa)"
                if p['lapsia_kotihoidontuella']>0:
                    pvhoito=" (kotihoidossa)"
                selite+=" ja 1 lapsi{}.".format(pvhoito)
            else:
                if p['lapsia_paivahoidossa']>0:
                    pvhoito=" ({paiva} päivähoidossa)".format(paiva=p['lapsia_paivahoidossa'])
                if p['lapsia_kotihoidontuella']>0:
                    pvhoito=" ({paiva} kotihoidossa)".format(paiva=p['lapsia_kotihoidontuella'])
                if p['lapsia']>1:
                    selite+=" ja {} lasta{}.".format(p['lapsia'],pvhoito)
                else:
                    selite+=" ja 1 lapsi{}.".format(pvhoito)
            #if p['lapsia_alle_3v']>0:
            #    selite+=" Lapsista {alle3v} alle 3v.".format(alle3v=p['lapsia_alle_3v'])
        else:
            selite=selite+", ei lapsia."
    else:
        if p['lapsia']>0:
            if p['lapsia']>1:
                selite+=" ja {lapsia} lasta.".format(lapsia=p['lapsia'])
            else:
                selite+=" ja 1 lapsi."
        else:
            selite=selite+", ei lapsia."   
                 
    if p2 is not None:
        selite+=' Siirtyy'
        if p['elakkeella']<1:
            if p['tyoton']>0:
                selite+=" työttömästä"
                if p['saa_ansiopaivarahaa']>0:
                    if short:
                        selite+=" (ansiopäiväraha)"
                    else:
                        selite+=" (ansiopäiväraha, peruste {v} e/kk)".format(v=p['vakiintunutpalkka'])
                else:
                    selite+=" (työmarkkinatuki)"
            elif p['opiskelija']>0:
                selite+=" opiskelijast"
            elif p['kotihoidontuella']>0:
                selite+=" kotihoidontuelta"
            else:
                selite+=" töistä"
        else:
            selite+=" Vanhuuseläkkeellä (työeläke {e} e/kk)".format(e=p['tyoelake'])
        if p2['elakkeella']<1:
            if p2['tyoton']>0:
                selite+=" työttömäksi"
                if p2['saa_ansiopaivarahaa']>0:
                    if short:
                        selite+=" (ansiopäiväraha)"
                    else:
                        selite+=" (ansiopäiväraha, peruste {v} e/kk)".format(v=p['vakiintunutpalkka'])
                else:
                    selite+=" (työmarkkinatuki)"
            elif p2['opiskelija']>0:
                selite+=" opiskelijaks"
            elif p2['kotihoidontuella']>0:
                selite+=" kotihoidontuelle"
            else:
                selite+=" töihin"
    else:
        if p['elakkeella']<1:
            if p['tyoton']>0:
                if p['saa_ansiopaivarahaa']>0:
                    if short:
                        selite+=" Ansiopäivärahalta työllistyvä"
                    else:
                        selite+=" Ansiopäivärahalta työllistyvä (peruste {v} e/kk)".format(v=p['vakiintunutpalkka'])
                else:
                    selite+=" Työmarkkinatuelta työllistyvä"
            elif p['opiskelija']>0:
                selite+=" Opiskelija"
            elif p['kotihoidontuella']>0:
                selite+=" Kotihoidontuella"
            else:
                selite+=" Töissä"
        else:
            selite+=" Vanhuuseläkkeellä (työeläke {e} e/kk)".format(e=p['tyoelake'])
        
    if not short:
        if p['aikuisia']>1:
            if p['puoliso_tyoton']>0:
                selite+=", puoliso työtön"
                if p['puoliso_saa_ansiopaivarahaa']>0:
                    selite+=" (ansiopäiväraha, peruste {v} e/kk).".format(v=p['puoliso_vakiintunutpalkka'])
                else:
                    selite+=" (työmarkkinatuki)."
            else:
                selite+=", puoliso töissä"
                selite+=" ({p} e/kk).".format(p=p['puoliso_tulot'])
        else:
            selite+=", ei puolisoa."
        
        #selite+=" Asumismenot {a} e/kk".format(a=p['asumismenot_toimeentulo'])
            
    return selite

def print_examples():
    for k in range(1,50):
        p,selite=perheparametrit(perhetyyppi=k,tulosta=False)
        print('Tapaus {}:\n{}\n'.format(k,selite))  