import cv2
import numpy as np
import os

def gabor_filter(img, ksize, sigma, theta, lambd, gamma, psi):
    gabor = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
    filtered_img = cv2.filter2D(img, cv2.CV_8UC3, gabor)
    return filtered_img

def enhance_fingerprint(img):
    thetas = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    enhanced_imgs = []
    for theta in thetas:
        filtered_img = gabor_filter(img, ksize=31, sigma=4.0, theta=theta, lambd=10.0, gamma=0.5, psi=0)
        enhanced_imgs.append(filtered_img)
    enhanced_img = np.mean(enhanced_imgs, axis=0).astype(np.uint8)
    return enhanced_img

def compare_histograms(img1, img2, method):
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    hist1 = cv2.normalize(hist1, hist1).flatten()
    hist2 = cv2.normalize(hist2, hist2).flatten()
    similarity = cv2.compareHist(hist1, hist2, method)
    return similarity

# Load the fingerprint images
fingerprint1_filename = 'image1.jpg'
fingerprint2_filename = 'image2.jpg'
fingerprint1 = cv2.imread(fingerprint1_filename, 0)
fingerprint2 = cv2.imread(fingerprint2_filename, 0)

# Check if images are loaded correctly
if fingerprint1 is None or fingerprint2 is None:
    print("Error: One or both images not found.")
else:
    print("Images loaded successfully.")

# Enhance fingerprints using Gabor filters
enhanced_fingerprint1 = enhance_fingerprint(fingerprint1)
enhanced_fingerprint2 = enhance_fingerprint(fingerprint2)

# Visualize enhanced images for debugging
cv2.imshow('Enhanced Fingerprint 1', enhanced_fingerprint1)
cv2.imshow('Enhanced Fingerprint 2', enhanced_fingerprint2)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Create output directory based on image names
output_dir = 'pattern_based_matching'
output_subdir = os.path.join(output_dir, os.path.splitext(os.path.basename(fingerprint1_filename))[0] + '_' + os.path.splitext(os.path.basename(fingerprint2_filename))[0])
if not os.path.exists(output_subdir):
    os.makedirs(output_subdir)

# Save intermediate Gabor filtered images for debugging
for i, theta in enumerate([0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]):
    filtered_img1 = gabor_filter(fingerprint1, ksize=31, sigma=4.0, theta=theta, lambd=10.0, gamma=0.5, psi=0)
    filtered_img2 = gabor_filter(fingerprint2, ksize=31, sigma=4.0, theta=theta, lambd=10.0, gamma=0.5, psi=0)
    cv2.imwrite(os.path.join(output_subdir, f'filtered1_theta{i}.jpg'), filtered_img1)
    cv2.imwrite(os.path.join(output_subdir, f'filtered2_theta{i}.jpg'), filtered_img2)

# Compare enhanced fingerprints using different methods
match_score_bhattacharyya = compare_histograms(enhanced_fingerprint1, enhanced_fingerprint2, method=cv2.HISTCMP_BHATTACHARYYA)

# Convert Bhattacharyya distance to similarity score (1 - distance)
final_match_score = 1 - match_score_bhattacharyya

print(f'Match score (Bhattacharyya): {match_score_bhattacharyya}')
print(f'Final Match Score: {final_match_score}')

# Save the enhanced images
enhanced_fingerprint1_filename = os.path.join(output_subdir, 'enhanced_fingerprint1.jpg')
enhanced_fingerprint2_filename = os.path.join(output_subdir, 'enhanced_fingerprint2.jpg')
cv2.imwrite(enhanced_fingerprint1_filename, enhanced_fingerprint1)
cv2.imwrite(enhanced_fingerprint2_filename, enhanced_fingerprint2)

# Save match scores
with open(os.path.join(output_subdir, 'match_scores.txt'), 'w') as f:
        f.write(f'Match score (Bhattacharyya): {match_score_bhattacharyya}\n')
    f.write(f'Final Match Score: {final_match_score}\n')

# Combine images side by side for visualization
combined_image = np.hstack((enhanced_fingerprint1, enhanced_fingerprint2))
combined_filename = os.path.join(output_subdir, 'enhanced_comparison.jpg')
cv2.imwrite(combined_filename, combined_image)

# Optional: Display the combined image
cv2.imshow('Enhanced Fingerprints', combined_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
