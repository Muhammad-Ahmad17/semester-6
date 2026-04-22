% Read colored image
img = imread('muzamil.png');  % replace with your image

% Convert to grayscale using built-in
grayImg = rgb2gray(img);

% Flip image horizontally manually
[rows, cols] = size(grayImg);
flippedImg = zeros(rows, cols, 'uint8');

for i = 1:rows
    for j = 1:cols
        flippedImg(i,j) = grayImg(rows-i+1, j);  % notice rows-i+1
    end
end

% Save flipped image
fname = input('Enter filename (with .jpg): ','s');
imwrite(flippedImg, fname);

% Show both images
subplot(1,2,1), imshow(grayImg), title('Gray');
subplot(1,2,2), imshow(flippedImg), title('Flipped');