clc;clear;close all

img = imread('cameraman.tif');
imshow(img);
title('Cameraman Image');
print('-dsvg', '-r300', 'cameraman_300dpi.svg');
print('-dsvg', '-r900', 'cameraman_300dpi.svg');
