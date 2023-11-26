import undetected_chromedriver as  uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pyautogui
from PIL import Image
import time
import base64

options= Options()
driver=  uc.Chrome(use_subprocess= True, chrome_options= options)

def Decode(url):
    slice_url= url.split(',')
    uncode_url= slice_url[-1]
    return base64.b64decode(uncode_url)



driver.get('https://gen.caca01.com/ttcode/codeking')
data_num= 0

while data_num< 10000:
    WebDriverWait(driver,10,0.5).until(EC.presence_of_element_located((By.ID,'start')))
    start_button= driver.find_element(By.ID,'start')
    driver.execute_script("arguments[0].click();", start_button)
    del start_button
    time.sleep(2)    
    while True:
        try:
            WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.ID,'code')))
            input_data= driver.find_element(By.ID,'code')
            input_data.send_keys('2')
            pyautogui.press('enter')
            input_data.clear()
            #time.sleep(0.1)
        except:
            print('scan fiinish!!!')
            break
    WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.CSS_SELECTOR,'#finishModal > div > div > div.errordiv > div')))
    data_sets= driver.find_elements(By.CSS_SELECTOR,'#finishModal > div > div > div.errordiv > div')

    file_name='C:/Users/chad/Desktop/Vertify_module/train_data/'
    for data_set in data_sets:
        data_num+= 1
        img_url= data_set.find_element(By.CSS_SELECTOR,'img').get_attribute('src')
        img_Name= data_set.find_element(By.CSS_SELECTOR,'div')
        img_name= (img_Name.text)[3:]
        decode_url= Decode(img_url)
        with open(file_name+img_name+str(data_num)+'.png','wb') as f:
            f.write(decode_url)
        
        #-------圖片裁切-----------
        image= Image.open(file_name+img_name+str(data_num)+'.png')
        width,height= image.size
        cropped_img= image.crop((10, 10, width-20, height-10))
        cropped_img.save(file_name+img_name+str(data_num)+'.png')

    print(data_num)
    again_button= driver.find_element(By.CSS_SELECTOR,'#finishModal > div > div > div.modal-footer > button')
    driver.execute_script("arguments[0].click();", again_button)

driver.close()



