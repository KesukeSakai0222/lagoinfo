# ANNICT ACCESS
ANNICT_BASE_URL:str = 'https://api.annict.com/graphql'
REQ_HEADER:dict = {'Authorization': 
            'bearer CZVYjeehMP8vRvbzwAk1Ct0s4VYglahtBOibYhb2HME'}
ANNICT_QUERY:str = """query {
    searchWorks(seasons:[%s]) {
        edges {
            node {
                annictId
                malAnimeId
                title
                titleEn
                media
                officialSiteUrl
                officialSiteUrlEn
                seasonYear
                seasonName
                casts(orderBy:{
                    field:SORT_NUMBER, direction:ASC}){
                        edges{
                            node{
                                character{name nameEn}
                                person{annictId}
                                name
                                nameEn
                                sortNumber}
                        }
                    }
                staffs(orderBy:{
                    field:SORT_NUMBER, direction:ASC}){
                        edges{
                            node{
                                annictId
                                roleText
                                name
                                nameEn
                                sortNumber}
                        }
                    }
            }
        }
    }
}
"""

# MyAnimeList
MAL_BASE_URL = 'https://myanimelist.net/'
MAL_CLIENT_ID:str = '26dd13c6deba3850699fa1016b7680b2'

# internal constants
SEASONS_LIST = ['winter', 'winter', 'spring', 'spring', 'spring', 'summer', 'summer'
                , 'summer', 'autumn', 'autumn', 'autumn', 'winter']
SEASONS:list = ['winter', 'spring', 'summer', 'autumn']
SEASONS_JP:list = ['冬', '春', '夏', '秋']

# Authlib parameter
MAL_CONSTS = {
    'client_id'         :'132d8eff21cfc53b6d03aa757b1d33db',
    'client_secret'     :'ca679f7d43584d98b00906559a64cee28daaa707dff163d7c4f80c1ed3bade08',
    'request_token_url' :'https://myanimelist.net/v1/oauth2/token',
    'authorize_url'     :'https://myanimelist.net/v1/oauth2/authorize',
    'api_base_url'      :'https://api.myanimelist.net/v0.20',
    'client_kwargs'     : {'code_challenge_method':'plain'},
    'redirect_url'      :'http://127.0.0.1:8000/auth/'
}