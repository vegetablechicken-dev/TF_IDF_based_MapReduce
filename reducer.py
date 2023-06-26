import sys
import json

# tfidf_of_word = json.load(open('test.json', 'r', encoding='utf-8'))
tfidf_of_word = json.load(sys.stdin)

with open('./data/split_data.json', 'r', encoding='utf-8') as f:
    text_data = json.load(f)

# 倒排索引表包含位置信息article_id, paragraph_list和TF_IDF值
inverted_index = {}

for i in range(len(tfidf_of_word)):
    for word, tf_idf in tfidf_of_word[i].items():
        if tf_idf != 0.0:
            word_info = {}
            word_aid = i
            word_paragraph = []
            for j, paragraph in enumerate(text_data[i]['content']):
                # 找到一个词在文章中所有出现的位置
                if word in paragraph:
                    word_paragraph.append(j)
            word_info['article_id'] = word_aid
            word_info['tf_idf'] = tf_idf
            word_info['paragraph'] = word_paragraph
            if len(word_info['paragraph']) != 0:
                if word in inverted_index:
                    inverted_index[word].append(word_info)
                else:
                    inverted_index[word] = [word_info]

# 排序
for word, word_info in inverted_index.items():
    mid_list = sorted(word_info, key=lambda x:x['tf_idf'] , reverse=True)
    inverted_index[word] = mid_list

print(inverted_index)
# a = json.dumps(inverted_index, ensure_ascii=False)
# with open('test2.json', 'w', encoding='utf-8') as f:
#     f.write(a)