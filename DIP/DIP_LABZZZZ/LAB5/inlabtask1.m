% Spatial Filtering
% Generate Matrix f
f = [0 0 0 0 0;
     0 0 1 0 0;
     0 0 0 0 0;
     0 0 0 0 0];

% Generate mask W
W = [1 2 3;
         4 5 6;
         7 8 9];

% Apply imfilter
disp('Using Options - corr, symmetric, full')
filt_1 = imfilter(f, W, 'corr', 'symmetric', 'full');
%corelation ma kernal flip nahi hota

% Apply imfilter
disp('Using Options - conv, symmetric, full')
filt_2 = imfilter(f, W, 'conv', 'symmetric', 'full');
%conv ma Kernel horizontal + vertical flip hota hai
%third arg default corelation hota hai

% Apply imfilter
disp('Using Options - corr, symmetric, same')
filt_3 = imfilter(f, W, 'corr', 'symmetric', 'same');

% Apply imfilter
disp('Using Options - conv, symmetric, same')
filt_4 = imfilter(f, W, 'conv', 'symmetric', 'same');

figure

subplot(3,2,1)
imshow(f, [])
%[] auto scaling
title('Original Image')

subplot(3,2,2)
imshow(filt_1, [])
title('corr, symmetric, full')

subplot(3,2,3)
imshow(filt_2, [])
title('conv, symmetric, full')

subplot(3,2,4)
imshow(filt_3, [])
title('corr, symmetric, same')

subplot(3,2,5)
imshow(filt_4, [])
title('conv, symmetric, same')


            %symmetric
  %Problem pehle samjho (Boundary Issue)

%Jab filter image ke edges (border) par jata hai:

%Kernel ka kuch hissa image ke bahar chala jata hai

%Wahan pixel values exist nahi karti

%Is problem ko boundary handling kehte hain

%symmetric image ke borders ko mirror (sheesha) ki tarah reflect karta hai.