from time import sleep
from random import randint
from selenium import webdriver

# CONFIGURAÇÕES PARA APLICAÇÃO
page_comment = "https://www.instagram.com/kellyjunkes/"
comments = ["@josecarlosklock", "@teste"]
user = "ojunkespro"
password = "Aa123456"
browser = ''


def access_instagram():
    print("Acessando Instagram")
    try:
        browser.get("http://www.instagram.com/")
    except e:
        print(e)
        return False
    return True


def login_instagram():
    print(f"Efetuando Login com usuário: {user}")
    try:
        field_user = browser.find_element_by_css_selector("input[name='username']")
        field_password = browser.find_element_by_css_selector("input[name='password")
        field_user.send_keys(user)
        field_password.send_keys(password)
        sleep(2)
        button_login = browser.find_element_by_xpath("//button[@type='submit']")
        button_login.click()
        sleep(2)
    except e:
        print(e)
        return False
    return True


def close_messages():
    print("Fechando Mensagens de Confirmação do Instagram")
    for i in range(2):
        print(f" Fechando Mensagen de Confirmação do Instagram nº {i+1}")
        try:
            button_not_now = browser.find_element_by_xpath("//button[text()='Agora não']")
            if button_not_now:
                button_not_now.click()
            sleep(3)
        except e:
            print(e)
            return False
    return True


def access_page_comment():
    print("Acessando Página de Comentário")
    browser.get(page_comment)
    """
    print("Pesquisar")
    campo_pesquisa = browser.find_element_by_xpath("//input[@placeholder='Pesquisar']")
    campo_pesquisa.send_keys('kellyjunkes')
    campo_pesquisa.send_keys(keys.ENTER)
    sleep(5)
    print("Vai clicar")
    campo_pesquisa = browser.find_element_by_xpath("//span[text()='Kelly Karoline Klock Junkes']")
    campo_pesquisa.click()
    """


def type_like_a_person(text, single_input_field):
    print("Escrevendo o Comentário")
    for letter in text:
        single_input_field.send_keys(letter)
        sleep(randint(1, 5) / 30)


# INICIO DA EXECUÇÃO
browser = webdriver.Chrome()
browser.implicitly_wait(5)

access_instagram()
sleep(5)
login_instagram()
sleep(2)
close_messages()
sleep(2)
access_page_comment()


print("clicar foto")
captura_foto = browser.find_element_by_xpath("//div/article/div/div/div/div/a[1]")
captura_foto.click()
sleep(3)

print("Comentando...")
browser.find_element_by_class_name('Ypffh').click()
campo_comentario = browser.find_element_by_class_name('Ypffh')
type_like_a_person("@josecarlosklock", campo_comentario)
'''
browser.find_element_by_xpath("//button[contains(text(), 'Publicar')]").click()
'''
sleep(20)

browser.close()

