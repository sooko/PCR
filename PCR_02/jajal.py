# # from PIL import Image
# # from numpy import asarray
# # # load the image
# # image = Image.open('img/6880.jpg')
# # # convert image to numpy array
# # data = asarray(image)
# # print(type(data))
# # # summarize shape
# # print(data.shape)

# # # create Pillow image
# # image2 = Image.fromarray(data)
# # print(type(image2))

# # # summarize image details
# # print(image2.mode)
# # print(image2.size)
# # print(data)

# import cv2
# image = cv2.imread("img/6880.jpg")
# # color = int(image[300, 300])
# # if image type is b g r, then b g r value will be displayed.
# # if image is gray then color intensity will be displayed.
# # print (color)
# img1 = cv2.imread("img/6880.jpg", cv2.IMREAD_UNCHANGED)
# print(img1)
# b,g,r = (img1[300, 300])
# print (r)
# print (g)
# print (b)


# import numpy as np

# # 1d array to list
# arr = np.array([1, 2, 3])
# # print(f'NumPy Array:\n{arr}')

# list1 = arr.tolist()
# print(f'List: {list1}')


# from kivy.metrics import d

# a=(10,20,30,40)

# b=(1,2,3,4)

# if b in range(a):
#     print(b)

# b=(1,2,3,4)
# # print(a is b)
# if b in a:
#     print("ya")

for i in range(10,20):
    print(i)