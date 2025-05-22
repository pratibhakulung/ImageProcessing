import  SimpleITK as sitk
import numpy as np
import os

def segmentation():

    #loading image and thresholding

    image=sitk.ReadImage("C:/Users/User/Desktop/Task/3702_left_knee.nii.gz")

    image_array=sitk.GetArrayFromImage(image)

    body_mask = sitk.BinaryThreshold(image, lowerThreshold=-150, upperThreshold=1500, insideValue=1, outsideValue=0)
    cc = sitk.ConnectedComponent(body_mask)
    stats = sitk.LabelShapeStatisticsImageFilter()
    stats.Execute(cc)

    largest_label = max(stats.GetLabels(), key=lambda l: stats.GetPhysicalSize(l))
    largest_component_mask = sitk.BinaryThreshold(cc, lowerThreshold=largest_label, upperThreshold=largest_label, insideValue=1, outsideValue=0)
    large=sitk.BinaryClosingByReconstruction(largest_component_mask,[5,5,5],sitk.sitkBall)


    body=sitk.GetArrayFromImage(large)
    
    #masking to remove bedrest

    cleaned_image=image_array*body
    clean=sitk.GetImageFromArray(cleaned_image)
    clean.SetOrigin(image.GetOrigin())
    clean.SetSpacing(image.GetSpacing())
    
    
    gradient = sitk.GradientMagnitude(clean)

    tibia=sitk.ReadImage('tibiaMask.nii.gz')
    femur=sitk.ReadImage('femurMarkers.nii.gz')
    
    #getting tibia and femur segmentation separately to get mask using markers by manual selection from ITK SNAP
    tibia_mask=sitk.MorphologicalWatershedFromMarkers(gradient,markerImage=tibia)
    femur_mask=sitk.MorphologicalWatershedFromMarkers(gradient,markerImage=femur)

    tibia_array=sitk.GetArrayFromImage(tibia_mask)
    femur_array=sitk.GetArrayFromImage(femur_mask)
    
    #combining mask

    whole_mask=tibia_array + femur_array

    whole_mask[whole_mask==3]=0
    
    #consistent labelling of foreground

    binary_mask=np.where(whole_mask>0,1,0)
    np.unique(binary_mask)


    whole_binary=sitk.GetImageFromArray(binary_mask)

    whole_binary.SetOrigin(clean.GetOrigin())
    whole_binary.SetSpacing(clean.GetSpacing())

    whole_binary=sitk.SmoothingRecursiveGaussian(whole_binary,sigma=[1]*3)
    sitk.WriteImage(whole_binary,'whole_binary_mask.nii.gz')


segmentation()