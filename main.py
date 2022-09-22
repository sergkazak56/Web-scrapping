from functions import scrape_articles

# Функция ввода метода скрапинга и поиска и вызова функции скрапинга
def main():
    """
    Функция ввода метода скрапинга и поиска и вызова функции скрапинга
    """
    parsing_method = int(input("Введите способ парсинга (1 - по превью статей, 0 - по полному тексту статей): "))
    find_method = int(input("Как ищем (1 - по словам, 0 - с помощью регулярного выражения): "))
    words_list = ['программа', 'цифровая', 'Microsoft', 'Apple', 'приложение', 'IT']
    regexp = '\s?[Пп]рограмм[а-яё]+\s?|\s?[Цц]ифр[а-яё]+\s?|\s?[Mm]icrosoft\s?|\s?[Aa]pple\s?|\s?[Пп]риложен[а-яё]\s?|\s?IT\s?'
    base_url = 'https://habr.com'
    second_url = '/ru/all/'
    if find_method:
        scrape_articles(words_list, base_url, second_url, parsing_method, find_method)
    else:
        scrape_articles(regexp, base_url, second_url, parsing_method, find_method)


if __name__ == '__main__':
    main()
