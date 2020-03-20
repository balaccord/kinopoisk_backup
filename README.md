﻿Бэкап собственных данных, введённых на сайте Кинопоиска в лучших (или, скорее, худших) традициях индусского кодинга

Данные пишутся в файл **kinopoisk_backup.txt**, поля разделены табуляцией, структура полей простецкая, но достаточная

Несмотря на некоторую (на самом деле изрядную) индусскость, в скрипте используются прикольные технологии:

- [Google Chrome Dev Protocol](https://chromedevtools.github.io/devtools-protocol/tot) - гугловский протокол удалённой отладки, через который можно делать много интересных штук, в том числе, вынимать данные

- [PySimpleGUI](https://pysimplegui.readthedocs.io/en/latest/) - забавная вещь:
кривой юзер-интерфейс пишется за 5 сек, а прямые конструкцией не предусмотрены, поэтому не пишутся и за год. Поскольку сделано на базе [Tk](http://www.tcl.tk/) с его вырвиглазной стилистикой и *нетрадиционным* подходом к обработке событий

Раньше на кинопоиске был хоть какой-никакой кривенький бэкап в Excel, но с некоторых пор и его не нахожу,
так что вот вам бэкап как есть с полным отказом от ответственности любого рода (as is, full disclaimer, responsibility refusal etc)

На всякий случай отмазка и от претензий Яндекса, если таковые будут иметь место: данный скрипт не управляет браузером,
не вносит никаких изменений в отображаемую сайтом информацию и не вмешивается в действия пользователя на сайте. Фактически, он делает то же, что мог бы делать вручную сам пользователь при помощи текстового редактора со страницей, сохранённой на диск

С функционалом и настройками решил не заморачиваться

- запускаете хром с ключиком **--remote-debugging-port=9230**
- запускаете этот скрипт, он откроет новую вкладку с кинопоиском

затем

- открываете в этой вкладке (именно в этой) нужную папочку с фильмами
- нажимаете волшебную кнопочку **Copy**
- данные допишутся в файл **kinopoisk_backup.txt**
- повторяете это столько раз, сколько у вас страниц с помеченными фильмами

Содержимое страниц HTML своих папок, как вы их видите под своим логином,
немножко отличается от содержимого чужих, доступных для просмотра, так что,
если хотите утащить чужое содержимое, то внизу меняете *copy_data_authorized()* на *copy_data_alien()*

Если порт 9230 у вас занят, то меняете на любой другой и исправляете соотв. строчку скрипта

Питон в моём случае 3.8, но, скорее всего, заработает и в более старом (не проверял). Установку самого питона и нужных модулей оставляю вам в качестве домашнего упражнения

Если Яндекс в очередной раз поменяет структуру страниц, и скрипт будет вылетать, то я ни при чём :)