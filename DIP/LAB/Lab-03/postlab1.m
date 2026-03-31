% Lab 03 - Post-Lab Task: Custom Intensity Transformation Functions
% Implement contrast stretching, log, and power law transformations
clc; clear; close all;

% Read grayscale image
img = imread('pout.tif');
img = double(img);

% Get image dimensions
[M, N] = size(img);

%% 1. Contrast Stretching Transformation
% s = 1 / (1 + (k/r)^E)
k = 128;  % midpoint
E_values = [1, 5, 10];  % different slope values

figure;
subplot(2,3,1);
imshow(uint8(img));
title('Original Image');

for i = 1:length(E_values)
    E = E_values(i);
    img_contrast = zeros(M, N);
    
    for x = 1:M
        for y = 1:N
            r = img(x, y);
            if r == 0
                r = 0.001;  % avoid division by zero
            end
            img_contrast(x, y) = 255 / (1 + (k/r)^E);
        end
    end
    
    subplot(2,3,i+1);
    imshow(uint8(img_contrast));
    title(['Contrast Stretch E=', num2str(E)]);
end

sgtitle('Contrast Stretching Transformation');

%% 2. Log Transformation
% s = c * log(1 + r)
c_values = [1, 30, 50];

figure;
subplot(2,2,1);
imshow(uint8(img));
title('Original Image');

for i = 1:length(c_values)
    c = c_values(i);
    img_log = c * log(1 + img);
    
    % Normalize to 0-255 range
    img_log = img_log / max(img_log(:)) * 255;
    
    subplot(2,2,i+1);
    imshow(uint8(img_log));
    title(['Log Transform c=', num2str(c)]);
end

sgtitle('Log Transformation');

%% 3. Power Law (Gamma) Transformation
% s = c * r^gamma
c = 1;
gamma_values = [0.4, 1.0, 2.0, 4.0];

figure;
subplot(2,3,1);
imshow(uint8(img));
title('Original Image');

% Normalize image to [0,1] for power law
img_norm = img / 255;

for i = 1:length(gamma_values)
    gamma = gamma_values(i);
    img_power = c * (img_norm .^ gamma);
    img_power = img_power * 255;
    
    subplot(2,3,i+1);
    imshow(uint8(img_power));
    title(['Power Law gamma=', num2str(gamma)]);
end

sgtitle('Power Law Transformation');

disp('Observations:');
disp('Contrast Stretching: Higher E values produce sharper transitions');
disp('Log Transform: Expands dark intensities, compresses bright intensities');
disp('Power Law: gamma<1 brightens, gamma>1 darkens the image');
