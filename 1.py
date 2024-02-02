import requests
from bs4 import BeautifulSoup

def get_douban_top250(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = []
    
    movies = soup.find_all('div', class_='info')
    for movie in movies:
        title = movie.find('span', class_='title').text
        # 这里只获取中文名，忽略其他国家名称
        if '\xa0' in title:
            continue
        rating = movie.find('span', class_='rating_num').text
        movie_list.append((title, rating))
    
    return movie_list

def save_to_file(movie_list, filename='douban_top250.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for movie in movie_list:
            f.write(f"{movie[0]} - 评分：{movie[1]}\n")

if __name__ == "__main__":
    all_movies = []
    for i in range(0, 250, 25):
        url = f'https://movie.douban.com/top250?start={i}&filter='
        all_movies.extend(get_douban_top250(url))

    save_to_file(all_movies)
    print('豆瓣Top250电影信息已保存到文件 douban_top250.txt')
