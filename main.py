import requests
import bs4
import fake_useragent
import re

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
        text_list = re.sub("[^\w]", " ", text).split()
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

# Функция парсинга по превью статей на переданной странице
def scrape_preview(text, words, base_url, find_method=0):
    """
     Функция парсинга по превью статей на переданной странице
    :param text: текст - разметка страницы
    :param words: список слов для поиска или регулярное выражение
    :param base_url: базовое url страницы
    :param find_method: метод поиска 1 - словами, 0 - регулярным выражением
    :return: вывод даты публикации, названия статьи и ссылки на статью в консоль
    """
    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')
    ind = 1
    print(f'Номер:  Дата, время:{" " * 9}Заголовок ---> cсылка:')
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
                h2 =  article.find("h2")
                title = h2.find("span").text
                href = h2.find("a").attrs["href"]
                print(f'{ind}.{" " * (7 - len(str(ind)))}{art_date}    {title} ---> {base_url + href}')
                ind += 1

# Функция ввода, считывания страницы и вызова скрапинга
def main():
    """
    Функция ввода метода поиска, считывания страницы и вызова скрапинга
    """
    parsing_method = int(input("Введите способ парсинга (1 - по превью статей, 0 - по полному тексту статей): "))
    find_method = int(input("Как ищем (1 - по словам, 0 - с помощью регулярного выражения): "))
    words_list = ['программа', 'цифровая', 'Microsoft', 'Apple', 'приложение', 'IT']
    regexp = '\s?[Пп]рограмм[а-яё]+\s?|\s?[Цц]ифр[а-яё]+\s?|\s?[Mm]icrosoft\s?|\s?[Aa]pple\s?|\s?[Пп]риложен[а-яё]\s?|\s?IT\s?'
    base_url = 'https://habr.com'
    page_url = base_url + '/ru/all/'
    ua = fake_useragent.UserAgent()
    response = requests.get(page_url, headers={'User-Agent': ua.chrome})
    text = response.text
    if find_method:
        scrape_preview(text, words_list, base_url, find_method)
    else:
        scrape_preview(text, regexp, base_url, find_method)

if __name__ == '__main__':
    main()
