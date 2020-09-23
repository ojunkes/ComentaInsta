import ast
from csv import reader
from datetime import datetime
from random import randint
from selenium import webdriver
from time import sleep

#ComentaInsta.ini
page_comment = ""
comments = []
total_comments = 0
between_schedules = []
user = ""
password = ""

#Global Variables
number_comments = 0


def get_params():
    console_log(True, "Buscando Parâmetros")
    global user
    global password
    global page_comment
    global comments
    global total_comments
    global between_schedules
    with open("ComentaInsta.ini", "r") as text_file:
        parameters = reader(text_file, delimiter='=')
        for parameter in parameters:
            if parameter[0] == "user":
                user = ''.join(parameter[1].rsplit('\n'))
            elif parameter[0] == "password":
                password = ''.join(parameter[1].rsplit('\n'))
            elif parameter[0] == "page_comment":
                page_comment = ''.join(parameter[1].rsplit('\n'))
            elif parameter[0] == "comments":
                comments = ''.join(parameter[1].rsplit('\n')).split(",")
            elif parameter[0] == "total_comments":
                total_comments = int(''.join(parameter[1].rsplit('\n')))
            elif parameter[0] == "between_schedules":
                between_schedules = ast.literal_eval('[%s]' % parameter[1])
    console_log(False, f"Usuário: {user}")
    if not password.isspace():
        console_log(False, f"Senha: ********")
    console_log(False, f"Página de comentário: {page_comment}")
    console_log(False, f"Comentário(s): {comments}")
    console_log(False, f"Número de comentário(s): {number_comments}")
    #console_log(False, f"Executar entre horários: {between_schedules}")


def access_instagram():
    try:
        browser.get("http://www.instagram.com/")
    except ValueError as e:
        print(e)
        return False
    return True


def login_instagram():
    try:
        field_user = browser.find_element_by_css_selector("input[name='username']")
        field_password = browser.find_element_by_css_selector("input[name='password")
        field_user.send_keys(user)
        field_password.send_keys(password)
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


def comment_v1():
    print("=============================================================")
    console_log(True, "Iniciando a publicação de comentários")
    x = 0
    while x < total_comments:
        schedule = False
        for time in between_schedules:
            time_now = int(datetime.now().strftime('%H%M'))
            if time[0] <= time_now < time[1]:
                console_log(False, "Abriu horário de comentários: " +
                            f"{'%s%s:%s%s' % tuple(str(time[0]).zfill(4))} " +
                            f"até {'%s%s:%s%s' % tuple(str(time[1]).zfill(4))}")
                schedule = True
                while time_now < time[1] and x < total_comments:
                    access_page_comment()
                    sleep(2)
                    try:
                        browser.find_element_by_class_name('Ypffh').click()
                        comment_field = browser.find_element_by_class_name('Ypffh')
                        type_like_a_person(x + 1, comments[randint(0, len(comments) - 1)], comment_field)
                        #browser.find_element_by_xpath("//button[contains(text(), 'Publicar')]").click()
                        sleep(randint(60, 70))
                        time_now = int(datetime.now().strftime('%H%M'))
                        x += 1
                    except ValueError as err:
                        print(err)
                        break
        if not schedule:
            console_log(False, "Fora do horário de trabalho, aguardar 1 minuto para próxima tentativa!")
            sleep(60)


def comment_v2():
    global number_comments
    print("=============================================================")
    number_comments_cicle = 0
    number_limit_comments = randint(20, 70)
    while number_comments_cicle < number_limit_comments:
        loaded_page = False
        if randint(2, 6) % 2 == 0 or number_comments_cicle == 0:
            loaded_page = True
            access_page_comment()
            sleep(3)
        try:
            browser.find_element_by_class_name('Ypffh').click()
            comment_field = browser.find_element_by_class_name('Ypffh')
            type_like_a_person(number_comments + 1, loaded_page, comments[randint(0, len(comments) - 1)], comment_field)
            browser.find_element_by_xpath("//button[contains(text(), 'Publicar')]").click()
            sleep(randint(40, 80))
            number_comments += 1
        except ValueError as err:
            print(err)
            break
        number_comments_cicle += 1


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

while number_comments < total_comments:
    console_log(True, "Abrindo navegador")
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    console_log(True, "Acessando Instagram")
    access_instagram()
    sleep(5)
    console_log(True, f"Efetuando Login com usuário: {user}")
    login_instagram()
    sleep(2)
    console_log(True, f"Efetuando Comentários")
    comment_v2()
    console_log(True, f"Fechando browser")
    browser.close()
    sleep(2)

console_log(True, f"Finalizou com Sucesso!")
input("Enter para fechar")
