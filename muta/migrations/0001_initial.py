# Generated by Django 3.1.3 on 2021-02-21 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpdateTran',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('season_year', models.IntegerField(default=1900)),
                ('season_name', models.CharField(choices=[('WINTER', '冬'), ('SPRING', '春'), ('SUMMER', '夏'), ('AUTUMN', '秋'), ('OTHER', 'その他')], default='OTHER', max_length=6)),
                ('update_at', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('annict_id', models.IntegerField(primary_key=True, serialize=False)),
                ('mal_anime_id', models.IntegerField(blank=True, null=True)),
                ('title', models.CharField(max_length=200)),
                ('title_en', models.CharField(max_length=200)),
                ('media', models.CharField(choices=[('MOVIE', '映画'), ('OTHER', 'その他'), ('OVA', 'OVA'), ('TV', 'TVシリーズ'), ('WEB', 'WEB')], max_length=10)),
                ('official_site_url', models.URLField(default='')),
                ('official_site_url_en', models.URLField(default='')),
                ('season_year', models.IntegerField(default=1900)),
                ('season_name', models.CharField(choices=[('WINTER', '冬'), ('SPRING', '春'), ('SUMMER', '夏'), ('AUTUMN', '秋'), ('OTHER', 'その他')], default='OTHER', max_length=6)),
                ('image_url', models.URLField(default='')),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('work', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='channel', serialize=False, to='muta.work')),
                ('b_ch_flag', models.BooleanField(default=False)),
                ('n_ch_flag', models.BooleanField(default=False)),
                ('d_anime_flag', models.BooleanField(default=False)),
                ('abema_flag', models.BooleanField(default=False)),
                ('amazon_prime_flag', models.BooleanField(default=False)),
                ('netflix_flag', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.CharField(default='', max_length=100, primary_key=True, serialize=False)),
                ('annict_id', models.IntegerField()),
                ('name', models.CharField(default='', max_length=500)),
                ('name_en', models.CharField(default='', max_length=500)),
                ('role_text', models.CharField(default='', max_length=30)),
                ('type_name', models.CharField(default='', max_length=30)),
                ('sort_number', models.IntegerField(default=9999)),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='muta.work')),
            ],
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.CharField(default='', max_length=100, primary_key=True, serialize=False)),
                ('annict_id', models.IntegerField()),
                ('name', models.CharField(default='', max_length=200)),
                ('name_en', models.CharField(default='', max_length=200)),
                ('character_name', models.CharField(default='', max_length=200)),
                ('character_name_en', models.CharField(default='', max_length=50)),
                ('sort_number', models.IntegerField(default='')),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cast', to='muta.work')),
            ],
        ),
    ]