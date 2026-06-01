Сортировщик писем
Программа автоматически читает письма из ZIP-архива и расскладывает их по папкам в зависимости от содержания письма

Структура проекта
mail_sorter_hackathon/
    |-sorted_emails/
     |-from_boss/
        |-mail_0005.txt
        |-mail_0011.txt
        |-mail_0014.txt
        |-mail_0016.txt
        |-mail_0017.txt
        |-mail_0022.txt
        |-mail_0023.txt
        |-mail_0025.txt
        |-mail_0029.txt
        |-mail_0033.txt
        |-mail_0038.txt
        |-mail_0041.txt
        |-mail_0049.txt
        |-mail_0052.txt
        |-mail_0055.txt
        |-mail_0057.txt
        |-mail_0060.txt
        |-mail_0062.txt
        |-mail_0065.txt
        |-mail_0067.txt
        |-mail_0071.txt
        |-mail_0073.txt
        |-mail_0074.txt
        |-mail_0082.txt
        |-mail_0085.txt
        |-mail_0087.txt
        |-mail_0093.txt
        |-mail_0095.txt
        |-mail_0098.txt
     |-inbox/
        |-mail_0001.txt
        |-mail_0003.txt
        |-mail_0006.txt
        |-mail_0007.txt
        |-mail_0008.txt
        |-mail_0010.txt
        |-mail_0013.txt
        |-mail_0015.txt
        |-mail_0018.txt
        |-mail_0019.txt
        |-mail_0020.txt
        |-mail_0021.txt
        |-mail_0024.txt
        |-mail_0026.txt
        |-mail_0027.txt
        |-mail_0028.txt
        |-mail_0030.txt
        |-mail_0031.txt
        |-mail_0032.txt
        |-mail_0034.txt
        |-mail_0035.txt
        |-mail_0036.txt
        |-mail_0037.txt
        |-mail_0039.txt
        |-mail_0040.txt
        |-mail_0042.txt
        |-mail_0043.txt
        |-mail_0044.txt
        |-mail_0045.txt
        |-mail_0046.txt
        |-mail_0047.txt
        |-mail_0048.txt
        |-mail_0050.txt
        |-mail_0051.txt
        |-mail_0053.txt
        |-mail_0054.txt
        |-mail_0056.txt
        |-mail_0058.txt
        |-mail_0059.txt
        |-mail_0061.txt
        |-mail_0063.txt
        |-mail_0066.txt
        |-mail_0068.txt
        |-mail_0069.txt
        |-mail_0070.txt
        |-mail_0072.txt
        |-mail_0075.txt
        |-mail_0076.txt
        |-mail_0077.txt
        |-mail_0078.txt
        |-mail_0079.txt
        |-mail_0080.txt
        |-mail_0081.txt
        |-mail_0083.txt
        |-mail_0084.txt
        |-mail_0086.txt
        |-mail_0088.txt
        |-mail_0089.txt
        |-mail_0090.txt
        |-mail_0091.txt
        |-mail_0092.txt
        |-mail_0094.txt
        |-mail_0096.txt
        |-mail_0097.txt
        |-mail_0099.txt
        |-mail_0100.txt
        |-mail_0102.txt
        |-mail_0103.txt
        |-mail_0107.txt
        |-mail_0108.txt
     |-spam/
        |-.DS_Store
        |-mail_0064.txt
        |-mail_0104.bin
        |-mail_0105.json
        |-mail_0106
        |-mail_0109.jpeg
     |-urgent/
        |-mail_0002.txt
        |-mail_0004.txt
        |-mail_0009.txt
        |-mail_0012.txt
        |-mail_0101.txt
    |src/
     |- __pycache__/
        |-actions.cpython-312.pyc
        |-email.cpython-312.pyc
        |-email_main.cpython-312.pyc
        |-parser.cpython-312.pyc
        |-reader.cpython-312.pyc
        |-rules_classifier.cpython-312.pyc
     |-actions.py
     |-email_main.py
     |-main.py
     |-parser.py
     |-reader.py
     |-rules_classifier.py
     |-run.sh

    |-test/
     |-test1.py
     |-test2.py
     |-test_letter1
     |-test_letter10.txt
     |-test_letter11
     |-test_letter12
     |-test_letter13
     |-test_letter14
     |-test_letter15
     |-test_letter16
     |-test_letter17
     |-test_letter18
     |-test_letter19
     |-test_letter2
     |-test_letter20
     |-test_letter3
     |-test_letter4
     |-test_letter5
     |-test_letter6
     |-test_letter7.txt
     |-test_letter8.txt
     |-test_letter9.txt
    |-.gitignore
    |-README.md
    |-TP_Hackathon.ipynb
    |-inbox.zip

Как это работает
1.Reader открыть ZIP-архив и пересчитать все файлы внутри
2.Для каждого .txt-файла LetterExtractorпарсит его в объект Letter
3.main_classifier последнее письмо по набору правил и определению параметра
4.emailsort переносит файл в соответствующий адрес внутри sorted_emails/
5.В конце выводится статистика по категориям

Критерии сортировки
from_boss #письма имеют отправителя
spam      #письма, которые содержат слова: акция,выигрыш, лотерея
urgent    #письма которое содежит слова:срочно, критично и т.д.
inbox     #письма, все остальные


Инструкция по запуску программы :
1) Закинуть архив с письмами "inbox.zip" в корневую папку проекта(важно, чтобы там лежал файл main.py!)
2) Открыть терминал в папке проекта , дать скрипту права для запуска:
 ```bash
    chmod +x run.sh
3) Запустить сам скрипт :
 ./run.sh
