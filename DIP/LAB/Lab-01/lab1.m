clc
clear
close all

% a row matrix
vector_1 = [1 2 3 4 5]

% taking transpose
vector_1_transporse = vector_1'

% a square matrix
matrix = [1 2 3 ;
          4 5 6 ;
          7 8 9
          ]

m = 100
n = 1000

img_zeros = zeros(m,n)
subplot(131)
imshow(img_zeros)

img_ones = ones(m,n)
subplot(132)
imshow(img_ones)

string_pattern = [img_zeros;img_ones;img_zeros;img_ones;img_zeros;img_ones;]
subplot(133)
imshow(string_pattern)

grid_pattern = [img_zeros img_ones img_zeros img_ones img_zeros img_ones;
                ]

