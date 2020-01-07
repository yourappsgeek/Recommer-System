import csv


def csv_loader(path):
    data_file = open(file=path)
    csv_reader = csv.reader(data_file, delimiter=',')
    data, flag = [], 0
    header = []
    for key in csv_reader:
        temp = {}
        if flag == 0:
            for key1 in key:
                header.append(key1)
            flag = 1
            continue
        for key1 in range(len(key)):
            temp.update({header[key1]: key[key1]})
        data.append(temp)
    return data


# Configurations Start

# path = '/Users/aliahsan/Desktop/RecomendedSystem/raw_movies.csv'
path_ratings = '/Users/aliahsan/Desktop/RecomendedSystem/raw_ratings.csv'
path = '/Users/aliahsan/Desktop/RecomendedSystem/raw_book_data.csv'
limit = 1000
genre_output_file = 'book_genre_tmp.csv'
data_output_file = 'book_data_tmp.csv'

# Configurations End

data0 = csv_loader(path)

if path.split("/")[-1].__contains__("movies"):
    data1 = csv_loader(path_ratings)

    movies = {}

    for key in data1:
        if list(movies.keys()).__contains__(key['movieId']):
            movies[key['movieId']]['count'] += 1
            movies[key['movieId']]['sum'] += float(key['rating'])
        else:
            movies.update({key['movieId']: {'count': 1, 'sum': float(key['rating'])}})

    for key in movies:
        movies[key] = movies[key]['sum'] / movies[key]['count']

    rating = 'rating'
    title = 'title'
    flag = 'movie'
else:
    rating = 'book_rating'
    title = 'book_title'
    flag = 'book'

movies_data = [['Id', 'title', 'rating']]
category_data = [['Id', 'category']]
for key in range(len(data0)):
    if limit:
        if key > limit:
            break
    categories = data0[key]['genres'].split('|')
    try:
        if flag == 'book':
            id_o = key
            movies_data.append([id_o, data0[key][title], data0[key][rating]])
        else:
            id_o = data0[key]['movieId']
            movies_data.append([id_o, data0[key][title], movies[data0[key]['movieId']]])
    except KeyError:
        movies_data.append([id_o, data0[key][title], 0])
    for key1 in categories:
        category_data.append([key, key1])

with open(genre_output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(category_data)
with open(data_output_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(movies_data)
