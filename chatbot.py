import os
import time
import ctypes
import wikipedia
import datetime
import json
import re
import webbrowser
import requests
import urllib.request as urllib2
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from youtube_search import YoutubeSearch

wikipedia.set_lang('vi')
language = 'vi'
path = ChromeDriverManager().install()

def stop():
    print("Hẹn gặp lại bạn sau!")

def get_text():
    for i in range(3):
        text = input()
        if text:
            return text.lower()
        elif i < 2:
            print("Bot không nghe rõ. Bạn nói lại được không!")
    time.sleep(2)
    stop()
    return 0

def hello(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        print("Chào buổi sáng bạn {}. Chúc bạn một ngày tốt lành.".format(name))
    elif 12 <= day_time < 18:
        print("Chào buổi chiều bạn {}. Bạn đã dự định gì cho chiều nay chưa.".format(name))
    else:
        print("Chào buổi tối bạn {}. Bạn đã ăn tối chưa nhỉ.".format(name))

def get_timer():
    print("Bạn Cần xem ngày hay giờ!")
    tot = input()
    now = datetime.datetime.now()
    if "giờ" in tot:
        print('Bây giờ là %d giờ %d phút' % (now.hour, now.minute))
    elif "ngày" in tot:
        print("Hôm nay là ngày %d tháng %d năm %d" %(now.day, now.month, now.year))
    else:
        print("Bot chưa hiểu ý của bạn. Bạn nói lại được không?")

def open_application():

    print("mở úng dụng gì")
    text = input()
    if "google" in text:

        os.startfile('C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    elif "word" in text:

        os.startfile('C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.EXE')
    elif "excel" in text:

        os.startfile('C:\\Program Files (x86)\\Microsoft Office\\root\Office16\\EXCEL.EXE')
    else:
        print("Ứng dụng chưa được cài đặt. Bạn hãy thử lại!")

def open_website():
    text=input()
    reg_ex = re.search(text,text)
    if reg_ex:
        domain = reg_ex.group()
        url = 'https://www.' + domain
        webbrowser.open(url)
        print("Trang web bạn yêu cầu đã được mở.")
        return True
    else:
        return False
def open_google_and_search(text):
    search_for = text.split("kiếm", 1)[1]
    print('Okay!')
    driver = webdriver.Chrome(path)
    driver.get("https://www.google.com")
    que = driver.find_element_by_xpath("//input[@name='q']")
    que.send_keys(str(search_for))
    que.send_keys(Keys.RETURN)


def current_weather():
    print("Bạn muốn xem thời tiết ở đâu ạ.")
    ow_url = "http://api.openweathermap.org/data/2.5/weather?"
    city = get_text()
    if not city:
        pass
    api_key = "fe8d8c65cf345889139d8e545f57819a"
    call_url = ow_url + "appid=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(call_url)
    data = response.json()
    if data["cod"] != "404":
        city_res = data["main"]
        current_temperature = city_res["temp"]
        current_pressure = city_res["pressure"]
        current_humidity = city_res["humidity"]
        suntime = data["sys"]
        sunrise = datetime.datetime.fromtimestamp(suntime["sunrise"])
        sunset = datetime.datetime.fromtimestamp(suntime["sunset"])
        wthr = data["weather"]
        weather_description = wthr[0]["description"]
        now = datetime.datetime.now()
        content = """
        Hôm nay là ngày {day} tháng {month} năm {year}
        Mặt trời mọc vào {hourrise} giờ {minrise} phút
        Mặt trời lặn vào {hourset} giờ {minset} phút
        Nhiệt độ trung bình là {temp} độ C
        Áp suất không khí là {pressure} héc tơ Pascal
        Độ ẩm là {humidity}%
        Trời hôm nay quang mây. Dự báo mưa rải rác ở một số nơi.""".format(day = now.day,month = now.month, year= now.year, hourrise = sunrise.hour, minrise = sunrise.minute,
                                                                           hourset = sunset.hour, minset = sunset.minute,
                                                                           temp = current_temperature, pressure = current_pressure, humidity = current_humidity)
        print(content)
        time.sleep(10)
    else:
        print("Không tìm thấy địa chỉ của bạn")



def help_me():
    print("""Bot có thể giúp bạn thực hiện các câu lệnh sau đây:
    1. Chào hỏi
    2. Hiển thị giờ
    3. Mở website, application
    4. Tìm kiếm trên Google
    5. Dự báo thời tiết""")
    time.sleep(10)

def assistant():
    print("Xin chào, bạn tên là gì nhỉ?")
#     name = get_text()
    name = input()
    if name:
        print("Chào bạn {}".format(name))
        print("Bạn cần Bot Alex có thể giúp gì ạ?")
        while True:
            text = get_text()
            if not text:
                break
            elif "dừng" in text or "tạm biệt" in text or "chào robot" in text or "ngủ thôi" in text:
                stop()
                break
            elif "có thể làm gì" in text:
                help_me()
            elif "chào trợ lý ảo" in text:
                hello(name)
            elif "hiện tại là" in text:
                get_timer()
            elif "mở" in text:
                print("Bạn cần mở gì!")
                tem=input()
                if 'mở google và tìm kiếm' in tem:
                    open_google_and_search(text=tem)
                elif "." in tem:
                    open_website()
                elif "mở ứng dụng" in tem:
                    open_application()
            elif "thời tiết" in text:
                current_weather()
            else:
                print("Bạn cần Bot giúp gì ạ?")

assistant()