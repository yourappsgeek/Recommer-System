import pandas as pd
import random
import math
import operator

genres = {}


def loadDataSet(filename, filename_genre, split, trainingSet=[], testSet=[]):
    csvFile = open(filename, 'rb')
    genreFile = open(filename_genre, 'rb')

    lines_genre = pd.read_csv(genreFile)
    lines = pd.read_csv(csvFile)
    dataSet = list(lines.values)
    genre = list(lines_genre.values)
    for x in range(len(dataSet) - 1):
        for y in range(len(dataSet[x])):
            try:
                dataSet[x][y] = float(dataSet[x][y])
            except ValueError:
                dataSet[x][y] = dataSet[x][y]
        if dataSet[x][0] > 1000:
            trainingSet.append(dataSet[x])
        else:
            testSet.append(dataSet[x])

    for x in genre:
        if list(genres.keys()).__contains__(x[0]):
            genres[x[0]].append(x[1])
        else:
            genres.update({x[0]: [x[1]]})


def euclideanDistance(instance1, instance2):
    inst1_genre = genres[instance1[0]]
    inst2_genre = genres[instance2[0]]

    count = 0
    for key in inst1_genre:
        if inst2_genre.__contains__(key):
            count += 1
    result = count / len(inst1_genre)

    return result


def getNeighbors(trainingSet, testInstance, k, k2):
    distances = []
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x])
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1), reverse=True)
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    neighbors.sort(key=operator.itemgetter(2), reverse=True)

    return neighbors[:k2]


def print_references(testInstance, references):
    print("\n" + testInstance[1])
    for key in references:
        print("\t" + str(key[1]) + "\t" + str(key[2]))


def main():
    # prepare data
    trainingSet = []
    testSet = []
    split = 0.70
    loadDataSet('/Users/aliahsan/Desktop/RecomendedSystem/movie_data.csv', '/Users/aliahsan/Desktop/RecomendedSystem/movie_genre.csv', split, trainingSet, testSet)
    print('Train set: ' + repr(len(trainingSet)))
    print('Test set: ' + repr(len(testSet)))
    k = 15
    k2 = 5
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k, k2)
        print_references(testSet[x], neighbors)


main()
