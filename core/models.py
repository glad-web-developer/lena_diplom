import math

from django.db import models


class NaborGraficov(models.Model):
    class Meta:
        verbose_name = 'Набор графиков'
        verbose_name_plural = 'Набор графиков'

    name = models.CharField('Название', max_length=255)
    tip = models.CharField('Тип', max_length=255, choices=(
        ('B3 и Beta', 'B3 и Beta'),
        ('B4 и Alpha', 'B4 и Alpha'),
    ))

    stroit_po = models.CharField('Строить по', max_length=255, choices=(
        ('kol_vo_tovara', 'q'),
        ('price', 'p'),
        ('udelnaia_stoimost_proizvodstva', 'c'),
        ('koefizent_discontirovania', 'a(n,r)'),
        ('negativ_vozdeistvia_na_obshestvo', 'd'),
        ('obiem_zagriaz_veshestv', 'e'),
        ('dolia_nackoplenia_zagr_vechesatv', 'δ'),
        ('stavka_diskontirovania', 'r'),
        ('nachalnii_moment_vremeni', 't'),
        ('investizii_v_rashirenie_proizvodstva', 'f'),

    ), default='price')

    skrit = models.BooleanField('Скрыть', default=False)

    def __str__(self):
        return f'#{self.id} {self.name[0:30]}...'


