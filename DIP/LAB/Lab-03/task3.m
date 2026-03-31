% Lab 03 - Task 3: Image Complement (Negative) using imcomplement
% Apply imcomplement to RGB and grayscale images
clc; clear; close all;

% Read RGB image
img_rgb = imread('peppers.png');

% Read grayscale image
img_gray = imread('cameraman.tif');

% Apply imcomplement to grayscale image
img_gray_neg = imcomplement(img_gray);

% Apply imcomplement to RGB image
img_rgb_neg = imcomplement(img_rgb);

% Display grayscale results
figure;
subplot(1,2,1);
imshow(img_gray);
title('Input Image');

subplot(1,2,2);
imshow(img_gray_neg);
title('Output Image');
sgtitle('Grayscale Image Complement');

% Display RGB results
figure;
subplot(1,2,1);
imshow(img_rgb);
title('Input Image');

subplot(1,2,2);
imshow(img_rgb_neg);
title('Output Image');
sgtitle('RGB Image Complement');

disp('Discussion: imcomplement inverts intensity values');
disp('For grayscale: output = 255 - input (for uint8)');
disp('For RGB: each channel is inverted independently');
