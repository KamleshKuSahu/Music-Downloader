from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import time

test = 2
while test != 0:
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        options.add_extension("AdBlock.crx")
        options.minimized = True
        options.add_argument("--blink-settings=imagesEnabled=false")
        # options.headless = True
        serv = Service("chromedriver.exe")
        serv.start()

        driver = webdriver.Chrome(service=serv, options=options)
        WebDriverWait(driver, 30).until(lambda driver: len(driver.window_handles) == 2)
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

        def song_url(song_name):
            song = song_name.split()
            temp = ""
            for i in range(0, len(song)):
                if i != len(song) - 1:
                    temp += song[i] + "+"
                else:
                    temp += song[i]
            driver.get("https://music.youtube.com/search?q=" + temp)
            source = driver.page_source
            index = source.find("x22videoId")
            return (
                "https://music.youtube.com/watch?v=" + source[index + 19 : index + 30]
            )

        def download(song_url):
            driver.get("https://x2download.app/en125/download-youtube-to-mp3")
            driver.find_element(By.ID, "s_input").send_keys(song_url)
            driver.find_element(By.CLASS_NAME, "btn-red").click()
            WebDriverWait(driver, 30).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "formatSelect")
                )
            )
            options = driver.find_element(By.ID, "formatSelect").find_elements(
                By.CSS_SELECTOR, "option"
            )
            print(driver.find_element(By.ID, "video_fn").get_attribute("value")[15:])
            print("Select to download: ")
            print("0. Exit")
            j = 1
            for i in options:
                print(str(j) + ".", i.text)
                j += 1

            op = int(input("Select option: "))
            if op == 0:
                return
            options[op - 1].click()

            driver.find_element(By.ID, "btn-action").click()
            WebDriverWait(driver, 30).until(
                expected_conditions.visibility_of_element_located((By.ID, "asuccess"))
            )
            driver.find_element(By.ID, "asuccess").click()

        while True:
            song_name = input("Enter song name(0 to cancel): ")
            if song_name[0] == "0" and len(song_name) == 1:
                break
            songurl = song_url(song_name)
            download(songurl)
    except Exception as e:
        test -= 1
        continue
    else:
        break