class ParametriGraficof(models.Model):
    class Meta:
        verbose_name = 'Параметры графиков'
        verbose_name_plural = 'Параметры графиков'
        ordering = ['period']

    nabor_graficov = models.ForeignKey(NaborGraficov, verbose_name='Набор графиков', null=True, blank=False,
                                       on_delete=models.CASCADE, related_name='parametri')
    period = models.IntegerField('n ˗ период', )
    kol_vo_tovara = models.IntegerField('q ˗ количество товара', )
    price = models.FloatField('p ˗ цена', )
    udelnaia_stoimost_proizvodstva = models.FloatField('c ˗ удельная стоимость производства', )
    koefizent_discontirovania = models.FloatField('a(n,r) ˗ коэффициент дисконтирования', editable=False, null=True,
                                                  blank=True)
    negativ_vozdeistvia_na_obshestvo = models.FloatField(
        'd ˗ негативное воздействие на качество жизни общества (социальный ущерб) в каждый период времени пропорционально объёму находящихся в окружающей среде загрязнений;', )
    obiem_zagriaz_veshestv = models.FloatField('e ˗ объем загрязняющего вещества на единицу товара', )
    dolia_nackoplenia_zagr_vechesatv = models.FloatField('δ ˗ доля накопленного загрязняющего вещества', )
    stavka_diskontirovania = models.FloatField('r ˗ ставка дисконтирования', )
    nachalnii_moment_vremeni = models.FloatField('t ˗ начальный момент времени', )
    investizii_v_rashirenie_proizvodstva = models.FloatField('f ˗ инвестиции в расширение производства', )

    velichina_vigod = models.FloatField('b3 ˗ величина выгод', editable=False, null=True, blank=True)
    b4 = models.FloatField('b4 ˗ величина выгод', editable=False, null=True, blank=True)
    graniza_privlekatelnosti = models.FloatField('beta - граница привлекательности инвестиций', editable=False,
                                                 null=True, blank=True)
    alpha = models.FloatField('alpha - граница привлекательности инвестиций', editable=False, null=True, blank=True)

    def __str__(self):
        return f'id #{self.id}'

    def str_graniza_privlekatelnosti(self):
        return str(self.graniza_privlekatelnosti).replace(',', '.')

    def str_alpha(self):
        return str(self.get_alpha()).replace(',', '.')

    def get_velichina_vigod(self):
        koefizent_discontirovania = 0
        for i in range(self.period):
            koefizent_discontirovania += 1 / (1 + float(self.stavka_diskontirovania)) ** (i + 1)
        sum = 0
        try:
            for i in range(self.period):
                sum += (1 - (1 - float(self.dolia_nackoplenia_zagr_vechesatv)) ** (i + 1)) / (
                        float(self.dolia_nackoplenia_zagr_vechesatv) * (1 + float(self.stavka_diskontirovania)) ** (
                        i + 1)) - float(self.investizii_v_rashirenie_proizvodstva)
            velichina_vigod = float(self.kol_vo_tovara) * (
                    float(self.price) - float(self.udelnaia_stoimost_proizvodstva)) * koefizent_discontirovania - float(
                self.negativ_vozdeistvia_na_obshestvo) * float(self.kol_vo_tovara) * float(
                self.obiem_zagriaz_veshestv) * sum

            velichina_vigod = velichina_vigod
        except ZeroDivisionError:
            velichina_vigod = 0
        return velichina_vigod

    def get_koefizent_discontirovania(self):
        koefizent_discontirovania = 0
        for i in range(self.period):
            koefizent_discontirovania += 1 / (1 + float(self.stavka_diskontirovania)) ** (i + 1)
        return koefizent_discontirovania

    def get_graniza_privlekatelnosti(self):
        try:
            graniza_privlekatelnosti = (math.log(1 - (float(self.dolia_nackoplenia_zagr_vechesatv) * (
                    float(self.price) - float(self.udelnaia_stoimost_proizvodstva))) / float(
                self.negativ_vozdeistvia_na_obshestvo) * float(self.obiem_zagriaz_veshestv)) / math.log(
                1 - self.dolia_nackoplenia_zagr_vechesatv)) - 1
        except Exception:
            graniza_privlekatelnosti = 0
        return str(graniza_privlekatelnosti).replace(',', '.')

    def save(self, *args, **kwargs):
        # РАСЧИТАТЬ КОЭФ ДИСКОРТИРОВАНИЯ
        koefizent_discontirovania = 0
        for i in range(self.period):
            koefizent_discontirovania += 1 / (1 + float(self.stavka_diskontirovania)) ** (i + 1)

        self.koefizent_discontirovania = koefizent_discontirovania

        # РАСЧЕТ b3
        sum = 0
        try:
            for i in range(self.period):
                sum += (1 - (1 - float(self.dolia_nackoplenia_zagr_vechesatv)) ** (i + 1)) / (
                            float(self.dolia_nackoplenia_zagr_vechesatv) * (1 + float(self.stavka_diskontirovania)) ** (
                                i + 1)) - float(self.investizii_v_rashirenie_proizvodstva)
            velichina_vigod = float(self.kol_vo_tovara) * (
                    float(self.price) - float(self.udelnaia_stoimost_proizvodstva)) * koefizent_discontirovania - float(
                self.negativ_vozdeistvia_na_obshestvo) * float(self.kol_vo_tovara) * float(
                self.obiem_zagriaz_veshestv) * sum

            self.velichina_vigod = velichina_vigod
        except ZeroDivisionError:
            self.velichina_vigod = 0

        # РАСЧЕТ beta
        try:
            graniza_privlekatelnosti = (math.log(1 - (float(self.dolia_nackoplenia_zagr_vechesatv) * (
                    float(self.price) - float(self.udelnaia_stoimost_proizvodstva))) / float(
                self.negativ_vozdeistvia_na_obshestvo) * float(self.obiem_zagriaz_veshestv)) / math.log(
                1 - self.dolia_nackoplenia_zagr_vechesatv)) - 1
        except Exception:
            graniza_privlekatelnosti = 0

        self.graniza_privlekatelnosti = graniza_privlekatelnosti

        self.b4 = self.get_b4()
        self.alpha = self.get_alpha()

        super(ParametriGraficof, self).save(*args, **kwargs)

    def get_b4(self):
        try:
            do_znaka_minus = self.kol_vo_tovara * (self.price - self.udelnaia_stoimost_proizvodstva) * (
                    1 / self.stavka_diskontirovania) * (1 - (1 / ((1 + self.stavka_diskontirovania) ** self.period)))
            summator = 0
            for i in range(self.period):
                t = i + 1
                summator += t / ((1 + self.stavka_diskontirovania) ** t)

            posle_znaka_minus = self.negativ_vozdeistvia_na_obshestvo * self.kol_vo_tovara * self.obiem_zagriaz_veshestv * summator

            b4 = do_znaka_minus - posle_znaka_minus - self.investizii_v_rashirenie_proizvodstva
        except Exception:
            b4 = 0
        return (b4)

    def get_alpha(self):
        try:
            tmp = (self.price - self.udelnaia_stoimost_proizvodstva) / (
                        self.negativ_vozdeistvia_na_obshestvo * self.obiem_zagriaz_veshestv) - 1
        except Exception:
            tmp = 0
        return tmp

    def get_spisok_vsex_tchek(self):
       return f"""n = {self.period},q = {self.kol_vo_tovara}"""


    def get_str_dlua_postroenia(self):
        parametr = self.nabor_graficov.stroit_po
        znach =  self.__getattribute__(parametr)
        return f'{self.nabor_graficov.get_stroit_po_display()} = {znach}'