clc; clear; close all;

% Read image
img = imread('cameraman.tif');

% Contrast Stretching
contrastImg = intensityTransform(img,'contrast',[70 0 140 255]);

% Log Transformation
logImg1 = intensityTransform(img,'log',1);     % c = 1
logImg2 = intensityTransform(img,'log',5);     % c = 5

% Power-Law Transformation
powerImg1 = intensityTransform(img,'power',[0.5 1]);   % gamma=0.5, c=1
powerImg2 = intensityTransform(img,'power',[2 1]);     % gamma=2, c=1

% Display
figure;

subplot(2,3,1), imshow(img), title('Original');
subplot(2,3,2), imshow(contrastImg), title('Contrast Stretching');
subplot(2,3,3), imshow(logImg1), title('Log c=1');
subplot(2,3,4), imshow(logImg2), title('Log c=5');
subplot(2,3,5), imshow(powerImg1), title('Power gamma=0.5');
subplot(2,3,6), imshow(powerImg2), title('Power gamma=2');