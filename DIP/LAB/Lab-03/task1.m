% Lab 03 - Task 1: Exploring imadjust function
% Intensity transformation using imadjust with different gamma values
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');

% Display original image
figure;
subplot(2,3,1);
imshow(img);
title('Original Image');

% Apply imadjust with default settings
img_adj = imadjust(img);
subplot(2,3,2);
imshow(img_adj);
title('Default imadjust');

% Apply imadjust with gamma < 1 (brighten)
img_gamma_low = imadjust(img, [], [], 0.5);
subplot(2,3,3);
imshow(img_gamma_low);
title('Gamma = 0.5 (Brighter)');

% Apply imadjust with gamma = 1 (no change)
img_gamma_one = imadjust(img, [], [], 1);
subplot(2,3,4);
imshow(img_gamma_one);
title('Gamma = 1 (No Change)');

% Apply imadjust with gamma > 1 (darken)
img_gamma_high = imadjust(img, [], [], 2);
subplot(2,3,5);
imshow(img_gamma_high);
title('Gamma = 2 (Darker)');

% Apply imadjust with very high gamma
img_gamma_vhigh = imadjust(img, [], [], 3);
subplot(2,3,6);
imshow(img_gamma_vhigh);
title('Gamma = 3 (Very Dark)');

sgtitle('Impact of Gamma in imadjust');
