<li> The location of the images are hardcoded so to run the scripts please run them in the given directory. </li>
<li>  The codes are placed inside code directory and the result images in output directory </li>


Explanation for used methods:

#### For Task 1:
<li> First of all the bed rest was removed by thresholding and connected component analysis </li>
<li> The markers were taken manually in single slice for both tibia and femur separately using ITK-SNAP.</li>
<li> Using these markers, individual masks were obtained using watershed segmentation on gradient watershed image for better generation of mask.</li>
<li> The final masks were obtained by combining the individual mask.</li>
<li> Post preprocessing as filling holes and smoothing were done, to get clean binary mask</li>

#### For Task 2:
<li> For task 2, the output from task 1 is needed so the path of that .nii file is already defined.</li>
<li> For dilation in mm, the structing elements which is in pixels should be converted in mm.</li>
<li> We can get the measurement for corresponding pixels to mm using the values from Spacing in .nii file.</li>
<li> Most libraries(as SimpleITK I used) doesn't take decimal value for structure element.</li>
<li> For this reason, I have used SignedMaurerDistanceMap for getting pixels at n distance, also allows to use mm unit.</li>
<li> Postpreprocessing such as filling holes inside boundary and smoothing are done to get final clean mask.</li>

#### For Task 3: 
<li>The process is similar except, the distance  conditions are applied to get mask that doesn't exceed 2mm and doesn't shrink. </li>

#### For Task 4:
This task hasn't been completed. I plan to apply the following process to get the points mentioned in tibia. 
<li> Getting connected components that belong to tibia(which may be either largest or second largest based on mask obtained from task 1 visualization) </li>
<li> Drawing at the midslice(2D image)</li>
<li> For middle point would be the centroid of the image.</li>
<li> For lateral end point, the end of the major axis would be the point. </li>
