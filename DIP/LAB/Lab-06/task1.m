% Lab 06 - Task 1: Linear and Non-Linear Spatial Filters
% Apply Mean, Weighted Average, Median, and Laplacian filters
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');
img = double(img);

% Add some noise for better demonstration
img_noisy = img + 20 * randn(size(img));
img_noisy = max(0, min(255, img_noisy));  % Clip to valid range

%% Part 1: Mean Filter (Box Filter)
figure;
sgtitle('Mean Filter with Different Sizes');

subplot(2,3,1);
imshow(uint8(img_noisy));
title('Noisy Image');

% 3x3 Mean filter
h_mean3 = ones(3,3) / 9;
img_mean3 = imfilter(img_noisy, h_mean3, 'replicate');
subplot(2,3,2);
imshow(uint8(img_mean3));
title('Mean 3x3');

% 5x5 Mean filter
h_mean5 = ones(5,5) / 25;
img_mean5 = imfilter(img_noisy, h_mean5, 'replicate');
subplot(2,3,3);
imshow(uint8(img_mean5));
title('Mean 5x5');

% 7x7 Mean filter
h_mean7 = ones(7,7) / 49;
img_mean7 = imfilter(img_noisy, h_mean7, 'replicate');
subplot(2,3,4);
imshow(uint8(img_mean7));
title('Mean 7x7');

% 9x9 Mean filter
h_mean9 = ones(9,9) / 81;
img_mean9 = imfilter(img_noisy, h_mean9, 'replicate');
subplot(2,3,5);
imshow(uint8(img_mean9));
title('Mean 9x9');

% 11x11 Mean filter
h_mean11 = ones(11,11) / 121;
img_mean11 = imfilter(img_noisy, h_mean11, 'replicate');
subplot(2,3,6);
imshow(uint8(img_mean11));
title('Mean 11x11');

%% Part 2: Weighted Average Filter (Gaussian-like)
figure;
sgtitle('Weighted Average Filters');

subplot(2,2,1);
imshow(uint8(img_noisy));
title('Noisy Image');

% Weighted average 3x3
h_weighted = [1 2 1; 2 4 2; 1 2 1] / 16;
img_weighted = imfilter(img_noisy, h_weighted, 'replicate');
subplot(2,2,2);
imshow(uint8(img_weighted));
title('Weighted 3x3');

% Gaussian filter (built-in weighted average)
h_gauss = fspecial('gaussian', [5 5], 1);
img_gauss = imfilter(img_noisy, h_gauss, 'replicate');
subplot(2,2,3);
imshow(uint8(img_gauss));
title('Gaussian 5x5, sigma=1');

% Gaussian with larger sigma
h_gauss2 = fspecial('gaussian', [5 5], 2);
img_gauss2 = imfilter(img_noisy, h_gauss2, 'replicate');
subplot(2,2,4);
imshow(uint8(img_gauss2));
title('Gaussian 5x5, sigma=2');

%% Part 3: Median Filter (Non-linear)
% Add salt and pepper noise
img_sp = img;
noise_density = 0.05;
salt = rand(size(img)) < noise_density/2;
pepper = rand(size(img)) < noise_density/2;
img_sp(salt) = 255;
img_sp(pepper) = 0;

figure;
sgtitle('Median Filter for Salt & Pepper Noise');

subplot(2,3,1);
imshow(uint8(img_sp));
title('Salt & Pepper Noise');

% Median filter with different sizes
img_med3 = medfilt2(uint8(img_sp), [3 3]);
subplot(2,3,2);
imshow(img_med3);
title('Median 3x3');

img_med5 = medfilt2(uint8(img_sp), [5 5]);
subplot(2,3,3);
imshow(img_med5);
title('Median 5x5');

img_med7 = medfilt2(uint8(img_sp), [7 7]);
subplot(2,3,4);
imshow(img_med7);
title('Median 7x7');

% Compare mean vs median on salt & pepper
img_mean_sp = imfilter(img_sp, h_mean3, 'replicate');
subplot(2,3,5);
imshow(uint8(img_mean_sp));
title('Mean 3x3 (Comparison)');

subplot(2,3,6);
imshow(uint8(img));
title('Original Clean');

%% Part 4: Laplacian Filter (Edge Detection)
figure;
sgtitle('Laplacian Filter');

subplot(2,2,1);
imshow(uint8(img));
title('Original Image');

% Standard Laplacian
h_lap1 = [0 1 0; 1 -4 1; 0 1 0];
img_lap1 = imfilter(img, h_lap1, 'replicate');
subplot(2,2,2);
imshow(uint8(abs(img_lap1)));
title('Laplacian (4-connected)');

% Diagonal Laplacian
h_lap2 = [1 1 1; 1 -8 1; 1 1 1];
img_lap2 = imfilter(img, h_lap2, 'replicate');
subplot(2,2,3);
imshow(uint8(abs(img_lap2)));
title('Laplacian (8-connected)');

% Sharpening using Laplacian
img_sharp = img - img_lap1;
img_sharp = max(0, min(255, img_sharp));
subplot(2,2,4);
imshow(uint8(img_sharp));
title('Sharpened Image');
