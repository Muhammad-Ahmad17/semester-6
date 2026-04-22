%use stretchlim adjust limits
I = imread('pout.tif');
J = imadjust(I,stretchlim(I),[]);
figure;
subplot(121)
imshow(I);
subplot(122)
 imshow(J)

 
 %? stretchlim(I)

%Image ke useful intensity limits nikalta hai.

%Matlab:

%Bahut dark aur bahut bright pixels ignore karta hai

%Beech ka range detect karta hai

%? imadjust(...)

%Image ka contrast stretch karta hai

%Pixel values ko new range me map karta hai

%[] ka matlab:
%? Output range default rakho (0 to 255 for uint8)

%Result:

%Dark pixels dark rahte hain

%Bright pixels bright ho jate hain

%Image zyada sharp lagti hai