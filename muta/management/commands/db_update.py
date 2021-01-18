from django.core.management.base import BaseCommand
from muta.models import *
import datetime
import time
from muta.consts import SEASONS_LIST, ANNICT_QUERY
from muta.utils import run_annict_query, save_annict_response

class Command(BaseCommand):
    """main"""
    def handle(self, *args, **options):
        today = datetime.date.today()
        for i in range(4):
            this_season = SEASONS_LIST[]
            year_season = '\"' + "\",\"".join(list(map(lambda k:str(y) + "-" +  k, ssn))) + '\"'
            res = run_annict_query(ANNICT_QUERY % year_season)
            save_annict_response(res)