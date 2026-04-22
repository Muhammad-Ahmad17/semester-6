clc; clear all; close all;
rgb_img = imread('peppers.png');
rgb_img = im2double(rgb_img);
gray_img = rgb2gray(rgb_img);
trans_img = imadjust(gray_img, [0.3 0.7], []);
match_img = histeq(gray_img, imhist(trans_img)); 
%this line match origional image with contrast adjusted image and make
%histogram
figure;
subplot(1, 3, 1);
imshow(gray_img);
title('Input Image');
subplot(1, 3, 2);
imshow(trans_img);
title('Transformed Image');
subplot(1, 3, 3);
imshow(match_img);
title('Matched Image');
figure;
subplot(1, 3, 1);
imhist(gray_img);
title('Hist(Input)');
subplot(1, 3, 2);
imhist(trans_img);
title('Hist(Transformed)');
subplot(1, 3, 3);
imhist(match_img);
title('Hist(Matched)');