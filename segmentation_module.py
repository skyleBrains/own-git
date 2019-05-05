import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from scipy.ndimage.filters import gaussian_filter

def make_subtracted_mean(image_path, image_list):
    subtracted_means = []
    saved_depth_info = []
    segment_info = []
    first_frame = cv2.imread(os.path.join(image_path, image_list[0]))
    for i in range(1, len(image_list)):
        next_frame = cv2.imread(os.path.join(image_path, image_list[i]))
        subtracted_means.append(np.mean(next_frame - first_frame))
        saved_depth_info.append(next_frame)
    # print(len(subtracted_means))
    saved_depth_info = np.asarray(saved_depth_info)
    subtracted_means = np.asarray(subtracted_means)
    filtered_mean = gaussian_filter(subtracted_means, sigma=5)
    i = 150
    while(i + 100 < 2260):
	segment_info.append(np.min(subtracted_means[i:i+100]))
	i += 250
    segment_info = np.asrray(segment_info)
    np.save('segment_info.npy', segment_info)
    np.save('filtered_mean.npy', filtered_mean)
    np.save('saved_depth_info.npy', saved_depth_info)
    plt.figure(figsize=(16,10))
    plt.plot(filtered_mean)
    plt.axhline(y=42.5, color='red', linestyle='-')
    plt.axvline(x=30, color='red', linestyle='-')
    plt.axvline(x=2220, color='red', linestyle='-')
    plt.axvline(x=segment_info, color='red', linestyle='-')
    plt.savefig('filtered_mean_set_6_with_another_sigma.png', format='png')


if __name__=="__main__":
    image_path = '../frame_set_6/'
    image_list = os.listdir(image_path)
    image_list = sorted(image_list)
    make_subtracted_mean(image_path, image_list)
