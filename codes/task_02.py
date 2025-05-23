import SimpleITK as sitk
import numpy as np

def dilation(struct_element):

    """
    input: the structure element size in mm
    
    """
    
    dilation_in_mm=struct_element
    
    image=sitk.Cast(sitk.ReadImage('whole_binary_mask.nii.gz'),sitk.sitkUInt8)

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