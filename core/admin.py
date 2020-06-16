from django.contrib import admin
from import_export import resources, widgets
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from core.models import ParametriGraficof, NaborGraficov


class ParametriGraficofResource(resources.ModelResource):
    id = Field(attribute='id', column_name='id', )

    period = Field(attribute='period', column_name='n ˗ период', )
    kol_vo_tovara = Field(attribute='kol_vo_tovara', column_name='q ˗ количество товара', )
    price = Field(attribute='price', column_name='p ˗ цена', )
    udelnaia_stoimost_proizvodstva = Field(attribute='udelnaia_stoimost_proizvodstva',
                                           column_name='c ˗ удельная стоимость производства', )
    negativ_vozdeistvia_na_obshestvo = Field(attribute='negativ_vozdeistvia_na_obshestvo',
                                             column_name='d ˗ негативное воздействие', )
    obiem_zagriaz_veshestv = Field(attribute='obiem_zagriaz_veshestv',
                                   column_name='e ˗ объем загрязняющего вещества на ед. товара', )
    dolia_nackoplenia_zagr_vechesatv = Field(attribute='dolia_nackoplenia_zagr_vechesatv',
                                             column_name='δ ˗ доля накопленного загрязняющего вещества', )
    stavka_diskontirovania = Field(attribute='stavka_diskontirovania', column_name='r ˗ ставка дисконтирования', )
    nachalnii_moment_vremeni = Field(attribute='nachalnii_moment_vremeni', column_name='t ˗ начальный момент времени', )
    investizii_v_rashirenie_proizvodstva = Field(attribute='investizii_v_rashirenie_proizvodstva',
                                                 column_name='f ˗ инвестиции в расширение производства', )

    velichina_vigod = Field(attribute='velichina_vigod',
                                                 column_name='b3 ˗ величина выгод', )
    b4 = Field(attribute='b4',
                                                 column_name='b4 ˗ величина выгод', )

    graniza_privlekatelnosti = Field(attribute='graniza_privlekatelnosti',
                                                 column_name='beta - граница привлекательности инвестиций', )

    alpha = Field(attribute='alpha',
                                                 column_name='alpha - граница привлекательности инвестиций', )

    class Meta:
        model = ParametriGraficof
        import_id_fields = ('id',)
        fields = (
            'id',
            'nabor_graficov',
            'period',
            'kol_vo_tovara',
            'price',
            'udelnaia_stoimost_proizvodstva',
            'negativ_vozdeistvia_na_obshestvo',
            'obiem_zagriaz_veshestv',
            'dolia_nackoplenia_zagr_vechesatv',
            'stavka_diskontirovania',
            'nachalnii_moment_vremeni',
            'investizii_v_rashirenie_proizvodstva',
            'velichina_vigod',
            'graniza_privlekatelnosti',
            'b4',
            'alpha',
        )

        skip_unchanged = True
        report_skipped = False


class ParametriGraficofAdmin(ImportExportModelAdmin):
    resource_class = ParametriGraficofResource
    list_display = (
        'id',
        'nabor_graficov',
        'period',
        'kol_vo_tovara',
        'price',
        'udelnaia_stoimost_proizvodstva',
        'koefizent_discontirovania',
        'negativ_vozdeistvia_na_obshestvo',
        'obiem_zagriaz_veshestv',
        'dolia_nackoplenia_zagr_vechesatv',
        'stavka_diskontirovania',
        'nachalnii_moment_vremeni',
        'investizii_v_rashirenie_proizvodstva',
        'velichina_vigod',
        'graniza_privlekatelnosti',
        'alpha',
        'b4',
    )

    list_display_links = ('id',)
    list_filter = ('nabor_graficov',)

    list_editable = (
        'nabor_graficov',
        'period',
        'kol_vo_tovara',
        'price',
        'udelnaia_stoimost_proizvodstva',
        'negativ_vozdeistvia_na_obshestvo',
        'obiem_zagriaz_veshestv',
        'dolia_nackoplenia_zagr_vechesatv',
        'stavka_diskontirovania',
        'nachalnii_moment_vremeni',
        'investizii_v_rashirenie_proizvodstva',
    )

    ordering = ('period',)
    save_on_top = True
    save_as = True


admin.site.register(ParametriGraficof, ParametriGraficofAdmin)

class ParametriGraficofInline(admin.TabularInline):
    model = ParametriGraficof

class NaborGraficovAdmin(ImportExportModelAdmin):

    inlines = [
        ParametriGraficofInline,
    ]

    list_display = (
        'id',
        'name',
        'tip',
        'stroit_po',
        'skrit',
    )
    search_fields = ('name',)

    list_display_links = ('id',)

    list_editable = (
        'tip',
        'name',
        'stroit_po',
        'skrit',

    )

    ordering = ('name',)
    save_on_top = True
    save_as = True

admin.site.register(NaborGraficov, NaborGraficovAdmin)