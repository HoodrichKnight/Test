import time
import re
import threading
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException

def is_valid_proxy(proxy: str) -> bool: #Проверка прокси на правильный формат через регулярку
    proxy_valid = re.compile(r'^(http://|https://|socks5://)?([a-zA-Z0-9._-]+(:[0-9]+)?)(:[0-9]{1,5})?$')
    return proxy_valid.match(proxy) is not None

def is_valid_mail(email: str) -> bool: #Проверка формата почты по аналогии с прокси
    email_valid = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return email_valid.match(email) is not None

def check_exists_message() -> bool: #Проверка на то, есть ли сообщение на странице о том, что пользователь не зареган
    try:
        driver.find_element(By.ID, 'i0116Error') #Поиск сообщения об ошибке по его айди
    except NoSuchElementException:
        return True
    return False

def checker(email: str, proxy: str) -> Optional[bool]: #Проверка регистрации соотвественно, включая проверку на ошибки и прочее
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument('--lang=en')

    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://login.live.com')
    driver.set_page_load_timeout(10)

    if not is_valid_proxy(proxy):
        return None

    if not is_valid_mail(email):
        return None

    try:
        email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'i0116'))) #Поиск поля для ввода майла
        email_field.send_keys(email)
        email_field.submit()

        time.sleep(5)

        if check_exists_message() is False:
            return True
        elif check_exists_message() is True:
            return False
        else:
            return None

    except (WebDriverException, TimeoutException) as e:
        return None
    finally:
        driver.close()

def thread_checker(email: str, proxy: str): #Запускает проверку в отдельном потоке
    result = checker(email, proxy)
    print(f'Email: {email} Registered: {result}')

if __name__ == "__main__":
    emails = [
        'gcbifaop45@mail.ru', 'yfyqdhiu29@mail.ru', 'qpqvzdmc81@bk.ru', 'eiucoyru86@gmail.com', 'tmttzxnf67@yandex.ru',
        'bcfxjlgn14@yahoo.com', 'lelexgrm64@list.ru', 'ieofala16@gmail.com', 'bybeekre73@hotmail.com',
        'xzrqtzgs24@internet.ru', 'buaevukd77@mail.ru', 'glibeldc41@yahoo.com', 'nnpxeqsn33@internet.ru',
        'zvlunjtq36@mail.ru', 'uvyxvuxk48@internet.ru', 'olghigzv61@mail.ru', 'ioroubol10@inbox.ru',
        'vsccesve17@list.ru', 'rqlzqfex45@yahoo.com', 'zrbxnjrl92@internet.ru', 'eioortjv44@gmail.com',
        'uuydecfc84@list.ru', 'dimdxcvv81@yandex.ru', 'etvxgodp96@inbox.ru', 'lbmldrkz69@hotmail.com',
        'nyntgacx55@yahoo.com', 'nvgiabuw15@aol.com', 'mrstictq41@yahoo.com', 'mkuurqhh11@gmail.com',
        'ldpcudfn5@list.ru', 'bsaotogb73@list.ru', 'relsoaqa4@yahoo.com', 'dqaauqdw27@yandex.ru', 'anvlynen95@bk.ru',
        'vqfitqmx6@inbox.ru', 'stuvchrw25@mail.ru', 'bnfxwqfu27@yandex.ru', 'irsuscqj46@aol.com',
        'oqrdtjst48@yandex.ru', 'mooqzjlx42@aol.com'
    ] #Рандом майлы для теста
    proxy = "" #Прокси

    threads = []
    max_threads = 100

    for email in emails:
        thread = threading.Thread(target=thread_checker, args=(email, proxy))
        threads.append(thread)
        thread.start()

        if len(threads) >= max_threads: #Если потоки превышают лимит, то ждем, пока потоки завершатся
            for thread in threads:
                thread.join() #Дожидаемся, пока все потоки завершатся
            threads = [] #Ресетаем потоки

    for thread in threads:
        thread.join()



'''Corner-кейсы, которые могут возникнуть с потоками: 
1. Race Conditions
2. Нехватка ресурсов
3. Передача ошибок из одного потока в другой
4. Разные таймауты у потоков
5. Проблемы с объединением потоков
6. Ограничения у прокси

Решенные corner-кейсы:
1. Проверка формата прокси
2. Проверка формата почты
3. Обработка таймаутов у вебдрайвера
4. Многопоточность для параллельных проверок
5. Добавление ограничения потоков, чтобы исключить перегрузку'''
