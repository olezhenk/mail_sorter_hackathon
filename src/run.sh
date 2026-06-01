#!/bin/bash

echo "Пристегнитесь, мы взлетаем(ну типо запуск классификатора писем)"
if [ ! -f "inbox.zip" ]; then
    echo "Ошибка: Забыл закинуть inbox.zip в папку!"
    exit 1
fi
python3 main.py
if [ $? -eq 0 ]; then
    echo "Все разложилось по папкам, все супер"
else
    echo "Произошли технические неполадки"
fi
      
