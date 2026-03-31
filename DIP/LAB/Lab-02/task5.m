clc;clear;close all

img_gray = imread('cameraman.tif');

fig1 = figure('Name', 'Grayscale Image with Tools');

h_panel_gray = imscrollpanel(fig1, imshow(img_gray));

h_img_gray = findobj(h_panel_gray, 'Type', 'image');

imcontrast(h_img_gray);
imdisplayrange(h_img_gray);
immagbox(fig1, h_img_gray);
imdistline(gca);