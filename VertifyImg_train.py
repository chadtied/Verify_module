import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow import keras
from keras import layers
from keras import models
from keras import preprocessing
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import img_to_array
from keras.utils import load_img
import cv2


#訓練參數

epochs= 10
img_rows= None
img_cols= None
digits_in_img= 4
x_list= []
y_list= []
x_train = []
y_train = []
x_test = []
y_test = []
char_int= {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8,'i':9,'j':10,'k':11,'l':12,'m':13,
           'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21,'v':22,'w':23,'x':24,'y':25,'z':26}
int_char= 'abcdefghijklmnopqrstuvwxyz'
data_file= 'C:/Users/chad/Desktop/Vertify_module/'

'''
# ----------------模型訓練----------------------------
def split_digits_in_img(img_array, x_list, y_list):
    for i in range(digits_in_img):
        step= img_cols // digits_in_img
        x_list.append(img_array[:, i*step:(i+1)*step]/255)
        y_list.append(char_int[img_filename[i]])
        #print(char_int[img_filename[i]])

img_filenames= os.listdir(data_file+ 'train_data')
#print(img_filenames)

for img_filename in img_filenames:
    if '.png' not in img_filename:
        continue
    img= load_img(data_file+'train_data/{0}'.format(img_filename), color_mode= 'grayscale')
    img_array= img_to_array(img)

    #print(len(img_array[0]))
    img_rows, img_cols, _= img_array.shape
    split_digits_in_img(img_array, x_list, y_list)

y_list= keras.utils.to_categorical(np.array(y_list)-1, num_classes= 26)
x_train, x_test, y_train, y_test= train_test_split(x_list, y_list)


if os.path.isfile(data_file+'cnn_model.h5'):
    model = models.load_model(data_file+'cnn_model.h5')
    print('Model loaded from file.')
else:
    model = models.Sequential()
    model.add(layers.Conv2D(32, kernel_size=(5, 5), activation='relu', input_shape=(img_rows, img_cols // digits_in_img, 1)))
    model.add(layers.Conv2D(64, (5, 5), activation='relu'))
    model.add(layers.MaxPooling2D(pool_size=(2, 2)))
    model.add(layers.Dropout(rate=0.25))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(rate=0.5))
    model.add(layers.Dense(26, activation='softmax'))
    print('New model created.')
 
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adam(), metrics=['accuracy'])
#model.fit(np.array(x_train, dtype=object), np.array(y_train), batch_size=digits_in_img, epochs=epochs, verbose=1, validation_data=(np.array(x_test, dtype=object), np.array(y_test)))

model.fit(np.array(x_train), np.array(y_train), batch_size=digits_in_img, epochs=epochs, verbose=1, validation_data=(np.array(x_test), np.array(y_test)))
 
loss, accuracy = model.evaluate(np.array(x_test), np.array(y_test), verbose=0)
print('Test loss:', loss)
print('Test accuracy:', accuracy)
 
model.save(data_file+'cnn_model.h5')
'''

#-------------------------測試模型--------------------------------------------

test_img_rows= None
test_img_cols= None
test_model =None
np.set_printoptions(suppress=True, linewidth=150, precision=9, formatter={'float': '{: 0.9f}'.format})

def split_digits_in_img(test_img_array):
    test_list = list()
    for i in range(digits_in_img):
        step = test_img_cols // digits_in_img
        test_list.append(test_img_array[:, i * step:(i + 1) * step] / 255)
    return test_list

if os.path.isfile(data_file+'cnn_model.h5'):
    test_model = models.load_model(data_file+'cnn_model.h5')
else:
    print('No trained model found.')
    exit(-1)

test_img_filename = input('Varification code img filename: ')
test_img = load_img(data_file+test_img_filename, color_mode='grayscale')
test_img_array = img_to_array(test_img)
test_img_rows, test_img_cols, _ = test_img_array.shape
test_list = split_digits_in_img(test_img_array)

varification_code = list()
for i in range(digits_in_img):
    confidences = test_model.predict(np.array([test_list[i]]), verbose=0)
    result_class = np.argmax(confidences, axis= 1)
    varification_code.append(int_char[np.squeeze(result_class)])
    print('Digit {0}: Confidence=> {1}    Predict=> {2}'.format(i + 1, np.squeeze(confidences), np.squeeze(result_class)))
print('Predicted varification code:', varification_code)