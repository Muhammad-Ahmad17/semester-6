% Lab 06 - Post-Lab Task: Interactive Filter Selection
% Script that applies different filters based on user choice
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');
img = double(img);

% Display menu
disp('=================================');
disp('Image Filtering Options');
disp('=================================');
disp('1. Mean Filter');
disp('2. Gaussian Filter');
disp('3. Median Filter');
disp('4. Laplacian Filter');
disp('5. Sobel Edge Detection');
disp('6. Prewitt Edge Detection');
disp('=================================');

choice = input('Select filter type (1-6): ');

% Default parameters
filter_size = 3;
sigma = 1;

% Process based on choice
switch choice
    case 1
        % Mean Filter
        filter_size = input('Enter filter size (e.g., 3, 5, 7): ');
        h = ones(filter_size, filter_size) / (filter_size^2);
        img_filtered = imfilter(img, h, 'replicate');
        filter_name = ['Mean Filter ', num2str(filter_size), 'x', num2str(filter_size)];
        
    case 2
        % Gaussian Filter
        filter_size = input('Enter filter size (e.g., 3, 5, 7): ');
        sigma = input('Enter sigma value (e.g., 0.5, 1, 2): ');
        h = fspecial('gaussian', [filter_size filter_size], sigma);
        img_filtered = imfilter(img, h, 'replicate');
        filter_name = ['Gaussian Filter ', num2str(filter_size), 'x', num2str(filter_size), ', sigma=', num2str(sigma)];
        
    case 3
        % Median Filter
        filter_size = input('Enter filter size (e.g., 3, 5, 7): ');
        img_filtered = medfilt2(uint8(img), [filter_size filter_size]);
        img_filtered = double(img_filtered);
        filter_name = ['Median Filter ', num2str(filter_size), 'x', num2str(filter_size)];
        
    case 4
        % Laplacian Filter
        disp('Laplacian type:');
        disp('1. 4-connected');
        disp('2. 8-connected');
        lap_type = input('Select type (1-2): ');
        if lap_type == 1
            h = [0 1 0; 1 -4 1; 0 1 0];
        else
            h = [1 1 1; 1 -8 1; 1 1 1];
        end
        img_filtered = imfilter(img, h, 'replicate');
        img_filtered = abs(img_filtered);
        filter_name = 'Laplacian Filter';
        
    case 5
        % Sobel Edge Detection
        disp('Sobel direction:');
        disp('1. Horizontal');
        disp('2. Vertical');
        disp('3. Both (Magnitude)');
        direction = input('Select direction (1-3): ');
        h_x = fspecial('sobel');
        h_y = h_x';
        if direction == 1
            img_filtered = abs(imfilter(img, h_x, 'replicate'));
        elseif direction == 2
            img_filtered = abs(imfilter(img, h_y, 'replicate'));
        else
            img_x = imfilter(img, h_x, 'replicate');
            img_y = imfilter(img, h_y, 'replicate');
            img_filtered = sqrt(img_x.^2 + img_y.^2);
        end
        filter_name = 'Sobel Edge Detection';
        
    case 6
        % Prewitt Edge Detection
        disp('Prewitt direction:');
        disp('1. Horizontal');
        disp('2. Vertical');
        disp('3. Both (Magnitude)');
        direction = input('Select direction (1-3): ');
        h_x = fspecial('prewitt');
        h_y = h_x';
        if direction == 1
            img_filtered = abs(imfilter(img, h_x, 'replicate'));
        elseif direction == 2
            img_filtered = abs(imfilter(img, h_y, 'replicate'));
        else
            img_x = imfilter(img, h_x, 'replicate');
            img_y = imfilter(img, h_y, 'replicate');
            img_filtered = sqrt(img_x.^2 + img_y.^2);
        end
        filter_name = 'Prewitt Edge Detection';
        
    otherwise
        disp('Invalid choice!');
        return;
end

% Display results
figure;
subplot(1,2,1);
imshow(uint8(img));
title('Original Image');

subplot(1,2,2);
imshow(uint8(img_filtered));
title(filter_name);

sgtitle('Image Filtering Result');
