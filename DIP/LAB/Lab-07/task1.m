% Lab 07 - Task 1: Frequency Domain Analysis
% Plot magnitude and phase response using mathematical formula
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');
img = double(img);

[M, N] = size(img);

%% Manual DFT Computation (for small region due to computational cost)
% For demonstration, we'll use fft2 but understand the formula:
% F(u,v) = sum(sum(f(x,y) * exp(-j*2*pi*(u*x/M + v*y/N))))

% Using built-in for efficiency
F = fft2(img);

% Shift DC component to center
F_shifted = fftshift(F);

%% Magnitude Response
% |F(u,v)| = sqrt(real(F)^2 + imag(F)^2)
magnitude = sqrt(real(F_shifted).^2 + imag(F_shifted).^2);

% Log scale for better visualization
magnitude_log = log(1 + magnitude);

%% Phase Response
% angle(F(u,v)) = atan2(imag(F), real(F))
phase = atan2(imag(F_shifted), real(F_shifted));

%% Display Results
figure;

subplot(2,2,1);
imshow(uint8(img));
title('Original Image');

subplot(2,2,2);
imshow(magnitude_log, []);
colormap(gray);
title('Magnitude Response (Log Scale)');
colorbar;

subplot(2,2,3);
imshow(phase, []);
colormap(gray);
title('Phase Response');
colorbar;

% Create frequency axis for plotting
u = -M/2:(M/2-1);
v = -N/2:(N/2-1);

subplot(2,2,4);
surf(v, u, magnitude_log);
shading interp;
title('3D Magnitude Surface');
xlabel('v'); ylabel('u'); zlabel('Log Magnitude');
view(45, 30);

sgtitle('Magnitude and Phase Response Analysis');

%% Analysis
disp('Magnitude Response Analysis:');
disp('- The bright center represents low frequencies (DC component)');
disp('- Edges and details contribute to high frequencies (outer regions)');
disp('- The pattern reveals directional information in the image');
disp(' ');
disp('Phase Response Analysis:');
disp('- Phase carries structural information about the image');
disp('- It determines the position of image features');
disp('- Phase is more important for image recognition than magnitude');
