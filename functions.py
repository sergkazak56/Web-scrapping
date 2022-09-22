import requests
import bs4
import fake_useragent
import re

# Функция считывания разметки страницы
def read_page(base_url='', second_url=''):
    """
    Функция считывания разметки страницы
    :param base_url: базовое url страницы
    :param second_url: вторичное url страницы
    :return: разметку страницы
    """
    link = base_url + second_url
    if link:
        ua = fake_useragent.UserAgent()
        response = requests.get(link, headers={'User-Agent': ua.chrome})
        return response.text
    return ''

# Функция поиска слов в тексте
def find_in_text(text, words, find_method):
    """
    Функция поиска слов в тексте. Если слово найдено - True, если нет - False
    :param text: текст для поиска
    :param words: список слов или регулярное выражение
    :param find_method: метод поиска 1 - словами, 0 - регулярным выражением
    :return: boolean
    """
    if find_method:
        text_list = re.sub("[^\w]", " ", text).lower().split()
        for word in words:
            if word in text_list:
                return True
            else:
                continue
        return False
    else:
        if re.search(words, text):
            return True
        else:
            return False

# Функция парсинга по тексту превью или полному тексту статей на переданной странице
def scrape_articles(words, base_url, second_url, parsing_method=1, find_method=0):
    """
     Функция парсинга по тексту превью или полному тексту статей на переданной странице
    :param words: список слов для поиска или регулярное выражение
    :param base_url: базовое url страницы
    :param second_url: вторичное url страницы
    :param parsing_method: метод парсинга 1 - по превью статей, 0 - по полному тексту статей
    :param find_method: метод поиска 1 - словами, 0 - регулярным выражением
    :return: вывод в консоль даты публикации, названия статьи и ссылки на статью в консоль
    """
    text = read_page(base_url, second_url)
    if not text:
        print('Неверно заданы url страницы')
        return
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    print(f'Номер:  Дата, время:{" " * 9}Заголовок ---> cсылка:')
    ind = 1
    if parsing_method:
        for article in articles:
            preview1 = article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-1')
            preview2 = article.find(class_='article-formatted-body article-formatted-body article-formatted-body_version-2')
            if preview1:
                preview_txt = preview1.text
            elif preview2:
                preview_txt = preview2.text
            else:
                preview_txt = ''
            if find_in_text(preview_txt, words, find_method):
                art_date = article.find("time").attrs["title"]
                h2 = article.find("h2")
                title = h2.find("span").text
                href = h2.find("a").attrs["href"]
                print(f'{ind}.{" " * (7 - len(str(ind)))}{art_date}    {title} ---> {base_url + href}')
                ind += 1
    else:
        for article in articles:
            h2 = article.find("h2")
            art_text = read_page(base_url, h2.find("a").attrs["href"])
            art_soup = bs4.BeautifulSoup(art_text, features='html.parser')
            art_body = art_soup.find('article')
            if find_in_text(art_body.text, words, find_method):
                art_date = article.find("time").attrs["title"]
                h2 =  article.find("h2")
                title = h2.find("span").text
                href = h2.find("a").attrs["href"]
                print(f'{ind}.{" " * (7 - len(str(ind)))}{art_date}    {title} ---> {base_url + href}')
                ind += 1
