import SimpleITK as sitk
import numpy as np

def dilation(struct_element):
    
    dilation_in_mm=struct_element
    
    image=sitk.Cast(sitk.ReadImage('whole_binary_mask.nii.gz'),sitk.sitkUInt8)
    
    original_mask_array=sitk.GetArrayFromImage(image)

    if not np.all(np.isin(np.unique(original_mask_array),[0,1])):
        raise ValueError(f'The backgrond and foreground labels should be 0 and 1')

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

    sitk.WriteImage(filled_mask,f'dilated_binary_{struct_element}mm.nii.gz')


dilation(2)