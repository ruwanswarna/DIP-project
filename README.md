% Read the input image
image = imread('leaves1.png');

% Convert the image to LAB color space
lab_image = rgb2lab(image);

% Extract the 'a' and 'b' channels
a_channel = lab_image(:,:,2);
b_channel = lab_image(:,:,3);

% Thresholding to identify green regions (leaves)
green_threshold = a_channel < 0 & b_channel > 0;
green_leaves_mask = imfill(green_threshold, 'holes');

% Create a mask for the background
background_mask = ~green_leaves_mask;

% Change the background color to black
black_background = image;
black_background(repmat(background_mask,[1 1 3])) = 0;

% Display the result
subplot(1,2,1), imshow(image), title('Original Image');
subplot(1,2,2), imshow(black_background), title('Black Background with Green Leaves');
