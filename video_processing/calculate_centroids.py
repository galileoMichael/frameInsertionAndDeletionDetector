def calculate_centroids(grouped_macroblocks):
    """
    Calculate centroids of grouped macroblocks in each frame and return their coordinates and RGB channel sums.

    Args:
        grouped_macroblocks (dict): Dictionary where keys are frame numbers and values are lists of grouped macroblocks.

    Returns:
        centroids (dict): Dictionary where keys are frame numbers and values are lists of centroids' coordinates and RGB channel sums.
    """

    centroids = {}

    for frame, groups in grouped_macroblocks.items():
        centroids[frame] = []
        for group in groups:
            if len(group) == 0:
                continue

            x_sum = sum([mb['X'] for mb in group]) 
            y_sum = sum([mb['Y'] for mb in group])
            red_sum = sum([mb['Red'] for mb in group]) / len(group)
            green_sum = sum([mb['Green'] for mb in group]) / len(group)
            blue_sum = sum([mb['Blue'] for mb in group]) / len(group)

            centroid_x = x_sum / len(group)
            centroid_y = y_sum / len(group)

            mean_r = red_sum / len(group)
            mean_g = green_sum / len(group)
            mean_b = blue_sum / len(group)

            centroids[frame].append((centroid_x, centroid_y, mean_r, mean_g, mean_b))

    return centroids