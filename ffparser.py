
#Script was created by kustiktm_kirill
#https://github.com/kustiktmkirill

import random
import os
import datetime
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time, pickle
import colorama
from colorama import Fore, Back

vk_session = vk_api.VkApi(token='0e9cb40ec710cb86355bfc6f7ccc8cd4b43415bafb8417d1d2f6524179bb499ac534625116d101f40a793')
longpoll = VkBotLongPoll(vk_session, 194807625 )
vk = vk_session.get_api()

colorama.init()

browser_options = Options()
browser_options.add_argument("--headless")
browser_options.add_argument("--window-size=2560x1440")
browser_options.add_argument("--disable-web-security")
chrome_driver = "files/chromedriver"

def pars(testfox_num = 0, peer_id = 0):
    if testfox_num == 0:
        vk.messages.send(
            random_id=get_random_id(),
            message="Некорректный запрос",
            peer_id=peer_id
        )
        vkbot()
    testfox_num = str(testfox_num)
    if os.path.exists('./train' + testfox_num + '/answers.txt') == True:
        file_name = vk_api.upload.VkUpload(vk).document_message(
            doc='./train' + testfox_num + '/answers.txt',
            peer_id=peer_id,
            title='train' + testfox_num,
            tags='121'
        )
        owner = file_name['doc']['owner_id']
        doc_id = file_name['doc']['id']
        vk.messages.send(
            random_id=get_random_id(),
            message="Данный тест уже был пройден",
            peer_id=peer_id,
            attachment='doc' + str(owner) + '_' + str(doc_id)
        )
        vkbot()
    print(Fore.YELLOW+"[" + datetime.datetime.today().strftime("%H:%M:%S") + "][QST]" + " Номер теста - " + str(testfox_num))
    url_pars_num = testfox_num
    url_pars = "https://foxford.ru/trainings/" + str(url_pars_num)
    print(Fore.YELLOW+"[" + datetime.datetime.today().strftime("%H:%M:%S") + "][QST]" + " Как Вы желаете получить ответы? Выберите вариант и введите цифру:\n1) Поместить ответы в текстовый файл\n2) Создать скриншоты ответов")
    variant = 1#int(input())
    driver_pars = webdriver.Chrome(options=browser_options, executable_path=chrome_driver)
    driver_pars.get("https://foxford.ru/dashboard")
    time.sleep(1)
    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][INFO]" + " Загрузка cookies из cookies.pkl...")
    with open('files/cookies.pkl', 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            if 'expiry' in cookie:
                del cookie['expiry']
            driver_pars.add_cookie(cookie)
    driver_pars.get(url_pars)
    time.sleep(2)
    tryes = 0

    while True:
        try:
            test_label = driver_pars.find_element_by_class_name("MathContent_content__EYPV_").text
            part_count_label = driver_pars.find_element_by_css_selector("span.Text_weight-bold__2PiyR").text
            part_count = part_count_label.split()[0]
        except NoSuchElementException:
            tryes += 1
            if tryes == 3:
                vk.messages.send(
                    random_id=get_random_id(),
                    message='Тест №' +  testfox_num + " не существует, или произошла ошибка",
                    peer_id=peer_id
                )
                break
                vkbot()
            else:
                pass
        vk.messages.send(
            random_id=get_random_id(),
            message='Тест №' + testfox_num + ":\n" + test_label + "\nТест состоит из " + part_count_label + "\nНачинаю работать...",
            peer_id=peer_id
        )
        tryes = 0
        break

    print(Fore.YELLOW + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][TRN]" + " Тест - " + test_label)
    print(Fore.YELLOW + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][TRN]" + " Тест состоит из " + part_count_label)
    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][PARS]" + " Приступаю к парсингу ответов...")
    try:
        driver_pars.find_element_by_class_name("Button_root__2dkqG").click()
        time.sleep(2)
        driver_pars.find_element_by_xpath('//*[@class="indicator_root__xvUCE"]/a[' + str(part_count) + ']').click()
        time.sleep(5)
        driver_pars.find_element_by_id("training-task-page-skip").click()
        time.sleep(2)
        driver_pars.find_element_by_id("training-complete-btn").click()
        driver_pars.find_element_by_id("training-complete-btn").click()
        time.sleep(2)
        driver_pars.find_element_by_id("training-main-page-btn").click()
        print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][PRS]" + " Ответы получены. Выгружаю...")
        num_train = url_pars.split('/')[4]
        os.mkdir("./train" + num_train)
        if variant == 1:
            open('./train' + num_train + '/answers.txt', "w").close()
            with open('./train' + num_train + '/answers.txt', "w") as ans:
                ans.write("FoxFordParser by kustiktm_kirill - Trainings " + num_train)
                ans.write("\n---------------------------------------------------------")
                for i in range(int(part_count)):
                    driver_pars.find_element_by_xpath('//*[@class="indicator_root__xvUCE"]/a[' + str(i + 1) + ']').click()
                    time.sleep(3)
                    temp_label = driver_pars.find_element_by_xpath('//*[@class="MathContent_content__EYPV_"]/p').text
                    if temp_label == ' ':
                        temp_label = driver_pars.find_element_by_xpath('//*[@class="MathContent_content__EYPV_"]/p[@dir="ltr"]/span').text
                    try:
                        #Радио и чекбоксы
                        check = driver_pars.find_element_by_xpath('//*[@class="styles_root__H6s8Y styles_isSolved__2osPp"]')
                        true_anss = driver_pars.find_elements_by_xpath('//*[@class="styles_root__H6s8Y styles_isSolved__2osPp styles_isCorrect__uutk1"]/div[@class="Text_root__3j40U Text_weight-normal__2T_yh Text_lineHeight-m__2YyYN Text_fontStyle-normal__264_c MathContent_root__2UyVb styles_label__1qiS3 Color_color-inherit__27FNT"]/span')
                        ans.write("\n\nВопрос " + str(i+1) + ": " + temp_label + "\nОтветы: ")
                        for j in range(len(true_anss)):
                            temp_ans = driver_pars.find_element_by_xpath('//*[@class="styles_root__H6s8Y styles_isSolved__2osPp styles_isCorrect__uutk1"]['+ str(j+1) +']/div[@class="Text_root__3j40U Text_weight-normal__2T_yh Text_lineHeight-m__2YyYN Text_fontStyle-normal__264_c MathContent_root__2UyVb styles_label__1qiS3 Color_color-inherit__27FNT"]/span').text
                            ans.write("\n" + temp_ans)
                        print("1")
                    except NoSuchElementException:
                        try:
                            check = driver_pars.find_element_by_xpath('//*[@class="LinkTaskRow_linkRowContent__3bAkC"]')
                            true_anss = driver_pars.find_elements_by_xpath('//*[@class="LinkTaskRow_linkRow__umxSp LinkTaskRow_text-text__u-c5e"]')
                            ans.write("\n\nВопрос " + str(i + 1) + ": " + temp_label + "\nОтветы: ")
                            for k in range(len(true_anss)):
                                ans_label = driver_pars.find_element_by_xpath('//*[@class="LinkTaskRow_linkRow__umxSp LinkTaskRow_text-text__u-c5e"][' + str(k + 1) + ']/div[@class="Text_root__3j40U Text_weight-normal__2T_yh Text_lineHeight-m__2YyYN Text_fontStyle-normal__264_c MathContent_root__2UyVb LinkTaskRow_linkRowTarget__2c1Mf LinkTaskRow_text__2LNwT Color_color-inherit__27FNT"]/span').text
                                true_ans = driver_pars.find_element_by_xpath('//*[@class="LinkTaskRow_linkRow__umxSp LinkTaskRow_text-text__u-c5e"][' + str(k + 1) + ']/div[@class="LinkTaskRow_linkRowContent__3bAkC"]/div[@class="Answer_root__1N6oB Answer_correct__N9Lhp Answer_text__1qKz5 Answer_size-m__J9HeQ"]/div/span').text
                                ans.write("\n" + ans_label + " -> " + true_ans)
                            print("2")
                        except NoSuchElementException:
                            try:
                                #Поле ввода
                                check = driver_pars.find_element_by_xpath('//*[@class="PadMarg_margin-top-52__3gZf8 PadMarg_margin-bottom-52__3tS2d"]')
                                ans.write("\n\nВопрос " + str(i + 1) + ": " + temp_label + "\n Ответ: ")
                                temp_ans = driver_pars.find_element_by_xpath('//*[@class="PadMarg_margin-top-32__1uRQ1 PadMarg_margin-bottom-52__3tS2d"]/div[3]/div/div[2]/div/div/div[@class="Solved_input__1Tm-3"]').text
                                ans.write("\n" + temp_ans)
                                true_anss = driver_pars.find_elements_by_xpath('//*[@class="PadMarg_margin-top-52__3gZf8 PadMarg_margin-bottom-52__3tS2d"]')
                                for n in range(len(true_anss)):
                                    temp_ans = driver_pars.find_element_by_xpath('//*[@class="PadMarg_margin-top-52__3gZf8 PadMarg_margin-bottom-52__3tS2d"]['+ str(n+1) +']/div[3]/div/div[2]/div/div/div[@class="Solved_input__1Tm-3"]').text
                                    ans.write(", " + temp_ans)
                                print("3")
                            except NoSuchElementException:
                                try:
                                    check = driver_pars.find_element_by_xpath('//*[@class="PadMarg_margin-top-32__1uRQ1 PadMarg_margin-bottom-52__3tS2d"]')
                                    check = driver_pars.find_element_by_xpath('//*[@class="Solved_input__1Tm-3 Solved_user__2d3fz Solved_incorrect__1EPW6 Solved_empty__G5aM_"]')
                                    ans.write("\n\nВопрос " + str(i + 1) + ": " + temp_label + "\nОтвет: ")
                                    true_anss = driver_pars.find_elements_by_xpath('//*[@class="PadMarg_margin-top-32__1uRQ1 PadMarg_margin-bottom-52__3tS2d"]/div/div/div[2]/div[@class="Solved_block__3q-AW"]')
                                    for h in range(len(true_anss)):
                                        true_ans = driver_pars.find_element_by_xpath('//*[@class="PadMarg_margin-top-32__1uRQ1 PadMarg_margin-bottom-52__3tS2d"]/div/div/div[2]/div[@class="Solved_block__3q-AW"]['+ str(h+1) +']/div/div').text
                                        ans.write(true_ans + ", ")
                                    print("4")
                                except NoSuchElementException:
                                    try:
                                        check = driver_pars.find_elements_by_xpath('//*[@class="FillGapsTask_paragraph__36OSG"]')
                                        ans.write("\n\nВопрос " + str(i + 1) + ": " + temp_label + "\nОтветы: ")
                                        tr_ans_count = 0
                                        for m in range(len(check)):
                                            true_anss = driver_pars.find_elements_by_xpath('//*[@class="FillGapsTask_paragraph__36OSG"]['+str(m+1)+']/span[@class="Answer_root__2n-6o"]')
                                            for l in range(len(true_anss)):
                                                true_ans = " "
                                                try:
                                                    #true_ans = driver_pars.find_element_by_xpath('//*[@class="Answer_root__2n-6o"][' + str(l + 1) + ']/span[2]/span').text
                                                    ans.write("\n" + str(tr_ans_count + 1) + ") " + true_anss[l].text)
                                                    tr_ans_count += 1
                                                    #print("part1")
                                                    print(true_anss[l].text)
                                                except NoSuchElementException:
                                                    try:
                                                        true_ans = driver_pars.find_element_by_xpath('//*[@class="Answer_root__2n-6o"][' + str(l + 1) + ']/span[@class="Text_root__3j40U Text_weight-normal__2T_yh Text_lineHeight-m__2YyYN Text_fontStyle-normal__264_c MathContent_root__2UyVb AnswerCheck_root__2aLs8 AnswerCheck_correctAnswer__2_byl Display_display-inline__306hu Color_color-inherit__27FNT"]/span[@class="MathContent_content__EYPV_"]').text
                                                        ans.write("\n" + str(tr_ans_count + 1) + ") " + true_ans)
                                                        tr_ans_count += 1
                                                        #print("part2")
                                                    except NoSuchElementException:
                                                        #print("err =(")
                                                        pass
                                    except NoSuchElementException as fff:
                                        print(Fore.YELLOW + "-----------------------------------------------------------------------")
                                        print(Fore.YELLOW + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][WARN]" + " Задание - " + str(i+1))
                                        print(Fore.YELLOW + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][WARN]" + " Произошла ошибка! Видимо, вид данного задания не учтен в скрипте. Свяжитесь, пожалуйста, с разработчиком.")
                                        print(Fore.YELLOW + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][WARN]" + " Вы можете выбрать 2 вариант - создание скриншотов. Программа продолжает работу...")
                                        print(Fore.YELLOW + "-----------------------------------------------------------------------")
                    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][PRS]" + " Ответ на задание " + str(i+1) + " записан")
        """elif variant == 2:
            for i in range(int(part_count)):
                driver_pars.find_element_by_xpath('//*[@class="indicator_root__xvUCE"]/a[' + str(i+1) + ']').click()
                time.sleep(1)
                driver_pars.get_screenshot_as_file("./train" + num_train + "/" + str(i+1) + ".png")
                print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][PRS]" + " Создан скриншот задания " + str(i+1))
            print(Fore.GREEN + "-----------------------------------------------------------------------")
            print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][DONE]" + " Скриншоты с ответами помещены в директорию ./train" + num_train + "/\nУдачного дня =)")
        driver_pars.close()
"""
        print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][DONE]" + " Текстовый файл с ответами помещен в директорию ./train" + num_train + "/\nУдачного дня =)")
        file_name = vk_api.upload.VkUpload(vk).document_message(
            doc='./train' + testfox_num + '/answers.txt',
            peer_id=peer_id,
            title='train' + testfox_num
        )
        owner = file_name['doc']['owner_id']
        doc_id = file_name['doc']['id']
        vk.messages.send(
            random_id=get_random_id(),
            message="Тест №" + str(testfox_num) + " - ответы успешно получены!",
            peer_id=peer_id,
            attachment='doc' + str(owner) + '_' + str(doc_id)
        )
        vkbot()

    except NoSuchElementException:
        vk.messages.send(
            random_id=get_random_id(),
            message="Произошла ошибка при работе.\nПопробуйте ",
            peer_id=peer_id
        )

