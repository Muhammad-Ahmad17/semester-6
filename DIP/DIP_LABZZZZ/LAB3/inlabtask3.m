%complementing the image

i=imread('muzamil.png');
subplot(1,2,1)
imshow(i);
title('origional image')

comp=imcomplement(i);
subplot(1,2,2)
imshow(comp);
title('complemented image')