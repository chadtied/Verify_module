from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import numpy as np
from keras import models
import os
from keras.utils import img_to_array
from keras.utils import load_img
import time
from datetime import datetime
import pytz

#訓練參數

test_img_rows= None
test_img_cols= None
test_model =None
digits_in_img= 4
char_int= {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,
           'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}
int_char= 'abcdefghijklmnopqrstuvwxyz'

#定義路徑
path= 'C:/Users/chad/Desktop/Vertify_module/'

np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})


# 創建一個Chromedriver實例
driver=  Driver(uc= True, incognito= False)


# 訪問包含SVG的網頁
driver.get('https://ticketplus.com.tw/')  # 替換成實際網頁的URL
input()

# 設定台灣台北的時區
taipei_timezone = pytz.timezone('Asia/Taipei')

# 獲取當前時間並將其設定為台北時區
current_time = datetime.now(taipei_timezone)

# 設定目標開始時間，這裡是11點
target_time = current_time.replace(hour=23, minute=30, second=0, microsecond=0)

# 計算距離目標時間還有多長時間
time_difference = target_time - current_time

# 等待直到達到目標時間
if time_difference.total_seconds() > 0:
    time.sleep(time_difference.total_seconds())



driver.get('https://ticketplus.com.tw/order/c752489ad3e922cbd8943deccdd22696/f985a29962a5b0072d835d6e70190183')

#選取票價區

try:
    WebDriverWait(driver,360,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.v-expansion-panel-header")))

    ticket_set= driver.find_elements(By.CSS_SELECTOR, "button.v-expansion-panel-header")
    driver.execute_script("arguments[0].click();", ticket_set[0])
    ticket_plus_button= driver.find_elements(By.CSS_SELECTOR, "div.v-expansion-panel-content__wrap i.mdi-plus")
    print(len(ticket_plus_button))
    driver.execute_script("arguments[0].click();", ticket_plus_button[0])
    #driver.execute_script("arguments[0].click();", ticket_plus_button[0])

except:
    print('選取票價區失敗!!!')


try:
    # 持續滾動直到底部
    while True:
        initial_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待一點時間以讓網頁載入新內容
        time.sleep(0.5)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == initial_height:
            break

    # 將SVG元素轉換為PNG
    WebDriverWait(driver,360,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span.captcha-img > svg")))
    svg_element= driver.find_element(By.CSS_SELECTOR,"span.captcha-img > svg")

    #將網頁拉到最下方
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 


    svg_element.screenshot(path+ 'vertify.png')

    image= Image.open(path+ 'vertify.png')
    # 使用crop方法進行縮小，這將保持原始圖像的長寬比
    image= image.crop((21,0,image.width-20,image.height))
    # 保存縮小後的圖像
    image.save(path+ 'vertify.png')

    #-------------------------測試模型--------------------------------------------

    def split_digits_in_img(test_img_array):
        test_list = list()
        for i in range(digits_in_img):
            step = test_img_cols // digits_in_img
            test_list.append(test_img_array[:, i * step:(i + 1) * step] / 255)
        return test_list

    if os.path.isfile(path+'concert_model.h5'):
        test_model = models.load_model(path+'concert_model.h5')
    else:
        print('No trained model found.')
        exit(-1)

    test_img = load_img(path+'vertify.png', color_mode='grayscale')
    test_img_array = img_to_array(test_img)
    test_img_rows, test_img_cols, _ = test_img_array.shape
    test_list = split_digits_in_img(test_img_array)

    varification_code = str()
    for i in range(digits_in_img):
        confidences = test_model.predict(np.array([test_list[i]]), verbose=0)
        result_class = np.argmax(confidences, axis= 1)
        varification_code+= int_char[np.squeeze(result_class)]

    print(varification_code)
    driver.find_element(By.CSS_SELECTOR,'div.recaptcha-area input').send_keys(varification_code)
except:
    print('驗證碼獲取失敗!!!')

try:
    first_submit= driver.find_element(By.CSS_SELECTOR,'div.order-footer Button.nextBtn')
    driver.execute_script("arguments[0].click();", first_submit)
except:
    print('第一次送票失敗!!!')

try:
    WebDriverWait(driver,900,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.timer')))
    second_submit= driver.find_element(By.CSS_SELECTOR,'div.order-footer Button.nextBtn')
    driver.execute_script("arguments[0].click();", second_submit)
    driver.execute_script("arguments[0].click();", second_submit)
except:
    print('第二次送票失敗!!!')

input()