import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer


data = json.load(sys.stdin)
text_list = []
for article in data:
    content = article['content']
    word_list = []
    for p in content:
        word_list = word_list + p
    text_list.append(' '.join(word_list))

vectorizer = TfidfVectorizer()
tfidf_res = vectorizer.fit_transform(text_list)

vocabulary_list = vectorizer.vocabulary_
tfidf_list = []

for i in range(len(text_list)):
    tfidf_word = {}
    for key in vocabulary_list.keys():
        tfidf_word[key] = tfidf_res[i, vocabulary_list[key]]
    tfidf_list.append(tfidf_word)

print(json.dumps(tfidf_list, ensure_ascii=False))
# with open('test.json', 'w', encoding='utf-8') as f:
#     f.write(a)