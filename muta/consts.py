# internal constants
SEASONS_LIST = ['winter', 'winter', 'spring', 'spring', 'spring', 'summer', 'summer'
                , 'summer', 'autumn', 'autumn', 'autumn', 'winter']
SEASONS:list = ['winter', 'spring', 'summer', 'autumn']
SEASONS_JP:list = ['冬', '春', '夏', '秋']

# MyAnimeList
MAL_BASE_URL = 'https://myanimelist.net/'
MAL_CLIENT_ID:str = '26dd13c6deba3850699fa1016b7680b2'
MAL_CONSTS = {
    'client_id'         :'132d8eff21cfc53b6d03aa757b1d33db',
    'client_secret'     :'ca679f7d43584d98b00906559a64cee28daaa707dff163d7c4f80c1ed3bade08',
    'request_token_url' :'https://myanimelist.net/v1/oauth2/token',
    'authorize_url'     :'https://myanimelist.net/v1/oauth2/authorize',
    'api_base_url'      :'https://api.myanimelist.net/v2/',
    'client_kwargs'     : {'code_challenge_method':'plain'},
    'redirect_url'      :'http://127.0.0.1:8000/auth/'
}