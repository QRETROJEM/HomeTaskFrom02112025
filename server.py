#Server.py
import socket # Модуль для работы с TCP/UDP сокетами
from datetime import datetime # Возможность вывести текущее время на странице

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Создание серверного сокета IPv4 | TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Разрешение немедленно повторно использовать этот адрес
server_socket.bind(('127.0.0.1', 8080)) # Привязка к адресу и порту
server_socket.listen(5) # Перевод сокета в режим ожидания подключений

print("Сервер запущен на http://127.0.0.1:8080")
print("Нажмите Ctrl+C для остаовки")

try:            # Обработчик критических ошибок, позволяющий серверу функционировать при сбои
    while True:         # Основной цикл сервера
        client_socket, addr = server_socket.accept() # блокирует выполнение, пока кто-то не подключится
        print(f"Подключение от {addr}")
        
        request_data = b""
        while True:
            chunk = client_socket.recv(1024) # Получает до 1024 байт из соединения и в случае превышения допустимого числа - заканчивает цикл
            if not chunk:
                break # End...
            request_data += chunk
            if b'\r\n\r\n' in request_data:
                break # End...
        
        request = request_data.decode('utf-8', errors='ignore') # превращает байты в строку
        
        first_line = request.split('\n')[0]
        path = first_line.split()[1]
        
        print(f"Запрошен путь: {path}") # Выводит в консоль, что запросил клиент.
        # Роутинг (выбор ответа по пути)
            # Если путь ровно /, формируем тело страницы и код 200
        if path == '/':
            response_body = "<h1>Hello, Web!</h1>"
            status_code = "200 OK"
            # Если путь /about, формируем другую HTML‑страницу
        elif path == '/about':
            response_body = f"""
            <h1>О сервере</h1>
            <p>Простой сокет-сервер на Python</p>
            <p>Поддерживаемые пути: <code>/</code>, <code>/about</code>, <code>/time</code></p>
            """
            status_code = "200 OK"
            # берёт текущее время и форматирует строкой - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -
        elif path == '/time':
            response_body = f"""
            <h1>Текущее дата и время</h1>
            <p>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p> 
            <p>Поддерживаемые пути: <code>/</code>, <code>/about</code>, <code>/time</code></p>
            """
            status_code = "200 OK"
            # браузер увидит, что страница не найдена
        else:
            response_body = """
            <h1>404 Not Found</h1>
            <p>Запрошенная страница не найдена!</p>
            <p>Поддерживаемые пути: <code>/</code>, <code>/about</code>, <code>/time</code></p>
            """
            status_code = "404 Not Found"
        
        response_body_bytes = response_body.encode('utf-8')
        response = f"""HTTP/1.1 {status_code}   
Content-Type: text/html; charset=utf-8
Content-Length: {len(response_body_bytes)}

{response_body}""".encode('utf-8')
        # Content-Type: text/html; charset=utf-8 - говорим браузеру, что это HTML в UTF‑8
        # Content-Length: - сколько байт в теле, чтобы браузер знал, когда ответ закончился.
        # по стандарту HTTP строки должны заканчиваться \r\n, а разделитель заголовков и тела должен быть \r\n\r\n
        client_socket.send(response) # Отправляет байты ответа по TCP соединению
        client_socket.close() # Закрытие клиентского соединения
        
except KeyboardInterrupt: # Обработка остановки сервера, Срабатывает при Ctrl+C в терминале
    print("\nСервер остановлен")
finally:
    server_socket.close()
