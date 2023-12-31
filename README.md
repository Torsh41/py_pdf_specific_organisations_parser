# pypdfparser
## Synopsis:
  Retrieve information about organisations
## Usage:
pypdfparser PDF_FILE [-p] [-h]
  PDF_FILE - (string) Path to PDF file
                      Путь до PDF файла
  [-p] - (int) Specify page where organisations list starts
               Укажите страницу, на которой начинается перечисление организаций
  [-h] - display similar help message
## Nuance:
  The program works with an assumption that pdf file contains list of organisation names, descriotion and information in a particular order and with three separate fonts
  Бла блабла , сейчас 2 часа ночи, мне надо отчет писать.

# НЕ ВАЖНО
## Туториал:
  Чтобы пользоваться этой программой, ее можно либо импортировать и мучиться с исходным кодом, или использовать в командной строке с аргументами
## Пример:
  python3 pypdfparser.py spravochnik-moskva-2023.pdf -p 11
#### где:
  spravochnik-moskva-2023.pdf : путь до pdf файла
  -p 11 : номер страницы, на которой начинаетсяп перечисление организаций. (-p 11 === 12 страница)  
      * для spravochnik-moskva-2023.pdf - это 12 страница (-p 11)  
      * для spravochnik-moskovskaya-oblast-2023.pdf - это 8 страница (-p 7)  
## Принцип работы:
  Со страницы, обозначенной `-p`, собирается информация о шрифтах. Затем из списка шрифтов, расположенных в порядке поступления текста, запоминаются последние 3, условно: header, description и info шрифты.
  Далее по всем страницам, начиная с `-p`-ой считываются строки, определяется их абсолютное положение и шрифт, и по этим двум параметрам, в виде наброска, сохраняются в текстовый (не слишком форматированный) контейнер.
  В конце содержимое получившихся контейнеров сбрасывается в stdout.

## Почему не PHP?
  Я смог найти библиотеку (Smalot/PdfParser), но, по непонятной мне причине, она неправильно выводит текст, добавляет случайные символы на подобие '\d', или просто заменяет на них некоторые буквы киррилицы.  
  Все другие библиотеки не предоставляли возможности просмотра внутренностей pdf-ки.  
  
  Но потом я наткнулся на https://github.com/adeel/php-pdf-parser, что, как оказалось, переписанная на php библиотека pypdf (та, которую я сейчас использовал).
  Эту библиотеку можно скачать, дописать буквально 5-6 функций, и получить тоже самое, только на PHP.  
  Это мой план на недалекое будующее.
