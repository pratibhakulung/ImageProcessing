import SimpleITK as sitk
import numpy as np

def dilation(max,random_number):

    """
    max: maximux size the mask can dilate
    random_number: randomized value used for 
    
    All units are in mm
    """
    
    dilation_in_mm=0
    
    image=sitk.Cast(sitk.ReadImage('whole_binary_mask.nii.gz'),sitk.sitkUInt8)
    
    if random_number<0:
        print(f'Possible of shrinking the contour less than original segmentation.\n SETTING struct element to 0')
        dilation_in_mm=0
    
    elif random_number>max:
        print(f'Exceed the contour greater than 2. \n SETTING struct elemnt to 2')
        dilation_in_mm=max
    else:
        dilation_in_mm=random_number

    signed_distance_map = sitk.SignedMaurerDistanceMap(image, squaredDistance=False, useImageSpacing=True)
    dilated_binary_image = (signed_distance_map<dilation_in_mm)
    filled_mask = sitk.VotingBinaryHoleFilling(
        dilated_binary_image,
        radius=[2]*3,
        majorityThreshold=3,
        foregroundValue=1,
        backgroundValue=0
)
    filled_mask=sitk.SmoothingRecursiveGaussian(filled_mask,sigma=[1]*3)

    sitk.WriteImage(filled_mask,f'dilated_binary_{random_number}mm.nii.gz')


dilation(2,1.2)