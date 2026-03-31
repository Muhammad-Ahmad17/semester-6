clc; clear; close all;

% Load a colorful, detailed image
img = imread('peppers.png'); %% 384×512, colorful

figure;
subplot(1,3,1);
imshow(img);
title('Original');

% Save with different JPEG quality
imwrite(img, 'peppers_high.jpg', 'Quality', 100); % Best quality
imwrite(img, 'peppers_low.jpg', 'Quality', 10); % Very compressed

% Read them back and display
img_high = imread('peppers_high.jpg');
img_low = imread('peppers_low.jpg');

subplot(1,3,2);
imshow(img_high);
title('High Quality (100)');

subplot(1,3,3);
imshow(img_low);
title('Low Quality (10) - See the blocks!');
