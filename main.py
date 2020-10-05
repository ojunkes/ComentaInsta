import ast
from csv import reader
from datetime import datetime
from random import randint
from selenium import webdriver
from time import sleep

# ComentaInsta.ini
from selenium.common.exceptions import ElementClickInterceptedException

logins = []
page_comment = ""
comments = []
total_comments = 0
time_between_comments = 120
total_comments_change_login = 60

# Global Variables
number_comments = 0
error_click = False
database = 'ComentaInsta.db'
login_control = 0
login_user = ''


def get_params():
    console_log(True, "Buscando Parâmetros")
    global logins
    global page_comment
    global comments
    global total_comments
    global time_between_comments
    global total_comments_change_login
    with open("ComentaInsta.ini", "r") as text_file:
        parameters = reader(text_file, delimiter='=')
        for parameter in parameters:
            if parameter[0] == "logins":
                logins = ast.literal_eval('[%s]' % parameter[1])
            elif parameter[0] == "page_comment":
                page_comment = ''.join(parameter[1].rsplit('\n'))
            elif parameter[0] == "comments":
                comments = ''.join(parameter[1].rsplit('\n')).split(",")
            elif parameter[0] == "total_comments":
                total_comments = int(''.join(parameter[1].rsplit('\n')))
            elif parameter[0] == "time_between_comments":
                time_between_comments = int(''.join(parameter[1].rsplit('\n')))
            elif parameter[0] == "total_comments_change_login":
                total_comments_change_login = int(''.join(parameter[1].rsplit('\n')))
    for i in range(len(logins)):
        console_log(False, f"Login ({i + 1})")
        console_log(False, f"Usuário: {logins[i][0]}")
        if not str.isspace(logins[i][1]):
            console_log(False, "Senha: ********")
    console_log(False, f"Página de comentário: {page_comment}")
    console_log(False, f"Comentário(s): {comments}")
    console_log(False, f"Total de comentário(s): {total_comments}")
    console_log(False, f"Tempo entre comentário: {time_between_comments}")
    console_log(False, f"Total comentários para mudar login: {total_comments_change_login}")


def read_number_comment():
    console_log(True, "Buscando Total de Comentários já realizados")
    global database
    amount = 0
    try:
        with open(database, "r") as text_file:
            text = text_file.read()
            if text != '':
                amount = int(text)
    except FileNotFoundError:
        console_log(False, f"Arquivo não existe")
    console_log(False, f"Qtd. Total: {amount}")
    return amount


def access_instagram():
    try:
        browser.get("http://www.instagram.com/")
    except ValueError as e:
        print(e)
        return False
    return True


def login_instagram():
    global login_control
    global login_user
    try:
        field_user = browser.find_element_by_css_selector("input[name='username']")
        field_password = browser.find_element_by_css_selector("input[name='password")
        if error_click is True:
            console_log(True, "Campo comentário DISABILITADO, mudando de login!")
        login_control += 1
        if login_control > (len(logins) - 1):
            login_control = 0
        console_log(True, f"Login com usuário: {logins[login_control][0]}")
        login_user = logins[login_control][0]
        field_user.send_keys(logins[login_control][0])
        field_password.send_keys(logins[login_control][1])
        sleep(2)
        button_login = browser.find_element_by_xpath("//button[@type='submit']")
        button_login.click()
        sleep(2)
    except ValueError as e:
        print(e)
        return False
    return True


def access_page_comment():
    browser.get(page_comment)


def comment():
    global number_comments
    global error_click
    global time_between_comments
    global login_user
    print("=============================================================")
    number_comments_cicle = 0
    number_limit_comments = randint(20, 70)
    while number_comments_cicle < number_limit_comments:
        loaded_page = False
        #if randint(2, 6) % 2 == 0 or number_comments_cicle == 0 or error_click is True:
        if number_comments_cicle == 0:
            loaded_page = True
            access_page_comment()
            sleep(3)
        try:
            browser.find_element_by_class_name('Ypffh').click()
            comment_field = browser.find_element_by_class_name('Ypffh')
            text = ''
            while text == '':
                text = comments[randint(0, len(comments) - 1)]
                if login_user in text:
                    text = ''
            type_like_a_person(number_comments + 1, loaded_page, text, comment_field)
            browser.find_element_by_xpath("//button[contains(text(), 'Publicar')]").click()
        except ValueError as err:
            number_comments -= 1    # Considerando que o comentário anterior também deu erro
            write_number_comment()
            print(f"Exceção(ValueError): {err}")
            break
        except ElementClickInterceptedException as err:
            error_click = True
            number_comments -= 1    # Considerando que o comentário anterior também deu erro
            write_number_comment()
            print(f"Exceção(ElementClickInterceptedException): {err}")
            break
        number_comments += 1
        write_number_comment()
        sleep(randint(time_between_comments, time_between_comments + 10))
        number_comments_cicle += 1
        if number_comments_cicle > total_comments_change_login:
            break


def write_number_comment():
    global database
    global number_comments
    text_file = open(database, "w+")
    text_file.write(str(number_comments))
    text_file.close()


def console_log(stage, message):
    if stage:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    else:
        print(f" =>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")


def type_like_a_person(comment_number, loaded_page, text, single_input_field):
    if loaded_page:
        console_log(False, f"{str(comment_number).zfill(len(str(total_comments)))}/{total_comments} - " +
                    f"{str((comment_number * 100) / total_comments).zfill(5)}% - Comentário: {text} **")
    else:
        console_log(False, f"{str(comment_number).zfill(len(str(total_comments)))}/{total_comments} - " +
                    f"{str((comment_number * 100) / total_comments).zfill(5)}% - Comentário: {text}")
    for letter in text:
        single_input_field.send_keys(letter)
        sleep(randint(1, 4) / 10)


# INICIO DA EXECUÇÃO
get_params()
number_comments = read_number_comment()
while number_comments < total_comments:
    console_log(True, "Abrindo navegador")
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    console_log(True, "Acessando Instagram")
    access_instagram()
    sleep(5)
    console_log(True, f"Efetuando Login")
    login_instagram()
    sleep(2)
    console_log(True, f"Efetuando Comentários")
    error_click = False
    comment()
    console_log(True, f"Fechando browser")
    browser.close()
    sleep(2)

console_log(True, f"Finalizou com Sucesso!")
input("Enter para fechar")
