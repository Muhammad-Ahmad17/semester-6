clc;clear;close all
img_rgb = imread('peppers.png');
img_rgb_gray = rgb2gray(img_rgb);
fig2 = figure('Name', 'RGB (Gray) Image with Tools');
h_panel_rgb = imscrollpanel(fig2, imshow(img_rgb_gray));
h_img_rgb = findobj(h_panel_rgb, 'Type', 'image');
imcontrast(h_img_rgb);
imdisplayrange(h_img_rgb);
immagbox(fig2, h_img_rgb);
imdistline(gca);