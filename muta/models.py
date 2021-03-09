from django.db import models

class Work(models.Model):
    SEASONS = ( ('WINTER', '冬'),
                ('SPRING', '春'),
                ('SUMMER', '夏'),
                ('AUTUMN', '秋'),
                ('OTHER', 'その他'))
    MEDIAS = (  ('MOVIE', '映画'),
                ('OTHER', 'その他'),
                ('OVA', 'OVA'),
                ('TV', 'TVシリーズ'),
                ('WEB', 'WEB'))
    annict_id = models.IntegerField(primary_key=True)
    mal_anime_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=200)
    title_en = models.CharField(max_length=200) 
    media = models.CharField(max_length=10, choices=MEDIAS)
    official_site_url = models.URLField(default='')
    official_site_url_en = models.URLField(default='')
    season_year = models.IntegerField(default=1900)
    season_name = models.CharField(max_length=6, choices=SEASONS, default='OTHER')
    image_url = models.URLField(default='')
    def __str__(self):
        return str(self.annict_id) + ':' + self.title


class Staff(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default='')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='staff')
    annict_id = models.IntegerField()
    name = models.CharField(max_length=500, default='')
    name_en = models.CharField(max_length=500, default='')
    role_text = models.CharField(max_length=30, default='')
    type_name = models.CharField(max_length=30, default='')
    sort_number = models.IntegerField(default=9999)

    def __str__(self):
        return str(self.annict_id) + ':' + self.name
    

class Cast(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default='')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='cast')
    annict_id = models.IntegerField()
    name = models.CharField(max_length=200, default='')
    name_en = models.CharField(max_length=200, default='')
    character_name = models.CharField(max_length=200, default='')
    character_name_en = models.CharField(max_length=50, default='')
    sort_number = models.IntegerField(default='')

    def __str__(self):
        return str(self.annict_id) + ":" + self.name
    

class Channel(models.Model):
    work = models.OneToOneField(Work, on_delete=models.CASCADE, primary_key=True, related_name='channel')
    b_ch_flag = models.BooleanField(default=False)
    n_ch_flag = models.BooleanField(default=False)
    d_anime_flag = models.BooleanField(default=False)
    abema_flag = models.BooleanField(default=False)
    amazon_prime_flag = models.BooleanField(default=False)
    netflix_flag = models.BooleanField(default=False)

    def __str__(self):
        return ' '.join(self.b_ch_flag, 
            self.n_ch_flag,
            self.d_anime_flag,
            self.abema_flag,
            self.amazon_prime_flag,
            self.netflix_flag)

class ImageUpdateTran(models.Model):
    SEASONS = ( ('WINTER', '冬'),
                ('SPRING', '春'),
                ('SUMMER', '夏'),
                ('AUTUMN', '秋'),
                ('OTHER', 'その他'))
    id = models.IntegerField(primary_key=True)
    season_year = models.IntegerField(default=1900)
    season_name = models.CharField(max_length=6, choices=SEASONS, default='OTHER')
    update_at = models.DateTimeField(null=True)
