# Pattern-Based-Fingerprint-Recognition
System Overview

This system is designed for fingerprint enhancement and comparison. It processes two fingerprint images to improve their quality and then evaluates their similarity. The system uses advanced image processing techniques to enhance the fingerprints and provides detailed comparison results.

Process Overview

Upload Fingerprint Images: Begin by uploading two grayscale fingerprint images that you want to analyze.

Enhancement: The system applies Gabor filters to both images. This enhancement step improves the details and clarity of the fingerprints, making key features more distinct.

Comparison: After enhancement, the system compares the two fingerprints using various histogram-based methods. This analysis measures the similarity between the images based on their pixel intensity distributions.

View Results: The results include side-by-side visualizations of the enhanced fingerprints and a set of similarity scores. These scores indicate how closely the fingerprints match. All results, including enhanced images and comparison scores, are saved in a specified output directory for easy access and review.
