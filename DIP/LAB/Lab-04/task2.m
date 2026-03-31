% Lab 04 - Task 2: Histogram Equalization without histeq
% Apply histogram equalization manually
clc; clear; close all;

% Read grayscale image
img = imread('pout.tif');

% Get image dimensions
[M, N] = size(img);
total_pixels = M * N;

% Step 1: Calculate histogram
histogram = zeros(1, 256);
for i = 1:M
    for j = 1:N
        intensity = img(i, j);
        histogram(intensity + 1) = histogram(intensity + 1) + 1;
    end
end

% Step 2: Calculate probability (PDF)
pdf = histogram / total_pixels;

% Step 3: Calculate cumulative distribution function (CDF)
cdf = zeros(1, 256);
cdf(1) = pdf(1);
for k = 2:256
    cdf(k) = cdf(k-1) + pdf(k);
end

% Step 4: Create transformation mapping
% Map CDF to 0-255 range
transform = round(cdf * 255);

% Step 5: Apply transformation to image
img_eq = zeros(M, N, 'uint8');
for i = 1:M
    for j = 1:N
        intensity = img(i, j);
        img_eq(i, j) = transform(intensity + 1);
    end
end

% Display results
figure;
subplot(2,2,1);
imshow(img);
title('Original Image');

subplot(2,2,2);
imshow(img_eq);
title('Histogram Equalized Image');

% Calculate histogram of equalized image
histogram_eq = zeros(1, 256);
for i = 1:M
    for j = 1:N
        intensity = img_eq(i, j);
        histogram_eq(intensity + 1) = histogram_eq(intensity + 1) + 1;
    end
end

subplot(2,2,3);
bar(0:255, histogram);
xlabel('Intensity Level');
ylabel('Pixels');
title('Original Histogram');
xlim([0 255]);

subplot(2,2,4);
bar(0:255, histogram_eq);
xlabel('Intensity Level');
ylabel('Pixels');
title('Equalized Histogram');
xlim([0 255]);

sgtitle('Histogram Equalization Without histeq()');
