% Lab 05 - Post-Lab Task: Spatial Filtering Variations
% Apply different boundary options and output size options
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');
img = double(img);

% Create averaging filter
h = fspecial('average', 7);

%% Part 1: Different boundary options
figure;
sgtitle('Boundary Options for Spatial Filtering');

subplot(2,3,1);
imshow(uint8(img));
title('Original');

% Zero padding (default)
img_zero = imfilter(img, h, 0);
subplot(2,3,2);
imshow(uint8(img_zero));
title('Zero Padding');

% Replicate boundary
img_rep = imfilter(img, h, 'replicate');
subplot(2,3,3);
imshow(uint8(img_rep));
title('Replicate');

% Symmetric boundary
img_sym = imfilter(img, h, 'symmetric');
subplot(2,3,4);
imshow(uint8(img_sym));
title('Symmetric');

% Circular boundary
img_circ = imfilter(img, h, 'circular');
subplot(2,3,5);
imshow(uint8(img_circ));
title('Circular');

%% Part 2: Output size options
figure;
sgtitle('Output Size Options');

subplot(1,3,1);
imshow(uint8(img));
title(['Original: ', num2str(size(img,1)), 'x', num2str(size(img,2))]);

% Same size output (default)
img_same = imfilter(img, h, 'same');
subplot(1,3,2);
imshow(uint8(img_same));
title(['Same: ', num2str(size(img_same,1)), 'x', num2str(size(img_same,2))]);

% Full output
img_full = imfilter(img, h, 'full');
subplot(1,3,3);
imshow(uint8(img_full));
title(['Full: ', num2str(size(img_full,1)), 'x', num2str(size(img_full,2))]);

%% Part 3: Correlation vs Convolution
figure;
sgtitle('Correlation vs Convolution');

% Create asymmetric filter to show difference
h_asym = [1 2 3; 4 5 6; 7 8 9];

subplot(1,3,1);
imshow(uint8(img));
title('Original');

% Correlation (default)
img_corr = imfilter(img, h_asym, 'corr', 'replicate');
img_corr = img_corr / sum(h_asym(:)) * 255;
subplot(1,3,2);
imshow(uint8(img_corr));
title('Correlation');

% Convolution (filter is flipped)
img_conv = imfilter(img, h_asym, 'conv', 'replicate');
img_conv = img_conv / sum(h_asym(:)) * 255;
subplot(1,3,3);
imshow(uint8(img_conv));
title('Convolution');

disp('Observations:');
disp('Boundary options affect edge handling');
disp('Output size options control final image dimensions');
disp('Correlation and Convolution differ when filter is asymmetric');
