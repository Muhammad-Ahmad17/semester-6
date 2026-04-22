% Read image
img = imread('cameraman.tif');

% Get image size
[rows, cols] = size(img);

% Create output image
mirrorImg = zeros(rows, cols, 'uint8');

% Nested loops for mirror image
for i = 1:rows
    for j = 1:cols
        mirrorImg(i, j) = img(i, cols - j + 1);
    end
end

% Display original and mirror image using subplot
subplot(1,2,1)
imshow(img);
title('Original Image');

subplot(1,2,2)
imshow(mirrorImg);
title('Mirror Image');