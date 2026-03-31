clc; clear; close all;

img = imread('peppers.png');
figure;

% --- Original Image ---
subplot(1, 2, 1); % 1 row, 2 columns, position 1
h_orig = imshow(img)
title('Original RGB Image');

% --- Modified Image ---
subplot(1, 2, 2); 
h_rgb = imshow(img); 
title('Modified RGB Image (Vertically Flipped)');
% Overwrite properties using OOP approach
set(h_rgb, 'CData', flipud(img)); % ColourData flip up down
% flip -> left right flip
set(h_rgb, 'Interpolation','bilinear'); % check the quality improvment 

% --- Display information in Command Window ---
disp('Modified Image Properties:');
disp(['Interpolation: ', get(h_rgb, 'Interpolation')]);
disp('CData:Flipped');