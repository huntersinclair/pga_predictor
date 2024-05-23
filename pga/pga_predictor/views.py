import base64
import zlib
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .utils import number_to_words, lowercase_first, fill_tournament_player_stats
import json
import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import logging
import sys
import gzip
from io import BytesIO
import brotlicffi
import brotli
import zstandard as zstd
from django.utils.encoding import smart_str


requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST = 'ALL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
# logging.debug('A debug message!')
# logging.info('We processed %d records', len(processed_records))


# Create your views here.
def flatten_data(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def index(request):


    api_url = "https://orchestrator.pgatour.com/graphql"
    # reposn = {"data":null,"errors":[{"path":null,"locations":[{"line":2,"column":3,"sourceName":null}],"message":"Validation error of type MissingFieldArgument: Missing field argument id @ 'scorecardV2'"},{"path":null,"locations":[{"line":2,"column":15,"sourceName":null}],"message":"Validation error of type UnknownArgument: Unknown field argument tournamentId @ 'scorecardV2'"},{"path":null,"locations":[{"line":4,"column":5,"sourceName":null}],"message":"Validation error of type FieldUndefined: Field 'payload' in type 'LeaderboardDrawerV2' is undefined @ 'scorecardV2/payload'"}]}
    scorecard = {"operationName":"ScorecardCompressedV3","variables":{"tournamentId":"R2024480","playerId":"48081"},"query":"query ScorecardCompressedV3($tournamentId: ID!, $playerId: ID!) {\n  scorecardCompressedV3(tournamentId: $tournamentId, playerId: $playerId) {\n    id\n    payload\n  }\n}"}
    scorecardstats = {"operationName":"ScorecardStatsV3Compressed","variables":{"scorecardStatsV3CompressedId":"R2024480","playerId":"48081"},"query":"query ScorecardStatsV3Compressed($scorecardStatsV3CompressedId: ID!, $playerId: ID!) {\n  scorecardStatsV3Compressed(\n    id: $scorecardStatsV3CompressedId\n    playerId: $playerId\n  ) {\n    id\n    payload\n  }\n}"}
    graphql = {"operationName":"ScorecardV2","variables":{"tournamentId":"R2024480","playerId":"48081"},"query":"query ScorecardV2($tournamentId: ID!, $playerId: ID!) {\n  scorecardV2(tournamentId: $tournamentId, playerId: $playerId) {\n    id\n    payload\n  }\n}"}
    graphql2 = {"operationName":"LeaderboardDrawerV2","variables":{"id":"R2024480","playerId":"48081"},"query":"query LeaderboardDrawerV2($id: ID!, $playerId: ID!) {\n  scorecardV2(id: $id, playerId: $playerId) {\n    id\n    roundScores\n  }\n}"}
    # Define the introspection query for the specific type
    introspection_query = {
        "query": """
        {
          __type(name: "LeaderboardDrawerV2") {
            name
            kind
            fields {
              name
              type {
                name
                kind
                ofType {
                  name
                  kind
                }
              }
              args {
                name
                type {
                  name
                  kind
                  ofType {
                    name
                    kind
                  }
                }
              }
            }
          }
        }
        """
    }

    api_req = requests.post(api_url, json = scorecardstats, headers={
                                'Accept':'*/*',
                                'Accept-Encoding':'gzip, deflate, br, zstd',
                                'Accept-Language':'en-US,en;q=0.9',
                                'Content-Type':'application/json',
                                'Content-Length':'282',
                                'Origin':'https://www.pgatour.com',
                                'Referer':'https://www.pgatour.com',
                                'Cache-Control':'max-age=0',
                                'Priority':'u=0, i',
                                'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                                'Sec-Ch-Ua-Mobile':'?0',
                                'Sec-ch-ua-platform':'"macOS"',
                                'Sec-Fetch-Dest':'empty',
                                'Sec-Fetch-Mode':'cors',
                                'Sec-Fetch-Site':'same-site',
                                'X-Amz-User-Agent':'aws-amplify/3.0.7',
                                'X-Api-Key':'da2-gsrx5bibzbb4njvhl7t37wqyl4',
                                'X-Pgat-Platform':'web',
                                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})

    #                                'Cookie':'gig_canary=false; _scor_uid=54722d6167af4ecb85108f8ccc0b9c0d; _gcl_au=1.1.235794155.1715895016; _ga=GA1.1.1788951515.1715895016; AMP_MKTG_38168c7a64=JTdCJTdE; permutive-id=11863a7f-29b8-4d8f-a636-415ed66e2264; _fbp=fb.1.1715895016662.415746191; gig_bootstrap_3_IscKmAoYcuwP8zpTnatC3hXBUm8rPuI-Hg_cZJ-jL-M7LgqCkxmwe-ps1Qy7PoWd=_gigya_ver4; __qca=P0-797204401-1715895016529; _sharedid=12192f91-f28b-4a77-b834-fe589f51cab1; _sharedid_cst=VyxHLMwsHQ%3D%3D; _lr_env_src_ats=false; idl_env=Aj2Ornraj6Z021bdnx1YvnSaolChq9OC0pje7NQVXKWonp_QXz4RVtSb0K-Vjv5UhkdGIhj9fqGhcCEsDCNqvBW6Wsrkt5xl8_MjS1Mw; idl_env_cst=VyxHLMwsHQ%3D%3D; idl_env_last=Thu%2C%2016%20May%202024%2021%3A30%3A17%20GMT; hb_insticator_uid=ab187fe0-af5a-4559-9016-e956e60ea830; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3A_b2hjjmGwMePakCWIMU2i8vpjrxbQ_xw0EMtffIh9Q5RaV98BGPGqv74Wkx13cDoalUsy5DHyR3I6k-Tu9UhPBaVGiQoBuVK--geGIcde1eEPblXe_L0uWjDc3CE4G1f%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; _lr_geo_location_state=TX; _lr_geo_location=US; gig_canary_ver=15936-3-28598280; OptanonConsent=isGpcEnabled=0&datestamp=Thu+May+16+2024+17%3A07%3A52+GMT-0500+(Central+Daylight+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=10cbad2c-fc99-4011-aff6-854bb97f6b55&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&AwaitingReconsent=false; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.pgatour.com/stats%22%2C%22sref%22:%22https://www.pgatour.com/stats/detail/02567%22%2C%22sts%22:1715969839356%2C%22slts%22:1715895015714}; _parsely_visitor={%22id%22:%22pid=c3b8e517-62a9-425f-abe1-151032275e62%22%2C%22session_count%22:2%2C%22last_session_ts%22:1715969839356}; AMP_38168c7a64=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIxZDc5ZGVhZi03YjQ3LTQxNWYtYmE4MC03OGI1MjM0ZmQ5YzIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE1OTY5ODM5NTg0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNTk2OTgzOTcxNSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzIlN0Q=; _awl=2.1715969840.5-9571efc268b02fb32e84fca80aca39f3-6763652d75732d63656e7472616c31-0; _ga_D4BWM9D122=GS1.1.1715969839.2.1.1715969840.59.0.0; __gads=ID=d9f44ffdbd0e559b:T=1715895018:RT=1715969840:S=ALNI_MbfHrbLrENHfo6TD_69f3fHlIHiHQ; __gpi=UID=00000e1d207eb34f:T=1715895018:RT=1715969840:S=ALNI_MZmR99_uFA0FsXhh6E8nS_TkEAcMg; __eoi=ID=ad04eeb1774539d7:T=1715895018:RT=1715969840:S=AA-AfjZD7c24IObWW3JfZzy_TYV6',
    
    # Check for a successful response
    if api_req.status_code == 200:
        # Decompress the response content if it's gzipped
        # Handle gzip compression
        if api_req.headers.get('Content-Encoding') == 'gzip':
            buf = BytesIO(api_req.content)
            with gzip.GzipFile(fileobj=buf) as f:
                decompressed_data = f.read()
            logging.debug("gzip encoding")
        # Handle deflate compression
        elif api_req.headers.get('Content-Encoding') == 'deflate':
            try:
                decompressed_data = zlib.decompress(api_req.content)
            except zlib.error:
                # Try with raw deflate (no headers)
                decompressed_data = zlib.decompress(api_req.content, -zlib.MAX_WBITS)
            logging.debug("deflate encoding")
        # Handle Brotli compression
        elif api_req.headers.get('Content-Encoding') == 'br':
            #decompressed_data = brotlicffi.decompress(api_req.content)
            # Alternatively, you can do incremental decompression.

            # decompressed_data = brotli.decompress(api_req.content) # This is getting done automatically by requests
            decompressed_data = api_req.content

            logging.debug("BR encoding")
        # Handle Zstandard compression
        elif api_req.headers.get('Content-Encoding') == 'zstd':
            dctx = zstd.ZstdDecompressor()
            decompressed_data = dctx.decompress(api_req.content)
            logging.debug("Zstandard encoding")
        else:
            decompressed_data = api_req.content
            logging.debug("fall through to no encoding header")

        logging.debug(decompressed_data)

        # Attempt to decode the decompressed data as JSON
        decoded_data = decompressed_data.decode('utf-8')
        logging.debug(decoded_data)
        json_data = json.loads(decoded_data)
        logging.debug(json_data)
        
        # Extract and decode the payload
        # payload_base64 = json_data['data']['scorecardCompressedV3']['payload']
        payload_base64 = json_data['data']['scorecardStatsV3Compressed']['payload']
        payload_compressed = base64.b64decode(payload_base64)

        # Decompress the payload
        payload_decompressed = gzip.decompress(payload_compressed)
        payload_json = json.loads(payload_decompressed.decode('utf-8'))
        logging.debug(payload_json)

        csv_file = 'csvs/player_stats2.csv'
        csv_obj = open(csv_file, 'w+')
        csv_writer = csv.writer(csv_obj)
        flat_data = flatten_data(payload_json)
        header = flat_data.keys()
        csv_writer.writerow(header)
        csv_writer.writerow(flat_data.values())
        csv_obj.close()

        # # Attempt to decode the decompressed data as JSON
        # try:
        #     decoded_data = decompressed_data.decode('utf-8')
        #     logging.debug(decoded_data)
        #     data = json.loads(decoded_data)
        #     logging.debug(data)
        # except UnicodeDecodeError:
        #     logging.debug("Failed to decode the response content as utf-8.")
        #     logging.debug(decompressed_data)
        #     logging.debug(decompressed_data.hex())  # Print hex representation
        # except json.JSONDecodeError:
        #     logging.debug("Failed to parse the response content as JSON.")
        #     logging.debug(decompressed_data)
        #     logging.debug(decompressed_data.hex())  # Print hex representation
    else:
        # Print the error message
        logging.debug(f"Query failed with status code {api_req.status_code}: {api_req.text}")

    
    #logging.debug('A debug API!')
    #logging.debug(api_req.text)
    return HttpResponse("Hello, world. You're at the predictor index.")


    ################# BUILDING STAT TYPE LIST ############################
    #load page in to soup and copy html code
    #page = 'https://www.pgatour.com/stats'
    #page = 'https://www.pgatour.com/leaderboard'
    page = "https://www.pgatour.com/tournaments/2024/wells-fargo-championship/R2024480"
    req = requests.get(page, headers={
                                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                'Accept-Encoding':'gzip, deflate, br, zstd',
                                'Accept-Language':'en-US,en;q=0.9',
                                'Cache-Control':'max-age=0',
                                'Priority':'u=0, i',
                                'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                                'Sec-Ch-Ua-Mobile':'?0',
                                'Sec-ch-ua-platform':'"macOS"',
                                'Sec-Fetch-Dest':'document',
                                'Sec-Fetch-Mode':'navigate',
                                'Sec-Fetch-Site':'same-origin',
                                'Sec-Fetch-User':'?1',
                                'Connection':'keep-alive',
                                'Pragma':'no-cache',
                                'Upgrade-Insecure-Requests':'1',
                                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})

    #                                'Cookie':'gig_canary=false; _scor_uid=54722d6167af4ecb85108f8ccc0b9c0d; _gcl_au=1.1.235794155.1715895016; _ga=GA1.1.1788951515.1715895016; AMP_MKTG_38168c7a64=JTdCJTdE; permutive-id=11863a7f-29b8-4d8f-a636-415ed66e2264; _fbp=fb.1.1715895016662.415746191; gig_bootstrap_3_IscKmAoYcuwP8zpTnatC3hXBUm8rPuI-Hg_cZJ-jL-M7LgqCkxmwe-ps1Qy7PoWd=_gigya_ver4; __qca=P0-797204401-1715895016529; _sharedid=12192f91-f28b-4a77-b834-fe589f51cab1; _sharedid_cst=VyxHLMwsHQ%3D%3D; _lr_env_src_ats=false; idl_env=Aj2Ornraj6Z021bdnx1YvnSaolChq9OC0pje7NQVXKWonp_QXz4RVtSb0K-Vjv5UhkdGIhj9fqGhcCEsDCNqvBW6Wsrkt5xl8_MjS1Mw; idl_env_cst=VyxHLMwsHQ%3D%3D; idl_env_last=Thu%2C%2016%20May%202024%2021%3A30%3A17%20GMT; hb_insticator_uid=ab187fe0-af5a-4559-9016-e956e60ea830; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3A_b2hjjmGwMePakCWIMU2i8vpjrxbQ_xw0EMtffIh9Q5RaV98BGPGqv74Wkx13cDoalUsy5DHyR3I6k-Tu9UhPBaVGiQoBuVK--geGIcde1eEPblXe_L0uWjDc3CE4G1f%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; _lr_geo_location_state=TX; _lr_geo_location=US; gig_canary_ver=15936-3-28598280; OptanonConsent=isGpcEnabled=0&datestamp=Thu+May+16+2024+17%3A07%3A52+GMT-0500+(Central+Daylight+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=10cbad2c-fc99-4011-aff6-854bb97f6b55&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&AwaitingReconsent=false; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.pgatour.com/stats%22%2C%22sref%22:%22https://www.pgatour.com/stats/detail/02567%22%2C%22sts%22:1715969839356%2C%22slts%22:1715895015714}; _parsely_visitor={%22id%22:%22pid=c3b8e517-62a9-425f-abe1-151032275e62%22%2C%22session_count%22:2%2C%22last_session_ts%22:1715969839356}; AMP_38168c7a64=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIxZDc5ZGVhZi03YjQ3LTQxNWYtYmE4MC03OGI1MjM0ZmQ5YzIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE1OTY5ODM5NTg0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNTk2OTgzOTcxNSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzIlN0Q=; _awl=2.1715969840.5-9571efc268b02fb32e84fca80aca39f3-6763652d75732d63656e7472616c31-0; _ga_D4BWM9D122=GS1.1.1715969839.2.1.1715969840.59.0.0; __gads=ID=d9f44ffdbd0e559b:T=1715895018:RT=1715969840:S=ALNI_MbfHrbLrENHfo6TD_69f3fHlIHiHQ; __gpi=UID=00000e1d207eb34f:T=1715895018:RT=1715969840:S=ALNI_MZmR99_uFA0FsXhh6E8nS_TkEAcMg; __eoi=ID=ad04eeb1774539d7:T=1715895018:RT=1715969840:S=AA-AfjZD7c24IObWW3JfZzy_TYV6',

    #req = requests.get(page)
    soup = bs(req.text, 'html.parser')
    logging.debug('A debug message!')
    #logging.debug(req.text)
    # logging.info('We processed %d records', len(processed_records))

    script_json = soup.findAll("script")
    if (len(script_json) < 1):
        return HttpResponse("Error: script_json length is less than 1")
    json_object = json.loads(script_json[len(script_json)-1].contents[0])
    tournament = json_object['props']['pageProps']['tournament']
    leaderboard = json_object['props']['pageProps']['leaderboard']
    players = leaderboard['players']
    #['tourNavFooter']['legalText']['tournament']['tournamentName']
    # logging.debug(players)

    csv_file = 'csvs/leaderboard.csv'
    csv_obj = open(csv_file, 'w+')
    csv_writer = csv.writer(csv_obj)
    flat_header = flatten_data(players[0])
    header = flat_header.keys()
    csv_writer.writerow(header)
    for item in players:
      flat_player = flatten_data(item)
      csv_writer.writerow(flat_player.values())
    csv_obj.close()



    # find correct part of html code
    #tab = soup.find('div',attrs={'class','chakra-table'})
    #a = tab.find_all('a')




    return HttpResponse("Hello, world. You're at the predictor index.")


def num_to_english(request):
    # Initialize `number` to None
    number = None

    if request.method == 'GET':
        # Handle GET request; expect `number` as a query parameter
        number = request.GET.get('number')
    elif request.method == 'POST':
        # Handle POST request; expect `number` in the JSON body
        try:
            data = json.loads(request.body)
            number = data.get('number')
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    # Process `number` if it's available
    if number is not None:
        try:
            number = int(number)  # Convert to integer
            return JsonResponse({"status": "ok", "num_in_english": number_to_words(number)})
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid input"}, status=400)
    
    # Default response if method is not supported or `number` is not provided
    return JsonResponse({"status": "error", "message": "Method not allowed or number parameter missing"}, status=405)


def get_tournament_stats(request):
    # Initialize `number` to None - this should be our tournament ID number which starts with 'R'
    number = None

    if request.method == 'GET':
        # Handle GET request; expect `number` as a query parameter
        number = request.GET.get('number')
        tournament_url = request.GET.get('tournament_url')
        file_type = request.GET.get('file_type')
    elif request.method == 'POST':
        # Handle POST request; expect `number` in the JSON body
        try:
            data = json.loads(request.body)
            number = data.get('number')
            tournament_url = data.get('tournament_url')
            file_type = data.get('file_type')
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)

    # Process `number` if it's available
    if number is not None and tournament_url is not None and file_type is not None:
        try:
            #TODO - clean the input number to make sure it's a valid tournament ID and prevent any security issues
            path_to_file = 'csvs/tournament_stats_' + number + '.csv'
            #path_to_file = 'csvs/player1.csv'
            process_tournament_stats(number, path_to_file, tournament_url)

            if (file_type == 'csv'):
                file_blob = open(path_to_file, 'rb').read()
            elif (file_type == 'json'):
                path_to_file_json = 'csvs/tournament_stats_' + number + '.json'
                file_blob = open(path_to_file_json, 'rb').read()
            
            return HttpResponse(file_blob, content_type='application/octet-stream')
            #return JsonResponse({"status": "ok", "success": number_to_words(number)})
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid input"}, status=400)
    return JsonResponse({"status": "error", "message": "Method not allowed or number parameter missing"}, status=405)

