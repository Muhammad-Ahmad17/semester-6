clc;clear;close all
i=imread('cameraman.tif')
subplot(2,1,1);
imshow(i);
title('origional image');
subplot(2,1,2);
imshow(i,[30 100]) % jin pixels ki value 30 say kam hai wp zero ma 
%conert ho jati haie or jin ki value 100 say zyada hai wo 1 ma convert ho jati hai