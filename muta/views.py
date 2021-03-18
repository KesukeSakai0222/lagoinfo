from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse, Http404, HttpResponseServerError
from django.views import generic
from django.views.decorators.csrf import requires_csrf_token
from muta.models import Work, Staff, Cast, Channel, ImageUpdateTran
from muta.utils import get_this_season, get_seasons
from django.shortcuts import redirect
from oauthlib.oauth2 import WebApplicationClient
from muta.consts import SEASONS, SEASONS_JP, SEASONS_LIST, MAL_CONSTS
import datetime
import time
import random, string, urllib, json

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        (year, season) = get_this_season()
        return redirect('/' + str(year) + '/' + season)

class AnimeListView(generic.TemplateView):
    template_name = 'muta/index.html'
    context_object_name = 'index'

    def get_context_data(self, **kwargs):
        ssn = get_seasons(datetime.date.today().year-2)
        if self.kwargs.get('season_year') is not None and self.kwargs.get('season_name') is not None:
            year = self.kwargs.get('season_year')
            season = self.kwargs.get('season_name')
        else:
            (year, season) = get_this_season()
        wrk = Work.objects.select_related('channel').prefetch_related('staff').prefetch_related('cast').filter(season_year=year, season_name=season.upper(), media__in=['TV', 'WEB'])
        context = {"seasons_list" : ssn, "season":SEASONS_JP[SEASONS.index(season)], "season_en":season, "year":year, "works" : wrk}
        return context

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        response = self.render_to_response(context)
        response['Access-Control-Allow-Origin'] = 'https://myanimelist.net/'
        return response

class AllSeasons(generic.TemplateView):
    template_name = 'muta/allSeasons.html'
    context_object_name = 'allSeasons'

    def get_context_data(self, **kwargs):
        ssn = get_seasons(2000)
        context = {"seasons_list" : ssn}
        return context


class Oauth(object):
    oauth = WebApplicationClient(MAL_CONSTS['client_id'], redirect_uri=MAL_CONSTS['redirect_url'])
    state = ''
    code_challenge = ''
    access_token = ''
    refresh_token = ''

    def make_random_str(self):
        Oauth.state = self.randomname(32)
        Oauth.code_challenge = self.randomname(128)

    def get_auth_url(self):
        url, headers, body = Oauth.oauth.prepare_authorization_request(
            MAL_CONSTS['authorize_url'],
            state=Oauth.state,
            code_challenge=Oauth.code_challenge)
        return url
    
    def get_token(self, cd:str):
        url, headers, body = Oauth.oauth.prepare_token_request(
            MAL_CONSTS['request_token_url'],
            client_secret=MAL_CONSTS['client_secret'],
            code=cd,
            code_verifier=Oauth.code_challenge)
        req = urllib.request.Request(url, body.encode(), headers=headers)
        with urllib.request.urlopen(req) as res:
            data = Oauth.oauth.parse_request_body_response(res.read())
        Oauth.access_token = data['access_token']
        Oauth.refersh_token = data['refresh_token']
    
    def refresh_token(self):
        url, headers, body = Oauth.oauth.prepare_refresh_token_request(MAL_CONSTS['request_token_url'], client_id=MAL_CONSTS['client_id'], client_secret=MAL_CONSTS['client_secret'])
        req = urllib.request.Request(url, body.encode(), headers=headers)
        with urllib.request.urlopen(req) as res:
            data = Oauth.oauth.parse_request_body_response(res.read())
        Oauth.access_token = data['access_token']
        Oauth.refersh_token = data['refresh_token']
    
    def get_anime_image(self, mal_anime_id):
        url = MAL_CONSTS['api_base_url'] + 'anime/' + str(mal_anime_id) + '?fields=main_picture'
        url, headers, body = Oauth.oauth.add_token(url)
        req = urllib.request.Request(url, headers=headers)
        try:
            res = urllib.request.urlopen(req)
            data = json.load(res)
            return data['main_picture']['large']
        except:
            return ''    

    def randomname(self, n):
        randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
        return ''.join(randlst)
        
    def has_access_token(self):
        return Oauth.access_token != ''


class MalLogin(generic.View, Oauth):
    def get(self, request, *args, **kwargs):
        self.make_random_str()
        return redirect(self.get_auth_url())


class Authorize(generic.View, Oauth):
    def get(self, request, *args, **kwargs):
        self.get_token(request.GET.get('code'))
        return redirect('/updateImage')


class UpdateImageView(generic.View, Oauth):
    context_object_name = 'updateImage'

    def get(self, request, *args, **kwargs):
        if not self.has_access_token():
            redirect('/login')
        if self.kwargs.get('season_year') is not None and self.kwargs.get('season_name') is not None:
            if (self.kwargs.get('season_name') not in SEASONS and self.kwargs.get('season_name') != 'all') or not 2000 <= self.kwargs.get('season_year') <= datetime.date.today().year + 2:
                raise Http404("validation error")
            self.refresh_token()
            year = self.kwargs.get('season_year')
            season = self.kwargs.get('season_name').upper()
            if season == 'ALL':
                self.get_and_save_all_images()
            else:
                self.get_and_save_images(year, season)
        context = self.get_context_data()
        return render(request, 'muta/updateImage.html', context)

    def get_context_data(self, **kwargs):
        ssn = get_seasons(2000)
        ssn.append({'name':'全件更新',
            'year':2000,
            'season':'all'
        })
        iut = ImageUpdateTran.objects.all()
        context = {"seasons_list" : ssn, 'update_tran': iut}
        return context
    
    def get_and_save_images(self, year, season):
        season_dict = {'OTHER':0, 'WINTER':1, 'SPRING':2, 'SUMMER':3, 'AUTUMN':4}
        work_list = Work.objects.filter(season_year=year, season_name=season)
        for w in work_list:
            if w.mal_anime_id is not None:
                w.image_url = self.get_anime_image(w.mal_anime_id)
                w.save()
        iut = ImageUpdateTran(id=year*10+season_dict[season], season_name=season, season_year=year, update_at=datetime.datetime.now())
        iut.save()

    def get_and_save_all_images(self):
        today = datetime.date.today()
        for y in reversed(range(2000, today.year+2)):
            for i in range(3, -1, -1):
                self.get_and_save_images(y, SEASONS[i].upper())
                time.sleep(10)


class PrivacyView(generic.TemplateView):
    template_name = 'muta/privacy.html'
    context_object_name = 'privacy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {}
        return context


class FormView(generic.TemplateView):
    template_name = 'muta/form.html'
    context_object_name = 'form'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {}
        return context


@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    import sys
    from django.views import debug
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)