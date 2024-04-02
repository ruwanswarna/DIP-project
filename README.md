# DIP-Project-Identify-Whiteflies-on-Crop-Leaves

In this project we have followed the digital image processing methods outlined in the research paper called "Using digital image processing for counting whiteflies on soybean leaves " to identify and count different stages of white flies on crop leaves.

The Whitefly is a type of airborne insect that harm various types of crops like soybean, bean, cassava by feeding on plant sap which causes them to fall off. The following image shows the lifecycle of the whitefly.

![whitefly_stages](whitefly_stages.jpg)  

Since whiteflies have different characteristics in different stages of their lifecycle. We can use digital image processing methods to idenfity and count whiteflies at various stages.

## The methods outlined in the research paper
There are two methods outlined.
1. Simple Color Transformation  
2. Chaining Color Transformations

### 1. Simple Color Transformation
In this method the RGB image is converted to another color format and from that a single channel or a operation on channels is extracted for further inspection. The following list shows color transformations used to highlight different lifecycle stags.

- from RGB subtract blue channel from green channel ---------> discriminate nymphs and exo skeletons
- convert RGB to CMYK and extract k channel -----------------> both adult whiteflies and nymphs
- convert RGB to CIELAB and extract b channel ---------------> empty exo skeletons and wings appear dark
- convert RGB to HSV and extract H channel ------------------> nymphs and abdomens of adults appear dark

### 2. Chaining Color Transformations
In this method multiple color transformations applied one after another, to reveal new information not visible in original images.
But this cannot be done simply tansforming one after another because resulting image will be equal to a direct transformation from original image to the last transformation.
Therfore it has to be done in the following way.
this is the youtube link  https://youtu.be/oMZeE4iG0ek
 