def process_tournament_stats(tournament_id, path_to_file, tournament_url):

    # First call main page for the leaderboard for tournament
    # page = "https://www.pgatour.com/tournaments/2024/wells-fargo-championship/R2024480"
    req = requests.get(tournament_url, headers={
                                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                                'Accept-Encoding':'gzip, deflate, br, zstd',
                                'Accept-Language':'en-US,en;q=0.9',
                                'Cache-Control':'max-age=0',
                                'Priority':'u=0, i',
                                'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                                'Sec-Ch-Ua-Mobile':'?0',
                                'Sec-ch-ua-platform':'"macOS"',
                                'Sec-Fetch-Dest':'document',
                                'Sec-Fetch-Mode':'navigate',
                                'Sec-Fetch-Site':'same-origin',
                                'Sec-Fetch-User':'?1',
                                'Connection':'keep-alive',
                                'Pragma':'no-cache',
                                'Upgrade-Insecure-Requests':'1',
                                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})

    #                                'Cookie':'gig_canary=false; _scor_uid=54722d6167af4ecb85108f8ccc0b9c0d; _gcl_au=1.1.235794155.1715895016; _ga=GA1.1.1788951515.1715895016; AMP_MKTG_38168c7a64=JTdCJTdE; permutive-id=11863a7f-29b8-4d8f-a636-415ed66e2264; _fbp=fb.1.1715895016662.415746191; gig_bootstrap_3_IscKmAoYcuwP8zpTnatC3hXBUm8rPuI-Hg_cZJ-jL-M7LgqCkxmwe-ps1Qy7PoWd=_gigya_ver4; __qca=P0-797204401-1715895016529; _sharedid=12192f91-f28b-4a77-b834-fe589f51cab1; _sharedid_cst=VyxHLMwsHQ%3D%3D; _lr_env_src_ats=false; idl_env=Aj2Ornraj6Z021bdnx1YvnSaolChq9OC0pje7NQVXKWonp_QXz4RVtSb0K-Vjv5UhkdGIhj9fqGhcCEsDCNqvBW6Wsrkt5xl8_MjS1Mw; idl_env_cst=VyxHLMwsHQ%3D%3D; idl_env_last=Thu%2C%2016%20May%202024%2021%3A30%3A17%20GMT; hb_insticator_uid=ab187fe0-af5a-4559-9016-e956e60ea830; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3A_b2hjjmGwMePakCWIMU2i8vpjrxbQ_xw0EMtffIh9Q5RaV98BGPGqv74Wkx13cDoalUsy5DHyR3I6k-Tu9UhPBaVGiQoBuVK--geGIcde1eEPblXe_L0uWjDc3CE4G1f%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; _lr_geo_location_state=TX; _lr_geo_location=US; gig_canary_ver=15936-3-28598280; OptanonConsent=isGpcEnabled=0&datestamp=Thu+May+16+2024+17%3A07%3A52+GMT-0500+(Central+Daylight+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=10cbad2c-fc99-4011-aff6-854bb97f6b55&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&AwaitingReconsent=false; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.pgatour.com/stats%22%2C%22sref%22:%22https://www.pgatour.com/stats/detail/02567%22%2C%22sts%22:1715969839356%2C%22slts%22:1715895015714}; _parsely_visitor={%22id%22:%22pid=c3b8e517-62a9-425f-abe1-151032275e62%22%2C%22session_count%22:2%2C%22last_session_ts%22:1715969839356}; AMP_38168c7a64=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIxZDc5ZGVhZi03YjQ3LTQxNWYtYmE4MC03OGI1MjM0ZmQ5YzIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE1OTY5ODM5NTg0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNTk2OTgzOTcxNSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzIlN0Q=; _awl=2.1715969840.5-9571efc268b02fb32e84fca80aca39f3-6763652d75732d63656e7472616c31-0; _ga_D4BWM9D122=GS1.1.1715969839.2.1.1715969840.59.0.0; __gads=ID=d9f44ffdbd0e559b:T=1715895018:RT=1715969840:S=ALNI_MbfHrbLrENHfo6TD_69f3fHlIHiHQ; __gpi=UID=00000e1d207eb34f:T=1715895018:RT=1715969840:S=ALNI_MZmR99_uFA0FsXhh6E8nS_TkEAcMg; __eoi=ID=ad04eeb1774539d7:T=1715895018:RT=1715969840:S=AA-AfjZD7c24IObWW3JfZzy_TYV6',

    #req = requests.get(page)
    soup = bs(req.text, 'html.parser')
    # logging.debug('A debug message!')
    # logging.debug(req.text)
    # logging.info('We processed %d records', len(processed_records))

    script_json = soup.findAll("script")
    if (len(script_json) < 1):
        return HttpResponse("Error: script_json length is less than 1")
    json_object = json.loads(script_json[len(script_json)-1].contents[0])
    tournament = json_object['props']['pageProps']['tournament']
    leaderboard = json_object['props']['pageProps']['leaderboard']
    players = leaderboard['players']
    #['tourNavFooter']['legalText']['tournament']['tournamentName']
    # logging.debug(players)

 
    counter = 0
    final_data = []
    for player in players:
        player_id = player['id']

        # Define the graphql queries for the player stats
        scorecard = {"operationName":"ScorecardCompressedV3","variables":{"tournamentId":tournament_id,"playerId":player_id},"query":"query ScorecardCompressedV3($tournamentId: ID!, $playerId: ID!) {\n  scorecardCompressedV3(tournamentId: $tournamentId, playerId: $playerId) {\n    id\n    payload\n  }\n}"}
        scorecardstats = {"operationName":"ScorecardStatsV3Compressed","variables":{"scorecardStatsV3CompressedId":tournament_id,"playerId":player_id},"query":"query ScorecardStatsV3Compressed($scorecardStatsV3CompressedId: ID!, $playerId: ID!) {\n  scorecardStatsV3Compressed(\n    id: $scorecardStatsV3CompressedId\n    playerId: $playerId\n  ) {\n    id\n    payload\n  }\n}"}

        # Then call the player scorecard stats for each player in the tournament
        scorecard_json = get_player_leaderboard_stats(player_id, tournament_id, scorecard)
        #players[counter]['scorecard'] = scorecard_json

        # Then call the player stats for each player in the tournament
        scorecard_stats_json = get_player_leaderboard_stats(player_id, tournament_id, scorecardstats)
        #players[counter]['stats'] = scorecard_stats_json

        final_data.append(fill_tournament_player_stats(player, scorecard_json, scorecard_stats_json, schema_type='simple'))

        counter += 1

    # Finally concatenate all the data into a single csv file
    csv_file = path_to_file
    csv_obj = open(csv_file, 'w+')
    csv_writer = csv.writer(csv_obj)
    flat_header = flatten_data(final_data[0])
    header = flat_header.keys()
    csv_writer.writerow(header)
    for item in final_data:
        flat_player = flatten_data(item)
        csv_writer.writerow(flat_player.values())
    csv_obj.close()

    json_file = path_to_file.replace(".csv", ".json")
    with open(json_file, 'w+', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    


def get_player_leaderboard_stats(player_id, tournament_id, graphql_query):

    api_url = "https://orchestrator.pgatour.com/graphql"
    logging.debug(f"Getting player stats for player {player_id} in tournament {tournament_id}")
    api_req = requests.post(api_url, json = graphql_query, headers={
                                'Accept':'*/*',
                                'Accept-Encoding':'gzip, deflate, br, zstd',
                                'Accept-Language':'en-US,en;q=0.9',
                                'Content-Type':'application/json',
                                'Content-Length':'282',
                                'Origin':'https://www.pgatour.com',
                                'Referer':'https://www.pgatour.com',
                                'Cache-Control':'max-age=0',
                                'Priority':'u=0, i',
                                'Sec-Ch-Ua':'"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                                'Sec-Ch-Ua-Mobile':'?0',
                                'Sec-ch-ua-platform':'"macOS"',
                                'Sec-Fetch-Dest':'empty',
                                'Sec-Fetch-Mode':'cors',
                                'Sec-Fetch-Site':'same-site',
                                'X-Amz-User-Agent':'aws-amplify/3.0.7',
                                'X-Api-Key':'da2-gsrx5bibzbb4njvhl7t37wqyl4',
                                'X-Pgat-Platform':'web',
                                'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'})

    #                                'Cookie':'gig_canary=false; _scor_uid=54722d6167af4ecb85108f8ccc0b9c0d; _gcl_au=1.1.235794155.1715895016; _ga=GA1.1.1788951515.1715895016; AMP_MKTG_38168c7a64=JTdCJTdE; permutive-id=11863a7f-29b8-4d8f-a636-415ed66e2264; _fbp=fb.1.1715895016662.415746191; gig_bootstrap_3_IscKmAoYcuwP8zpTnatC3hXBUm8rPuI-Hg_cZJ-jL-M7LgqCkxmwe-ps1Qy7PoWd=_gigya_ver4; __qca=P0-797204401-1715895016529; _sharedid=12192f91-f28b-4a77-b834-fe589f51cab1; _sharedid_cst=VyxHLMwsHQ%3D%3D; _lr_env_src_ats=false; idl_env=Aj2Ornraj6Z021bdnx1YvnSaolChq9OC0pje7NQVXKWonp_QXz4RVtSb0K-Vjv5UhkdGIhj9fqGhcCEsDCNqvBW6Wsrkt5xl8_MjS1Mw; idl_env_cst=VyxHLMwsHQ%3D%3D; idl_env_last=Thu%2C%2016%20May%202024%2021%3A30%3A17%20GMT; hb_insticator_uid=ab187fe0-af5a-4559-9016-e956e60ea830; pbjs_fabrickId=%7B%22fabrickId%22%3A%22E1%3A_b2hjjmGwMePakCWIMU2i8vpjrxbQ_xw0EMtffIh9Q5RaV98BGPGqv74Wkx13cDoalUsy5DHyR3I6k-Tu9UhPBaVGiQoBuVK--geGIcde1eEPblXe_L0uWjDc3CE4G1f%22%7D; pbjs_fabrickId_cst=VyxHLMwsHQ%3D%3D; _lr_geo_location_state=TX; _lr_geo_location=US; gig_canary_ver=15936-3-28598280; OptanonConsent=isGpcEnabled=0&datestamp=Thu+May+16+2024+17%3A07%3A52+GMT-0500+(Central+Daylight+Time)&version=202301.1.0&isIABGlobal=false&hosts=&consentId=10cbad2c-fc99-4011-aff6-854bb97f6b55&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&AwaitingReconsent=false; _parsely_session={%22sid%22:2%2C%22surl%22:%22https://www.pgatour.com/stats%22%2C%22sref%22:%22https://www.pgatour.com/stats/detail/02567%22%2C%22sts%22:1715969839356%2C%22slts%22:1715895015714}; _parsely_visitor={%22id%22:%22pid=c3b8e517-62a9-425f-abe1-151032275e62%22%2C%22session_count%22:2%2C%22last_session_ts%22:1715969839356}; AMP_38168c7a64=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIxZDc5ZGVhZi03YjQ3LTQxNWYtYmE4MC03OGI1MjM0ZmQ5YzIlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzE1OTY5ODM5NTg0JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTcxNTk2OTgzOTcxNSUyQyUyMmxhc3RFdmVudElkJTIyJTNBMzIlN0Q=; _awl=2.1715969840.5-9571efc268b02fb32e84fca80aca39f3-6763652d75732d63656e7472616c31-0; _ga_D4BWM9D122=GS1.1.1715969839.2.1.1715969840.59.0.0; __gads=ID=d9f44ffdbd0e559b:T=1715895018:RT=1715969840:S=ALNI_MbfHrbLrENHfo6TD_69f3fHlIHiHQ; __gpi=UID=00000e1d207eb34f:T=1715895018:RT=1715969840:S=ALNI_MZmR99_uFA0FsXhh6E8nS_TkEAcMg; __eoi=ID=ad04eeb1774539d7:T=1715895018:RT=1715969840:S=AA-AfjZD7c24IObWW3JfZzy_TYV6',
    
    # Check for a successful response
    if api_req.status_code == 200:
        # Decompress the response content if it's gzipped
        # Handle gzip compression
        if api_req.headers.get('Content-Encoding') == 'gzip':
            buf = BytesIO(api_req.content)
            with gzip.GzipFile(fileobj=buf) as f:
                decompressed_data = f.read()
            logging.debug("gzip encoding")
        # Handle deflate compression
        elif api_req.headers.get('Content-Encoding') == 'deflate':
            try:
                decompressed_data = zlib.decompress(api_req.content)
            except zlib.error:
                # Try with raw deflate (no headers)
                decompressed_data = zlib.decompress(api_req.content, -zlib.MAX_WBITS)
            logging.debug("deflate encoding")
        # Handle Brotli compression
        elif api_req.headers.get('Content-Encoding') == 'br':
            #decompressed_data = brotlicffi.decompress(api_req.content)
            # Alternatively, you can do incremental decompression.

            # decompressed_data = brotli.decompress(api_req.content) # This is getting done automatically by requests
            decompressed_data = api_req.content

            logging.debug("BR encoding")
        # Handle Zstandard compression
        elif api_req.headers.get('Content-Encoding') == 'zstd':
            dctx = zstd.ZstdDecompressor()
            decompressed_data = dctx.decompress(api_req.content)
            logging.debug("Zstandard encoding")
        else:
            decompressed_data = api_req.content
            logging.debug("fall through to no encoding header")

        logging.debug(decompressed_data)

        # Attempt to decode the decompressed data as JSON
        decoded_data = decompressed_data.decode('utf-8')
        # logging.debug(decoded_data)
        json_data = json.loads(decoded_data)
        logging.debug(json_data)
        
        # Extract and decode the payload
        # payload_base64 = json_data['data']['scorecardCompressedV3']['payload']
        payload_base64 = json_data['data'][lowercase_first(graphql_query['operationName'])]['payload']
        payload_compressed = base64.b64decode(payload_base64)

        # Decompress the payload
        payload_decompressed = gzip.decompress(payload_compressed)
        payload_json = json.loads(payload_decompressed.decode('utf-8'))
        # logging.debug(payload_json)

        return payload_json

        # wrapped_payload = {"scorecard": payload_json}

        # csv_file = 'csvs/player_stats2.csv'
        # csv_obj = open(csv_file, 'w+')
        # csv_writer = csv.writer(csv_obj)
        # flat_data = flatten_data(payload_json)
        # header = flat_data.keys()
        # csv_writer.writerow(header)
        # csv_writer.writerow(flat_data.values())
        # csv_obj.close()

        # # Attempt to decode the decompressed data as JSON
        # try:
        #     decoded_data = decompressed_data.decode('utf-8')
        #     logging.debug(decoded_data)
        #     data = json.loads(decoded_data)
        #     logging.debug(data)
        # except UnicodeDecodeError:
        #     logging.debug("Failed to decode the response content as utf-8.")
        #     logging.debug(decompressed_data)
        #     logging.debug(decompressed_data.hex())  # Print hex representation
        # except json.JSONDecodeError:
        #     logging.debug("Failed to parse the response content as JSON.")
        #     logging.debug(decompressed_data)
        #     logging.debug(decompressed_data.hex())  # Print hex representation
    else:
        # Print the error message
        logging.debug(f"Query failed with status code {api_req.status_code}: {api_req.text}")
        return {}

    return {}

