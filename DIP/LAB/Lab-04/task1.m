% Lab 04 - Task 1: Histogram Formation without imhist
% Display histogram of an image using custom implementation
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');

% Get image dimensions
[M, N] = size(img);

% Initialize histogram array (256 bins for 0-255)
histogram = zeros(1, 256);

% Count pixel intensities
for i = 1:M
    for j = 1:N
        intensity = img(i, j);
        histogram(intensity + 1) = histogram(intensity + 1) + 1;
    end
end

% Display original image
figure;
subplot(2,2,1);
imshow(img);
title('Original Grayscale Image');

% Display histogram as bar graph
subplot(2,2,2);
bar(0:255, histogram);
xlabel('Intensity Level');
ylabel('Number of Pixels');
title('Histogram (Bar Graph)');
xlim([0 255]);

% Display histogram as stem plot
subplot(2,2,3);
stem(0:255, histogram, 'Marker', 'none');
xlabel('Intensity Level');
ylabel('Number of Pixels');
title('Histogram (Stem Plot)');
xlim([0 255]);

% Display histogram as line plot
subplot(2,2,4);
plot(0:255, histogram, 'b-', 'LineWidth', 1);
xlabel('Intensity Level');
ylabel('Number of Pixels');
title('Histogram (Line Plot)');
xlim([0 255]);

sgtitle('Histogram Formation Without imhist()');
