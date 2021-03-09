from django.core.management.base import BaseCommand
from muta.models import *
import datetime
import time
from muta.consts import SEASONS
from muta.utils import run_annict_query, save_annict_response

class Command(BaseCommand):
    """main"""
    def handle(self, *args, **options):
        # 今年と来年の作品を更新する
        year = datetime.date.today().year
        for ssn in SEASONS:
            year_season = '\"' + str(year) + '-' + ssn + '\",\"' + str(year+1) + '-' + ssn + '\"'
            res = run_annict_query(year_season)
            save_annict_response(res)