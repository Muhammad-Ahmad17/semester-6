% Lab 07 - Pre-Lab Task: Fourier Transform of Image
% Find Fourier transform and display frequency domain representation
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');
img = double(img);

% Compute 2D Fourier Transform
F = fft2(img);

% Shift zero frequency to center
F_shifted = fftshift(F);

% Compute magnitude spectrum
magnitude = abs(F_shifted);
magnitude_log = log(1 + magnitude);  % Log for better visualization

% Compute phase spectrum
phase = angle(F_shifted);

% Display results
figure;

subplot(2,2,1);
imshow(uint8(img));
title('Original Image');

subplot(2,2,2);
imshow(magnitude_log, []);
colormap(gray);
title('Magnitude Spectrum (Log Scale)');
colorbar;

subplot(2,2,3);
imshow(phase, []);
colormap(gray);
title('Phase Spectrum');
colorbar;

subplot(2,2,4);
mesh(magnitude_log);
title('3D Magnitude Spectrum');
xlabel('u'); ylabel('v'); zlabel('Magnitude');

sgtitle('Frequency Domain Analysis');
