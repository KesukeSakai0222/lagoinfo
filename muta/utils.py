from muta.consts import ANNICT_BASE_URL, REQ_HEADER
import requests
from muta.models import Work, Cast, Staff

def run_annict_query(query)->list:
        request = requests.post(ANNICT_BASE_URL, json={'query': query}, headers=REQ_HEADER)
        if request.status_code == 200:
            return dict(request.json())['data']['searchWorks']['edges']
        else:
            raise Exception("failed: {}".format(request.status_code))


def save_annict_response(res)->bool:
    try:
        for node in res:
            nd = node['node']
            w = Work(annict_id = nd['annictId'],
                mal_anime_id = nd['malAnimeId'],
                title = nd['title'],
                title_en = nd['titleEn'],
                media = 'media',
                official_site_url = nd['officialSiteUrl'],
                official_site_url_en = nd['officialSiteUrlEn'],
                season_year = nd['seasonYear'],
                season_name = nd['seasonName'])
            w.save()
            for cast in nd['casts']['edges']:
                nd2 = cast['node']
                c = Cast(work=w,
                            cast_annict_id = nd2['person']['annictId'],
                            name = nd2['name'],
                            name_en = nd2['nameEn'],
                            character_name = nd2['character']['name'],
                            character_name_en = nd2['character']['nameEn'],
                            sort_number = nd2['sortNumber'])
                c.save()
            for staff in nd['staffs']['edges']:
                nd3 = staff['node']
                s = Staff(work = w,
                            annict_id = nd3['annictId'],
                            name = nd3['name'],
                            name_en = nd3['nameEn'],
                            role_text = nd3['roleText'],
                            sort_number = nd3['sortNumber'])
                s.save()
    except as e:
        print(e)
        return False
    else:
        return True