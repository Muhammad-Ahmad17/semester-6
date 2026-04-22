clc;clear;close all
M=100
N=1000

subplot(1,3,1);
img_zeros=zeros(M,N)
imshow(img_zeros)
title('matrix of zeros');

subplot(1,3,2);
img_ones=ones(M,N)
imshow(img_ones)
title('matrix of ones');

subplot(1,3,3);
strips_pattern=[img_zeros;img_ones;img_zeros;img_ones;img_zeros;img_ones;]
imshow(strips_pattern);
title('total 6 rows')