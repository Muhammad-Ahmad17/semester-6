
i = imread('cameraman.tif');
bw = im2bw(i, 128/255);
binaryImg = uint8(bw) * 255;
subplot(1,2,1)
imshow(i)
title('origional image')

subplot(1,2,2)
imshow(binaryImg);
title('binarize image')


%im2bw grayscale image ko binary image me convert karta hai jahan
%threshold se kam pixels 0 aur threshold se zyada pixels 1 ban jate hain.