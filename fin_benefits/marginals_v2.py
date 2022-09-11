"""

    benefits
    
    implements social security and social insurance benefits in the Finnish social security schemes


"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite
from .labels import Labels
from .ben_utils import get_palette_EK,get_style_EK, compare_q_print, print_q
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
import math


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
        axs.plot(tva,'k',lw=3)

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
                ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=False,incl_alv=False,show_xlabel=True,show_ylabel=True,
                csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True,baseline_eff=None):
        if ax is None:
            figi,axs = plt.subplots()
        else:
            axs=ax
        #sns.set_theme()
        axs.set_axisbelow(False)
        self.plot_marg_extra(axs,palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
            incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv)
                    
        axs.plot(eff,'k',lw=2.0)
        if baseline_eff is not None:
            axs.plot(baseline_eff,'g--',lw=3)
        if show_xlabel:
            axs.set_xlabel(self.labels['wage'],**csfont)
        if show_ylabel:
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

        axs.plot(osatva,'k',lw=3)
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
            
        axs.plot(netto,'k',lw=3)
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
        
    def lp_marginaalit_apu(self,axs,otsikko='',p=None,min_salary=0,max_salary=8000,type='eff',dt=100,selite=False,source=False,
                            header=False,head_text='',incl_perustulo=None,grayscale=False,palette_EK=True,incl_alv=False,
                            legend=False,figname=None,show=True):
        
        if type=='eff':
            self.laske_ja_plottaa_marginaalit(p=p,p0=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=False,plot_eff=True,plot_netto=False,figname=None,grayscale=False,head_text=head_text,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=False,header=header,source=source,palette=None,palette_EK=palette_EK,square=False)
        elif type=='tva':
            self.laske_ja_plottaa_marginaalit(p=p,p0=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=True,plot_eff=False,plot_netto=False,figname=None,grayscale=False,head_text=head_text,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=False,header=header,source=source,palette=None,palette_EK=palette_EK,square=False)
        elif type=='osatva':
            self.laske_ja_plottaa_marginaalit(p=p,p0=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=False,plot_eff=False,plot_netto=False,figname=None,grayscale=False,head_text=head_text,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=True,header=header,source=source,palette=None,palette_EK=palette_EK,square=False)
        else:
            self.laske_ja_plottaa_marginaalit(p=p,p0=None,min_salary=min_salary,max_salary=max_salary,
                    dt=dt,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=legend,ret=False,
                    plot_tva=False,plot_eff=False,plot_netto=True,figname=None,grayscale=False,head_text=head_text,
                    incl_perustulo=incl_perustulo,incl_elake=True,ax=axs,incl_alv=incl_alv,show=show,
                    plot_osatva=False,header=header,source=source,palette=None,palette_EK=palette_EK,square=False)
                            
                                        
    def laske_ja_plottaa_marginaalit(self,p=None,p0=None,min_salary=0,max_salary=8000,
                basenetto=None,baseeff=None,basetva=None,dt=100,plottaa=True,
                otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=True,ret=False,
                plot_tva=True,plot_eff=True,plot_netto=True,figname=None,grayscale=False,
                incl_perustulo=False,incl_elake=True,fig=None,ax=None,incl_opintotuki=False,
                incl_alv=False,incl_kotihoidontuki=False,show=True,head_text=None,
                plot_osatva=True,header=True,source='Lähde: EK',palette=None,palette_EK=False,
                baseline_eff=None,
                square=False):
        
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
            if head_text is None:
                head_text=tee_selite(p,p0=p0,short=False)
        else:
            head_text=None

        netto,palkka,nettopalkka,tva,osatva,effmarg,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,\
            elake,elatustuki,perustulo,opintotuki,kotihoidontuki,margasumistuki,margtoimeentulotuki,\
            margansiopvraha,margverot,margalv,margelake,margpvhoito,margyht,margperustulo,margopintotuki,\
            margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_ansiopvraha,tva_verot,\
            tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,osatva,osatva_asumistuki,\
            osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_verot,osatva_alv,osatva_elake,\
            osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht\
            =self.comp_all_margs(p,p0=p0,incl_alv=incl_alv,min_salary=min_salary,max_salary=max_salary,dt=dt)
                
        if plot_eff and plottaa:
            self.plot_eff_marg(effmarg,palkka,margverot,margasumistuki,margtoimeentulotuki,margansiopvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show,
                baseline_eff=baseline_eff)
        
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
               
        if ret: 
            return netto,effmarg,tva,osatva
            
            
    def add_source(self,source,**csfont):
        plt.annotate(source, xy=(0.88,-0.1), xytext=(0,0), xycoords='axes fraction', textcoords='offset points', va='top', **csfont)

    def laske_ja_plottaa_veromarginaalit(self,p=None,min_salary=0,max_salary=8000,basenetto=None,baseeff=None,incl_perustulo=False,incl_alv=False,
            basetva=None,dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Perustapaus",selite=True,palette_EK=True,include_alv=True,figname=None,
            ret=False,source='Lähde: EK'):
        palkka=np.zeros(max_salary+1)
        margtyotvakmaksu=np.zeros(max_salary+1)        
        margsairausvakuutusmaksu=np.zeros(max_salary+1)
        margptel=np.zeros(max_salary+1)
        margtyotulovah=np.zeros(max_salary+1)
        margansiotulovah=np.zeros(max_salary+1)
        margalv=np.zeros(max_salary+1)
        margverot=np.zeros(max_salary+1)        
        margkunnallisvero=np.zeros(max_salary+1)        
        margvaltionvero=np.zeros(max_salary+1)  
        margperusvahennys=np.zeros(max_salary+1)  
        margpuolisonverot=np.zeros(max_salary+1)  
        margperustulovero=np.zeros(max_salary+1) 
        tyotvakmaksu=np.zeros(max_salary+1)        
        sairausvakuutusmaksu=np.zeros(max_salary+1)
        ptel=np.zeros(max_salary+1)
        nettoverot=np.zeros(max_salary+1)
        tyotulovah=np.zeros(max_salary+1)
        ansiotulovah=np.zeros(max_salary+1)        
        verot=np.zeros(max_salary+1)        
        kunnallisvero=np.zeros(max_salary+1)        
        valtionvero=np.zeros(max_salary+1)  
        perusvahennys=np.zeros(max_salary+1)  
        puolisonverot=np.zeros(max_salary+1)  
        perustulovero=np.zeros(max_salary+1)  
        valtionveroperuste=np.zeros(max_salary+1)  
        kunnallisveroperuste=np.zeros(max_salary+1)  
        #brutto=np.zeros(max_salary+1)  
        
        if p is None:
            p,selite=self.get_default_parameter()
            
        p2=p.copy()
        
        if palette_EK:
            csfont,pal=self.setup_EK_fonts()
        else:
            csfont = {}

        p2['t']=0 # palkka
        n0,q0=self.ben.laske_tulot_v3(p2,include_alv=incl_alv)
        for t in range(0,max_salary+1):
            p2['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v3(p2,include_alv=incl_alv)
            p2['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v3(p2,include_alv=incl_alv)
            palkka[t]=t
            
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            margvaltionvero[t]=marg['valtionvero']
            margkunnallisvero[t]=marg['kunnallisvero']
            margverot[t]=marg['ansioverot']
            margansiotulovah[t]=marg['ansiotulovahennys']
            margtyotulovah[t]=marg['tyotulovahennys']
            margperusvahennys[t]=marg['perusvahennys']
            margptel[t]=marg['ptel']
            margalv[t]=marg['alv']
            margperustulovero[t]=marg['perustulovero']
            margsairausvakuutusmaksu[t]=marg['sairausvakuutusmaksu']
            margtyotvakmaksu[t]=marg['tyotvakmaksu']
            margpuolisonverot[t]=marg['puoliso_verot']
            tyotvakmaksu[t]=q1['tyotvakmaksu']
            sairausvakuutusmaksu[t]=q1['sairausvakuutusmaksu']
            ptel[t]=q1['ptel']
            nettoverot[t]=q1['verot']
            valtionvero[t]=q1['valtionvero']
            kunnallisvero[t]=q1['kunnallisvero']
            valtionveroperuste[t]=q1['valtionveroperuste']
            kunnallisveroperuste[t]=q1['kunnallisveroperuste']
            if 'perustulovero' in q1:
                perustulovero[t]=q1['perustulovero']
            puolisonverot[t]=0 #q1['puolisoverot']
            #brutto[t]=q1['bruttotulot']
            
        fig,axs = plt.subplots()
        if incl_perustulo:
            axs.stackplot(palkka,margvaltionvero,margkunnallisvero,margptel,margsairausvakuutusmaksu,margtyotvakmaksu,margpuolisonverot,margperustulovero,
                labels=('State tax','Municipal tax','Employee pension premium','Sairaanhoitomaksu','työttömyysvakuutusmaksu','puolison verot','perustulovero'))
        else:
            axs.stackplot(palkka,margvaltionvero,margkunnallisvero,margptel,margsairausvakuutusmaksu,margtyotvakmaksu,
                labels=('State tax','Municipal tax','Employee pension premium','Sairaanhoitomaksu','työttömyysvakuutusmaksu'))
        axs.plot(margverot,color='black',label='yhteensä',lw=2.0)
        #axs.plot(margyht,label='Vaihtoehto2')
        #axs.plot(margyht2,label='Vaihtoehto3')
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel(self.labels['effective'])
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_xlim(0, max_salary)
        axs.set_ylim(-50, 120)
        if selite:
            axs.legend(loc='upper left')
        if source is not None:
            self.add_source(source,**csfont)
        plt.show()
        
        fig,axs = plt.subplots()
        if incl_perustulo:
            axs.stackplot(palkka,tyotvakmaksu,sairausvakuutusmaksu,ptel,kunnallisvero,valtionvero,puolisonverot,perustulovero,
                labels=('työttömyysvakuutusmaksu','sairausvakuutusmaksu','työntekijän työeläkemaksu','kunnallisvero','valtionvero','puolisonverot','perustulovero'))
        else:
            axs.stackplot(palkka,tyotvakmaksu,sairausvakuutusmaksu,ptel,kunnallisvero,valtionvero,
                labels=('työttömyysvakuutusmaksu','sairausvakuutusmaksu','työntekijän työeläkemaksu','kunnallisvero','valtionvero'))
        axs.plot(nettoverot,color='black',label='yhteensä',lw=2.0)
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel('Verot yhteensä (e/kk)')
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_xlim(0, max_salary)
        if selite:        
            axs.legend(loc='upper left')
        if source is not None:
            self.add_source(source,**csfont)
        plt.show()
        
        fig,axs = plt.subplots()
        axs.plot(palkka,valtionveroperuste,label='valtionveroperuste')
        axs.plot(palkka,kunnallisveroperuste,label='kunnallisveroperuste')
        axs.set_xlabel(self.labels['wage'])
        axs.set_ylabel('Veroperuste')
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_xlim(0, max_salary)
        if selite:        
            axs.legend(loc='lower right')
        if source is not None:
            self.add_source(source,**csfont)
        plt.show()
        
        if ret:
            return q1
        
    def laske_ja_plottaa_hila(self,min_salary=0,max_salary=8000,type='eff',dt=100,maxn=None,dire=None,palette_EK=True,grayscale=False,
            incl_perustulo=False,incl_alv=False,source='Lähde: EK'):
        if maxn is None:
            maxn=36
            
        fig,axs = plt.subplots(int(maxn/5),5,sharex=True,sharey=True)
        for k in range(1,maxn):
            x=(k-1) % 5
            y=int(np.floor((k-1)/5))
            #ax=plt.subplot(10,3,k)
            p,_=perheparametrit(k)
            self.lp_marginaalit_apu(axs[y,x],otsikko='Tapaus '+str(k),p=p,min_salary=min_salary,source='',
                max_salary=max_salary,type=type,dt=dt,grayscale=grayscale,palette_EK=palette_EK,incl_perustulo=incl_perustulo,
                incl_alv=incl_alv,show=False,head_text='#'+str(k),header=True)

        csfont,pal=self.setup_EK_fonts()            
        if source is not None:
            self.add_source(source,**csfont)

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
                plt.savefig(figname+'_effmarg.png', format='png')
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
                plt.savefig(figname+'_tva.png', format='png')
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
                plt.savefig(figname+'_osatva.png', format='png')
            plt.show()    
    
    def laske_ja_plottaa(self,p=None,p0=None,min_salary=0,max_salary=8000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,incl_alv=False,
            figname=None,grayscale=None,source='Lähde: EK',header=True,short=False):
            
        netto,eff,tva,osa_tva=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,incl_alv=incl_alv,
                                                   max_salary=max_salary,step_salary=step_salary,dt=dt)
                
        if header:
            head_text=tee_selite(p,p0=p0,short=short)
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
            
        n0,q0=self.ben.laske_tulot_v3(p2b,include_alv=incl_alv)
        k=0
        for t in np.arange(min_salary,max_salary+step_salary,step_salary):
            p3['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
            p3['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
            p3['t']=t+max(t,dt) # palkka
            n3,q3=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
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
            basenetto[k],_=self.ben.laske_tulot_v3(p2b,include_alv=incl_alv)

#             if osa_tva[k]<0:
#                 print('otva',osa_tva[k],':',n3,n1,delta_t)
#             if tva[k]<0:
#                 print('tva',tva[k],':',n1,n0,t)

            k=k+1
            
        if p0 is not None:
            return netto,eff,tva,osa_tva#,basenetto
        else:
            return netto,eff,tva,osa_tva
            
            
    def comp_emtr(self,p0,p1,t,dt=1200,alku='',display=False):
        '''
        Computes EMTR at wage t
        '''
        p3=p1.copy()
            
        n0,q0=self.ben.laske_tulot_v3(p0,include_alv=False)
        k=0
        
        t=t/12
        dt=dt/12
        
        p3[alku+'t']=t # palkka nykytilassa
        n1,q1=self.ben.laske_tulot_v3(p3,include_alv=False)
        p3[alku+'t']=t+dt # palkka
        n1b=q1['omat_netto']
        n2,q2=self.ben.laske_tulot_v3(p3,include_alv=False)
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
        n0,q0=self.laske_tulot_v3(p2,include_alv=incl_alv)
        k=0
        wages=np.arange(min_salary,max_salary+step_salary,step_salary)
        for t in wages:
            p3['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
            p3['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
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
        
        
    def comp_top_marginaali(self,p=None,incl_alv=False):
    
        if p==None:
            p,selite=perheparametrit(perhetyyppi=1)
        salary=150_000/12.5
        n,eff,_,_=self.comp_insentives(p=p,min_salary=salary,max_salary=salary+1,step_salary=1,dt=100,incl_alv=incl_alv)
        #print(n,eff)
        
        return eff[0]

        
    def laske_marginaalit(self,q1,q2,dt,incl_perustulo=False):
        '''
        Apurutiini
        '''
    
        if dt<1:
            dt=np.nan

        # lasketaan marginaalit
        marg={}        
        marg['asumistuki']=(-q2['asumistuki']+q1['asumistuki'])*100/dt
        marg['kotihoidontuki']=(-q2['kotihoidontuki_netto']+q1['kotihoidontuki_netto'])*100/dt
        marg['ansiopvraha']=(+q1['ansiopvraha_netto']-q2['ansiopvraha_netto'])*100/dt # verot mukana
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
        marg['perustulo']=(-q2['perustulo_netto']+q1['perustulo_netto'])*100/dt # verot mukana
        if 'perustulovero' in q1:
            marg['perustulovero']=(-q1['perustulovero']+q2['perustulovero'])*100/dt # verot mukana
        else:
            marg['perustulovero']=0
        marg['tyotulovahennys']=(-q2['tyotulovahennys']+q1['tyotulovahennys'])*100/dt # verot mukana
        marg['ansiotulovahennys']=(-q2['ansiotulovahennys']+q1['ansiotulovahennys'])*100/dt # verot mukana
        marg['perusvahennys']=(-q2['perusvahennys']+q1['perusvahennys'])*100/dt # verot mukana
    
        marg['sivukulut']=marg['tyotvakmaksu']+marg['sairausvakuutusmaksu']+marg['ptel'] # sisältyvät jo veroihin
        marg['etuudet']=marg['ansiopvraha']+marg['asumistuki']+marg['toimeentulotuki']+marg['kotihoidontuki']+marg['perustulo']
        marg['verot']=marg['palkkaverot'] # sisältää sivukulut
        marg['ansioverot']=marg['palkkaverot']+marg['elake'] # sisältää sivukulut
        marg['marginaali']=marg['pvhoito']+marg['etuudet']+marg['verot']+marg['elake']+marg['alv']
    
        # ja käteen jää
        tulot={}
        tulot['kateen1']=q1['netto']
        tulot['kateen2']=q2['netto']
        tulot['tulotnetto']=q1['netto']
            
        marg['marginaaliveroprosentti']=100-(tulot['kateen2']-tulot['kateen1'])*100/dt 
    
        return tulot,marg
        
    def laske_ja_selita(self,p=None,p0=None,min_salary=0,max_salary=3000,step_salary=1500,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osaeff=True,incl_alv=False,
            figname=None,grayscale=None,source='Lähde: EK',header=True):
            
        head_text=tee_selite(p,short=False)

        if p0 is None:
            netto,eff,tva,osa_tva=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,incl_alv=incl_alv,
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
            netto,eff,tva,osa_tva,basenetto=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,incl_alv=incl_alv,
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
        if incl_alv:
            print('Alv mukana')
        else:
            print('Alv ei mukana')
        
        return netto,eff,tva,osa_tva        
        
        
    def comp_all_margs(self,p,p0=None,incl_alv=False,min_salary=0,max_salary=6_000,dt=100):
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
        
        if p0 is None:
            p_finale=p.copy()
            p_initial=p.copy()
        else:
            p_finale=p.copy()
            p_initial=p0.copy()
            plot_eff=False  
        
        p_initial['t']=0 # palkka
        n0,q0=self.ben.laske_tulot_v3(p_initial,include_alv=incl_alv)
        for t in range(0,max_salary+1):
            p_finale['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
            p_finale['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
            deltat=max(t,dt)
            p_finale['t']=t+deltat # palkka
            n3,q3=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
            
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            _,tvat=self.laske_marginaalit(q0,q1,t)
            _,osatvat=self.laske_marginaalit(q1,q3,deltat)
            palkka[t]=t
            netto[t]=n1
            effmarg[t]=marg['marginaaliveroprosentti']
            margyht[t]=marg['marginaali']
            margalv[t]=marg['alv']
                
            margasumistuki[t]=marg['asumistuki']
            margtoimeentulotuki[t]=marg['toimeentulotuki']
            margverot[t]=marg['verot']
            margelake[t]=marg['elake']
            margansiopvraha[t]=marg['ansiopvraha']
            margpvhoito[t]=marg['pvhoito']
            margperustulo[t]=marg['perustulo']
            margkotihoidontuki[t]=marg['kotihoidontuki']
            margopintotuki[t]=marg['opintotuki']
            
            elake[t]=q1['kokoelake_nettonetto']
            asumistuki[t]=q1['asumistuki_nettonetto']
            toimeentulotuki[t]=q1['toimeentulotuki']
            opintotuki[t]=q1['opintotuki_nettonetto']
            ansiopvraha[t]=q1['ansiopvraha_nettonetto']
            lapsilisa[t]=q1['lapsilisa_nettonetto']
            perustulo[t]=q1['perustulo_nettonetto']
            elatustuki[t]=q1['elatustuki_nettonetto']
            nettotulot[t]=tulot['tulotnetto']
            nettopalkka[t]=q1['palkkatulot_nettonetto']
            kotihoidontuki[t]=q1['kotihoidontuki_nettonetto']
            
            tva[t]=tvat['marginaaliveroprosentti']
            tva_yht[t]=tvat['marginaali']
            tva_alv[t]=tvat['alv']
                
            tva_asumistuki[t]=tvat['asumistuki']
            tva_kotihoidontuki[t]=tvat['kotihoidontuki']
            tva_toimeentulotuki[t]=tvat['toimeentulotuki']
            tva_verot[t]=tvat['verot']
            tva_elake[t]=tvat['elake']
            tva_perustulo[t]=tvat['perustulo']
            tva_ansiopvraha[t]=tvat['ansiopvraha']
            tva_opintotuki[t]=tvat['opintotuki']
            tva_pvhoito[t]=tvat['pvhoito']
            
            osatva[t]=osatvat['marginaaliveroprosentti']
            osatva_yht[t]=osatvat['marginaali']
            osatva_alv[t]=osatvat['alv']
                
            osatva_asumistuki[t]=osatvat['asumistuki']
            osatva_kotihoidontuki[t]=osatvat['kotihoidontuki']
            osatva_toimeentulotuki[t]=osatvat['toimeentulotuki']
            osatva_verot[t]=osatvat['verot']
            osatva_elake[t]=osatvat['elake']
            osatva_perustulo[t]=osatvat['perustulo']
            osatva_ansiopvraha[t]=osatvat['ansiopvraha']
            osatva_opintotuki[t]=osatvat['opintotuki']
            osatva_pvhoito[t]=osatvat['pvhoito']
                    
        return netto,palkka,nettopalkka,tva,osatva,effmarg,asumistuki,toimeentulotuki,ansiopvraha,nettotulot,lapsilisa,\
            elake,elatustuki,perustulo,opintotuki,kotihoidontuki,margasumistuki,margtoimeentulotuki,\
            margansiopvraha,margverot,margalv,margelake,margpvhoito,margyht,margperustulo,margopintotuki,\
            margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_ansiopvraha,tva_verot,\
            tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,osatva,osatva_asumistuki,\
            osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_ansiopvraha,osatva_verot,osatva_alv,osatva_elake,\
            osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht