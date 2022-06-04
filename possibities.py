from main import check_conditions
from main import load_words
from main import table2color

import multiprocessing as mp

import math
import time
import pickle

from time import time_ns as xd
from operator import itemgetter
from itertools import product
from itertools import repeat
from scipy.stats import entropy

all_lists = list(product([3,1,0],repeat=5));
all_colors = [table2color(x) for x in all_lists]

#Zwraca liste słów które dalej są możliwe
def reduce(guess, colors, words):
    return [word for word in words if colors == LUT[word][guess]]

#Sprawdza czy słowo jest legalne po danej próbie
def fits_rules(guess,colors,word):
    colors2 = check_conditions(word, guess);
    return colors2==colors

#Liczy entropie słowa -- WIP
def get_entropy(guess,words):
    list = []
    for color in all_colors:
        new_words = reduce(guess,color,words)
        prob = len(new_words)/len(words)
        list.append(prob)
    sum = entropy(list, base=2)
    global count
    count += 1
    print("|= " + guess + " : " + str(sum) + "   " + str(count))
    return (guess, sum)

def find_best_guess(words):
    entropies = []
    with mp.Pool(mp.cpu_count()) as pool:
        entropies = pool.starmap(get_entropy, zip(words, repeat(words)))

    best = max(entropies, key=itemgetter(1))

    return best

with open('data.pkl','rb') as file:
    LUT = pickle.load(file)
print("loaded")

count = 0
words = load_words()
(guess, e) = find_best_guess(words)
print(guess + " : " + str(e))
