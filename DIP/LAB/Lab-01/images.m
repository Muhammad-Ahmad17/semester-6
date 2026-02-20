clc
clear
close all

% read an image
i = imread('img1.jpg')
% showing image
imshow(i)
% checking size of that image
size(i)


subplot(121)
j = imread('img1.jpg')
imshow(j)
% decreasing the intensity of an image
subplot(122)
u = j-100
imshow(u)

% stored
imwrite(u,"img1_low-intens.jpg")

% imshow(i,[low,high] -> we give a threshold for both high and low below and above this intensity set to low or high
imshow(j,[33,100])
