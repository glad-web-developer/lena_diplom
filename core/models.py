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
    def __str__(self):
        return f'#{self.id} {self.name[0:30]}...'

class ParametriGraficof(models.Model):
    class Meta:
        verbose_name = 'Параметры графиков'
        verbose_name_plural = 'Параметры графиков'
    nabor_graficov = models.ForeignKey(NaborGraficov, verbose_name='Набор графиков', null=True, blank=False, on_delete=models.CASCADE, related_name='parametri')
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
    graniza_privlekatelnosti = models.FloatField('beta - граница привлекательности инвестиций', editable=False,
                                                 null=True, blank=True)

    def __str__(self):
        return f'id #{self.id}'

    def str_graniza_privlekatelnosti(self):
        return str(self.graniza_privlekatelnosti).replace(',','.')


    def get_velichina_vigod(self):
        koefizent_discontirovania = 0
        for i in range(self.period):
            koefizent_discontirovania += 1 / (1 + float(self.stavka_diskontirovania)) ** (i + 1)
        return koefizent_discontirovania

        sum = 0
        for i in range(self.period):
            sum += (1 - (1 - float(self.dolia_nackoplenia_zagr_vechesatv)) ** (i + 1)) / (
                        float(self.dolia_nackoplenia_zagr_vechesatv) * (1 + float(self.stavka_diskontirovania)) ** (
                            i + 1)) - float(self.investizii_v_rashirenie_proizvodstva)
        velichina_vigod = float(self.kol_vo_tovara) * (
                float(self.price) - float(self.udelnaia_stoimost_proizvodstva)) * koefizent_discontirovania - float(
            self.negativ_vozdeistvia_na_obshestvo) * float(self.kol_vo_tovara) * float(
            self.obiem_zagriaz_veshestv) * sum
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
        return str(graniza_privlekatelnosti).replace(',','.')

    def save(self, *args, **kwargs):
            # РАСЧИТАТЬ КОЭФ ДИСКОРТИРОВАНИЯ
            koefizent_discontirovania = 0
            for i in range(self.period):
                koefizent_discontirovania += 1 / (1 + float(self.stavka_diskontirovania)) ** (i + 1)

            self.koefizent_discontirovania = koefizent_discontirovania

            # РАСЧЕТ b3
            sum = 0
            for i in range(self.period):
                sum += (1-(1-float(self.dolia_nackoplenia_zagr_vechesatv))**(i+1))/(float(self.dolia_nackoplenia_zagr_vechesatv)*(1+float(self.stavka_diskontirovania))**(i+1)) - float(self.investizii_v_rashirenie_proizvodstva)
            velichina_vigod = float(self.kol_vo_tovara) * (
                        float(self.price) - float(self.udelnaia_stoimost_proizvodstva)) * koefizent_discontirovania - float(self.negativ_vozdeistvia_na_obshestvo) * float(self.kol_vo_tovara) * float(self.obiem_zagriaz_veshestv) * sum
            self.velichina_vigod = velichina_vigod

            # РАСЧЕТ beta
            try:
                graniza_privlekatelnosti = (math.log(1 - (float(self.dolia_nackoplenia_zagr_vechesatv) * (
                        float(self.price) - float(self.udelnaia_stoimost_proizvodstva))) / float(self.negativ_vozdeistvia_na_obshestvo) * float(self.obiem_zagriaz_veshestv)) / math.log(
                    1 - self.dolia_nackoplenia_zagr_vechesatv)) - 1
            except Exception:
                graniza_privlekatelnosti = 0
            self.graniza_privlekatelnosti = graniza_privlekatelnosti

            super(ParametriGraficof, self).save(*args, **kwargs)


        # def get_raschet(self):
        #     graniza_privlekatelnosti = (math.log(1 - (self.dolia_nackoplenia_zagr_vechesatv * (
        #                 self.price - self.udelnaia_stoimost_proizvodstva)) / self.negativ_vozdeistvia_na_obshestvo * self.obiem_zagriaz_veshestv) / math.log(
        #         1 - self.dolia_nackoplenia_zagr_vechesatv)) - 1
        #
        #     print(graniza_privlekatelnosti)
