from keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt 
from PIL import Image, ImageOps

def remove_shadows(img):
    rgb_planes = cv2.split(img)

    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img,None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
        result = cv2.merge(result_planes)
        result_norm = cv2.merge(result_norm_planes)
        return result

def preprocess_images(imgs): # should work for both a single image and multiple images
    sample_img = imgs if len(imgs.shape) == 2 else imgs[0]
    assert sample_img.shape in [(28, 28, 1), (28, 28)], sample_img.shape # make sure images are 28x28 and single-channel (grayscale)
    return imgs / 255.0



def detect_num(img):
    img_proc = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(img_proc, 127, 255, cv2.THRESH_BINARY)
    img_proc = cv2.resize(blackAndWhiteImage, (28, 28))

    img_proc = preprocess_images(img_proc)

    img_proc = 1 - img_proc # inverse since training dataset is white text with black background

    # img = np.array([img_proc])
    # plt.imshow(img[0],cmap='gray')
    # plt.show()
    net_in = np.expand_dims(img_proc, axis=0)
    y_pred = model.predict(net_in)[0]
    print(y_pred)
    print("Prediction :",np.argmax(y_pred))
    return np.argmax(y_pred)

    
model = load_model('mnist2.h5')
# path = r"C:\\Personal\\University\\Sem-1\\Mobile_computing\\Project2\\Backend\\test_images\\7crop.png"
# img = cv2.imread(r"test_images\\z5.jpeg")

# detect_num(img)


# img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# image = resize_to_28x28(img)
# img = cv2.resize(img,(28,28))
#img = cv2.resize(img,(28,28))/255
# img=np.pad(img,(10,10),'constant',constant_values=0)
# img = cv2.resize(img,(28,28))/255
# img= np.expand_dims(img, -1)

# cv2.imshow('image window', img)
# add wait key. window waits until user presses a key
# cv2.waitKey(0)

# img = np.array([image])
# plt.imshow(img[0],cmap='binary')
# plt.show()

# if img.shape[0] != 720:
#         img = cv2.resize(img, (720, 720))
       
    #preprocess the image for prediction
# img_proc = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# img = np.array([img_proc])
# plt.imshow(img[0],cmap='binary')
# plt.show()


# img_pil = Image.fromarray(img_proc)
# img_proc = img_pil.resize((28,28), Image.ANTIALIAS)
# img_proc= Image.open(path).convert('L')
# img_proc = img_proc.resize((28,28), Image.ANTIALIAS)
# img_proc = ImageOps.grayscale(img_proc)
# img_proc = cv2.cvtColor(np.array(img_proc), cv2.COLOR_)
# img_proc = preprocess_images(img_proc)
# img_proc=remove_shadows(img)

# img_proc = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# # img_proc=remove_shadows(img)
# # img = np.array([img_proc])
# # plt.imshow(img[0],cmap='binary')
# # plt.show()

# (thresh, blackAndWhiteImage) = cv2.threshold(img_proc, 127, 255, cv2.THRESH_BINARY)

# # blackAndWhiteImage=remove_shadows(blackAndWhiteImage)

# # img = np.array([blackAndWhiteImage])
# # plt.imshow(img[0],cmap='binary')
# # plt.show()
# img_proc = cv2.resize(blackAndWhiteImage, (28, 28))

# img_proc = preprocess_images(img_proc)

# img_proc = 1 - img_proc # inverse since training dataset is white text with black background

# img = np.array([img_proc])
# plt.imshow(img[0],cmap='binary')
# plt.show()
# # img_proc.show()
# net_in = np.expand_dims(img_proc, axis=0)
# net_in = np.expand_dims(net_in, axis=3) # expand dimension to specify number of channels
# # img_proc.show()

# y_pred = model.predict(net_in)[0]
# print(y_pred)
# print("Prediction :",np.argmax(y_pred))
