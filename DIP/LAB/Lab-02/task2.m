clc
clear
close all

i = imread("peppers.png");
i_gray = rgb2gray(i);

info = imfinfo("peppers.png")

subplot(121)
imshow(i)
imwrite(i,'color.jpg')
subplot(122)
imshow(i_gray)
imwrite(i_gray,'bnw.png')

img_gray = imtool(i_gray);
