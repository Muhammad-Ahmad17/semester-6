clc
clear all
close all
img=imread('peppers.png')
img1=rgb2gray(img)

figure(1)
subplot(1,2,1)
imshow(img1)
title('origional image')

subplot(1,2,2)
img2=histeq(img1)
imshow(img2)
title('histeq image')

figure(2)
subplot(1,2,1)
imhist(img1)
title('histogram origional image')

subplot(1,2,2)
imhist(img2)
title('histogram histeq image')