import os
import json
import webbrowser

import urllib.parse
import urllib.request

listing_page_html = """
<!DOCTYPE html>
<html>
<head>
  <title>Movies</title>
  <style>
  html
  {{
    margin:0;
    padding:0;
  }}
  body 
  {{
    background-color: #DCDCDC;
    font-family: Arial, Helvetica, sans-serif;
    font-size: 1.2em;
  }}
  h1
  {{
    background-color: #0F5738;
    color: #FFFFFF;
    text-align: center;
    padding: 4px;
    font-size: 1.6em;
  }}
  div
  {{
    border: 1px solid #003A21;
    padding: 4px;
    background-color: #FFFFFF;
  }}
  .small
  {{
    font-size: .8em;
  }}
  </style>
</head>
<body>
{0}
</body>
</html>
"""


movie_html = """
<h1>{title}</h1>
<div>Year: {year}</div>
<div class="small">Plot:{plot}</div>
"""


def get_movie_dirs(top_dir):
    try:
        return next(os.walk(top_dir))[1]
    except:
        print('error finding directories')
        return []


def parse_movie_title(movie_dir):
    title = ''
    year = ''
    if len(movie_dir) > 6:
        if movie_dir.endswith(')'):
            length = len(movie_dir)
            year = movie_dir[length - 5 : length - 1]
            title = movie_dir[0 : length - 6]
        else:
            title = movie_dir
    else:
        title = movie_dir

    return {'t': title, 'y': year}


def get_key_value(movie, key):
    if key in movie:
        return movie[key]
    else:
        return 'N/A'


def get_movie_info(url):
    response = urllib.request.urlopen(url).read().decode('utf8')
    obj = json.loads(response)
    return obj


def write_file(html_file, html):
    f = open(html_file, 'w')
    f.write(html)
    f.close()


top_dir = input('top directory: ')
print('searching for movies in "' + top_dir + '"')

movie_names = get_movie_dirs(top_dir)
if len(movie_names) > 0:
    content = ''

    for cur_dir in movie_names:
        search = parse_movie_title(cur_dir)
        # will need to add api lookup here
        search_query = urllib.parse.urlencode(search)
        api_url = "http://www.omdbapi.com/?apikey=7a6c480b&{}&plot=full".\
                format(search_query)
        # print(api_url)
        movie = get_movie_info(api_url)
        if get_key_value(movie,'Response') == 'False':
            print('Movie titled {} not found.'.format(cur_dir))
        else:
            print('Adding {}.'.format(search['t']))
            year = get_key_value(movie, 'Year')
            plot = get_key_value(movie, 'Plot')
            movie_info = {'title': search['t'], 'year': year, 'plot': plot}
            content = content + movie_html.format_map(movie_info)

    result = listing_page_html.format(content)
    html_file = top_dir + os.sep + 'movies.htm'
    write_file(html_file,result)
    webbrowser.open('file:\\{}'.format(html_file))


#OTHER INFORMATION

# api key 7a6c480b

# sample output
# {"Title":"Office Space","Year":"1999","Rated":"R","Released":"19 Feb 1999","Runtime":"89 min","Genre":"Comedy","Director":"Mike Judge","Writer":"Mike Judge (Milton animated shorts), Mike Judge (screenplay)","Actors":"Ron Livingston, Jennifer Aniston, David Herman, Ajay Naidu","Plot":"In the Initech office, the insecure Peter Gibbons hates his job and the abusive Division VP Bill Lumbergh that has just hired two consultants to downsize the company. His best friends are the software engineers Michael Bolton and Samir Nagheenanajar that also hate Initech, and his next door neighbor Lawrence. His girlfriend Anne is cheating on him but she convinces Peter to visit the hypnotherapist Dr. Swanson. Peter tells how miserable his life is and Dr. Swanson hypnotizes him and he goes into a state of ecstasy. However, Dr. Swanson dies immediately after giving the hypnotic suggestion to Peter. He dates the waitress Joanna and changes his attitude in the company, being promoted by the consultants. When he discovers that Michael and Samir will be fired, they decide to plant a virus in the account system to embezzle fraction of cents in each financial operation into Peter's account. However Michael commits a mistake in the software and instead of decimals, they steal a large amount. The desperate trio tries to fix the problem or they will go to prison.","Language":"English","Country":"USA","Awards":"2 nominations.","Poster":"https://images-na.ssl-images-amazon.com/images/M/MV5BOTA5MzQ3MzI1NV5BMl5BanBnXkFtZTgwNTcxNTYxMTE@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.8/10"},{"Source":"Rotten Tomatoes","Value":"79%"},{"Source":"Metacritic","Value":"68/100"}],"Metascore":"68","imdbRating":"7.8","imdbVotes":"210,817","imdbID":"tt0151804","Type":"movie","DVD":"31 Aug 1999","BoxOffice":"N/A","Production":"20th Century Fox","Website":"http://www.officeguy.com","Response":"True"}

# sample url
# http://www.omdbapi.com/?apikey=7a6c480b&t=office+space&y=1999&plot=full


