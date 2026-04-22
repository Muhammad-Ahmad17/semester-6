clc; clear; close all

% Load grayscale image
img = imread('coins.png');
% Convert to double for filtering
img = double(img);

% Define a 3x3 spatial filter (example: smoothing)
W = [1 1 1;
     1 1 1;
     1 1 1] / 9;

%% -------- Padding Options --------

% 1) Numeric scalar padding (0)
f1 = imfilter(img, W, 'corr', 0, 'same');

% 2) Symmetric padding
f2 = imfilter(img, W, 'corr', 'symmetric', 'same');

% 3) Replicate padding
f3 = imfilter(img, W, 'corr', 'replicate', 'same');

% 4) Circular padding
f4 = imfilter(img, W, 'corr', 'circular', 'same');

%% -------- Output Size & Conv/Corr --------

% Correlation - full
f5 = imfilter(img, W, 'corr', 'symmetric', 'full');

% Convolution - same
f6 = imfilter(img, W, 'conv', 'symmetric', 'same');

%% -------- Display Results --------
figure

subplot(3,3,1), imshow(uint8(img)), title('Original')
subplot(3,3,2), imshow(uint8(f1)), title('corr + zero + same')
subplot(3,3,3), imshow(uint8(f2)), title('corr + symmetric + same')

subplot(3,3,4), imshow(uint8(f3)), title('corr + replicate + same')
subplot(3,3,5), imshow(uint8(f4)), title('corr + circular + same')

subplot(3,3,6), imshow(uint8(f5)), title('corr + symmetric + full')
subplot(3,3,7), imshow(uint8(f6)), title('conv + symmetric + same')