def register(comm = None, tempid = 0):
    if os.path.exists('./files/cookies.pkl') == True:
        os.remove('./files/cookies.pkl')
    vk.messages.send(
        random_id=get_random_id(),
        message="Начинаю процесс регистрации нового пользователя...",
        peer_id=tempid
    )
    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][REG]" + " Начинаю процесс регистрации нового пользователя...")

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    temp_fn = ''
    temp_sn = ''
    temp_email = ''

    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][REG]" + " Генерация ФИО и Email...")

    for i in range(10):
        temp_fn += random.choice(chars)
        temp_sn += random.choice(chars)
        temp_email += random.choice(chars)

    temp_fio = temp_fn + ' ' + temp_sn
    temp_email = temp_email + '@gmail.com'

    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][REG]" + " Регистрация...")

    driver = webdriver.Chrome(options=browser_options, executable_path=chrome_driver)
    driver.get("https://foxford.ru/user/registration")
    time.sleep(3)
    while True:
        try:
            fio_label = driver.find_element_by_name("name")
            fio_label.send_keys(temp_fio)
            break
        except NoSuchElementException:
            continue
    email_label = driver.find_element_by_name("email")
    email_label.send_keys(temp_email)
    email_label.send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_class_name("GradeCheck_grade__3qSNQ").click()
    time.sleep(1)
    driver.find_element_by_class_name("Button_root__2dkqG").click()
    time.sleep(1)
    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][COOKIES]" + " Сохраняю cookies...")
    with open('files/cookies.pkl', 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)
    driver.close()
    vk.messages.send(
        random_id=get_random_id(),
        message="Регистрация завершена",
        peer_id=tempid
    )
    print(Fore.GREEN + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][REG]" + " Регистрация звершена")
    if comm == "regaway":
        vkbot()
    else:
        pars(comm, tempid)

