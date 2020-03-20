import os
import pychrome
import PySimpleGUI as sg
import sys
import lxml.html
import re
from typing import Optional

basename: str
tab: Optional[pychrome.Tab] = None


# дла чужих открытых папок
def copy_data_alien():
    global tab

    # https://gist.github.com/magician11/a979906401591440bd6140bd14260578
    rootNode = tab.DOM.getDocument()
    html = tab.DOM.getOuterHTML(nodeId=rootNode['root']['nodeId'])['outerHTML']
    # with open(f"{basename}.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    # return
    # with open(f"{basename}.html", "r", encoding="utf-8") as f:
    #     html = f.read()
    with open(f"{basename}.txt", "a", encoding="utf-8") as f:
        # f.write("\n")
        tree = lxml.html.fromstring(html)
        films = tree.xpath('//ul[@id="itemList"]/li')
        folders = tree.xpath('//div[@class="folders"]/div[contains(@class, "act")]/font[@class="name"]')
        folder = folders[0].xpath('string()')
        print(films)
        for film in films:
            item = int(film.xpath('@id')[0].replace('film_', ''))
            name = film.xpath('div[@class="info"]/div/font/a[@class="name"]')[0]
            name_orig = film.xpath('div[@class="info"]/span')[0]
            info = film.xpath('div[@class="info"]/b')[0]  # .xpath('string()')
            name = name.xpath('string()')
            name_orig = re.sub(r'\s\d+\s+мин\.$', '', name_orig.xpath('string()'))
            info = info.xpath('string()').replace('\n', '').strip().replace('реж. ', '')
            info = re.sub(r'\s\s+', ' ', info)
            info = re.sub(r'^(\S+)\.\.\. ', r'\1, ', info)
            f.write(f"{folder}\t{item}\t{name}\t{name_orig}\t{info}\n")
    pass

# дла своих папок после авторизации
def copy_data_authorized():
    global tab

    # https://gist.github.com/magician11/a979906401591440bd6140bd14260578
    rootNode = tab.DOM.getDocument()
    html = tab.DOM.getOuterHTML(nodeId=rootNode['root']['nodeId'])['outerHTML']
    # для удобства отладки парсера хтмыл пишем на диск
    # with open(f"{basename}.html", "w", encoding="utf-8") as f:
    #     f.write(html)
    # return
    # with open(f"{basename}.html", "r", encoding="utf-8") as f:
    #     html = f.read()
    with open(f"{basename}.txt", "a", encoding="utf-8") as f:
        # f.write("\n")
        tree = lxml.html.fromstring(html)
        films = tree.xpath('//ul[@id="itemList"]/li[@class="item"]')
        folders = tree.xpath('//ul[@id="folderList"]/li[contains(@class, "act")]/span[@class="nameAndNum"]')
        folder = folders[0].xpath('string()')
        # print(films)
        for film in films:
            item = int(film.xpath('@data-id')[0])
            name = film.xpath('div[@class="info"]/a[@class="name"]')[0]
            name_orig = name.xpath('following-sibling::span')[0]
            info = name_orig.xpath('following-sibling::span')[0]

            name = name.xpath('string()')
            name_orig = re.sub(r'\s\d+\s+мин\.$', '', name_orig.xpath('string()'))
            info = info.xpath('string()').replace('\n', '').strip().replace('реж. ', '')
            info = re.sub(r'\s\s+', ' ', info)
            info = re.sub(r'^(\S+)\.\.\. ', r'\1, ', info)
            f.write(f"{folder}\t{item}\t{name}\t{name_orig}\t{info}\n")
    pass


def main():
    global tab

    window = sg.Window('Kinopoisk', return_keyboard_events=True).Layout([
        [sg.Text(f"Копировать данные")],
        [sg.Button("Copy", key="-copy")],
    ])

    browser = pychrome.Browser(url="http://127.0.0.1:9230")
    globals()['tab'] = browser.new_tab()
    tab.start()
    tab.Network.enable()
    tab.Page.navigate(url="https://www.kinopoisk.ru/mykp/movies/", _timeout=10)

    while True:  # Event Loop
        event, values = window.read()
        print({event: values})
        if event == '-copy':
            copy_data_authorized()  # or copy_data_alien()
        elif event is None:
            break
    pass


if __name__ == "__main__":
    basename = os.path.splitext(os.path.basename(__file__))[0]
    main()
    sys.exit(1)
