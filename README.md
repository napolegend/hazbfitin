# Hazbfitin

__Работу сделал__:

**ФИО**:

Шигалугов Мурат Бесланович

**ИСУ**:

468089

# Установка софта
```
git clone https://github.com/napolegend/hazbfitin; cd hazbfitin; python3 -m pip install -r requirements.txt
```

# Запуск 
### Необходимо сначала запустить сервер на главном компьютере
```
cd hazbfitin; python3 server.py
```
Здесь вам нужно выбрать максимальное количество участников переговоров 

### Затем запускаются клиенты на главном компьютере и на остальных
```
cd hazbfitin; python3 main.py
```
Никнейм является уникальным и заполняется только с помощью английский букв и цифр

IP адрес указывается без порта, порт используется стандартный 50051, для главного компьютера использовать localhost

Пароль задается единожды первым пользователем, который выбрал пароль и отправил сообщение. Паролем может быть любая заранее оговоренная последовательность символов, пробелов, спецзнаков итд

## Примечание
Сервер хранит у себя сообщения в зашифрованном виде. Сервер не имеет доступа к ключам