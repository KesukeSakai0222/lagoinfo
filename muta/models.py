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
    title = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100) 
    media = models.CharField(max_length=10)
    official_site_url = models.URLField(default='')
    official_site_url_en = models.URLField(default='')
    season_year = models.IntegerField(default=1900)
    season_name = models.CharField(max_length=6, choices=SEASONS, default='OTHER')
    image_url = models.URLField(default='')
    def __str__(self):
        return str(self.annict_id) + ':' + self.title


class Staff(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    annict_id = models.IntegerField()
    name = models.CharField(max_length=50, default='')
    name_en = models.CharField(max_length=50, default='')
    role_text = models.CharField(max_length=30, default='')
    sort_number = models.IntegerField(default=9999)

    def __str__(self):
        return str(self.annict_id) + ':' + self.name
    

class Cast(models.Model):
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    cast_annict_id = models.IntegerField()
    name = models.CharField(max_length=50, default='')
    name_en = models.CharField(max_length=50, default='')
    character_name = models.CharField(max_length=50, default='')
    character_name_en = models.CharField(max_length=50, default='')
    sort_number = models.IntegerField(default='')

    def __str__(self):
        return str(self.cast_annict_id) + ":" + self.name
    

class Channel(models.Model):
    id = models.IntegerField(primary_key=True, default='1')
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='')

    def __str__(self):
        return self.name
    