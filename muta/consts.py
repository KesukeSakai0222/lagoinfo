import os

# internal constants
SEASONS_LIST = ['winter', 'winter', 'spring', 'spring', 'spring', 'summer', 'summer'
                , 'summer', 'autumn', 'autumn', 'autumn', 'winter']
SEASONS:list = ['winter', 'spring', 'summer', 'autumn']
SEASONS_JP:list = ['冬', '春', '夏', '秋']

# MyAnimeList
MAL_BASE_URL = 'https://myanimelist.net/'
MAL_CONSTS = {
    'client_id'         :os.environ.get('MAL_CLIENT_ID'),
    'client_secret'     :os.environ.get('MAL_CLIENT_SECRET'),
    'request_token_url' :'https://myanimelist.net/v1/oauth2/token',
    'authorize_url'     :'https://myanimelist.net/v1/oauth2/authorize',
    'api_base_url'      :'https://api.myanimelist.net/v2/',
    'client_kwargs'     : {'code_challenge_method':'plain'},
    'redirect_url'      :'https://lagoinfo.herokuapp.com/auth/'
}