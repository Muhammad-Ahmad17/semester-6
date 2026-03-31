% Lab 07 - Task 2: Fourier Transform and Inverse Fourier Transform
% Apply FFT and IFFT to verify reconstruction
clc; clear; close all;

% Read grayscale image
img = imread('cameraman.tif');
img = double(img);

%% Step 1: Apply Fourier Transform
F = fft2(img);

% Shift for visualization
F_shifted = fftshift(F);

%% Step 2: Visualize frequency domain
magnitude = log(1 + abs(F_shifted));

%% Step 3: Apply Inverse Fourier Transform
img_reconstructed = ifft2(F);

% Take real part (imaginary should be negligible)
img_reconstructed = real(img_reconstructed);

%% Step 4: Verify reconstruction
reconstruction_error = abs(img - img_reconstructed);
max_error = max(reconstruction_error(:));

%% Display Results
figure;

subplot(2,2,1);
imshow(uint8(img));
title('Original Image');

subplot(2,2,2);
imshow(magnitude, []);
colormap(gray);
title('Fourier Transform (Magnitude)');

subplot(2,2,3);
imshow(uint8(img_reconstructed));
title('Reconstructed Image (IFFT)');

subplot(2,2,4);
imshow(reconstruction_error, []);
title('Reconstruction Error');
colorbar;

sgtitle('Fourier Transform and Inverse');

%% Verification
disp('=== Reconstruction Verification ===');
disp(['Maximum reconstruction error: ', num2str(max_error)]);
disp(['Mean reconstruction error: ', num2str(mean(reconstruction_error(:)))]);

if max_error < 1e-10
    disp('SUCCESS: Image is perfectly reconstructed!');
else
    disp('Note: Small numerical errors exist (floating-point precision)');
end

% Compare original and reconstructed
figure;
subplot(1,2,1);
imshow(uint8(img));
title('Original');

subplot(1,2,2);
imshow(uint8(img_reconstructed));
title('Reconstructed');

sgtitle('Comparison: Original vs Reconstructed');
