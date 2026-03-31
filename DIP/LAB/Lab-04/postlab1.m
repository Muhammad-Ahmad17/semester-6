% Lab 04 - Post-Lab Task: Histogram Matching
% Match histogram of grayscale image to transformed version
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');

% Create intensity transformed image (e.g., using imadjust)
img_target = imadjust(img, [], [], 0.5);  % Brighter image as target

% Get image dimensions
[M, N] = size(img);
total_pixels = M * N;

%% Calculate histogram and CDF of source image
hist_src = zeros(1, 256);
for i = 1:M
    for j = 1:N
        hist_src(img(i,j) + 1) = hist_src(img(i,j) + 1) + 1;
    end
end
pdf_src = hist_src / total_pixels;
cdf_src = cumsum(pdf_src);

%% Calculate histogram and CDF of target image
hist_tar = zeros(1, 256);
for i = 1:M
    for j = 1:N
        hist_tar(img_target(i,j) + 1) = hist_tar(img_target(i,j) + 1) + 1;
    end
end
pdf_tar = hist_tar / total_pixels;
cdf_tar = cumsum(pdf_tar);

%% Create mapping function for histogram matching
mapping = zeros(1, 256);
for i = 1:256
    % Find closest CDF value in target
    [~, idx] = min(abs(cdf_tar - cdf_src(i)));
    mapping(i) = idx - 1;  % Convert back to 0-255 range
end

%% Apply mapping to source image
img_matched = zeros(M, N, 'uint8');
for i = 1:M
    for j = 1:N
        img_matched(i,j) = mapping(img(i,j) + 1);
    end
end

%% Display results
figure;
subplot(2,3,1);
imshow(img);
title('Source Image');

subplot(2,3,2);
imshow(img_target);
title('Target Image');

subplot(2,3,3);
imshow(img_matched);
title('Matched Image');

% Calculate histogram of matched image
hist_matched = zeros(1, 256);
for i = 1:M
    for j = 1:N
        hist_matched(img_matched(i,j) + 1) = hist_matched(img_matched(i,j) + 1) + 1;
    end
end

subplot(2,3,4);
bar(0:255, hist_src);
title('Source Histogram');
xlim([0 255]);

subplot(2,3,5);
bar(0:255, hist_tar);
title('Target Histogram');
xlim([0 255]);

subplot(2,3,6);
bar(0:255, hist_matched);
title('Matched Histogram');
xlim([0 255]);

sgtitle('Histogram Matching');
