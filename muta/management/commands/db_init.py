from django.core.management.base import BaseCommand
from muta.models import *
import logging
import datetime
import time
from muta.consts import SEASONS_SEP, ANNICT_QUERY
from muta.utils import run_annict_query, save_annict_response

class Command(BaseCommand):
    """main"""
    def handle(self, *args, **options):
        for y in range(2000, datetime.date.today().year+2):
            for ssn in SEASONS_SEP:
                year_season = '\"' + "\",\"".join(list(map(lambda k:str(y) + "-" +  k, ssn))) + '\"'
                res = run_annict_query(ANNICT_QUERY % year_season)
                save_annict_response(res)

