from django.shortcuts import render, get_list_or_404
from django.http import HttpResponse
from django.views import generic
from muta.models import Work
from django.shortcuts import redirect
from oauthlib.oauth2 import WebApplicationClient
from muta.consts import SEASONS, SEASONS_JP, SEASONS_LIST, MAL_CONSTS
import datetime
import random, string, urllib, json

class IndexView(generic.TemplateView):
    template_name = 'muta/index.html'
    context_object_name = 'index'

    def get_context_data(self, **kwargs):
        ssn = []
        today = datetime.date.today()
        for y in reversed(range(2016, today.year+2)):
            for i in range(3, -1, -1):
                ssn.append({'name':str(y) + '年' + SEASONS_JP[i] + 'アニメ',
                    'year':y,
                    'season':SEASONS[i]})
        if today.month == 12:
            selected = str(today.year + 1) + '-' + SEASONS_LIST[today.month - 1]
        else:
            selected = str(today.year) + '-' + SEASONS_LIST[today.month - 1]

        
        context = {"seasons_list" : ssn, "this_season":selected}
        return context


class AnimeListView(generic.ListView):
    def animeList(request, season_year, season_name):
        return HttpResponse(request, 'muta/index.html', {})


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
        url = MAL_CONSTS['api_base_url'] + str(mal_anime_id) + '?fields=main_picture'
        url, headers, body = Oauth.oauth.add_token(url)
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as res:
            data = json.load(res)
        return data['main_picture']['medium']

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
            self.refresh_token()
            year = self.kwargs.get('season_year')
            season = self.kwargs.get('season_name').upper()
            self.get_and_save_images(year, season)
        context = self.get_context_data()
        return render(request, 'muta/updateImage.html', context)

    def get_context_data(self, **kwargs):
        ssn = []
        today = datetime.date.today()
        for y in reversed(range(2000, today.year+2)):
            for i in range(3, -1, -1):
                ssn.append({'name':str(y) + '年' + SEASONS_JP[i] + 'アニメ',
                    'year':y,
                    'season':SEASONS[i]})
        if today.month == 12:
            selected = str(today.year + 1) + '-' + SEASONS_LIST[today.month - 1]
        else:
            selected = str(today.year) + '-' + SEASONS_LIST[today.month - 1]
        context = {"seasons_list" : ssn, "this_season":selected}
        return context
    
    def get_and_save_images(self, year, season):
        work_list = Work.objects.filter(season_year=year, season_name=season)
        for w in work_list:
            if w.mal_anime_id is not None:
                w.image_url = self.get_anime_image(w.mal_anime_id)
                w.save()


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
