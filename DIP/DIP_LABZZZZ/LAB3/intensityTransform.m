function outImg = intensityTransform(img, type, varargin)
% INTENSITYTRANSFORM Apply different intensity transformations
% img  : input grayscale image (uint8)
% type : 'contrast', 'log', 'power'
% varargin : extra parameters depending on type
%
% Usage:
% outImg = intensityTransform(img,'contrast',[r1 s1 r2 s2])
% outImg = intensityTransform(img,'log',c)
% outImg = intensityTransform(img,'power',gamma,c)

img = double(img); % convert to double for calculations

switch lower(type)
    
    case 'contrast'
        % Contrast stretching
        % varargin = [r1 s1 r2 s2]
        r1 = varargin{1}(1);
        s1 = varargin{1}(2);
        r2 = varargin{1}(3);
        s2 = varargin{1}(4);
        
        outImg = zeros(size(img));
        % piecewise linear mapping
        idx1 = img <= r1;
        idx2 = img > r1 & img <= r2;
        idx3 = img > r2;
        
        outImg(idx1) = (s1/r1) * img(idx1);
        outImg(idx2) = ((s2-s1)/(r2-r1))*(img(idx2)-r1) + s1;
        outImg(idx3) = ((255-s2)/(255-r2))*(img(idx3)-r2) + s2;
        
    case 'log'
        % Log Transformation
        % varargin = c
        c = varargin{1};
        outImg = c * log(1 + img);
        outImg = uint8(255 * mat2gray(outImg)); % normalize 0-255
        
    case 'power'
        % Power-law (gamma) Transformation
        % varargin = [gamma c]
        gamma = varargin{1}(1);
        c     = varargin{1}(2);
        outImg = c * (img.^gamma);
        outImg = uint8(255 * mat2gray(outImg)); % normalize 0-255
        
    otherwise
        error('Unknown transformation type');
end

outImg = uint8(outImg);

end