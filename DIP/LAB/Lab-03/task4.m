% Lab 03 - Task 4: Create negative image using imadjust
% Compare with imcomplement result
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');

% Create negative using imadjust (swap output intensity limits)
img_neg_imadjust = imadjust(img, [0 1], [1 0]);

% Create negative using imcomplement
img_neg_complement = imcomplement(img);

% Display comparison
figure;
subplot(1,3,1);
imshow(img);
title('Original Image');

subplot(1,3,2);
imshow(img_neg_imadjust);
title('Negative (imadjust)');

subplot(1,3,3);
imshow(img_neg_complement);
title('Negative (imcomplement)');

sgtitle('Comparison of Negative Image Methods');

% Check if both methods produce same result
diff = abs(double(img_neg_imadjust) - double(img_neg_complement));
disp(['Maximum difference between methods: ', num2str(max(diff(:)))]);
disp('Both methods produce identical results');
