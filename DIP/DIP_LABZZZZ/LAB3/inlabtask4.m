I = imread('muzamil.png');
I = im2double(I);   
subplot(1,3,1);
imshow(I);
title('origiobal image');

subplot(1,3,2)
neg = imadjust(I,[0 1],[1 0]);   
imshow(neg);
title('using adjust function');

subplot(1,3,3)
comp =imcomplement(I)  ;
imshow(comp);
title('using imcomplement');



