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
        console_log(False, f"Fechando Mensage nº {i + 1}")
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
    """
    browser.get("https://www.instagram.com/kellyjunkes/")
    print("Pesquisar")
    campo_pesquisa = browser.find_element_by_xpath("//input[@placeholder='Pesquisar']")
    campo_pesquisa.send_keys('kellyjunkes')
    campo_pesquisa.send_keys(keys.ENTER)
    sleep(5)
    print("Vai clicar")
    campo_pesquisa = browser.find_element_by_xpath("//span[text()='Kelly Karoline Klock Junkes']")
    campo_pesquisa.click()    
    sleep(2)
    print("clicar foto")
    captura_foto = browser.find_element_by_xpath("//div/article/div/div/div/div/a[1]")
    captura_foto.click()
    sleep(3)
    """


def console_log(stage, message):
    if stage:
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")
    else:
        print(f" =>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")


def type_like_a_person(text, single_input_field):
    console_log(False, f"Escrevendo o Comentário: {text}")
    for letter in text:
        single_input_field.send_keys(letter)
        sleep(randint(1, 5) / 10)


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

# FAZER O QUE VIEMOS FAZER, COMENTAR!!!!!
console_log(True, "Iniciando a publicação de comentários")
x = 0
while x < number_comments:
    time_now = int(datetime.now().strftime('%H%M'))
    for time in between_schedules:
        if time[0] <= time_now <= time[1]:
            while time_now <= time[1] and x < number_comments:
                try:
                    console_log(False, f"Comentário de número: {x + 1}")
                    sleep(randint(2, 10))
                    browser.find_element_by_class_name('Ypffh').click()
                    comment_field = browser.find_element_by_class_name('Ypffh')
                    type_like_a_person(comments[randint(0, len(comments) - 1)], comment_field)
                    #browser.find_element_by_xpath("//button[contains(text(), 'Publicar')]").click()
                    x += 1
                except ValueError as err:
                    print(err)
                    x = number_comments
                    break

console_log(True, f"Finalizou com Sucesso!")
browser.close()
input("Enter para fechar")
