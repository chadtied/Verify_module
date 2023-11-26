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
from selenium.webdriver.support.ui import Select
import requests

#驗證碼圖片切割
def split_digits_in_img(test_img_array):
    test_list = list()
    for i in range(digits_in_img):
        step = test_img_cols // digits_in_img
        test_list.append(test_img_array[:, i * step:(i + 1) * step] / 255)
    return test_list

#初始化
access= True

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

#模型載入
if os.path.isfile(path+'cnn_model.h5'):
    test_model = models.load_model(path+'cnn_model.h5')
else:
    print('No trained model found.')
    exit(-1)

np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})


# 創建一個Chromedriver實例
driver=  Driver(uc= True, incognito= False)


# 訪問包含SVG的網頁
driver.get('https://tixcraft.com/')  # 替換成實際網頁的URL
input()

# 設定台灣台北的時區
taipei_timezone = pytz.timezone('Asia/Taipei')

# 獲取當前時間並將其設定為台北時區
current_time = datetime.now(taipei_timezone)

# 設定目標開始時間，這裡是11點
target_time = current_time.replace(hour=0, minute=57, second=0, microsecond=0)

# 計算距離目標時間還有多長時間
time_difference = target_time - current_time


# 等待直到達到目標時間
if time_difference.total_seconds() > 0:
    time.sleep(time_difference.total_seconds())



driver.get('https://tixcraft.com/activity/game/23_mchotdog')

#選取票價區

WebDriverWait(driver,360,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#gameList > table > tbody > tr > td:nth-child(4) > button")))
ticket_link= driver.find_element(By.CSS_SELECTOR, "#gameList > table > tbody > tr > td:nth-child(4) > button")
driver.execute_script("arguments[0].click();", ticket_link)

print('選取票價區失敗!!!')



WebDriverWait(driver,360,0.5).until(EC.presence_of_element_located((By.ID, "group_0")))
ticket_area= driver.find_elements(By.CSS_SELECTOR, "#group_0 > li> a")
driver.execute_script("arguments[0].click();", ticket_area[5])


while access:
    WebDriverWait(driver,360,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#ticketPriceList> tbody> tr> td> select")))
    select= Select(driver.find_element(By.CSS_SELECTOR, "#ticketPriceList> tbody> tr> td> select"))
    select.select_by_index(2)

    # 找到包含验证码图片的元素
    verify_img_element = driver.find_element(By.ID, "TicketForm_verifyCode-image")

    # 获取验证码图片元素的位置和尺寸
    location = verify_img_element.location
    size = verify_img_element.size

    # 截取验证码图片的屏幕截图
    driver.save_screenshot('screenshot.png')

    # 计算验证码图片在整个截图中的位置
    left = location['x']
    top = location['y']
    right = left + size['width']
    bottom = top + size['height']

    screenshot = Image.open('screenshot.png')
    verify_img = screenshot.crop((left, top, right, bottom))

    # 保存验证码图片
    verify_img.save(path+ 'verify.png')
    #-------圖片裁切-----------
    image= Image.open(path+'verify.png')
    width,height= image.size
    cropped_img= image.crop((10, 10, width-20, height-10))
    cropped_img.save(path+'verify.png')

    test_img = load_img(path+'verify.png', color_mode='grayscale')
    test_img_array = img_to_array(test_img)
    test_img_rows, test_img_cols, _ = test_img_array.shape
    test_list = split_digits_in_img(test_img_array)

    varification_code = str()
    for i in range(digits_in_img):
        confidences = test_model.predict(np.array([test_list[i]]), verbose=0)
        result_class = np.argmax(confidences, axis= 1)
        varification_code+= int_char[np.squeeze(result_class)]
    driver.find_element(By.ID, "TicketForm_verifyCode").send_keys(varification_code)
    ticket_agree= driver.find_element(By.ID, "TicketForm_agree")
    driver.execute_script("arguments[0].click();", ticket_agree)
    ticket_send= driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary")
    driver.execute_script("arguments[0].click();", ticket_send)
    try:
        driver.current_url
        access= False
    except:
        print("Verify fail!")


WebDriverWait(driver,360,0.5).until(EC.presence_of_element_located((By.ID, "submitButton")))
#36 信用卡 54 atm
ticket_payment= driver.find_element(By.ID, "CheckoutForm_paymentId_36")
driver.execute_script("arguments[0].click();", ticket_payment)

ticket_final_check= driver.find_element(By.ID, "submitButton")
#driver.execute_script("arguments[0].click();", ticket_final_check)
input()