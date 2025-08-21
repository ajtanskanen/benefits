"""

    benefits
    
    implements social security and social insurance benefits in the Finnish social security schemes


"""

import numpy as np
from .parameters import perheparametrit, print_examples, tee_selite,get_n_perheet
from .labels import Labels
from .ben_utils import get_palette_EK,get_style_EK, compare_q_print, print_q
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as font_manager
import pandas as pd
import math
from celluloid import Camera
from tqdm import tqdm_notebook as tqdm

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
            elif key=='language' or key=='lang': # language for plotting
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

    def plot_tva_marg(self,tva,palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_tyotpvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,tva_alv,pal,
                ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=False,incl_alv=False,
                csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True,
                extraheader=None,counter=False,countertext='',min_y=None,max_y=None):
        if ax is None:
            figi,axs = plt.subplots()
        else:
            #figi=fig
            axs=ax
            
        #sns.set_theme(**csfont)
        axs.set_axisbelow(False)
        self.plot_marg_extra(axs,palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_tyotpvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,tva_alv,pal,
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

        if extraheader is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_extraheader(head_text,**csfont)
        if counter is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_counter(countertext,**csfont)
    
        if figname is not None:
            plt.savefig(figname+'_tva.png',dpi=200)
        if show:
            plt.show()    
    
    def plot_eff_marg(self,eff,palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
                ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=False,incl_alv=False,show_xlabel=True,show_ylabel=True,
                csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True,baseline_eff=None,
                extraheader=None,dodisplay=False,counter=False,countertext='',min_y=None,max_y=None):
        if ax is None:
            figi,axs = plt.subplots()
            noshow=False
        else:
            axs=ax
            noshow=True
        #sns.set_theme()
        axs.set_axisbelow(False)
        self.plot_marg_extra(axs,palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
            incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv)

        if dodisplay: 
            df = pd.DataFrame([margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv])
            display(df)

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

        if not noshow:
            if legend:
                #axs.legend(loc='upper right')
                handles, labels = axs.get_legend_handles_labels()
                lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
            if source is not None:
                self.add_source(source,**csfont)
            if header is not None:
                axs.set_title(head_text,**csfont)
            if extraheader is not None:
                #axs.title.set_text(head_text,csfont)
                self.add_extraheader(head_text,**csfont)
            if counter is not None:
                #axs.title.set_text(head_text,csfont)
                self.add_counter(countertext,**csfont)
    
            if figname is not None:
                plt.savefig(figname+'_eff.png')
            if show:
                plt.show()    
    
    def plot_osatva_marg(self,osatva,palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,osatva_alv,pal,
                ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=False,incl_alv=False,
                csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True,
                extraheader=None,counter=False,countertext='',
                min_y=None,max_y=None):
        if ax is None:
            figi,axs = plt.subplots()
        else:
            axs=ax
        axs.set_axisbelow(False)
        self.plot_marg_extra(axs,palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,osatva_alv,pal,
            incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv)

        axs.plot(osatva,'k',lw=3)
        axs.set_xlabel(self.labels['parttimewage'],**csfont)
        axs.set_ylabel('Ef. rajaveroaste osa-aikatyöstä kokoaikatyöhön (%)',**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_facecolor('white')
        axs.set_xlim(min_salary, max_salary)
        axs.set_ylim(0, 100)
        if min_y is not None:
            axs.set_xlim(min_y, max_y)
        if legend:
            #axs.legend(loc='upper right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='upper right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
        if extraheader is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_extraheader(head_text,**csfont)
        if counter is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_counter(countertext,**csfont)
    
        if figname is not None:
            plt.savefig(figname+'_osatva.png',dpi=200)
        if show:
            plt.show()                
    
    def plot_netto_income(self,netto,palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
            ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=True,
            csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True,
            extraheader=None,counter=False,countertext='',min_y=None,max_y=None):
    
        if ax is None:
            figi,axs = plt.subplots()
        else:
            #figi=fig
            axs=ax
        #sns.set_theme(**csfont)
        axs.set_axisbelow(False)

        if incl_perustulo:
            axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                    self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
        else:
            if incl_elake:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['elatustuki']),colors=pal)
            elif incl_opintotuki:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki']),colors=pal)
            elif incl_kotihoidontuki:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            else:
                axs.stackplot(palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki']),colors=pal)
    
        axs.plot(netto,'k',lw=3)
        axs.set_xlabel(self.labels['wage'],**csfont)
        axs.set_ylabel(self.labels['net income'],**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_facecolor('white')
        axs.set_xlim(min_salary, max_salary)
        if min_y is not None:
            axs.set_xlim(min_y, max_y)
        if legend:
            #axs.legend(loc='lower right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='lower right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
        if extraheader is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_extraheader(head_text,**csfont)
        if counter is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_counter(countertext,**csfont)
    
        if figname is not None:
            plt.savefig(figname+'_netto.png')
        if show:
            plt.show()

    def plot_julkinen_vaikutus(self,netto,palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
            ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=True,
            csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True,
            extraheader=None,counter=False,countertext='',
            min_y=None,max_y=None):
    
        if ax is None:
            figi,axs = plt.subplots()
        else:
            #figi=fig
            axs=ax
        #sns.set_theme(**csfont)
        axs.set_axisbelow(False)

        if incl_perustulo:
            axs.stackplot(palkka,palkka-nettopalkka,-asumistuki,-toimeentulotuki,-tyotpvraha,-kotihoidontuki,-lapsilisa,-elake,-opintotuki,-elatustuki,-perustulo,
                labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                    self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
        else:
            if incl_elake:
                axs.stackplot(palkka,palkka-nettopalkka,-asumistuki,-toimeentulotuki,-tyotpvraha,-kotihoidontuki,-lapsilisa,-elake,-opintotuki,-elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['elatustuki']),colors=pal)
            elif incl_opintotuki:
                axs.stackplot(palkka,palkka-nettopalkka,-asumistuki,-toimeentulotuki,-tyotpvraha,-kotihoidontuki,-lapsilisa,-elake,-opintotuki,-elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki']),colors=pal)
            elif incl_kotihoidontuki:
                axs.stackplot(palkka,palkka-nettopalkka,-asumistuki,-toimeentulotuki,-tyotpvraha,-kotihoidontuki,-lapsilisa,-elake,-opintotuki,-elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            else:
                axs.stackplot(palkka,palkka-nettopalkka,-asumistuki,-toimeentulotuki,-tyotpvraha,-kotihoidontuki,-lapsilisa,-elake,-opintotuki,-elatustuki,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki']),colors=pal)
    
        axs.plot(palkka-nettopalkka-asumistuki-toimeentulotuki-tyotpvraha-kotihoidontuki-lapsilisa-elake-opintotuki-elatustuki,'k',lw=3)
        axs.set_xlabel(self.labels['wage'],**csfont)
        axs.set_ylabel('Nettovaikutus julkiseen talouteen (e/kk)',**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_facecolor('white')
        axs.set_xlim(min_salary, max_salary)
        if min_y is not None:
            axs.set_xlim(min_y, max_y)

        if legend:
            #axs.legend(loc='lower right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='lower right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
        if extraheader is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_extraheader(head_text,**csfont)
        if counter is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_counter(countertext,**csfont)
    
        if figname is not None:
            plt.savefig(figname+'_netto.png')
        if show:
            plt.show()            
            
    def plot_brutto_income(self,brutto,palkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
            ax=None,incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=True,
            csfont=None,min_salary=None,max_salary=None,legend=True,source=None,header=None,head_text='',figname=None,show=True,
            extraheader=False,counter=False,countertext='',
            min_y=None,max_y=None):
    
        if ax is None:
            figi,axs = plt.subplots()
        else:
            #figi=fig
            axs=ax
        #sns.set_theme(**csfont)
        axs.set_axisbelow(False)

        if incl_perustulo:
            axs.stackplot(palkka,palkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                    self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
        else:
            if incl_elake:
                axs.stackplot(palkka,palkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            elif incl_opintotuki:
                axs.stackplot(palkka,palkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            elif incl_kotihoidontuki:
                axs.stackplot(palkka,palkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
            else:
                axs.stackplot(palkka,palkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,
                    labels=(self.labels['wage'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['kotihoidontuki'],self.labels['lapsilisa'],
                        self.labels['elake'],self.labels['opintotuki'],self.labels['elatustuki'],self.labels['perustulo']),colors=pal)
    
        axs.plot(netto,'k',lw=3)
        axs.set_xlabel(self.labels['wage'],**csfont)
        axs.set_ylabel(self.labels['brutto income'],**csfont)
        plt.yticks(**csfont)
        plt.xticks(**csfont)
        axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
        axs.set_facecolor('white')
        axs.set_xlim(min_salary, max_salary)
        if min_y is not None:
            axs.set_xlim(min_y, max_y)

        if legend:
            #axs.legend(loc='lower right')
            handles, labels = axs.get_legend_handles_labels()
            lgd=axs.legend(handles[::-1], labels[::-1], loc='lower right')
        if source is not None:
            self.add_source(source,**csfont)
        if header is not None:
            #axs.title.set_text(head_text,csfont)
            axs.set_title(head_text,**csfont)
        if extraheader is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_extraheader(head_text,**csfont)
        if counter is not None:
            #axs.title.set_text(head_text,csfont)
            self.add_counter(countertext,**csfont)
    
        if figname is not None:
            plt.savefig(figname+'_netto.png')
        if show:
            plt.show()    

    def plot_marg_extra(self,axs,palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
            incl_perustulo=False,incl_elake=False,incl_opintotuki=False,incl_kotihoidontuki=True,incl_alv=False,
            min_y=None,max_y=None):
    
        if not incl_alv:
            if incl_perustulo:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margopintotuki,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['opintotuki']),
                        colors=pal)
                elif incl_kotihoidontuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margpvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['paivahoito']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito']),
                        colors=pal)
        else:
            if incl_perustulo:
                axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,
                    labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['perustulo'],self.labels['alv']),
                    colors=pal)
            else:
                if incl_elake:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['elake'],self.labels['opintotuki'],self.labels['alv']),
                        colors=pal)
                elif incl_opintotuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margopintotuki,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['tyottomyysturva'],self.labels['paivahoito'],self.labels['opintotuki'],self.labels['alv']),
                        colors=pal)
                elif incl_kotihoidontuki:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margpvhoito,margalv,
                        labels=(self.labels['taxes'],self.labels['asumistuki'],self.labels['toimeentulotuki'],self.labels['paivahoito'],self.labels['alv']),
                        colors=pal)
                else:
                    axs.stackplot(palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margalv,
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
                    
    def verotaulukko(self,p=None,p0=None,min_salary=1_000,max_salary=200_000,step=1_000,
                dt=100,plottaa=True,header=True,source='Lähde: EK',head_text=None,
                incl_alv=False,include_tuet=False):

        tulos=pd.DataFrame(columns=('kokonaistulo, e/v','palkka, e/kk','vero [%]','marginaali','netto','brutto','tva'))

        if p is None:
            p,selite=self.get_default_parameter()
    
        if header:
            if head_text is None:
                head_text=tee_selite(p,p0=p0,short=False)
        else:
            head_text=None

        if not include_tuet:
            p['asumismenot_asumistuki']=0
            p['asumismenot_toimeentulotuki']=0
            p['ei_toimeentulotukea']=1

        kerroin=12

        netto,palkka,nettopalkka,tva,osatva,effmarg,asumistuki,toimeentulotuki,tyotpvraha,nettotulot,lapsilisa,\
        elake,elatustuki,perustulo,opintotuki,kotihoidontuki,margasumistuki,margtoimeentulotuki,\
        margtyotpvraha,margverot,margalv,margelake,margpvhoito,margyht,margperustulo,margopintotuki,\
        margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_tyotpvraha,tva_verot,\
        tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,osatva,osatva_asumistuki,\
        osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_verot,osatva_alv,osatva_elake,\
        osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht,\
        elake_brutto,asumistuki_brutto,toimeentulotuki_brutto,opintotuki_brutto,tyotpvraha_brutto,\
        lapsilisa_brutto,perustulo_brutto,elatustuki_brutto,bruttotulot,kotihoidontuki_brutto\
            =self.comp_all_margs(p,p0=p0,incl_alv=incl_alv,min_salary=min_salary/kerroin,max_salary=max_salary/kerroin,step=1000/kerroin,dt=dt,emtr_percent=True)       

        for k,pa in enumerate(palkka):
            tulos.loc[k,'kokonaistulo, e/v']=pa*kerroin
            tulos.loc[k,'palkka, e/kk']=pa
            tulos.loc[k,'netto']=netto[k]*kerroin
            tulos.loc[k,'brutto']=bruttotulot[k]*kerroin
            tulos.loc[k,'vero [%]']=(bruttotulot[k]-netto[k])/max(1e-9,bruttotulot[k])*100 #np.max(1e-6,bruttotulot[k]*100)
            tulos.loc[k,'tva']=tva[k]
            tulos.loc[k,'marginaali']=effmarg[k]

        pd.options.display.max_rows = 1000
        pd.set_option("display.precision", 2)
        display(tulos)

    def laske_ja_plottaa_marginaalit(self,p=None,p0=None,min_salary=0,max_salary=8000,
                basenetto=None,baseeff=None,basetva=None,basebrutto=None,plot_julkinen=True,dt=100,plottaa=True,
                otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=True,ret=False,
                plot_tva=True,plot_eff=True,plot_netto=True,plot_brutto=False,plot_osatva=True,
                figname=None,grayscale=False,
                incl_perustulo=False,incl_elake=True,fig=None,ax=None,incl_opintotuki=False,
                incl_alv=False,incl_kotihoidontuki=False,show=True,head_text=None,
                header=True,source='Lähde: EK',palette=None,palette_EK=False,
                baseline_eff=None,min_y=None,max_y=None,minmarg_y=None,maxmarg_y=None,
                square=False):

        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            #if ax is not None:
            #    ax.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
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

        netto,palkka,nettopalkka,tva,osatva,effmarg,asumistuki,toimeentulotuki,tyotpvraha,nettotulot,lapsilisa,\
            elake,elatustuki,perustulo,opintotuki,kotihoidontuki,margasumistuki,margtoimeentulotuki,\
            margtyotpvraha,margverot,margalv,margelake,margpvhoito,margyht,margperustulo,margopintotuki,\
            margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_tyotpvraha,tva_verot,\
            tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,osatva,osatva_asumistuki,\
            osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_verot,osatva_alv,osatva_elake,\
            osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht,\
            elake_brutto,asumistuki_brutto,toimeentulotuki_brutto,opintotuki_brutto,tyotpvraha_brutto,\
            lapsilisa_brutto,perustulo_brutto,elatustuki_brutto,bruttotulot,kotihoidontuki_brutto\
            =self.comp_all_margs(p,p0=p0,incl_alv=incl_alv,min_salary=min_salary,max_salary=max_salary,dt=dt)

        if plot_netto and plottaa:
            # ALV:ia ei plotata nettotuloissa
            #print(tyotpvraha[0])
            self.plot_netto_income(netto,palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show,
                min_y=min_y,max_y=max_y)

        if plot_julkinen and plottaa:
            # ALV:ia ei plotata nettotuloissa
            self.plot_julkinen_vaikutus(netto,palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,extraheader=header,header=None,head_text=head_text,figname=None,show=show,
                min_y=min_y,max_y=max_y)


        if plot_eff and plottaa:
            self.plot_eff_marg(effmarg,palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show,
                baseline_eff=baseline_eff,min_y=minmarg_y,max_y=maxmarg_y)

        if plot_brutto and plottaa:
            # ALV:ia ei plotata bruttotuloissa
            self.plot_brutto_income(bruttotulot,palkka,asumistuki_brutto,toimeentulotuki_brutto,tyotpvraha_brutto,kotihoidontuki_brutto,lapsilisa_brutto,elake_brutto,opintotuki_brutto,elatustuki_brutto,perustulo_brutto,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show,
                min_y=min_y,max_y=max_y)

        if plot_tva and plottaa:
            self.plot_tva_marg(tva,palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_tyotpvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,tva_alv,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show,
                min_y=minmarg_y,max_y=maxmarg_y)
    
        if plot_osatva and plottaa:
            self.plot_osatva_marg(osatva,palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,osatva_alv,pal,
                ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,header=header,head_text=head_text,figname=figname,show=show,
                min_y=minmarg_y,max_y=maxmarg_y)
       
        if ret: 
            return netto,effmarg,tva,osatva#,bruttotulot
            
    def laske_ja_animoi_marginaalit(self,p=None,p0=None,animate_p=True,
                imax=100,p_indeksi='vakiintunutpalkka',p_alku=2000,p_step=1000,
                p2_indeksi=None,p2_alku=2000,p2_step=1000,
                min_salary=0,max_salary=8000,stopplot=False,
                basenetto=None,baseeff=None,basetva=None,basebrutto=None,dt=100,plottaa=True,
                otsikko="Vaihtoehto",otsikkobase="Perustapaus",legend=False,
                plot_tva=True,plot_eff=False,plot_netto=False,plot_brutto=False,plot_osatva=False,
                figname=None,grayscale=False,incl_perustulo=False,incl_elake=True,fig=None,ax=None,incl_opintotuki=False,
                incl_alv=False,incl_kotihoidontuki=False,head_text=None,extra_text=None,
                header=True,source='Lähde: EK',palette=None,palette_EK=True,
                baseline_eff=None,interval=60,square=False,countertext='',endstop=10):

        if palette is not None:
            pal=sns.color_palette(palette, 12)
    
        if palette_EK:
            csfont,pal=self.setup_EK_fonts()
        else:
            csfont = {}

        if p is None:
            p,selite=self.get_default_parameter()
    
        show=False
        fig,ax = plt.subplots()
        if not stopplot:
            camera = Camera(fig)
            
        tqdm_e = tqdm(range(int(imax)+endstop), desc='Kuva', leave=True, unit="kuva")
            
        koot=list(np.arange(imax+1))
        koot.extend((np.zeros(endstop,dtype=int)+imax).tolist())

        for k in koot:
            tqdm_e.update(1)
            tqdm_e.set_description("Kuva " + str(k+1))
            if animate_p:
                p_0=p0.copy()
                p_2=p.copy()
                p_2[p_indeksi]=p_alku+p_step*k
                p_0[p_indeksi]=p_alku+p_step*k
                if p2_indeksi is not None:
                    p_2[p2_indeksi]=p2_alku+p2_step*k
                    p_0[p2_indeksi]=p2_alku+p2_step*k
            else:
                p_2=p
                p_0=p0.copy()
                if p0 is not None:
                    p_0[p_indeksi]=p_alku+p_step*k
                    if p2_indeksi is not None:
                        p_0[p2_indeksi]=p2_alku+p2_step*k    

            if header:
                if head_text is None:
                    head_text=tee_selite(p_2,p0=p_0,short=False)
            else:
                head_text=None

            extraheader=countertext+' '+str(p_0[p_indeksi])+' e/kk'

            netto,palkka,nettopalkka,tva,osatva,effmarg,asumistuki,toimeentulotuki,tyotpvraha,nettotulot,lapsilisa,\
                elake,elatustuki,perustulo,opintotuki,kotihoidontuki,margasumistuki,margtoimeentulotuki,\
                margtyotpvraha,margverot,margalv,margelake,margpvhoito,margyht,margperustulo,margopintotuki,\
                margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_tyotpvraha,tva_verot,\
                tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,osatva,osatva_asumistuki,\
                osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_verot,osatva_alv,osatva_elake,\
                osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht,\
                elake_brutto,asumistuki_brutto,toimeentulotuki_brutto,opintotuki_brutto,tyotpvraha_brutto,\
                lapsilisa_brutto,perustulo_brutto,elatustuki_brutto,bruttotulot,kotihoidontuki_brutto\
                =self.comp_all_margs(p_2,p0=p_0,incl_alv=incl_alv,min_salary=min_salary,max_salary=max_salary,dt=dt)
        
            if plot_netto and plottaa:
                # ALV:ia ei plotata nettotuloissa
                self.plot_netto_income(netto,palkka,nettopalkka,asumistuki,toimeentulotuki,tyotpvraha,kotihoidontuki,lapsilisa,elake,opintotuki,elatustuki,perustulo,pal,
                    ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,
                    csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,extraheader=header,header=None,head_text=head_text,figname=None,show=show,
                    counter=True,countertext=extraheader)

            if plot_eff and plottaa:
                self.plot_eff_marg(effmarg,palkka,margverot,margasumistuki,margtoimeentulotuki,margtyotpvraha,margpvhoito,margelake,margopintotuki,margperustulo,margalv,pal,
                    ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                    csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,extraheader=header,header=None,head_text=head_text,figname=None,show=show,
                    baseline_eff=baseline_eff,counter=True,countertext=extraheader)

            if plot_tva and plottaa:
                self.plot_tva_marg(tva,palkka,tva_verot,tva_asumistuki,tva_toimeentulotuki,tva_tyotpvraha,tva_pvhoito,tva_elake,tva_opintotuki,tva_perustulo,tva_alv,pal,
                    ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                    csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,extraheader=header,header=None,head_text=head_text,figname=None,show=show,
                    counter=True,countertext=extraheader)
    
            if plot_brutto and plottaa:
                # ALV:ia ei plotata bruttotuloissa
                self.plot_brutto_income(bruttotulot,palkka,asumistuki_brutto,toimeentulotuki_brutto,tyotpvraha_brutto,kotihoidontuki_brutto,lapsilisa_brutto,elake_brutto,opintotuki_brutto,elatustuki_brutto,perustulo_brutto,pal,
                    ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,
                    csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,extraheader=header,header=None,head_text=head_text,figname=None,show=show)

            if plot_osatva and plottaa:
                self.plot_osatva_marg(osatva,palkka,osatva_verot,osatva_asumistuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_pvhoito,osatva_elake,osatva_opintotuki,osatva_perustulo,osatva_alv,pal,
                    ax=ax,incl_perustulo=incl_perustulo,incl_elake=incl_elake,incl_opintotuki=incl_opintotuki,incl_kotihoidontuki=incl_kotihoidontuki,incl_alv=incl_alv,
                    csfont=csfont,min_salary=min_salary, max_salary=max_salary,legend=legend,source=source,extraheader=header,header=None,head_text=head_text,figname=None,show=show)

            camera.snap()

        animation = camera.animate(interval=interval, blit=True)
        if figname is not None:
            #animation.save(figname, writer = 'imagemagick')          
            animation.save(figname, writer = 'pillow')          
    
    def add_source(self,source,**csfont):
        plt.annotate(source, xy=(0.88,-0.1), xytext=(0,0), xycoords='axes fraction', textcoords='offset points', va='top', **csfont)

    def add_extraheader(self,source,**csfont):
        plt.annotate(source, xy=(-0.05,1.1), xytext=(0,0), xycoords='axes fraction', textcoords='offset points', va='top', **csfont)

    def add_counter(self,source,**csfont):
        plt.annotate(source, xy=(0.65,0.9), xytext=(0,0), xycoords='axes fraction', textcoords='offset points', va='top', **csfont)

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
            maxn=_n_perheet()
    
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

    def plot_insentives(self,netto,eff,tva,osa_tva,brutto=None,min_y=None,max_y=None,
            min_salary=0,max_salary=6000,step_salary=1,publication=False,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,basebrutto=None,
            basenetto2=None,baseeff2=None,basetva2=None,baseosatva2=None,basebrutto2=None,
            basenetto3=None,baseeff3=None,basetva3=None,baseosatva3=None,basebrutto3=None,
            dt=100,otsikko="Vaihtoehto",otsikkobase="Nykytila",otsikkobase2="",otsikkobase3="",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osatva=False,plot_brutto=False,
            figname=None,grayscale=False,source=None,header=None,palette_EK=True,ax=None):
    
        if grayscale:
            plt.style.use('grayscale')
            plt.rcParams['figure.facecolor'] = 'white' # Or any suitable colour...
            pal=sns.dark_palette("darkgray", 6, reverse=True)
            reverse=True
        else:
            pal=sns.color_palette()    
    
        if palette_EK and not publication:
            csfont,pal=self.setup_EK_fonts()
        else:
            csfont = {}
            linecolors ={}

        if publication:
            linestyle={'linewidth': 2}
            linestyle2={'linewidth': 2}
            linestyle3={'linewidth': 2,'linestyle': 'dashed'}
            linestyle4={'linewidth': 2,'linestyle': 'dashed'}
            legendstyle={'frameon': False}
        else:
            linestyle={'linewidth': 3}
            linestyle2={'linewidth': 3}
            linestyle3={'linewidth': 3,'linestyle': 'dashed'}
            linestyle4={'linewidth': 3,'linestyle': 'dashed'}
            legendstyle={'frameon': False}
    
        x=np.arange(min_salary,max_salary,step_salary)
        if plot_netto:
            if ax is not None:
                axs = ax
                noshow = True
            else:
                fig, axs = plt.subplots()
                noshow = False
            if basenetto is not None or basenetto2 is not None or basenetto3 is not None:
                axs.plot(x,netto,label=otsikko,**linestyle)
                if basenetto is not None:
                    axs.plot(x,basenetto,label=otsikkobase,**linestyle)
                if basenetto2 is not None:
                    axs.plot(x,basenetto2,label=otsikkobase2,**linestyle2)
                if basenetto3 is not None:
                    axs.plot(x,basenetto3,label=otsikkobase3,**linestyle3)
                if selite:
                    axs.legend(loc='upper left',**legendstyle)
            else:
                axs.plot(x,netto,**linestyle)
            axs.set_xlabel(self.labels['wage'],**csfont)
            axs.set_ylabel(self.labels['net income'],**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(0, max_salary)
            if min_y is not None:
                axs.set_ylim(min_y, max_y)
            if not noshow:
                if source is not None:
                    self.add_source(source,**csfont)
        
                if header is not None:
                    #axs.title.set_text(head_text,csfont)
                    axs.set_title(header,**csfont)
            
                if figname is not None:
                    #plt.savefig(figname+'_netto.eps', format='eps')
                    plt.savefig(figname+'_netto.png', format='png',dpi=300)
            
                plt.show()
            
        if plot_brutto:
            if ax is not None:
                axs = ax
                noshow = True
            else:
                fig, axs = plt.subplots()
                noshow = False
            if basebrutto is not None or basebrutto2 is not None:
                axs.plot(x,brutto,label=otsikko,**linestyle)
                if basebrutto is not None:
                    axs.plot(x,basebrutto,label=otsikkobase,**linestyle)
                if basebrutto2 is not None:
                    axs.plot(x,basebrutto2,label=otsikkobase2,**linestyle)
                if basebrutto3 is not None:
                    axs.plot(x,basebrutto3,label=otsikkobase3,**linestyle)
                if selite:
                    axs.legend(loc='upper right',**legendstyle)
            else:
                axs.plot(x,brutto,**linestyle)
            axs.set_xlabel(self.labels['wage'],**csfont)
            axs.set_ylabel(self.labels['brutto income'],**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(0, max_salary)
            if min_y is not None:
                axs.set_ylim(min_y, max_y)
            if not noshow:
                if source is not None:
                    self.add_source(source,**csfont)
        
                if header is not None:
                    #axs.title.set_text(head_text,csfont)
                    axs.set_title(header,**csfont)
            
                if figname is not None:
                    #plt.savefig(figname+'_brutto.eps', format='eps')
                    plt.savefig(figname+'_brutto.png', format='png',dpi=300)
            
                plt.show()            

        if plot_eff:
            if ax is not None:
                axs = ax
                noshow = True
            else:
                fig, axs = plt.subplots()
                noshow = False
            if baseeff is not None or baseeff2 is not None:
                if baseeff is not None:
                    axs.plot(x,baseeff,label=otsikkobase,**linestyle)
                if baseeff2 is not None:
                    axs.plot(x,baseeff2,label=otsikkobase2,**linestyle)
                if baseeff3 is not None:
                    axs.plot(x,baseeff3,label=otsikkobase3,**linestyle)
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
            if not noshow:
                if source is not None:
                    self.add_source(source,**csfont)
        
                if header is not None:
                    #axs.title.set_text(head_text,csfont)
                    axs.set_title(header,**csfont)
                if figname is not None:
                    plt.savefig(figname+'_effmarg.png', format='png')
                plt.show()

        if plot_tva:
            if ax is not None:
                axs = ax
                noshow = True
            else:
                fig, axs = plt.subplots()
                noshow = False
            if basetva is not None or basetva2 is not None:
                if basetva is not None:
                    axs.plot(x,basetva,label=otsikkobase,**linestyle)
                if basetva2 is not None:
                    axs.plot(x,basetva2,label=otsikkobase2,**linestyle)
                if basetva3 is not None:
                    axs.plot(x,basetva3,label=otsikkobase3,**linestyle)
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
            if not noshow:
                if source is not None:
                    self.add_source(source,**csfont)
    
                if header is not None:
                    #axs.title.set_text(head_text,csfont)
                    axs.set_title(header,**csfont)
                if figname is not None:
                    plt.savefig(figname+'_tva.png', format='png')
                plt.show()

        if plot_osatva:
            if ax is not None:
                axs = ax
                noshow = True
            else:
                fig, axs = plt.subplots()
                noshow = False
            if baseosatva is not None or baseosatva2 is not None or baseosatva3 is not None:
                if baseosatva is not None:
                    axs.plot(x,baseosatva,label=otsikkobase,**linestyle)
                if baseosatva2 is not None:
                    axs.plot(x,baseosatva2,label=otsikkobase2,**linestyle)
                if baseosatva3 is not None:
                    axs.plot(x,baseosatva3,label=otsikkobase3,**linestyle)
                axs.plot(x,osa_tva,label=otsikko,**linestyle)
                if selite:
                    axs.legend(loc='upper right',**legendstyle)
            else:
                axs.plot(x,osa_tva,**linestyle)
               
            axs.set_xlabel('Osatyön palkka (e/kk)',**csfont)
            axs.set_ylabel('Osatyöstä kokotyöhön siirtymisen eff.rajavero (%)',**csfont)
            axs.grid(True,color='black',fillstyle='top',lw=0.5,axis='y',alpha=1.0)
            axs.set_xlim(0, max_salary)
            if not noshow:
                if source is not None:
                    self.add_source(source,**csfont)
                if header is not None:
                    #axs.title.set_text(head_text,csfont)
                    axs.set_title(header,**csfont)
                if figname is not None:
                    plt.savefig(figname+'_osatva.png', format='png')
                plt.show()    
    
    def laske_ja_plottaa(self,p=None,p0=None,min_salary=0,max_salary=8000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,basebrutto=None,
            basenetto2=None,baseeff2=None,basetva2=None,baseosatva2=None,basebrutto2=None,
            basenetto3=None,baseeff3=None,basetva3=None,baseosatva3=None,basebrutto3=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",otsikkobase2="",otsikkobase3="",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_brutto=True,plot_osatva=True,min_y=None,max_y=None,
            incl_alv=False,figname=None,grayscale=None,source='Lähde: EK',header=True,short=False,ax=None,
            publication=False):
    
        netto,eff,tva,osa_tva,brutto=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,incl_alv=incl_alv,
                                                   max_salary=max_salary,step_salary=step_salary,dt=dt)
        
        if header:
            head_text=tee_selite(p,p0=p0,short=short)
        else:
            head_text=None
        
        if plottaa:
            self.plot_insentives(netto,eff,tva,osa_tva,brutto=brutto,min_salary=min_salary,max_salary=max_salary+1,
                step_salary=step_salary,min_y=min_y,max_y=max_y,ax=ax,publication=publication,
                basenetto=basenetto,baseeff=baseeff,basetva=basetva,baseosatva=baseosatva,basebrutto=basebrutto,
                dt=dt,otsikko=otsikko,otsikkobase=otsikkobase,selite=selite,
                plot_tva=plot_tva,plot_eff=plot_eff,plot_netto=plot_netto,plot_osatva=plot_osatva,plot_brutto=plot_brutto,
                figname=figname,grayscale=grayscale,source=source,header=head_text,
                basenetto2=basenetto2,baseeff2=baseeff2,basetva2=basetva2,baseosatva2=baseosatva2,basebrutto2=basebrutto2,otsikkobase2=otsikkobase2,
                basenetto3=basenetto3,baseeff3=baseeff3,basetva3=basetva3,baseosatva3=baseosatva3,basebrutto3=basebrutto3,otsikkobase3=otsikkobase3)

        return netto,eff,tva,osa_tva,brutto

    
    def plot(self,p=None,p0=None,min_salary=0,max_salary=6000,step_salary=1,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osatva=True,
            figname=None,grayscale=None,source='Lähde: EK',header=True,short=False):
    
        netto,eff,tva,osa_tva,brutto=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,
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
                plot_tva=plot_tva,plot_eff=plot_eff,plot_netto=plot_netto,plot_osatva=plot_osatva,
                figname=figname,grayscale=grayscale,source=source,header=head_text)

        return netto,eff,tva,osa_tva


    def comp_insentives(self,p=None,p0=None,min_salary=0,max_salary=6000,step_salary=1,dt=100,incl_alv=False,samapalkka=False):
        '''
        Laskee marginaalit ja nettotulot
        Toimii sekä ALV että ilman ALV
        '''
    
        n_salary=int((max_salary+step_salary-min_salary)/step_salary)
        netto=np.zeros(n_salary)
        brutto=np.zeros(n_salary)
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
            if samapalkka:
                p3['puoliso_tulot']=t # palkka
            n1,q1=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
            p3['t']=t+dt # palkka
            if samapalkka:
                p3['puoliso_tulot']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
            p3['t']=t+max(t,dt) # palkka
            if samapalkka:
                p3['puoliso_tulot']=t+max(t,dt) # palkka
            n3,q3=self.ben.laske_tulot_v3(p3,include_alv=incl_alv)
            netto[k]=n1
            brutto[k]=q1['brutto']
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
            return netto,eff,tva,osa_tva,brutto#,basenetto
        else:
            return netto,eff,tva,osa_tva,brutto
    
    def laske_tulot_sami(self,p):
        n0,q0=self.ben.laske_tulot_v3(p,include_alv=False)
        print('Työmarkkinatuki (brutto)',q0['tyotpvraha'])
        print('Työmarkkinatuki (netto)',q0['tyotpvraha_nettonetto'])
        print('Lapsilisät',q0['lapsilisa'])
        print('Elatustuki (Kela)',q0['elatustuki'])
        print('Toimeentulotuki (Kela)',q0['toimeentulotuki'])
        print('Päivähoitomaksut',q0['pvhoito'])
        print('Asumistuki (Kela)',q0['asumistuki'],q0['asumistuki_nettonetto'])
        print('Kokonaisnettotulot',n0)

    
    def comp_emtr(self,p0,p1,t,dt=1200,alku='',display=False,full=False):
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
        n2,q2=self.ben.laske_tulot_v3(p3,include_alv=False)
        netto=n1
        eff=(1-(n2-n1)/dt)*100
        if t>0:
            tva=(1-(n1-n0)/t)*100
            #osa_tva=(1-(n3-n1)/t)*100
        else:
            tva=np.nan
            #osa_tva=0
    
        if tva<0 or display:
            if alku=='':
                alku2='omat_'
            else:
                alku2='puoliso_'

            n1b=q1[alku2+'netto']
            n2b=q2[alku2+'netto']
            print('eff',eff,'tva',tva,'netto0',n0,'netto1',n1,'netto2',n2,'palkka',t,'dt',dt)
            print('n1',n1,n1b)
            print('n2',n2,n2b)
            #compare_q_print(q1,q2)
    
        #print(n0,n1,tva,t)

        if full:
            return netto,eff,tva,q0,q1
        else:
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
        n,eff,_,_,_=self.comp_insentives(p=p,min_salary=salary,max_salary=salary+1,step_salary=1,dt=100,incl_alv=incl_alv)
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
        marg['tyotpvraha']=(+q1['tyotpvraha_netto']-q2['tyotpvraha_netto'])*100/dt # verot mukana
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
        marg['etuudet']=marg['tyotpvraha']+marg['asumistuki']+marg['toimeentulotuki']+marg['kotihoidontuki']+marg['perustulo']
        marg['verot']=marg['palkkaverot'] # sisältää sivukulut
        marg['ansioverot']=marg['palkkaverot']+marg['elake'] # sisältää sivukulut
        marg['marginaali']=marg['pvhoito']+marg['etuudet']+marg['verot']+marg['elake']+marg['alv']
    
        # ja käteen jää
        tulot={}
        tulot['kateen1']=q1['netto']
        tulot['kateen2']=q2['netto']
        tulot['tulotnetto']=q1['netto']
        tulot['brutto1']=q1['brutto']
        tulot['brutto2']=q2['brutto']
    
        marg['marginaaliveroprosentti']=100-(tulot['kateen2']-tulot['kateen1'])*100/dt 
    
        return tulot,marg

    def laske_ja_selita(self,p=None,p0=None,min_salary=0,max_salary=3000,step_salary=1500,
            basenetto=None,baseeff=None,basetva=None,baseosatva=None,
            dt=100,plottaa=True,otsikko="Vaihtoehto",otsikkobase="Nykytila",selite=True,
            plot_tva=True,plot_eff=True,plot_netto=True,plot_osatva=True,incl_alv=False,
            figname=None,grayscale=None,source='Lähde: EK',header=True):
    
        head_text=tee_selite(p,short=False)

        netto,eff,tva,osa_tva,brutto=self.comp_insentives(p=p,p0=p0,min_salary=min_salary,incl_alv=incl_alv,
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

    def comp_all_margs(self,p,p0=None,incl_alv=False,min_salary=0,max_salary=6_000,dt=100,step=1,emtr_percent=False):
        '''
        Jaottelee marginaalit ja tulot eriin
        '''

        size=int(max_salary/step)+1

        netto=np.zeros(size)
        palkka=np.zeros(size)
        nettopalkka=np.zeros(size)
        tva=np.zeros(size)
        osatva=np.zeros(size)
        eff=np.zeros(size)
        asumistuki=np.zeros(size)
        asumistuki2=np.zeros(size)
        toimeentulotuki=np.zeros(size)
        tyotpvraha=np.zeros(size)
        nettotulot=np.zeros(size)
        lapsilisa=np.zeros(size)
        elake=np.zeros(size)    
        elatustuki=np.zeros(size)
        perustulo=np.zeros(size)
        opintotuki=np.zeros(size)
        kotihoidontuki=np.zeros(size)    
        asumistuki_brutto=np.zeros(size)
        toimeentulotuki2=np.zeros(size)
        toimeentulotuki_brutto=np.zeros(size)
        tyotpvraha_brutto=np.zeros(size)
        bruttotulot=np.zeros(size)
        lapsilisa_brutto=np.zeros(size)
        elake_brutto=np.zeros(size)    
        elatustuki_brutto=np.zeros(size)
        perustulo_brutto=np.zeros(size)
        opintotuki_brutto=np.zeros(size)
        kotihoidontuki_brutto=np.zeros(size)    
        effmarg=np.zeros(size)
        margasumistuki=np.zeros(size)
        margtoimeentulotuki=np.zeros(size)
        margtyotpvraha=np.zeros(size)
        margverot=np.zeros(size)    
        margalv=np.zeros(size)    
        margelake=np.zeros(size)    
        margpvhoito=np.zeros(size)
        margyht=np.zeros(size)
        margperustulo=np.zeros(size)    
        margopintotuki=np.zeros(size)    
        margkotihoidontuki=np.zeros(size)    
        tva=np.zeros(size)
        tva_asumistuki=np.zeros(size)
        tva_kotihoidontuki=np.zeros(size)    
        tva_toimeentulotuki=np.zeros(size)
        tva_tyotpvraha=np.zeros(size)
        tva_verot=np.zeros(size)
        tva_alv=np.zeros(size)    
        tva_elake=np.zeros(size)
        tva_pvhoito=np.zeros(size)
        tva_perustulo=np.zeros(size)
        tva_opintotuki=np.zeros(size)
        tva_yht=np.zeros(size)
        osatva=np.zeros(size)
        osatva_asumistuki=np.zeros(size)
        osatva_kotihoidontuki=np.zeros(size)    
        osatva_toimeentulotuki=np.zeros(size)
        osatva_tyotpvraha=np.zeros(size)
        osatva_verot=np.zeros(size)
        osatva_alv=np.zeros(size)    
        osatva_elake=np.zeros(size)
        osatva_pvhoito=np.zeros(size)
        osatva_perustulo=np.zeros(size)
        osatva_opintotuki=np.zeros(size)
        osatva_yht=np.zeros(size)

        if p0 is None:
            p_finale=p.copy()
            p_initial=p.copy()
        else:
            p_finale=p.copy()
            p_initial=p0.copy()
            plot_eff=False  

        p_initial['t']=0 # palkka
        n0,q0=self.ben.laske_tulot_v3(p_initial,include_alv=incl_alv)
        ind=0
        for t in np.arange(0,max_salary+1,step):
            if emtr_percent:
                dt=0.01 * t

            p_finale['t']=t # palkka
            n1,q1=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
            p_finale['t']=t+dt # palkka
            n2,q2=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
            deltat=max(t,dt)
            p_finale['t']=t+deltat # palkka
            n3,q3=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
    
            tulot,marg=self.laske_marginaalit(q1,q2,dt)
            _,osatvat=self.laske_marginaalit(q1,q3,deltat)
            #print(n1,n2)
            _,tvat=self.laske_marginaalit(q0,q1,t)
            palkka[ind]=t
            netto[ind]=n1

            #print(t,q1['tyotpvraha_nettonetto'],q2['tyotpvraha_nettonetto'],marg['tyotpvraha'],q1['kateen'],q2['kateen'],1-(q2['kateen']-q1['kateen'])/dt)

            effmarg[ind]=marg['marginaaliveroprosentti']
            margyht[ind]=marg['marginaali']
            margalv[ind]=marg['alv']
        
            margasumistuki[ind]=marg['asumistuki']
            margtoimeentulotuki[ind]=marg['toimeentulotuki']
            margverot[ind]=marg['verot']
            margelake[ind]=marg['elake']
            margtyotpvraha[ind]=marg['tyotpvraha']
            margpvhoito[ind]=marg['pvhoito']
            margperustulo[ind]=marg['perustulo']
            margkotihoidontuki[ind]=marg['kotihoidontuki']
            margopintotuki[ind]=marg['opintotuki']
    
            elake[ind]=q1['kokoelake_nettonetto']
            asumistuki[ind]=q1['asumistuki_nettonetto']
            asumistuki2[ind]=q2['asumistuki_nettonetto']
            toimeentulotuki[ind]=q1['toimeentulotuki']
            toimeentulotuki2[ind]=q2['toimeentulotuki']
            opintotuki[ind]=q1['opintotuki_nettonetto']
            tyotpvraha[ind]=q1['tyotpvraha_nettonetto']
            lapsilisa[ind]=q1['lapsilisa_nettonetto']
            perustulo[ind]=q1['perustulo_nettonetto']
            elatustuki[ind]=q1['elatustuki_nettonetto']
            nettotulot[ind]=tulot['kateen1']
            nettopalkka[ind]=q1['palkkatulot_nettonetto']
            kotihoidontuki[ind]=q1['kotihoidontuki_nettonetto']

            elake_brutto[ind]=q1['kokoelake']
            asumistuki_brutto[ind]=q1['asumistuki']
            toimeentulotuki_brutto[ind]=q1['toimeentulotuki']
            opintotuki_brutto[ind]=q1['opintotuki']
            tyotpvraha_brutto[ind]=q1['tyotpvraha']
            lapsilisa_brutto[ind]=q1['lapsilisa']
            perustulo_brutto[ind]=q1['perustulo']
            elatustuki_brutto[ind]=q1['elatustuki']
            bruttotulot[ind]=tulot['brutto1']
            kotihoidontuki_brutto[ind]=q1['kotihoidontuki']
    
            tva[ind]=tvat['marginaaliveroprosentti']
            tva_yht[ind]=tvat['marginaali']
            tva_alv[ind]=tvat['alv']
        
            tva_asumistuki[ind]=tvat['asumistuki']
            tva_kotihoidontuki[ind]=tvat['kotihoidontuki']
            tva_toimeentulotuki[ind]=tvat['toimeentulotuki']
            tva_verot[ind]=tvat['verot']
            tva_elake[ind]=tvat['elake']
            tva_perustulo[ind]=tvat['perustulo']
            tva_tyotpvraha[ind]=tvat['tyotpvraha']
            tva_opintotuki[ind]=tvat['opintotuki']
            tva_pvhoito[ind]=tvat['pvhoito']
    
            osatva[ind]=osatvat['marginaaliveroprosentti']
            osatva_yht[ind]=osatvat['marginaali']
            osatva_alv[ind]=osatvat['alv']
        
            osatva_asumistuki[ind]=osatvat['asumistuki']
            osatva_kotihoidontuki[ind]=osatvat['kotihoidontuki']
            osatva_toimeentulotuki[ind]=osatvat['toimeentulotuki']
            osatva_verot[ind]=osatvat['verot']
            osatva_elake[ind]=osatvat['elake']
            osatva_perustulo[ind]=osatvat['perustulo']
            osatva_tyotpvraha[ind]=osatvat['tyotpvraha']
            osatva_opintotuki[ind]=osatvat['opintotuki']
            osatva_pvhoito[ind]=osatvat['pvhoito']

            ind += 1

        #df = pd.DataFrame([toimeentulotuki,toimeentulotuki2,margtoimeentulotuki,asumistuki,asumistuki2])
        #display(df)
            
        return netto,palkka,nettopalkka,tva,osatva,effmarg,asumistuki,toimeentulotuki,tyotpvraha,nettotulot,lapsilisa,\
            elake,elatustuki,perustulo,opintotuki,kotihoidontuki,margasumistuki,margtoimeentulotuki,\
            margtyotpvraha,margverot,margalv,margelake,margpvhoito,margyht,margperustulo,margopintotuki,\
            margkotihoidontuki,tva,tva_asumistuki,tva_kotihoidontuki,tva_toimeentulotuki,tva_tyotpvraha,tva_verot,\
            tva_alv,tva_elake,tva_pvhoito,tva_perustulo,tva_opintotuki,tva_yht,osatva,osatva_asumistuki,\
            osatva_kotihoidontuki,osatva_toimeentulotuki,osatva_tyotpvraha,osatva_verot,osatva_alv,osatva_elake,\
            osatva_pvhoito,osatva_perustulo,osatva_opintotuki,osatva_yht,\
            elake_brutto,asumistuki_brutto,toimeentulotuki_brutto,opintotuki_brutto,tyotpvraha_brutto,\
            lapsilisa_brutto,perustulo_brutto,elatustuki_brutto,bruttotulot,kotihoidontuki_brutto          

    def comp_test_margs(self,p,p0=None,incl_alv=False,salary=0,dt=100,emtr_percent=True,pension=0,include_kansanelake=False,include_takuuelake=False):
        '''
        Jaottelee marginaalit ja tulot eriin
        '''

        if p0 is None:
            p_finale=p.copy()
            p_initial=p.copy()
        else:
            p_finale=p.copy()
            p_initial=p0.copy()

        if pension>0:
            p_initial['elakkeella']=1
            p_finale['elakkeella']=1
            p_initial['t']=0 # palkka
            p_initial['tyoelake']=0 
            p_initial['elake_maksussa']=0 
            n0,q0=self.ben.laske_tulot_v3(p_initial,include_alv=incl_alv,include_kansanelake=include_kansanelake,include_takuuelake=include_takuuelake)
            ind=0
            if emtr_percent:
                dt=0.01 * pension
            p_finale['t']=salary # palkka
            p_finale['tyoelake']=pension 
            p_finale['elake_maksussa']=p_finale['tyoelake']
            n1,q1=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv,include_kansanelake=include_kansanelake,include_takuuelake=include_takuuelake)
            p_finale['t']=salary 
            p_finale['tyoelake']=pension+dt 
            p_finale['elake_maksussa']=p_finale['tyoelake']
            n2,q2=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv,include_kansanelake=include_kansanelake,include_takuuelake=include_takuuelake)
            _,tvat=self.laske_marginaalit(q0,q1,pension)
        else:
            p_initial['t']=0 # palkka
            p_initial['tyoelake']=0 
            n0,q0=self.ben.laske_tulot_v3(p_initial,include_alv=incl_alv,include_kansanelake=include_kansanelake,include_takuuelake=include_takuuelake)
            ind=0
            if emtr_percent:
                dt=0.01 * salary
            p_finale['t']=salary # palkka
            n1,q1=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
            p_finale['t']=salary+dt # palkka
            n2,q2=self.ben.laske_tulot_v3(p_finale,include_alv=incl_alv)
            _,tvat=self.laske_marginaalit(q0,q1,salary)

        _,marg=self.laske_marginaalit(q1,q2,dt)
        eff=marg['marginaaliveroprosentti']
        tva=tvat['marginaaliveroprosentti']

        return eff,tva

    def compare_netto(self,marg_base,include_alv=False,min_salary=0,max_salary=6000,step_salary=1,dt=100,kuntaryhmä=1,min_y=None,max_y=None,
                        vuosi=2023,otsikko="Yleistuki",otsikkobase='baseline',plot_tva=True,plot_eff=True,plot_netto=True,plot_brutto=False,plot_osatva=True):

        for pn in range(1,73):
            p,selite = perheparametrit(perhetyyppi=pn,kuntaryhmä=kuntaryhmä,vuosi=vuosi,tulosta=False)
            basenetto,baseeff,basetva,baseosatva,basebrutto = \
                marg_base.comp_insentives(p=p,p0=p,min_salary=min_salary,incl_alv=include_alv,max_salary=max_salary,step_salary=step_salary,dt=dt)

            basenetto_YT,baseeff_YT,basetva_YT,baseosatva_YT,basebrutto_YT = \
                self.laske_ja_plottaa(p,basenetto=basenetto,baseeff=baseeff,basetva=basetva,baseosatva=baseosatva,
                                    basebrutto=basebrutto,incl_alv=include_alv,otsikko=otsikko,otsikkobase=otsikkobase,
                                    min_salary=min_salary,max_salary=max_salary,min_y=min_y,max_y=max_y,
                                    plot_tva=plot_tva,plot_eff=plot_eff,plot_netto=plot_netto,plot_brutto=plot_brutto,plot_osatva=plot_osatva)