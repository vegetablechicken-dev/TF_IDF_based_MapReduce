from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from collections import defaultdict
import json
import jieba

app = Flask(__name__, template_folder = '.')
data = json.loads(open('./data/data.json', 'r', encoding='utf-8').read())
inverted_index = json.loads(open('./data/inverted_index.json', 'r', encoding='utf-8').read())

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('./template/index.html', data = data)
    if request.method == 'POST':
        keyword = request.form.get("keyword")
        stopwords_1 = [w.strip() for w in open('./stopwords/hit_stopwords.txt', 'r', encoding='utf-8').readlines()]
        stopwords_2 = [w.strip() for w in open('./stopwords/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
        stopwords_3 = [w.strip() for w in open('./stopwords/scu_stopwords.txt', 'r', encoding='utf-8').readlines()]
        stopwords = stopwords_1 + stopwords_2 + stopwords_3
        real_keywords = [word for word in jieba.cut(keyword) if word not in stopwords]
        keyword_info = {key:value for key, value in inverted_index.items() if key in real_keywords}
        res = defaultdict(lambda:{'tf_idf':0, 'paragraph':[]})
        for info in keyword_info.values():
            for word_info in info:
                res[word_info['article_id']]['tf_idf'] += word_info['tf_idf']
                res[word_info['article_id']]['paragraph'] += word_info['paragraph']
        res = sorted(res.items(), key = lambda x:x[1]['tf_idf'], reverse=True)
        res = [[int(item[0]), sorted(list(set(item[1]['paragraph'])))] for item in res]

        return redirect(url_for('result', result=json.dumps(res), keywords=json.dumps(real_keywords)))

@app.route('/result', methods = ['GET'])
def result():
    keywords = json.loads(request.args.get('keywords'))
    result = json.loads(request.args.get('result'))
    return render_template('./template/results.html', result=result, keywords=keywords, origin_text=data, num=len(result))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
