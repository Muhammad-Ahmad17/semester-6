% clc;
% clear all;
% close all;
% % Load and process image
% img = imread('peppers.png');
% img = im2double(img);% used while reconstruction
% % Convert to grayscale
% img_gray = rgb2gray(img);
% % Apply contrast adjustment
% img_adjust = imadjust(img_gray, [0.3, 0.7], [0 1]);% 0.3 less contrast level covert  into zero and 0.7 greater contrast level convert into 1
% figure();
% subplot(1, 3, 1);
% imshow(img);
% title('Original RGB Image');
% subplot(1, 3, 2);
% imshow(img_gray);
% title('Grayscale Image');
% subplot(1, 3, 3);
% imshow(img_adjust);
% title('Contrast Adjusted Image')

%for color full image
% clc;
% clear all;
% close all;
% RGB = imread('peppers.png');
% subplot(121)
% imshow(RGB)
% title('original')
% RGB2 = imadjust(RGB,[.2 .3 0; .6 .7 1],[]); red stretch form 0.2 to 0.6
% green 0.3 to 0.7 blue 0 to 1 already max value
% subplot(122)
% 
% imshow(RGB2)
% title('Adjusted')

%another build in image pout 
clc;
clear all;
close all;
i = imread('pout.tif');
subplot(121)
imshow(i)
title('original')
i2 = imadjust(i, [0.3, 0.7], [0 1]);
subplot(122)
imshow(i2)
title('contrat adjusted')