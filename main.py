import os
import requests
import pandas as pd



api_key = os.getenv("API_KEY")
API_KEY ='b6a13693bb25fc01d346c527c6a24035'

SPORT = 'upcoming' # use the sport_key from the /sports endpoint below, or use 'upcoming' to see the next 8 games across all sports

REGIONS = 'uk' # uk | us | eu | au. Multiple can be specified if comma delimited

MARKETS = 'h2h' # h2h | spreads | totals. Multiple can be specified if comma delimited

ODDS_FORMAT = 'decimal' # decimal | american

DATE_FORMAT = 'iso' # iso | unix

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# First get a list of in-season sports
#   The sport 'key' from the response can be used to get odds in the next request
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

sports_response = requests.get(
    'https://api.the-odds-api.com/v4/sports', 
    params={
        'api_key': API_KEY
    }
)


if sports_response.status_code != 200:
    print(f'Failed to get sports: status_code {sports_response.status_code}, response body {sports_response.text}')

else:
    print('List of in season sports:', sports_response.json())



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# Now get a list of live & upcoming games for the sport you want, along with odds for different bookmakers
# This will deduct from the usage quota
# The usage quota cost = [number of markets specified] x [number of regions specified]
# For examples of usage quota costs, see https://the-odds-api.com/liveapi/guides/v4/#usage-quota-costs
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

odds_response = requests.get(
    f'https://api.the-odds-api.com/v4/sports/{SPORT}/odds',
    params={
        'api_key': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
        'dateFormat': DATE_FORMAT,
    }
)

if odds_response.status_code != 200:
    print(f'Failed to get odds: status_code {odds_response.status_code}, response body {odds_response.text}')

else:
    odds_json = odds_response.json()
    print('Number of events:', len(odds_json))
    print(odds_json)

    # Check the usage quota
    print('Remaining requests', odds_response.headers['x-requests-remaining'])
    print('Used requests', odds_response.headers['x-requests-used'])


# Organizando os dados recebidos da API com Pandas

# Dados da API
data = {
    'success': True,
    'data': [
        {
            'sport_key': 'soccer_epl',
            'teams': ['Arsenal', 'Everton'],
            'commence_time': 1610296800,
            'sites': [
                {
                    'site_key': 'betfair',
                    'site_nice': 'Betfair',
                    'last_update': 1610288638,
                    'odds': {
                        'h2h': [2.2, 3.3, 3.9]
                    }
                }
            ]
        },
        # ...
    ]
}

# Transformando os dados em um DataFrame
df = pd.json_normalize(data['data'], 'sites', ['teams', 'commence_time', 'sport_key', ], record_prefix='site_')
df['odd'] = df['odds.h2h'].apply(lambda x: x[0]) # Adicionando a odd de casa (home) como uma coluna
df['odd_away'] = df['odds.h2h'].apply(lambda x: x[1]) # Adicionando a odd de visitante (away) como uma coluna

# Visualizando o DataFrame
print(df)
