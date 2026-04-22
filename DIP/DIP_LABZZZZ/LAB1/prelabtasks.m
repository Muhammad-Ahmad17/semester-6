%rading a grey scale image
% clc;clear;close all
% i=imread('cameraman.tif')
% imshow(i)



%reading a colour full image
% clc;clear;close all
% i=imread('peppers.png')
% imshow(i)


%subplot
clc;clear;close all
i=imread('cameraman.tif')
U=i-100   %-100 form each value like imtensity etc
subplot(1,2,1);
imshow(i);
title('origional image')
subplot(1,2,2);
imshow(U);
title('updated image')
imwrite(U,'new.png')



%finding no of rowsa and no of cols of image
% A=imread('cameraman.tif')
% [rows,cols]=size(A)


