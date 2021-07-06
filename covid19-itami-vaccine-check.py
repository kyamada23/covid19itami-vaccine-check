#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import re
import slackweb
import datetime

target_url = "https://vaccines.sciseed.jp/itami/login"
chrome_driver_path = ""
coupon_number = ""
passwd = ""
slack_webhook_URL = ""

option = Options()
option.add_argument('--headless')
driver = webdriver.Chrome(chrome_driver_path, options=option)
driver.get(target_url)
sleep(1)

number = driver.find_element_by_css_selector("input[type=\"tel\"]")
number.send_keys(coupon_number)
sleep(1)
password = driver.find_element_by_css_selector("input[type=\"password\"]")
password.send_keys(passwd)
sleep(1)
driver.find_element_by_css_selector("input[type=\"checkbox\"]").click()
sleep(1)
driver.find_element_by_css_selector("button[type=\"submit\"]").click()
sleep(3)

# 新規予約の場合と予約変更の場合を切り替え
# driver.find_element_by_xpath("//*[text()=\" 新規予約\"]").click()
driver.find_element_by_xpath("//*[text()=\" 予約変更\"]").click()
sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div/button[1]").click()
sleep(2)
driver.find_element_by_css_selector("input[type=\"checkbox\"]").click();
sleep(3)
element = driver.find_element_by_class_name("page-department-search_nav-header__count")
result = re.sub(r"\D", "", element.text)

dt_now = datetime.datetime.now()
print(dt_now);

# slack通知
slack = slackweb.Slack(url=slack_webhook_URL)

if result != "0":
    print(result);
    slack.notify(text="<!channel> 空いてるよ！！！")
else:
    print("空いてなかったよ")

driver.quit()
