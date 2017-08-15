import os

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
<div>released: {year}</div>
<div class="small">more info</div>
"""


def get_movie_dirs(top_dir):
    return next(os.walk(top_dir))[1]


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

    return {'title': title, 'year': year}


top_dir = input('top directory: ')
print('searching for movies in "' + top_dir + '"')

movie_names = get_movie_dirs(top_dir)
print(movie_names)
content = ''

for cur_dir in movie_names:
    print(cur_dir)
    search = parse_movie_title(cur_dir)
    print(search)
    content = content + movie_html.format_map(search)

    
print(content)
result = listing_page_html.format(content)
print(result)

# api key 7a6c480b
