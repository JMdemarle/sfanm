# Generated by Django 3.0.5 on 2020-07-10 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apiculteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Capacite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datecapa', models.DateField(verbose_name='Date Capacité')),
                ('nreinesmax', models.IntegerField(default=0, verbose_name='capacité reines')),
                ('stationouverte', models.BooleanField(default=False)),
                ('depotpossible', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['datecapa'],
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nbreine', models.IntegerField(default=1, verbose_name='nombre reines')),
                ('datedepot', models.DateField(verbose_name='Date depot')),
                ('dateretrait', models.DateField(verbose_name='Date retrait')),
                ('nbtypfecond1', models.IntegerField(default=0, verbose_name='nombre apidea/Kieler ')),
                ('nbtypfecond2', models.IntegerField(default=0, verbose_name='nombre Miniplus      ')),
                ('nbtypfecond3', models.IntegerField(default=0, verbose_name='nombre Warre         ')),
                ('nbtypfecond4', models.IntegerField(default=0, verbose_name='nombre ruchette      ')),
                ('ordre', models.IntegerField(default=1, verbose_name='ordre')),
                ('enattente', models.BooleanField(default=False, verbose_name='En attente')),
                ('apiculteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='resasfanm.Apiculteur')),
            ],
        ),
        migrations.CreateModel(
            name='Presence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='capas', to='resasfanm.Capacite')),
                ('resa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resas', to='resasfanm.Reservation')),
            ],
        ),
    ]
