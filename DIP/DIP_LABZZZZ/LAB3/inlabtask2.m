%gamma parameter here


clc;
clear all;
close all;
% Load and process image
img = imread('peppers.png');
img = im2double(img);
% Convert to grayscale
img_gray = rgb2gray(img);
%Gamma Correction with imadjust 
subplot(2,2,1);
imshow(img_gray);
title('Original Image');
% Gamma < 1
J1 = imadjust(img_gray, [], [], 0.5);
subplot(2,2,2); imshow(J1); title('Gamma = 0.5 (Bright)');
% Gamma = 1
J2 = imadjust(img_gray, [0 1], [0 1], 1);
subplot(2,2,3); imshow(J2); title('Gamma = 1(Nochange)');
% Gamma = 1.5
J3 = imadjust(img_gray, [], [], 1.5); subplot(2,2,4);
imshow(J3); title('Gamma = 1.5(Dark)');

% gamma value less then 0, image get   brigher
% gamma 1 no change
% gamma value greater then 1, image get   darker