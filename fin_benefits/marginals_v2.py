"""

    benefits
    
    implements social security and social insurance benefits in the Finnish social security schemes


"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite
from .labels import Labels
from .ben_utils import get_palette_EK,get_style_EK
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
import math

    
def print_q(a):
    '''
    pretty printer for dict
    '''
    for x in a.keys():
        if a[x]>0 or a[x]<0:
            print('{}:{:.2f} '.format(x,a[x]),end='')
            
    print('')
        
        
def compare_q_print(q,q2,omat='omat_',puoliso='puoliso_'):
    '''
    Helper function that prettyprints arrays
    '''
    for key in q:
        if key in q and key in q2:
            if not math.isclose(q[key],q2[key]):
                print(f'{key}: {q[key]:.2f} vs {q2[key]:.2f}')
        else:
            if key in q:
                print(key,' not in q2')
            else:
                print(key,' not in q')
class Marginals():
    """
    Description:
        The Finnish Earnings-related Social Security

    Source:
        AT
        
    v2: takes care of household issues

    """
    
    def __init__(self,ben,**kwargs):
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
        self.ben=ben
        
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
        self.ben.set_year(self.year)
        self.lab=Labels()
        self.labels=self.lab.ben_labels(self.language)
        
        if self.vaihtuva_tyelmaksu:
            self.get_tyelpremium()        

    def plot_tva_marg(self,tva,palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,tva_alv,pal,
                ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=False,incl_alv=False,
                csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True):
        if ax is None:
            figi,axs = plt.subplots()
        else:
            #figi=fig
            axs=ax
        #sns.set_theme(**csfont)
        axs.set_axisbelow(False)
        self.plot_marg_extra(axs,palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,tva_alv,pal,
            incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv)
        axs.plot(tva,'k',lw=4.5)

        axs.set_xlabel(self.labels['wage'],**csfont)
        axs.set_ylabel('Työllistymisveroaste (%)',**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_facecolor('white')
        axs.set_xlim(min_salary, max_salary)
        axs.set_ylim(0, 120)
        if legend:
            #axs.legend(loc='upper right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
            
        if figname is not None:
            plt.savefig(figname+'_tva.png',dpi=200)
        if show:
            plt.show()    
            
    def plot_eff_marg(self,eff,palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
                ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=False,incl_alv=False,
                csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True):
        if ax is None:
            figi,axs = plt.subplots()
        else:
            axs=ax
        #sns.set_theme()
        axs.set_axisbelow(False)
        self.plot_marg_extra(axs,palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
            incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv)
                    
        axs.plot(eff,'k',lw=4.5)
        axs.set_xlabel(self.labels['wage'],**csfont)
        axs.set_ylabel(self.labels['effective'],**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_xlim(min_salary, max_salary)
        axs.set_ylim(0, 119)
        if legend:
            #axs.legend(loc='upper right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
            
        if figname is not None:
            plt.savefig(figname+'_eff.png')
        if show:
            plt.show()            
            
    def plot_osatva_marg(self,osatva,palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,osatva_alv,pal,
                ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=False,incl_alv=False,
                csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True):
        if ax is None:
            figi,axs = plt.subplots()
        else:
            axs=ax
        axs.set_axisbelow(False)
        self.plot_marg_extra(axs,palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,osatva_alv,pal,
            incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv)

        axs.plot(osatva,'k',lw=4.5)
        axs.set_xlabel(self.labels['parttimewage'],**csfont)
        axs.set_ylabel('Eff. rajaveroaste osa-aikatyöstä kokoaikatyöhön (%)',**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_facecolor('white')
        axs.set_xlim(min_salary, max_salary)
        axs.set_ylim(0, 100)
        if legend:
            #axs.legend(loc='upper right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
            
        if figname is not None:
            plt.savefig(figname+'_osatva.png',dpi=200)
        if show:
            plt.show()                        
            
    def plot_netto_income(self,netto,palkka,nettopalkka,asumistuki,toimeentulotuki,ansiopvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
            ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=True,
            csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True):
            
        if ax is None:
            figi,axs = plt.subplots()
        else:
            #figi=fig
            axs=ax
        #sns.set_theme(**csfont)
        axs.set_axisbelow(False)
        
        if incl_perustulo:
            axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,ansiopvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                    self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
        else:
            if incl_elake:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,ansiopvraha,kotihoidontuki,lapsilisa,elake,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            elif incl_opintotuki:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,ansiopvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            elif incl_kotihoidontuki:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,ansiopvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            else:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,ansiopvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            
        axs.plot(netto,'k',lw=4.5)
        axs.set_xlabel(self.labels['wage'],**csfont)
        axs.set_ylabel(self.labels['net income'],**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_facecolor('white')
        axs.set_xlim(min_salary, max_salary)
        if legend:        
            #axs.legend(loc='lower right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='lower right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
            
        if figname is not None:
            plt.savefig(figname+'_netto.png')
        if show:
            plt.show()
            
    def plot_marg_extra(self,axs,palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
            incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=True,incl_alv=False):
            
        if not incl_alv:
            if incl_perustulo:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margopintotuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['opintotuki']),
                        colors=pal)
                elif incl_kotihoidontuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margpvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['paivahoito']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito']),
                        colors=pal)
        else:
            if incl_perustulo:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo'],self.labels['alv']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['alv']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margopintotuki,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['opintotuki'],self.labels['alv']),
                        colors=pal)
                elif incl_kotihoidontuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margpvhoito,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['paivahoito'],self.labels['alv']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['alv']),
                        colors=pal)

            
    def setup_EK_fonts(self):
        pal=get_palette_EK()
        #csfont = {'fontname':'Comic Sans MS'}
        fontname='IBM Plex Sans'
        csfont = {'font':fontname,'family':fontname,'fontsize':15}
        #fontprop = font_manager.FontProperties(family=fontname,weight='normal',style='normal', size=12)
        custom_params = {"axes.spines.right": False, "axes.spines.top": False, "axes.spines.left": False, 'ytick.left': False}
        sns.set_theme(style="ticks", font=fontname,rc=custom_params)
        linecolors = {'color':'red'}
        
        return csfont,pal
        
    def lp_marginaalit_apu(self,axs,otsikko='',p=None,min_salary=0,max_salary=6000,type='eff',dt=100,selite=False,source=False,
                            header=False,head_text='',incl_perustulo=None,grayscale=False,palette_EK=True,incl_alv=False,
                            legend=False,figname=None,show=True):
        
        if type=='eff':
            self.laske_ja_plottaa_marginaalit(p=p,p2=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=False,plot_eff=True,plot_netto=False,figname=None,grayscale=False,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=False,header=header,source='Lähde: EK',palette=None,palette_EK=palette_EK,square=False)
        elif type=='tva':
            self.laske_ja_plottaa_marginaalit(p=p,p2=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=True,plot_eff=False,plot_netto=False,figname=None,grayscale=False,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=False,header=header,source='Lähde: EK',palette=None,palette_EK=palette_EK,square=False)
        elif type=='osatva':
            self.laske_ja_plottaa_marginaalit(p=p,p2=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=False,plot_eff=False,plot_netto=False,figname=None,grayscale=False,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=True,header=header,source='Lähde: EK',palette=None,palette_EK=palette_EK,square=False)
        else:
            self.laske_ja_plottaa_marginaalit(p=p,p2=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=False,plot_eff=False,plot_netto=True,figname=None,grayscale=False,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=False,header=header,source='Lähde: EK',palette=None,palette_EK=palette_EK,square=False)
                            
                                        
    def laske_ja_plottaa_marginaalit(self,p=None,p2=None,min_salary=0,max_salary=6000,
                basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,
                otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=True,ret=False,
                plot_tva=True,plot_eff=True,plot_netto=True,figname=None,grayscale=False,
                incl_perustulo=False,incl_elake=True,fig=None,ax=None,incl_opintotuki=False,
                incl_alv=False,incl_kotihoidontuki=False,show=True,
                plot_osatva=True,header=True,source='Lähde: EK',palette=None,palette_EK=False,square=False):
        
        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            reverse=True
        else:
            pal=sns.color_palette()

        if palette is not None:
            pal=sns.color_palette(palette, 12)
            
        if palette_EK:
            csfont,pal=self.setup_EK_fonts()
        else:
            csfont = {}

        if p is None:
            p,selite=self.get_default_parameter()
            
        if header:
            head_text=tee_selite(p,p2=p2,short=False)
        else:
            head_text=None

        netto,palkka,nettopalkka,tva,osatva,eff,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,\
            elake,elatustuki,perustulo,opintotuki,kotihoidontuki,effmarg,margasumistuki,margtoimeentulotuki,\
            margansiopvraha,margverot,margalv,margelake,margpvhoito,margyht,margyht2,margperustulo,margopintotuki,\
            margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_ansiopvraha,tva_verot,\
            tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,tva_yht2,osatva,osatva_asumistuki,\
            osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_verot,osatva_alv,osatva_elake,\
            osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht,osatva_yht2\
            =self.comp_all_margs(p,p2=p2,incl_alv=incl_alv,min_salary=min_salary,max_salary=max_salary,dt=dt)
                
        if plot_eff and plottaa:
            self.plot_eff_marg(effmarg,palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show)
        
        if plot_netto and plottaa:
            # ALV:ia ei plotata nettotuloissa
            self.plot_netto_income(netto,palkka,nettopalkka,asumistuki,toimeentulotuki,ansiopvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show)

        if plot_tva and plottaa:
            self.plot_tva_marg(tva,palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_ansiopvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,tva_alv,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show)
            
        if plot_osatva and plottaa:
            self.plot_osatva_marg(osatva,palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,osatva_alv,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show)
            print(osatva_yht,osatva_yht2,osatva)
            plt.plot(palkka,osatva_yht)
            plt.plot(palkka,osatva_yht2)
            plt.plot(palkka,osatva)
            plt.show()
               
        if ret: 
            return netto,eff,tva,osatva
            
            
    def add_source(self,source,**csfont):
        plt.annotate(source, xy=(0.88,-0.1), xytext=(0,0), xycoords='axes fraction', textcoords='offset points', va='top', **csfont)

    def laske_ja_plottaa_veromarginaalit(self,p=None,min_salary=0,max_salary=6000,basenetto=None,baseeff=None,
            basetva=None,dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",selite=True,palette_EK=True):
        palkka=np.zeros(max_salary+1)
        margtyotvakmaksu=np.zeros(max_salary+1)        
        margsairausvakuutusmaksu=np.zeros(max_salary+1)
        margptel=np.zeros(max_salary+1)
        margtyotulovah=np.zeros(max_salary+1)
        margansiotulovah=np.zeros(max_salary+1)        
        margverot=np.zeros(max_salary+1)        
        margkunnallisvero=np.zeros(max_salary+1)        
        margvaltionvero=np.zeros(max_salary+1)  
        margperusvahennys=np.zeros(max_salary+1)  
        margpuolisonverot=np.zeros(max_salary+1)  
        tyotvakmaksu=np.zeros(max_salary+1)        
        sairausvakuutusmaksu=np.zeros(max_salary+1)
        ptel=np.zeros(max_salary+1)
        tyotulovah=np.zeros(max_salary+1)
        ansiotulovah=np.zeros(max_salary+1)        
        verot=np.zeros(max_salary+1)        
        kunnallisvero=np.zeros(max_salary+1)        
        valtionvero=np.zeros(max_salary+1)  
        perusvahennys=np.zeros(max_salary+1)  
        puolisonverot=np.zeros(max_salary+1)  
        #brutto=np.zeros(max_salary+1)  
        
        if p is None:
            p,selite=self.get_default_parameter()
            
        p2=p.copy()
        
        if palette_EK:
            csfont,pal=self.setup_EK_fonts()
        else:
            csfont = {}

        p2['t']=0 # palkka
        n0,q0=self.ben.laske_tulot_v2(p2)
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v2(p2)
            p2['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v2(p2)
            palkka[t]=t
            
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            margvaltionvero[t]=marg['valtionvero']
            margkunnallisvero[t]=marg['kunnallisvero']
            margverot[t]=marg['ansioverot']
            margansiotulovah[t]=marg['ansiotulovah']
            margtyotulovah[t]=marg['tyotulovahennys']
            margperusvahennys[t]=marg['perusvahennys']
            margptel[t]=marg['ptel']
            margsairausvakuutusmaksu[t]=marg['sairausvakuutusmaksu']
            margtyotvakmaksu[t]=marg['tyotvakmaksu']
            margpuolisonverot[t]=marg['puoliso_verot']
            tyotvakmaksu[t]=q1['tyotvakmaksu']
            sairausvakuutusmaksu[t]=q1['sairausvakuutusmaksu']
            ptel[t]=q1['ptel']
            kunnallisvero[t]=q1['kunnallisvero']
            valtionvero[t]=q1['valtionvero']
            puolisonverot[t]=0 #q1['puolisoverot']
            #brutto[t]=q1['bruttotulot']
                            
        fig,axs = plt.subplots()
        axs.stackplot(palkka,margvaltionvero,margkunnallisvero,margptel,margsairausvakuutusmaksu,margtyotvakmaksu,margpuolisonverot,
            #labels=('Valtionvero','Kunnallisvero','PTEL','sairausvakuutusmaksu','työttömyysvakuutusmaksu','puolison verot'))
            labels=('State tax','Municipal tax','Employee pension premium','sairausvakuutusmaksu','työttömyysvakuutusmaksu','puolison verot'))
        #axs.plot(margverot,label='Yht')
        #axs.plot(margyht,label='Vaihtoehto2')
        #axs.plot(margyht2,label='Vaihtoehto3')
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel(self.labels['effective'])
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_xlim(0, max_salary)
        axs.set_ylim(-50, 120)
        if selite:
            axs.legend(loc='upper left')
        plt.show()
        
        fig,axs = plt.subplots()
        axs.stackplot(palkka,tyotvakmaksu,sairausvakuutusmaksu,ptel,kunnallisvero,valtionvero,puolisonverot,
            labels=('tyotvakmaksu','sairausvakuutusmaksu','ptel','kunnallisvero','valtionvero','puolisonverot'))
        #axs.plot(netto)
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel('Verot yhteensä (e/kk)')
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_xlim(0, max_salary)
        if selite:        
            axs.legend(loc='lower right')
        plt.show()

    def laske_ja_plottaa_hila(self,min_salary=0,max_salary=6000,type='eff',dt=100,maxn=None,dire=None,palette_EK=True,grayscale=False,
            incl_perustulo=False,incl_alv=False):
        if maxn is None:
            maxn=36
        fig,axs = plt.subplots(int(maxn/5),5,sharex=True,sharey=True)
        for k in range(1,maxn):
            x=(k-1) % 5
            y=int(np.floor((k-1)/5))
            #ax=plt.subplot(10,3,k)
            p,_=perheparametrit(k)
            self.lp_marginaalit_apu(axs[y,x],otsikko='Tapaus '+str(k),p=p,min_salary=min_salary,
                max_salary=max_salary,type=type,dt=dt,grayscale=grayscale,palette_EK=palette_EK,incl_perustulo=incl_perustulo,
                incl_alv=incl_alv,show=False)

        if dire is not None:
            fig.savefig(dire+'multiple_'+type+'.eps',bbox_inches='tight')
            fig.savefig(dire+'multiple_'+type+'.png',bbox_inches='tight')

        plt.show()

    def plot_insentives(self,netto,eff,tva,osa_tva,
            min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=False,
            figname=None,grayscale=False,source=None,header=None,palette_EK=True):
            
        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            reverse=True
        else:
            pal=sns.color_palette()            
            
        if palette_EK:
            csfont,pal=self.setup_EK_fonts()
        else:
            csfont = {}
            linecolors ={}
            
        linestyle={'linewidth': 3}
        legendstyle={'frameon': False}
            
        x=np.arange(min_salary,max_salary,step_salary)
        if plot_netto:
            fig, axs = plt.subplots()
            if basenetto is not None:
                axs.plot(x,basenetto,label=otsikkobase,**linestyle)
                axs.plot(x,netto,label=otsikko,**linestyle)
                if selite:
                    axs.legend(loc='upper right',**legendstyle)
            else:
                axs.plot(x,netto,**linestyle)
            axs.set_xlabel(self.labels['wage'],**csfont)
            axs.set_ylabel(self.labels['net income'],**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(0, max_salary)
            if source is not None:
                self.add_source(source,**csfont)
            
            if header is not None:
                #axs.title.set_text(head_text,csfont)
                axs.set_title(header,**csfont)
                
            if figname is not None:
                plt.savefig(figname+'_netto.eps', format='eps')
                plt.savefig(figname+'_netto.png', format='png',dpi=300)
                
            plt.show()

        if plot_eff:
            fig, axs = plt.subplots()
            if baseeff is not None:
                axs.plot(x,baseeff,label=otsikkobase,**linestyle)
                axs.plot(x,eff,label=otsikko,**linestyle)
                if selite:
                    axs.legend(loc='upper right',**legendstyle)
            else:
                axs.plot(x,eff,**linestyle)
            axs.set_xlabel(self.labels['wage'],**csfont)
            axs.set_ylabel(self.labels['effective'],**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 119)
            if source is not None:
                self.add_source(source,**csfont)
            
            if header is not None:
                #axs.title.set_text(head_text,csfont)
                axs.set_title(header,**csfont)
            if figname is not None:
                plt.savefig(figname+'_effmarg.eps', format='eps')
            plt.show()

        if plot_tva:
            fig, axs = plt.subplots()
            if basenetto is not None:
                axs.plot(x,basetva,label=otsikkobase,**linestyle)
                axs.plot(x,tva,label=otsikko,**linestyle)
                if selite:
                    axs.legend(loc='upper right',**legendstyle)
            else:
                axs.plot(x,tva,**linestyle)
            axs.set_xlabel(self.labels['wage'],**csfont)
            axs.set_ylabel('Työllistymisveroaste (%)',**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(0, max_salary)
            axs.set_ylim(0, 120)
            if source is not None:
                self.add_source(source,**csfont)
            
            if header is not None:
                #axs.title.set_text(head_text,csfont)
                axs.set_title(header,**csfont)
            if figname is not None:
                plt.savefig(figname+'_tva.eps', format='eps')
            plt.show()

        if plot_osaeff:
            fig, axs = plt.subplots()
            if baseosatva is not None:
                axs.plot(x,baseosatva,label=otsikkobase,**linestyle)
                axs.plot(x,osa_tva,label=otsikko,**linestyle)
                if selite:
                    axs.legend(loc='upper right',**legendstyle)
            else:
                axs.plot(x,osa_tva,**linestyle)
                       
            axs.set_xlabel('Osatyön palkka (e/kk)',**csfont)
            axs.set_ylabel('Osatyöstä kokotyöhön siirtymisen eff.rajavero (%)',**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(0, max_salary)
            if source is not None:
                self.add_source(source,**csfont)
            if header is not None:
                #axs.title.set_text(head_text,csfont)
                axs.set_title(header,**csfont)
            if figname is not None:
                plt.savefig(figname+'_osatva.eps', format='eps')
            plt.show()    
    
    def laske_ja_plottaa(self,p=None,p0=None,min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,incl_alv=False,
            figname=None,grayscale=None,source='Lähde: EK',header=True,short=False):
            
        netto,eff,tva,osa_tva=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,incl_alv=incl_alv,
                                                   max_salary=max_salary,step_salary=step_salary,dt=dt)
                
        if header:
            head_text=tee_selite(p,short=short)
        else:
            head_text=None
                
        if plottaa:
            self.plot_insentives(netto,eff,tva,osa_tva,min_salary=min_salary,max_salary=max_salary+1,
                step_salary=step_salary,
                basenetto=basenetto,baseeff=baseeff,basetva=basetva,baseosatva=baseosatva,
                dt=dt,otsikko=otsikko,otsikkobase=otsikkobase,selite=selite,
                plot_tva=plot_tva,plot_eff=plot_eff,plot_netto=plot_netto,plot_osaeff=plot_osaeff,
                figname=figname,grayscale=grayscale,source=source,header=head_text)
        
        return netto,eff,tva,osa_tva

    
    def plot(self,p=None,p0=None,min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,
            figname=None,grayscale=None,source='Lähde: EK',header=True,short=False):
            
        netto,eff,tva,osa_tva=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,
                                                max_salary=max_salary,step_salary=step_salary,dt=dt)
                
        if header:
            head_text=tee_selite(p,short=short)
        else:
            head_text=None
                
        if plottaa:
            self.plot_insentives(netto,eff,tva,osa_tva,min_salary=min_salary,max_salary=max_salary+1,
                step_salary=step_salary,
                basenetto=basenetto,baseeff=baseeff,basetva=basetva,baseosatva=baseosatva,
                dt=dt,otsikko=otsikko,otsikkobase=otsikkobase,selite=selite,
                plot_tva=plot_tva,plot_eff=plot_eff,plot_netto=plot_netto,plot_osaeff=plot_osaeff,
                figname=figname,grayscale=grayscale,source=source,header=head_text)
        
        return netto,eff,tva,osa_tva

        
    def comp_insentives(self,p=None,p0=None,min_salary=0,max_salary=6000,step_salary=1,dt=100,incl_alv=False):
        '''
        Laskee marginaalit ja nettotulot
        Toimii sekä ALV että ilman ALV
        '''
    
        n_salary=int((max_salary+step_salary-min_salary)/step_salary)
        netto=np.zeros(n_salary)
        basenetto=np.zeros(n_salary)
        palkka=np.zeros(n_salary)
        tva=np.zeros(n_salary)
        osa_tva=np.zeros(n_salary)
        eff=np.zeros(n_salary)
        
        if p is None:
            p,selite=self.get_default_parameter()

        if p0 is None:
            p2b=p.copy()
        else:
            p2b=p0.copy()
        
        p3=p.copy()
            
        n0,q0=self.ben.laske_tulot_v2(p2b)
        k=0
        for t in np.arange(min_salary,max_salary+step_salary,step_salary):
            p3['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v2(p3,include_alv=incl_alv)
            p3['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v2(p3,include_alv=incl_alv)
            p3['t']=t+max(t,dt) # palkka
            n3,q3=self.ben.laske_tulot_v2(p3,include_alv=incl_alv)
            netto[k]=n1
            palkka[k]=t
            eff[k]=(1-(n2-n1)/dt)*100
            delta_t=max(t,dt)
            if t>0:
                tva[k]=(1-(n1-n0)/t)*100
            else:
                tva[k]=np.nan
            if delta_t>0:
                osa_tva[k]=(1-(n3-n1)/delta_t)*100
            else:
                osa_tva[k]=np.nan
            p2b['t']=t # palkka
            basenetto[k],_=self.ben.laske_tulot_v2(p2b,include_alv=incl_alv)

            if osa_tva[k]<0:
                print('otva',osa_tva[k],':',n3,n1,delta_t)
            if tva[k]<0:
                print('tva',tva[k],':',n1,n0,t)

            k=k+1
            
        if p0 is not None:
            return netto,eff,tva,osa_tva,basenetto
        else:
            return netto,eff,tva,osa_tva
            
            
    def comp_emtr(self,p0,p1,t,dt=1200,alku='',display=False):
        '''
        Computes EMTR at wage t
        '''
        p3=p1.copy()
            
        n0,q0=self.ben.laske_tulot_v2(p0,include_alv=False)
        k=0
        
        t=t/12
        dt=dt/12
        
        p3[alku+'t']=t # palkka nykytilassa
        n1,q1=self.ben.laske_tulot_v2(p3,include_alv=False)
        p3[alku+'t']=t+dt # palkka
        n1b=q1['omat_netto']
        n2,q2=self.ben.laske_tulot_v2(p3,include_alv=False)
        n2b=q2['omat_netto']
        netto=n1
        palkka=t
        eff=(1-(n2-n1)/dt)*100
        if t>0:
            tva=(1-(n1-n0)/t)*100
            #osa_tva=(1-(n3-n1)/t)*100
        else:
            tva=np.nan
            #osa_tva=0
            
        if tva<0 or display:
            print('eff',eff,'tva',tva,'netto1',n1,'netto2',n2,'palkka',t,'dt',dt)
            print('n1',n1,n1b)
            print('n2',n2,n2b)
            compare_q_print(q1,q2)
            
        #print(n0,n1,tva,t)

        return netto,eff,tva#,osa_tva        

    def comp_taxes(self,p=None,p2=None,min_salary=0,max_salary=6000,step_salary=1,dt=100,incl_alv=False):
        n_salary=int((max_salary+step_salary-min_salary)/step_salary)+1
        netto=np.zeros(n_salary)
        palkka=np.zeros(n_salary)
        taxes=np.zeros(n_salary)
        contributions=np.zeros(n_salary)
        eff=np.zeros(n_salary)
        
        if p is None:
            p,selite=self.get_default_parameter()

        if p2 is None:
            p2=p.copy()
            p2['t']=0 # palkka
        p3=p.copy()
        n0,q0=self.laske_tulot_v2(p2,include_alv=incl_alv)
        k=0
        wages=np.arange(min_salary,max_salary+step_salary,step_salary)
        for t in wages:
            p3['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v2(p3,include_alv=incl_alv)
            p3['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v2(p3,include_alv=incl_alv)
            netto[k]=n1
            palkka[k]=t
            eff[k]=(1-(n2-n1)/dt)*100
            taxes[k]=q1['verot']
            
            #print(f"{t:.2f},{q1['verot']:.2f},{q1['valtionvero']:.2f},{q1['kunnallisvero']:.2f}")
            #print(f"sv:{q1['ptel']:.2f},{q1['sairausvakuutusmaksu']:.2f},{q1['tyotvakmaksu']:.2f},{q1['tyel_kokomaksu']:.2f},{q1['ylevero']}")
            #print(f"vä:{q1['ansiotulovahennys']:.2f},{q1['perusvahennys']:.2f},{q1['tyotulovahennys']:.2f},{q1['tyotulovahennys_kunnallisveroon']}")
            #print(f"pe:{t:.2f},{q1['kunnallisveronperuste']:.2f},{q1['valtionveroperuste']:.2f}")

            k=k+1
            
        return wages,netto,eff,taxes
        
        
    def comp_top_marginaali(self,p=None):
    
        if p==None:
            p,selite=perheparametrit(perhetyyppi=1)
        salary=150_000/12.5
        n,eff,_,_=self.comp_insentives(p=p,min_salary=salary,max_salary=salary+1,step_salary=1,dt=100)
        #print(n,eff)
        
        return eff[0]

        
    def laske_marginaalit(self,q1,q2,dt,tyollistymisveroaste=False):
        '''
        Apurutiini
        '''
    
        if dt<1:
            dt=np.nan

        # lasketaan marginaalit
        marg={}        
        marg['asumistuki']=(-q2['asumistuki']+q1['asumistuki'])*100/dt
        marg['kotihoidontuki']=(-q2['kotihoidontuki_netto']+q1['kotihoidontuki_netto'])*100/dt
        marg['ansiopvraha']=(+q1['ansiopvraha_netto']-q2['ansiopvraha_netto'])*100/dt 
        marg['pvhoito']=(-q1['pvhoito']+q2['pvhoito'])*100/dt
        marg['toimeentulotuki']=(+q1['toimeentulotuki']-q2['toimeentulotuki'])*100/dt
        marg['palkkaverot']=(-q1['verot_ilman_etuuksia']+q2['verot_ilman_etuuksia'])*100/dt
        marg['valtionvero']=(-q1['valtionvero']+q2['valtionvero'])*100/dt
        marg['alv']=(-q1['alv']+q2['alv'])*100/dt
        marg['elake']=(q1['kokoelake_netto']-q2['kokoelake_netto'])*100/dt
        marg['opintotuki']=(q1['opintotuki_netto']-q2['opintotuki_netto'])*100/dt
        marg['kunnallisvero']=(-q1['kunnallisvero']+q2['kunnallisvero'])*100/dt
        marg['ptel']=(-q1['ptel']+q2['ptel'])*100/dt
        marg['sairausvakuutusmaksu']=(-q1['sairausvakuutusmaksu']+q2['sairausvakuutusmaksu'])*100/dt
        marg['tyotvakmaksu']=(-q1['tyotvakmaksu']+q2['tyotvakmaksu'])*100/dt
        marg['puoliso_verot']=(-q1['puoliso_verot']+q2['puoliso_verot'])*100/dt
        marg['perustulo']=(-q2['perustulo_nettonetto']+q1['perustulo_nettonetto'])*100/dt
    
        marg['sivukulut']=marg['tyotvakmaksu']+marg['sairausvakuutusmaksu']+marg['ptel'] # sisältyvät jo veroihin
        marg['etuudet']=marg['ansiopvraha']+marg['asumistuki']+marg['toimeentulotuki']+marg['kotihoidontuki']+marg['perustulo']
        marg['verot']=marg['palkkaverot'] # sisältää sivukulut
        marg['ansioverot']=marg['palkkaverot']+marg['elake'] # sisältää sivukulut
        marg['marginaali']=marg['pvhoito']+marg['etuudet']+marg['verot']+marg['elake']+marg['alv']
    
        # ja käteen jää
        tulot={}
        tulot['kateen1']=q1['netto']
        tulot['kateen2']=q2['netto']
    
        if 'omattulot_netto' in q1: # v1
            omattulotnetto1=q1['omattulot_netto'] # ilman etuuksia
            omattulotnetto2=q2['omattulot_netto'] # ilman etuuksia
            puolisontulotnetto1=q1['puoliso_tulot_netto'] # ilman etuuksia
            puolisontulotnetto2=q2['puoliso_tulot_netto'] # ilman etuuksia
        else:
            omattulotnetto1=q1['omat_netto'] # ilman etuuksia
            omattulotnetto2=q2['omat_netto'] # ilman etuuksia
            puolisontulotnetto1=q1['puoliso_netto'] # ilman etuuksia
            puolisontulotnetto2=q2['puoliso_netto'] # ilman etuuksia

        if tyollistymisveroaste:
            tulot['tulotnetto']=omattulotnetto2+puolisontulotnetto2
        else:
            tulot['tulotnetto']=omattulotnetto1+puolisontulotnetto1
            
        marg['marginaaliveroprosentti']=100-(tulot['kateen2']-tulot['kateen1'])*100/dt 
    
        return tulot,marg
        
    def laske_ja_selita(self,p=None,p0=None,min_salary=0,max_salary=3000,step_salary=1500,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,
            figname=None,grayscale=None,source='Lähde: EK',header=True):
            
        head_text=tee_selite(p,short=False)

        if p0 is None:
            netto,eff,tva,osa_tva=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,
                                                    max_salary=max_salary,step_salary=step_salary,dt=dt)
                
            tyottomana_base=basenetto[0]
            tyottomana_vaihtoehto=netto[0]
            tyottomana_ero=tyottomana_vaihtoehto-tyottomana_base
            tyossa_base=basenetto[2]
            tyossa_vaihtoehto=netto[2]
            tyossa_ero=tyossa_vaihtoehto-tyossa_base
            osatyossa_base=basenetto[1]
            osatyossa_vaihtoehto=netto[1]
            osatyossa_ero=osatyossa_vaihtoehto-osatyossa_base
        else:
            netto,eff,tva,osa_tva,basenetto=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,
                                                    max_salary=max_salary,step_salary=step_salary,dt=dt)
            tyottomana_base=basenetto[0]
            tyottomana_vaihtoehto=netto[0]
            tyottomana_ero=tyottomana_vaihtoehto-tyottomana_base
            tyossa_base=basenetto[2]
            tyossa_vaihtoehto=netto[2]
            tyossa_ero=tyossa_vaihtoehto-tyossa_base
            osatyossa_base=basenetto[1]
            osatyossa_vaihtoehto=netto[1]
            osatyossa_ero=osatyossa_vaihtoehto-osatyossa_base
        

        if header:
            print(head_text)
        print(f'Nettotulot työttömänä {tyottomana_vaihtoehto:.2f} perus {tyottomana_base:.2f}  ero {tyottomana_ero:.2f}')
        print(f'Nettotulot työssä (palkka {max_salary:.2f} e/kk) {tyossa_vaihtoehto:.2f} perus {tyossa_base:.2f}  ero {tyossa_ero:.2f} tva {tva[2]:.3f}%')
        print(f'Nettotulot 50% osa-aikatyössä (palkka {max_salary/2:.2f} e/k) {osatyossa_vaihtoehto:.2f} perus {osatyossa_base:.2f} ero {osatyossa_ero:.2f}  tva {tva[1]:.3f}%')
        
        return netto,eff,tva,osa_tva        
        
        
    def comp_all_margs(self,p,p2=None,incl_alv=False,min_salary=0,max_salary=6_000,dt=100):
        '''
        Jaottelee marginaalit ja tulot eriin
        '''
        netto=np.zeros(max_salary+1)
        palkka=np.zeros(max_salary+1)
        nettopalkka=np.zeros(max_salary+1)
        tva=np.zeros(max_salary+1)
        osatva=np.zeros(max_salary+1)
        eff=np.zeros(max_salary+1)
        asumistuki=np.zeros(max_salary+1)
        toimeentulotuki=np.zeros(max_salary+1)
        ansiopvraha=np.zeros(max_salary+1)
        nettotulot=np.zeros(max_salary+1)
        lapsilisa=np.zeros(max_salary+1)
        elake=np.zeros(max_salary+1)    
        elatustuki=np.zeros(max_salary+1)
        perustulo=np.zeros(max_salary+1)
        opintotuki=np.zeros(max_salary+1)        
        kotihoidontuki=np.zeros(max_salary+1)    
        effmarg=np.zeros(max_salary+1)
        margasumistuki=np.zeros(max_salary+1)
        margtoimeentulotuki=np.zeros(max_salary+1)
        margansiopvraha=np.zeros(max_salary+1)
        margverot=np.zeros(max_salary+1)    
        margalv=np.zeros(max_salary+1)    
        margelake=np.zeros(max_salary+1)    
        margpvhoito=np.zeros(max_salary+1)        
        margyht=np.zeros(max_salary+1)        
        margyht2=np.zeros(max_salary+1)    
        margperustulo=np.zeros(max_salary+1)    
        margopintotuki=np.zeros(max_salary+1)    
        margkotihoidontuki=np.zeros(max_salary+1)    
        tva=np.zeros(max_salary+1)
        tva_asumistuki=np.zeros(max_salary+1)
        tva_kotihoidontuki=np.zeros(max_salary+1)    
        tva_toimeentulotuki=np.zeros(max_salary+1)
        tva_ansiopvraha=np.zeros(max_salary+1)
        tva_verot=np.zeros(max_salary+1)        
        tva_alv=np.zeros(max_salary+1)    
        tva_elake=np.zeros(max_salary+1)        
        tva_pvhoito=np.zeros(max_salary+1)        
        tva_perustulo=np.zeros(max_salary+1)        
        tva_opintotuki=np.zeros(max_salary+1)        
        tva_yht=np.zeros(max_salary+1)        
        tva_yht2=np.zeros(max_salary+1)        
        osatva=np.zeros(max_salary+1)
        osatva_asumistuki=np.zeros(max_salary+1)
        osatva_kotihoidontuki=np.zeros(max_salary+1)    
        osatva_toimeentulotuki=np.zeros(max_salary+1)
        osatva_ansiopvraha=np.zeros(max_salary+1)
        osatva_verot=np.zeros(max_salary+1)        
        osatva_alv=np.zeros(max_salary+1)    
        osatva_elake=np.zeros(max_salary+1)        
        osatva_pvhoito=np.zeros(max_salary+1)        
        osatva_perustulo=np.zeros(max_salary+1)        
        osatva_opintotuki=np.zeros(max_salary+1)        
        osatva_yht=np.zeros(max_salary+1)        
        osatva_yht2=np.zeros(max_salary+1)      
        
        if p2 is None:
            p1=p.copy()
            p2=p.copy()
            p3=p.copy()
        else:
            p1=p.copy()
            p3=p2.copy()
            plot_eff=False  
        
        p1['t']=0 # palkka
        n0_alv,q0_alv=self.ben.laske_tulot_v2(p1,include_alv=True)
        n0_noalv,q0_noalv=self.ben.laske_tulot_v2(p1,include_alv=False)
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1_noalv,q1_noalv=self.ben.laske_tulot_v2(p2,include_alv=False)
            n1_alv,q1_alv=self.ben.laske_tulot_v2(p2,include_alv=True)
            p2['t']=t+dt # palkka
            n2_noalv,q2_noalv=self.ben.laske_tulot_v2(p2,include_alv=False)
            n2_alv,q2_alv=self.ben.laske_tulot_v2(p2,include_alv=True)
            deltat=max(t,dt)
            p3['t']=t+deltat # palkka
            n3_noalv,q3_noalv=self.ben.laske_tulot_v2(p3,include_alv=False)
            n3_alv,q3_alv=self.ben.laske_tulot_v2(p3,include_alv=True)
            
            tulot_noalv,marg_noalv=self.laske_marginaalit(q1_noalv,q2_noalv,dt)
            tulot_alv,marg_alv=self.laske_marginaalit(q1_alv,q2_alv,dt)
            tulot2_noalv,tvat_noalv=self.laske_marginaalit(q0_noalv,q1_noalv,t,tyollistymisveroaste=True)
            tulot2_alv,tvat_alv=self.laske_marginaalit(q0_alv,q1_alv,t,tyollistymisveroaste=True)
            tulot3_alv,osatvat_alv=self.laske_marginaalit(q2_alv,q3_alv,deltat,tyollistymisveroaste=True)
            tulot3_noalv,osatvat_noalv=self.laske_marginaalit(q2_noalv,q3_noalv,deltat,tyollistymisveroaste=True)
            palkka[t]=t
            if incl_alv:
                netto[t]=n1_alv
                effmarg[t]=marg_alv['marginaaliveroprosentti']
                margyht[t]=marg_alv['marginaali']
                margyht2[t]=marg_alv['marginaaliveroprosentti']
                margalv[t]=marg_alv['alv']
            else:
                netto[t]=n1_noalv
                effmarg[t]=marg_noalv['marginaaliveroprosentti']
                margyht[t]=marg_noalv['marginaali']
                margyht2[t]=marg_noalv['marginaaliveroprosentti']
                margalv[t]=marg_noalv['alv']
                
            margasumistuki[t]=marg_noalv['asumistuki']
            margtoimeentulotuki[t]=marg_noalv['toimeentulotuki']
            margverot[t]=marg_noalv['verot']
            margelake[t]=marg_noalv['elake']
            margansiopvraha[t]=marg_noalv['ansiopvraha']
            margpvhoito[t]=marg_noalv['pvhoito']
            margperustulo[t]=marg_noalv['perustulo']
            margkotihoidontuki[t]=marg_noalv['kotihoidontuki']
            margopintotuki[t]=marg_noalv['opintotuki']
            
            if incl_alv:
                elake[t]=q1_alv['kokoelake_netto']
                asumistuki[t]=q1_alv['asumistuki']
                toimeentulotuki[t]=q1_alv['toimeentulotuki']
                opintotuki[t]=q1_alv['opintotuki']
                ansiopvraha[t]=q1_alv['ansiopvraha_nettonetto']
                lapsilisa[t]=q1_alv['lapsilisa']
                perustulo[t]=q1_alv['perustulo_nettonetto']
                elatustuki[t]=q1_alv['elatustuki']
                nettotulot[t]=tulot_alv['tulotnetto']
                nettopalkka[t]=q1_alv['palkkatulot_nettonetto']
                kotihoidontuki[t]=q1_alv['kotihoidontuki_netto']
            else:
                elake[t]=q1_noalv['kokoelake_netto']
                asumistuki[t]=q1_noalv['asumistuki']
                toimeentulotuki[t]=q1_noalv['toimeentulotuki']
                opintotuki[t]=q1_noalv['opintotuki']
                ansiopvraha[t]=q1_noalv['ansiopvraha_nettonetto']
                lapsilisa[t]=q1_noalv['lapsilisa']
                perustulo[t]=q1_noalv['perustulo_nettonetto']
                elatustuki[t]=q1_noalv['elatustuki']
                nettotulot[t]=tulot_noalv['tulotnetto']
                nettopalkka[t]=q1_noalv['palkkatulot_nettonetto']
                kotihoidontuki[t]=q1_noalv['kotihoidontuki_netto']
            
            if incl_alv:
                tva[t]=tvat_alv['marginaaliveroprosentti']
                tva_yht[t]=tvat_alv['marginaali']
                tva_yht2[t]=tvat_alv['marginaaliveroprosentti']
                tva_alv[t]=tvat_alv['alv']
            else:
                tva[t]=tvat_noalv['marginaaliveroprosentti']
                tva_yht[t]=tvat_noalv['marginaali']
                tva_yht2[t]=tvat_noalv['marginaaliveroprosentti']
                tva_alv[t]=tvat_noalv['alv']
                
            tva_asumistuki[t]=tvat_noalv['asumistuki']
            tva_kotihoidontuki[t]=tvat_noalv['kotihoidontuki']
            tva_toimeentulotuki[t]=tvat_noalv['toimeentulotuki']
            tva_verot[t]=tvat_noalv['verot']
            tva_elake[t]=tvat_noalv['elake']
            tva_perustulo[t]=tvat_noalv['perustulo']
            tva_ansiopvraha[t]=tvat_noalv['ansiopvraha']
            tva_opintotuki[t]=tvat_noalv['opintotuki']
            tva_pvhoito[t]=tvat_noalv['pvhoito']
            
            if incl_alv:
                osatva[t]=osatvat_alv['marginaaliveroprosentti']
                osatva_yht[t]=osatvat_alv['marginaali']
                osatva_yht2[t]=osatvat_alv['marginaaliveroprosentti']
                osatva_alv[t]=osatvat_alv['alv']
            else:
                osatva[t]=osatvat_noalv['marginaaliveroprosentti']
                osatva_yht[t]=osatvat_noalv['marginaali']
                osatva_yht2[t]=osatvat_noalv['marginaaliveroprosentti']
                osatva_alv[t]=osatvat_noalv['alv']
                
            if osatva[t]<0:
                print(tulot3_alv[t-1],tulot3_alv[t])
                print(tulot3_noalv[t-1],tulot3_noalv[t])
                
            osatva_asumistuki[t]=osatvat_noalv['asumistuki']
            osatva_kotihoidontuki[t]=osatvat_noalv['kotihoidontuki']
            osatva_toimeentulotuki[t]=osatvat_noalv['toimeentulotuki']
            osatva_verot[t]=osatvat_noalv['verot']
            osatva_elake[t]=osatvat_noalv['elake']
            osatva_perustulo[t]=osatvat_noalv['perustulo']
            osatva_ansiopvraha[t]=osatvat_noalv['ansiopvraha']
            osatva_opintotuki[t]=osatvat_noalv['opintotuki']
            osatva_pvhoito[t]=osatvat_noalv['pvhoito']

            if incl_alv:
                if dt>0:
                    eff[t]=(1-(n2_alv-n1_alv)/dt)*100
                else:
                    eff[t]=np.nan
                #if t>0:
                #    tva[t]=(1-(n1_alv-n0_alv)/t)*100
                #else:
                #    tva[t]=np.nan
                
                #if deltat>0:
                #    osatva[t]=(1-(n3_alv-n1_alv)/deltat)*100
                #else:
                #    osatva[t]=np.nan
            else:
                if dt>0:
                    eff[t]=(1-(n2_noalv-n1_noalv)/dt)*100
                else:
                    eff[t]=np.nan
                #if t>0:
                #    tva[t]=(1-(n1_noalv-n0_noalv)/t)*100
                #else:
                #    tva[t]=np.nan
                
                #if deltat>0:
                #    osatva[t]=(1-(n3_noalv-n1_noalv)/deltat)*100
                #else:
                #    osatva[t]=np.nan
                    
        return netto,palkka,nettopalkka,tva,osatva,eff,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,\
            elake,elatustuki,perustulo,opintotuki,kotihoidontuki,effmarg,margasumistuki,margtoimeentulotuki,\
            margansiopvraha,margverot,margalv,margelake,margpvhoito,margyht,margyht2,margperustulo,margopintotuki,\
            margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_ansiopvraha,tva_verot,\
            tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,tva_yht2,osatva,osatva_asumistuki,\
            osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_verot,osatva_alv,osatva_elake,\
            osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht,osatva_yht2