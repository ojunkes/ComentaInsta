import ast
from csv import reader
from datetime import datetime
from random import randint
from selenium import webdriver
from time import sleep


page_comment = ""
comments = []
number_comments = 0
between_schedules = []
user = ""
password = ""


def get_params():
    global user
    global password
    global page_comment
    global comments
    global number_comments
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
            elif parameter[0] == "number_comments":
                number_comments = int(''.join(parameter[1].rsplit('\n')))
            elif parameter[0] == "between_schedules":
                between_schedules = ast.literal_eval('[%s]' % parameter[1])
    console_log(False, f"Usuário: {user}")
    if not password.isspace():
        console_log(False, f"Senha: ********")
    console_log(False, f"Página de comentário: {page_comment}")
    console_log(False, f"Comentário(s): {comments}")
    console_log(False, f"Número de comentário(s): {number_comments}")
    console_log(False, f"Executar entre horários: {between_schedules}")


def access_instagram():
    console_log(True, "Acessando Instagram")
    try:
        browser.get("http://www.instagram.com/")
    except ValueError as e:
        print(e)
        return False
    return True


def login_instagram():
    console_log(True, f"Efetuando Login com usuário: {user}")
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


def close_messages():
    console_log(True, "Fechando Mensagens de Confirmação")
    for i in range(2):
        console_log(False, f"Fechando Mensagem nº {i + 1}")
        try:
            button_not_now = browser.find_element_by_xpath("//button[text()='Agora não']")
            if button_not_now:
                button_not_now.click()
            sleep(3)
        except ValueError as e:
            print(e)
            return False
    return True


def access_page_comment():
    console_log(True, "Acessando Página de Comentário")
    browser.get(page_comment)

def access_page_secondary():
    console_log(True, "Acessando Página Secundária")
    #campo_pesquisa = browser.find_element_by_xpath("//input[@placeholder='Pesquisar']")
    if (randint(1, 6) % 2) == 0:
        browser.get("https://www.instagram.com/kellyjunkes/")
        #campo_pesquisa.send_keys('kellyjunkes')
        #campo_pesquisa.send_keys(keys.ENTER)
        #sleep(5)
        #campo_pesquisa = browser.find_element_by_xpath("//span[text()='Kelly Karoline Klock Junkes']")
        #campo_pesquisa.click()
        sleep(2)
        captura_foto = browser.find_element_by_xpath("//div/article/div/div/div/div/a[1]")
        captura_foto.click()
        sleep(3)
    else:
        browser.get("https://www.instagram.com/drijunkes_/")
        #campo_pesquisa.send_keys('jksandressa')
        #campo_pesquisa.send_keys(keys.ENTER)
        #sleep(5)
        #campo_pesquisa = browser.find_element_by_xpath("//span[text()='Andressa']")
        #campo_pesquisa.click()
        sleep(2)
        captura_foto = browser.find_element_by_xpath("//div/article/div/div/div/div/a[1]")
        captura_foto.click()
        sleep(3)


def comment():
    print("=============================================================")
    console_log(True, "Iniciando a publicação de comentários")
    x = 0
    while x < number_comments:
        schedule = False
        for time in between_schedules:
            time_now = int(datetime.now().strftime('%H%M'))
            if time[0] <= time_now < time[1]:
                console_log(False, "Abriu horário de comentários: " +
                            f"{'%s%s:%s%s' % tuple(str(time[0]).zfill(4))} " +
                            f"até {'%s%s:%s%s' % tuple(str(time[1]).zfill(4))}")
                schedule = True
                while time_now < time[1] and x < number_comments:

                    if (randint(1, 6) % 2) == 0:
                        access_page_secondary()
                    else:
                        access_page_comment()
                        try:
                            browser.find_element_by_class_name('Ypffh').click()
                            comment_field = browser.find_element_by_class_name('Ypffh')
                            type_like_a_person(x + 1, comments[randint(0, len(comments) - 1)], comment_field)
                            browser.find_element_by_xpath("//button[contains(text(), 'Publicar')]").click()
                            sleep(randint(5, 20))
                            time_now = int(datetime.now().strftime('%H%M'))
                            x += 1
                        except ValueError as err:
                            print(err)
                            x = number_comments
                            break
        if not schedule:
            console_log(False, "Fora do horário de trabalho, aguardar 1 minuto para próxima tentativa!")
            sleep(60)


def console_log(stage, message):
    if stage:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    else:
        print(f" =>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")


def type_like_a_person(comment_number, text, single_input_field):
    console_log(False, f"{str(comment_number).zfill(len(str(number_comments)))}/{number_comments} - " +
                f"{str((comment_number * 100) / number_comments).zfill(5)}% - Comentário: {text}")
    for letter in text:
        single_input_field.send_keys(letter)
        sleep(randint(1, 4) / 10)


# INICIO DA EXECUÇÃO
console_log(True, "Buscando Parâmetros")
get_params()
console_log(True, "Abrindo navegador")
browser = webdriver.Chrome()
browser.implicitly_wait(5)

access_instagram()
sleep(5)
login_instagram()
sleep(2)
close_messages()
sleep(2)
access_page_comment()
sleep(2)
comment()

console_log(True, f"Finalizou com Sucesso!")
browser.close()
input("Enter para fechar")
