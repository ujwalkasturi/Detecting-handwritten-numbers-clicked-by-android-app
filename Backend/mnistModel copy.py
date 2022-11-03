from keras.models import load_model
import cv2
import numpy as np
import matplotlib.pyplot as plt 
import skimage.io
import skimage.color
import skimage.filters
from PIL import Image, ImageOps

def resize_to_28x28(img):
    img_h, img_w = img.shape
    dim_size_max = max(img.shape)

    if dim_size_max == img_w:
        im_h = (26 * img_h) // img_w
        if im_h <= 0 or img_w <= 0:
            print("Invalid Image Dimention: ", im_h, img_w, img_h)
        tmp_img = cv2.resize(img, (26,im_h),0,0,cv2.INTER_NEAREST)
    else:
        im_w = (26 * img_w) // img_h
        if im_w <= 0 or img_h <= 0:
            print("Invalid Image Dimention: ", im_w, img_w, img_h)
        tmp_img = cv2.resize(img, (im_w, 26),0,0,cv2.INTER_NEAREST)

    out_img = np.zeros((28, 28), dtype=np.ubyte)

    nb_h, nb_w = out_img.shape
    na_h, na_w = tmp_img.shape
    y_min = (nb_w) // 2 - (na_w // 2)
    y_max = y_min + na_w
    x_min = (nb_h) // 2 - (na_h // 2)
    x_max = x_min + na_h

    out_img[x_min:x_max, y_min:y_max] = tmp_img

    return out_img

def preprocess_images(imgs): # should work for both a single image and multiple images
    sample_img = imgs if len(imgs.shape) == 2 else imgs[0]
    assert sample_img.shape in [(28, 28, 1), (28, 28)], sample_img.shape # make sure images are 28x28 and single-channel (grayscale)
    return imgs / 255.0

    
model = load_model('mnist2.h5')
path = r"C:\\Personal\\University\Sem-1\\Mobile_computing\\Project2\\test_images\\7crop.png"
img = cv2.imread(r"C:\\Personal\\University\Sem-1\\Mobile_computing\\Project2\\test_images\\s6.jpeg")
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
img_proc = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(img_proc, 127, 255, cv2.THRESH_BINARY)
img_proc = cv2.resize(blackAndWhiteImage, (28, 28))
img_proc = preprocess_images(img_proc)

img_proc = 1 - img_proc # inverse since training dataset is white text with black background

img = np.array([img_proc])
plt.imshow(img[0],cmap='binary')
plt.show()
# img_proc.show()
net_in = np.expand_dims(img_proc, axis=0)
# net_in = np.expand_dims(net_in, axis=3) # expand dimension to specify number of channels
# img_proc.show()

y_pred = model.predict(net_in)[0]
print(y_pred)
print("Prediction :",np.argmax(y_pred))
