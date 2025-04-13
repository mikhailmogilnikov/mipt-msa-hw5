import requests
import time
import re
from collections import defaultdict
from functools import lru_cache

@lru_cache(maxsize=32)
def get_text(url):
    try:
        response = requests.get(url, timeout=5)
        return response.text
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return ""

def preprocess_text(text):
    return re.findall(r'\b\w+\b', text.lower())

def count_word_occurrences(words, target_words_set):
    counts = defaultdict(int)
    for word in words:
        if word in target_words_set:
            counts[word] += 1
    return counts

def read_words_from_file(file_path):
    words = []
    with open(file_path, 'r') as file:
        for line in file:
            word = line.strip()
            if word:
                words.append(word)
    return words

def main():
    words_file = "words.txt"
    url = "https://eng.mipt.ru/why-mipt/"
    
    start_time = time.time()
    
    words_to_count = read_words_from_file(words_file)
    text = get_text(url)
    text_words = preprocess_text(text)
    words_set = set(word.lower() for word in words_to_count)
    counts = count_word_occurrences(text_words, words_set)
    frequencies = {}
    
    for word in words_to_count:
        frequencies[word] = counts.get(word.lower(), 0)

    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.4f} seconds")
    print(frequencies)

if __name__ == "__main__":
    main()