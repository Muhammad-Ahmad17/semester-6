%Fundamentals of image processing 
%Write a MATLAB code that perform the following operations. 
%1. Ask the user to enter the name of the image file. 
%2. Read the image file. 
%3. Store the file with a different format and name, the name and format should also be 
%chosen by the user.
name=input('enter the input image file name with extension : ')
new=input('enter the output image file name with extension : ')
A=imread(name)
imwrite(A,new)