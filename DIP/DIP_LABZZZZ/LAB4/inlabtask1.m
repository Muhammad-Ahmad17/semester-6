clear; clear all; close all; 
img=imread('peppers.png');
imgd=rgb2gray(img);
H=imhist(imgd)
imhist(imgd)
% x axis individual pixel vale 
%y axis no of pixels exist

%plot(H)