from bs4 import BeautifulSoup
import re
import requests
import jieba
import json

url = 'http://www.news.cn/politics/index.html'

def main():
    response = requests.get(url)
    if response.status_code == 200:
        response = response.content.decode()
        soup = BeautifulSoup(response, 'html.parser')
        title_href_list = soup.find_all('div', class_='tit')
        
        text_data = [{
            'title':s.find('a').text,
            'time':'',
            'url':s.find('a').get('href'),
            'content':[]
        } for s in title_href_list if s.find('a').text and s.find('a').get('href') is not None]
        # print(text_data)
        for i in range(len(text_data)):
            response = requests.get(text_data[i]['url'])
            if response.status_code == 200:
                response = response.content.decode()
                soup = BeautifulSoup(response, 'html.parser')
                time = soup.find('div', class_='header-time left')
                content = soup.find('div', {'id': 'detail'})
                if content is not None:
                    content = content.text.replace('\xa0',' ').replace('\u2003','\u3000').split('\u3000')
                    content = [t for t in content if t is not None and t != '' and t.strip() != '']
                    text_data[i]['content'] = content
                    # print(content)
                else:
                    continue
                if time is not None:
                    year = time.find('span', class_='year').text
                    date = time.find('span', class_='day').text
                    time_ = time.find('span', class_='time').text
                    text_data[i]['time'] = (year+'/'+date+'/'+time_).replace(' ', '')         
            else:
                # print(text_data[i]['url'])
                print('Failed')
        
        no_content = []
        for i in range(len(text_data)):
            if len(text_data[i]['content']) == 0:
                no_content.append(text_data[i])
        for i in no_content:
            text_data.remove(i) 
        
        with open('./data/data.json', 'w', encoding='utf-8') as f:
            json.dump(text_data, f, ensure_ascii=False)
        
        stopwords_1 = [w.strip() for w in open('./stopwords/hit_stopwords.txt', 'r', encoding='utf-8').readlines()]
        stopwords_2 = [w.strip() for w in open('./stopwords/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
        stopwords_3 = [w.strip() for w in open('./stopwords/scu_stopwords.txt', 'r', encoding='utf-8').readlines()]
        stopwords = stopwords_1 + stopwords_2 + stopwords_3
        split_data = []
        for article in text_data:
            content = article['content']
            split_content = []
            for p in content:
                p = re.sub(r'\d+', '', p.replace('\n', '').replace('\r', '').replace(' ', ''))
                split_paragraph = [w for w in list(jieba.cut(p)) if w not in stopwords]
                split_content.append(split_paragraph)
            article['content'] = split_content
            split_data.append(article)
        
        with open('./data/split_data.json', 'w', encoding='utf-8') as f:
            json.dump(split_data, f, ensure_ascii=False)

    else:
        print('Failed')    

if __name__ == '__main__':
    main()



