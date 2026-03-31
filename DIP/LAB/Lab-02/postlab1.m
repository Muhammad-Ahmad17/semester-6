clc
clear
close all

% Read image
img = imread('peppers.png');

% Convert to grayscale if needed
if size(img,3) == 3
    img = rgb2gray(img);
end

% Initialize output image
binary_img = zeros(size(img), 'uint8');

% Apply threshold
binary_img(img <= 128) = 0;
binary_img(img > 128)  = 255;

% Display results
figure
subplot(1,2,1)
imshow(img)
title('Original Grayscale Image')

subplot(1,2,2)
imshow(binary_img)
title('Binary Image (Threshold = 128)')