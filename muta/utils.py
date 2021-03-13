import requests
import datetime
from muta.models import Work, Cast, Staff, Channel
from muta.consts import SEASONS_LIST, SEASONS_JP, SEASONS

ANNICT_BASE_URL:str = 'https://api.annict.com/graphql'
REQ_HEADER:dict = {'Authorization': 
            'bearer CZVYjeehMP8vRvbzwAk1Ct0s4VYglahtBOibYhb2HME'}
ANNICT_QUERY:str = """query {
    searchWorks(seasons:[%s]) {
        nodes {
            annictId
            malAnimeId
            title
            titleEn
            media
            officialSiteUrl
            officialSiteUrlEn
            seasonYear
            seasonName
            casts(orderBy:{field:SORT_NUMBER, direction:ASC}){
                nodes {
                    id
                    character{name nameEn}
                    person{annictId}
                    name
                    nameEn
                    sortNumber
                }
            }
            staffs(orderBy:{field:SORT_NUMBER, direction:ASC}){
                nodes {
                    id
                    resource {
                        __typename
                        ... on Organization{annictId}
                        ... on Person{annictId}
                    }
                    roleText
                    name
                    nameEn
                    sortNumber
                }
            }
            programs {
                nodes {
                    channel {name}
                }
            }
        }
    }
}
"""

def run_annict_query(param)->list:
        query = ANNICT_QUERY % param
        request = requests.post(ANNICT_BASE_URL, json={'query': query}, headers=REQ_HEADER)
        if request.status_code == 200 and 'data' in request.json():
            return request.json()['data']['searchWorks']['nodes']
        else:
            raise Exception("failed: {}".format(request.status_code))

def save_annict_response(res)->bool:
    for node in res:
        w, created = Work.objects.get_or_create(annict_id = node['annictId'])
        w.mal_anime_id = node['malAnimeId']
        w.title = node['title']
        w.title_en = node['titleEn']
        w.media = node['media']
        w.official_site_url = node['officialSiteUrl']
        w.official_site_url_en = node['officialSiteUrlEn']
        w.season_year = node['seasonYear']
        w.season_name = node['seasonName']
        w.save()
        for cast in node['casts']['nodes']:
            c = Cast(id = cast['id'],
                        work=w,
                        annict_id = cast['person']['annictId'],
                        name = cast['name'],
                        name_en = cast['nameEn'],
                        character_name = cast['character']['name'],
                        character_name_en = cast['character']['nameEn'],
                        sort_number = cast['sortNumber'])
            c.save()
        for staff in node['staffs']['nodes']:
            s = Staff(id = staff['id'],
                        work = w,
                        annict_id = staff['resource']['annictId'],
                        name = staff['name'],
                        name_en = staff['nameEn'],
                        role_text = staff['roleText'],
                        type_name = staff['resource']['__typename'],
                        sort_number = staff['sortNumber'])
            s.save()
        ch = Channel(work = w)
        channel_set = set()
        for channel in node['programs']['nodes']:
            channel_set.add(channel['channel']['name'])
        ch.d_anime_flag = 'dアニメストア' in channel_set
        ch.n_ch_flag = 'ニコニコチャンネル' in channel_set
        ch.b_ch_flag = 'バンダイチャンネル' in channel_set
        ch.amazon_prime_flag = 'Amazon プライム・ビデオ' in channel_set
        ch.abema_flag = 'ABEMAビデオ' in channel_set
        ch.netflix_flag = 'Netflix' in channel_set
        ch.save()
        
def get_this_season()->tuple:
    today = datetime.date.today()
    if today.month == 12:
        year = today.year + 1
    else:
        year = today.year
    season = SEASONS_LIST[today.month - 1]
    return (year, season)

def get_seasons(start_year)->list:
    ssn = []
    today = datetime.date.today()
    last_index = SEASONS.index(SEASONS_LIST[today.month - 1]) + 2
    for i in range(last_index, -1, -1):
        if i < 4:
            ssn.append({'name':str(today.year) + '年' + SEASONS_JP[i] + 'アニメ',
                'year':today.year,
                'season':SEASONS[i]})
        else:
            ssn.append({'name':str(today.year + 1) + '年' + SEASONS_JP[i%4] + 'アニメ',
                'year':today.year + 1,
                'season':SEASONS[i%4]})
    for y in reversed(range(start_year, today.year)):
        for i in range(3, -1, -1):
            ssn.append({'name':str(y) + '年' + SEASONS_JP[i] + 'アニメ',
                'year':y,
                'season':SEASONS[i]})
    return ssn
