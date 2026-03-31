clc
clear
close all

% 1. Read the image
img = imread('peppers.png');

% Convert to grayscale if needed
if size(img,3) == 3
    img = rgb2gray(img);
end

[rows, cols] = size(img);

% Create output image
mirror_img = img;   % copy original

% 2. Outer loop (rows)
for i = 1:rows
    
    % 3. Inner loop (columns)
    for j = 1:floor(cols/2)
        
        % 4. Swap pixels
        temp = mirror_img(i,j);
        mirror_img(i,j) = mirror_img(i, cols-j+1);
        mirror_img(i, cols-j+1) = temp;
        
    end
end

% Display
figure
subplot(1,2,1)
imshow(img)
title('Original Image')

subplot(1,2,2)
imshow(mirror_img)
title('Mirror Image (Using Nested Loops)')