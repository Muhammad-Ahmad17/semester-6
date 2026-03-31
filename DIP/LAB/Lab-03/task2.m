% Lab 03 - Task 2: Analyzing impact of different gamma values
% Display and discuss observations with various gamma settings
clc; clear; close all;

% Read grayscale image
img = imread('pout.tif');

% Create figure for comparison
figure;

% Original image
subplot(2,4,1);
imshow(img);
title('Original');

% Different gamma values
gamma_values = [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0];

for i = 1:length(gamma_values)
    gamma = gamma_values(i);
    img_transformed = imadjust(img, [], [], gamma);
    subplot(2,4,i+1);
    imshow(img_transformed);
    title(['Gamma = ', num2str(gamma)]);
end

sgtitle('Impact of Different Gamma Values');

% Display observations
disp('Observations:');
disp('Gamma < 1: Image becomes brighter, dark regions are enhanced');
disp('Gamma = 1: No change in intensity');
disp('Gamma > 1: Image becomes darker, bright regions are compressed');
