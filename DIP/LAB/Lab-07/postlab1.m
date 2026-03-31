% Lab 07 - Post-Lab Task: Inverse Fourier Transform
% Verify that IFFT produces identical image to input
clc; clear; close all;

% Read multiple test images
images = {'cameraman.tif', 'coins.png', 'rice.png'};

figure;
plot_idx = 1;

for i = 1:length(images)
    % Read image
    img = imread(images{i});
    
    % Convert to grayscale if needed
    if size(img, 3) == 3
        img = rgb2gray(img);
    end
    img = double(img);
    
    %% Apply Fourier Transform
    F = fft2(img);
    
    %% Apply Inverse Fourier Transform
    img_recovered = ifft2(F);
    img_recovered = real(img_recovered);
    
    %% Calculate error
    error_img = abs(img - img_recovered);
    total_error = sum(error_img(:));
    max_error = max(error_img(:));
    
    %% Display results
    subplot(3, 4, plot_idx);
    imshow(uint8(img));
    title(['Original: ', images{i}]);
    
    subplot(3, 4, plot_idx + 1);
    F_mag = log(1 + abs(fftshift(F)));
    imshow(F_mag, []);
    title('FFT Magnitude');
    
    subplot(3, 4, plot_idx + 2);
    imshow(uint8(img_recovered));
    title('Recovered (IFFT)');
    
    subplot(3, 4, plot_idx + 3);
    imshow(error_img, []);
    title(['Error (max: ', num2str(max_error, '%.2e'), ')']);
    
    plot_idx = plot_idx + 4;
    
    % Print verification
    disp(['Image: ', images{i}]);
    disp(['  Total Error: ', num2str(total_error)]);
    disp(['  Max Error: ', num2str(max_error)]);
    if max_error < 1e-10
        disp('  Status: PERFECTLY IDENTICAL');
    else
        disp('  Status: Negligible floating-point errors');
    end
    disp(' ');
end

sgtitle('Inverse Fourier Transform Verification');

%% Additional Analysis: Phase vs Magnitude Importance
figure;

img = double(imread('cameraman.tif'));
[M, N] = size(img);

% Get FFT of two images
F1 = fft2(img);
F2 = fft2(double(imread('coins.png')));

% Resize F2 to match F1 if needed
if ~isequal(size(F1), size(F2))
    img2 = imresize(double(imread('coins.png')), [M N]);
    F2 = fft2(img2);
end

% Magnitude of F1, Phase of F2
F_mag1_phase2 = abs(F1) .* exp(1j * angle(F2));
img_mag1_phase2 = real(ifft2(F_mag1_phase2));

% Magnitude of F2, Phase of F1
F_mag2_phase1 = abs(F2) .* exp(1j * angle(F1));
img_mag2_phase1 = real(ifft2(F_mag2_phase1));

subplot(2,2,1);
imshow(uint8(img));
title('Image 1 (Cameraman)');

subplot(2,2,2);
imshow(uint8(imresize(double(imread('coins.png')), [M N])));
title('Image 2 (Coins)');

subplot(2,2,3);
imshow(uint8(abs(img_mag1_phase2)));
title('Mag of Img1 + Phase of Img2');

subplot(2,2,4);
imshow(uint8(abs(img_mag2_phase1)));
title('Mag of Img2 + Phase of Img1');

sgtitle('Phase vs Magnitude Importance');

disp('Observation: The reconstructed image looks more like the image');
disp('whose PHASE was used, demonstrating that phase carries more');
disp('structural information than magnitude.');
