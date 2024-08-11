import csv
import json
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = 'https://map.kakao.com/'
driver = webdriver.Chrome()  # 드라이버 경로
driver.get(url)
key_word = '24시 동물병원'  # 검색어

def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

def hospital_list_print():
    time.sleep(0.2)

    name_list = driver.find_elements(By.CSS_SELECTOR, '.head_item > .tit_name > .link_name')
    number_list = driver.find_elements(By.CSS_SELECTOR, '.info_item >.contact >.phone')
    address_list = driver.find_elements(By.CSS_SELECTOR, '.info_item > .addr')

    for index in range(len(name_list)):
        hospital_name = name_list[index].text
        hospital_number = number_list[index].text
        hospital_address = address_list[index].text

        dict_temp = {
            'hospital_name': hospital_name,
            'hospital_number': hospital_number,
            'hospital_addr': hospital_address,
        }

        hospital_dict['병원정보'].append(dict_temp)
        print(f'{hospital_name} ...완료')

time_wait(10, 'div.box_searchbar > input.query')

search = driver.find_element(By.CSS_SELECTOR, 'div.box_searchbar > input.query')
search.send_keys(key_word)
search.send_keys(Keys.ENTER)

sleep(1)

place_tab = driver.find_element(By.CSS_SELECTOR, '#info\.main\.options > li.option1 > a')
place_tab.send_keys(Keys.ENTER)

sleep(1)

hospital_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

hospital_dict = {'병원정보': []}
start = time.time()
print('[크롤링 시작...]')

page = 1
page2 = 0
error_cnt = 0

while 1:
    try:
        page2 += 1
        print("**", page, "**")

        page_xpath = f'//*[@id="info.search.page.no{page2}"]'
        page_element = driver.find_element(By.XPATH, page_xpath)
        page_element.send_keys(Keys.ENTER)

        hospital_list_print()

        hospital_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

        if len(hospital_list) < 15 or not page_element.is_enabled():
            break

        if page2 % 5 == 0:
            next_page_element = driver.find_element(By.XPATH, '//*[@id="info.search.page.next"]')
            next_page_element.send_keys(Keys.ENTER)
            page2 = 0

        page += 1

    except Exception as e:
        error_cnt += 1
        print(e)
        print('ERROR')

        if error_cnt > 5:
            break

csv_file_path = 'data/hospital_data.csv'
csv_file = open(csv_file_path, 'w', newline='', encoding='utf-8-sig')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['hospital_name', 'hospital_number', 'hospital_addr'])  # Write header

for hospital_info in hospital_dict['병원정보']:
    csv_writer.writerow([hospital_info['hospital_name'], hospital_info['hospital_number'], hospital_info['hospital_addr']])

csv_file.close()  # Close the CSV file

print('[데이터 수집 완료]\n소요 시간:', time.time() - start)
driver.quit()
