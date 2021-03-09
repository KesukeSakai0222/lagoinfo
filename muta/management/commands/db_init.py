from django.core.management.base import BaseCommand
import datetime
import time
from tqdm import tqdm
from muta.consts import SEASONS
from muta.utils import run_annict_query, save_annict_response

class Command(BaseCommand):
    """main"""
    def handle(self, *args, **options):
        for y in tqdm(range(2000, datetime.date.today().year+2)):
            for ssn in SEASONS:
                year_season = '\"' + str(y) + "-" + ssn + '\"'
                res = run_annict_query(year_season)
                save_annict_response(res)
                time.sleep(5)
                
