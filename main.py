import io
from os import listdir
import nltk as nltk
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def load_file_text(filename):
    with open(filename, mode='r', encoding='utf-8') as reader:
        return reader.read()


def load_special_characters(filename):
    with open(filename, mode='r', encoding='utf-8') as reader:
        lines = reader.read().split("\n")
    return lines


def cosinus_similarity(array1, array2):
    return np.dot(np.array(array1), np.array(array2)) / (np.linalg.norm(np.array(array1)) * np.linalg.norm(np.array(array2)))


db_path = "db"

stopwords = set(nltk.corpus.stopwords.words("english"))

all_words = []
file_word_freq = {}
file_data = {}


for file in listdir(db_path):
    text = load_file_text(f'{db_path}/{file}')

    tokenized_words = nltk.tokenize.word_tokenize(text)
    tokenized_words_frequency = nltk.probability.FreqDist(tokenized_words)

    print(f'Najbardziej popularne słowa w pliku [{file}]')
    print(tokenized_words_frequency.most_common(10))
    print()

    stemmed_words = [nltk.stem.PorterStemmer().stem(word) for word in tokenized_words]
    stemmed_words_freq = nltk.probability.FreqDist(stemmed_words)

    print(f'Najbardziej popularne wystemowane słowa w pliku [{file}]')
    print(stemmed_words_freq.most_common(10))
    print()

    file_word_freq[file] = {}
    for (word, amount) in stemmed_words_freq.items():
        file_word_freq[file][word] = amount
        if word not in all_words:
            all_words.append(word)

for word in all_words:
    for file in file_word_freq:
        if file_word_freq[file].get(word) is None:
            file_word_freq[file][word] = 0

for file in file_word_freq:
    file_word_freq[file] = sorted(file_word_freq[file].items())
    file_data[file] = [value for (key, value) in file_word_freq[file]]

for file1 in file_data:
    for file2 in file_data:
        print(f'Podobieństwo cosinusowe plików [{file1}] oraz [{file2}] {cosinus_similarity(file_data[file1], file_data[file2])}')

for file in file_word_freq:
    strings = []
    for (word, amount) in file_word_freq[file]:
        for i in range(amount):
            strings.append(word)

    plt.figure(figsize=(15, 15))

    wordcloud = WordCloud(font_path=f'common/{"JakeHand.ttf"}', width=2000, height=1000, collocations=False)
    wordcloud.generate(' '.join(strings))

    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
