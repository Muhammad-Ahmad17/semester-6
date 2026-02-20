clc
clear
close all

clc
clear
close all

i = imread("peppers.jpg");
i_gray = rgb2gray(i);

subplot(121)
imshow(i)
subplot(122)
imshow(i_gray)

img_gray = imtool(i_gray);
