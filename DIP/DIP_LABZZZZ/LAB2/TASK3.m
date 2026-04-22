clc; clear; close all;
img = imread('peppers.png');
figure;
% --- Original Image ---
subplot(1,2,1); % 1 row, 2 columns, position 1
h_orig = imshow(img);
title('Original RGB Image');

% --- Modified Image ---
subplot(1, 2, 2); % 1 row, 2 columns, position 2
h_rgb = imshow(img); % Initialize with original
title('Modified RGB Image (Vertically Flipped)');
% Overwrite properties using OOP approach
set(h_rgb, 'CData', flipud(img)); 
set(h_rgb, 'Interpolation','bilinear');

% --- Display information in Command Window ---
disp('Modified Image Properties:');
disp(['Interpolation: ', get(h_rgb, 'Interpolation')]);
disp(['CData:Flipped']);