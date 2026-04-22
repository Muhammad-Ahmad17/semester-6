clc;clear;close all
f = [0 0 0 1 0 0 0 0]; 
w = [1 2 3 2 0];       %this is filter or kernal
% --- 1-D CORRELATION ---
corr_full = imfilter(f, w, 'corr', 0, 'full') %coorelation ma kernal flip nahi hota, fill mtlb
%pura output
corr_same = imfilter(f, w, 'corr', 0, 'same') %output ka size input jaisa
% --- 1-D CONVOLUTION ---

conv_full = imfilter(f, w, 'conv', 0, 'full')%conv ma kernal pehly flip hoga baki same process
conv_same = imfilter(f, w, 'conv', 0, 'same')

%conv and correlation donu same value produce karti but conv ma flip output
%hota hai


%IMFILTER ki command say ham pixel ki values ko directly change krty hai

%Spatial Filtering kya hoti hai?
%Spatial filtering ka matlab:
%Image ke pixels ko unke paas ke pixels (neighbors) ki madad se modify karna

%Linear spatial filtering convolution par based hoti hai.


% One-Line Summary (Exam/Lab)
%Spatial filtering pixel neighborhood par kaam karti hai
%Linear filtering weighted sum use karti hai
%Convolution me kernel flip hota hai
%Correlation me kernel flip nahi hota
%imfilter se image smooth, sharp, ya edges detect kiye jate hain