def check(comm = 0, tempid = 0):
    try:
        with open('files/cookies.pkl') as f:
            if f.read() != '':
                pars(comm, tempid)
            else:
                register(comm, tempid)
    except FileNotFoundError:
        register(comm, tempid)
    except PermissionError:
        vk.messages.send(
            random_id=get_random_id(),
            message="@kustiktm_kirill, &#10060; Cookies access denied! Please, check log",
            peer_id=tempid
        )
        print(Fore.RED + "-----------------------------------------------------------------------")
        print(Fore.RED + "[" + datetime.datetime.today().strftime("%H:%M:%S") + "][ERR]" + "Нет прав для открытия cookies.pkl! Проверьте права доступа к файлу.")
    except Exception:
        vk.messages.send(
            random_id=get_random_id(),
            message="@kustiktm_kirill, &#10060; Cookies error! Please, check log\nFunction register is called now",
            peer_id=tempid
        )
        register(comm, tempid)

def vkbot():
    print("Bot has been start...")
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:
                    response = event.object['message']['text'].lower()
                    if "фоксфорд" in response:
                        vk.messages.send(
                            random_id=get_random_id(),
                            message='Фоксфорд изи, хо-хо-хо =)',
                            peer_id=event.object['message']['peer_id']
                        )
                    elif "/парсинг" in response:
                        comm = str(response).split(" ")[1]
                        vk.messages.send(
                            random_id=get_random_id(),
                            message='Поиск теста №' + comm + "..." ,
                            peer_id=event.object['message']['peer_id']
                        )
                        check(int(comm), event.object['message']['peer_id'])
                    elif response == "/register()":
                        register("regaway",event.object['message']['peer_id'])
                if event.object['message']['action']['type'] == 'chat_invite_user':
                    vk.messages.send(
                        random_id=get_random_id(),
                        message='&#128075; Приветствую!\n&#128520; Вы на закрытом бета тестировании бота по сливу ответов FoxFord\n\nБот активно разрабатывается, поэтому просим нормально относиться к неполным ответам или ошибкам\n\n&#128377; Доступные команды для Вас:\n\n/парсинг <номер теста>\n\n&#128215; "Ворует" ответы на любое тестирование имеющее вид trainings/<номер>\n\n/register()\n\n	&#9888; Экстренная команда на случай возникновения множества ошибок. Испольнять могут только администраторы беседы\n\n&#8252; Во время выполнения команд бот НЕ отвечает на Ваши сообщения\n\n',
                        peer_id=event.object['message']['peer_id']
                    )
        except Exception:
            continue

if __name__ == "__main__":
    print(Fore.WHITE + "||--------------------------------------------------------------------------------||")
    print(Fore.WHITE + "||--------------------------------------------------------------------------------||")
    print(Fore.WHITE + "||                                                                                ||")
    print(Fore.WHITE + "||                                                                                ||")
    print(Fore.WHITE + "||                           " + Fore.RED + "FoxFord Trainings Parser 0.1" + Fore.WHITE +"                          ||")
    print(Fore.WHITE + "||                            " + Fore.RED + "Created by kustiktm_kirill" + Fore.WHITE +"                          ||")
    print(Fore.WHITE + "||                                                                                ||")
    print(Fore.WHITE + "||                    " + Fore.RED + "https://github.com/kustiktmkirill/ffparser" + Fore.WHITE +"                  ||")
    print(Fore.WHITE + "||                                                                                ||")
    print(Fore.WHITE + "||                                                                                ||")
    print(Fore.WHITE + "||--------------------------------------------------------------------------------||")
    print(Fore.WHITE + "||--------------------------------------------------------------------------------||")
    vkbot()

#Script was created by kustiktm_kirill
#https://github.com/kustiktmkirill
