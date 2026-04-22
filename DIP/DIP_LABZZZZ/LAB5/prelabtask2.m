clc;clear;close all
% Load a built-in image
img = imread('coins.png');
% Create a 5x5 averaging filter (all values are 1/25)
% This averages a 5x5 neighborhood for every pixel
kernel_smooth = ones(5, 5) / 25; %5x5 ka matrix sab ki value 1 or /25 har value div by 25
% Apply the filter
smoothed_img = imfilter(img, kernel_smooth);
%imfilter kernel ko image par slide karta hai
%Har pixel ke liye:
%Uske 5×5 neighbors leta hai
%Unka average nikalta hai
%Center pixel ko replace kar deta hai

% Display results
subplot(1,2,1), imshow(img), title('Original');
subplot(1,2,2), imshow(smoothed_img), title('Smoothed (5x5 Average)')