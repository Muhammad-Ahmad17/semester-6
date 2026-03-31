% Lab 05 - Task 1: Spatial Filtering using imfilter
% Explore different filter options with imfilter
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');
img = double(img);

% Create a simple averaging filter (3x3)
h = fspecial('average', 3);

% Apply filter with different options
figure;

% Original image
subplot(2,3,1);
imshow(uint8(img));
title('Original Image');

% Default filtering
img_default = imfilter(img, h);
subplot(2,3,2);
imshow(uint8(img_default));
title('Default Filtering');

% Filtering with 'replicate' boundary option
img_replicate = imfilter(img, h, 'replicate');
subplot(2,3,3);
imshow(uint8(img_replicate));
title('Replicate Boundary');

% Filtering with 'symmetric' boundary option
img_symmetric = imfilter(img, h, 'symmetric');
subplot(2,3,4);
imshow(uint8(img_symmetric));
title('Symmetric Boundary');

% Filtering with 'circular' boundary option
img_circular = imfilter(img, h, 'circular');
subplot(2,3,5);
imshow(uint8(img_circular));
title('Circular Boundary');

% Filtering using 'conv' instead of 'corr'
img_conv = imfilter(img, h, 'conv');
subplot(2,3,6);
imshow(uint8(img_conv));
title('Convolution');

sgtitle('Spatial Filtering with imfilter - Different Options');

%% Explore different filter types
figure;

% Gaussian filter
h_gaussian = fspecial('gaussian', [5 5], 1.5);
img_gauss = imfilter(img, h_gaussian, 'replicate');
subplot(2,3,1);
imshow(uint8(img_gauss));
title('Gaussian Filter');

% Laplacian filter
h_laplacian = fspecial('laplacian', 0.2);
img_lap = imfilter(img, h_laplacian, 'replicate');
img_lap = img_lap + 128;  % Shift for visualization
subplot(2,3,2);
imshow(uint8(img_lap));
title('Laplacian Filter');

% Sobel filter (horizontal)
h_sobel = fspecial('sobel');
img_sobel = imfilter(img, h_sobel, 'replicate');
subplot(2,3,3);
imshow(uint8(abs(img_sobel)));
title('Sobel Filter (Horizontal)');

% Prewitt filter
h_prewitt = fspecial('prewitt');
img_prewitt = imfilter(img, h_prewitt, 'replicate');
subplot(2,3,4);
imshow(uint8(abs(img_prewitt)));
title('Prewitt Filter');

% Motion blur filter
h_motion = fspecial('motion', 20, 45);
img_motion = imfilter(img, h_motion, 'replicate');
subplot(2,3,5);
imshow(uint8(img_motion));
title('Motion Blur');

% Unsharp masking
h_unsharp = fspecial('unsharp');
img_unsharp = imfilter(img, h_unsharp, 'replicate');
subplot(2,3,6);
imshow(uint8(img_unsharp));
title('Unsharp Masking');

sgtitle('Different Filter Types');
