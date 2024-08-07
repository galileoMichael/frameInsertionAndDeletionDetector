import numpy as np

def assign_macroblock_identifiers(centroids):
    """
    Assign identifiers to grouped macroblocks based on their centroid changes and color similarity.

    Args:
        centroids (dict): Dictionary where keys are frame numbers and values are lists of centroid coordinates and RGB channel sums.
        centroid_changes (dict): Dictionary where keys are frame pairs and values are lists of centroid changes.

    Returns:
        identifiers (dict): Dictionary where keys are object IDs and values are lists of dictionaries containing frame numbers and centroids.
    """
    identifiers = {}
    objects = []  

    color_threshold = 5 #35
    distance_threshold = 16 * 65  # 16 * 40

    for frame, frame_centroids in centroids.items():
        for centroid in frame_centroids:
            distances = []
            r_total = []
            g_total = []
            b_total = []
            matching_object = None
            for obj in objects:
                color_diff_r = abs(centroid[2] - obj['centroid'][2])
                # r_total.append(color_diff_r)
                # r_threshold = np.mean(r_total) + np.std(r_total)
                color_diff_g = abs(centroid[3] - obj['centroid'][3])
                # g_total.append(color_diff_g)
                # g_threshold = np.mean(g_total) + np.std(g_total)
                color_diff_b = abs(centroid[4] - obj['centroid'][4])
                # b_total.append(color_diff_b)
                # b_threshold = np.mean(b_total) + np.std(b_total)
                prev_frame, prev_centroid = obj['prev_centroid']
                distance = np.sqrt((centroid[0] - prev_centroid[0]) ** 2 + (centroid[1] - prev_centroid[1]) ** 2)
                distances.append(distance)
                # distance_threshold = np.mean(distances) + np.std(distances)
                # print(color_diff_r, " ", color_diff_g, " ", color_diff_b, " ", distance, " ", distance_threshold, " ", color_threshold)
            #     if color_diff_r <= color_threshold or color_diff_g <= color_threshold or color_diff_b <= color_threshold and distance <= distance_threshold:
            for i, obj in enumerate(objects):
                if (color_diff_r <= color_threshold and color_diff_g <= color_threshold and color_diff_b <= color_threshold and distances[i] == min(distances)):
                    matching_object = obj
                    break                
                # if color_diff_r <= color_threshold or color_diff_g <= color_threshold or color_diff_b <= color_threshold and distance <= distance_threshold:
                #     matching_object = obj
                #     break

            if matching_object:
                matching_object['centroids'].append({'frame': frame, 'centroid': centroid})
                matching_object['centroid'] = centroid
                matching_object['prev_centroid'] = (frame, centroid)
            else:
                new_object = {
                    'id': len(objects),
                    'centroid': centroid,
                    'centroids': [{'frame': frame, 'centroid': centroid}],
                    'prev_centroid': (frame, centroid)
                }
                objects.append(new_object)

    for obj in objects:
        if len(obj['centroids']) > 1:
            identifiers[obj['id']] = obj['centroids']

    return identifiers

# import math
# import numpy as np

# def assign_macroblock_identifiers(centroids):
#     """
#     Assign identifiers to grouped macroblocks based on their centroid changes and color similarity.

#     Args:
#         centroids (dict): Dictionary where keys are frame numbers and values are lists of centroid coordinates and RGB channel sums.

#     Returns:
#         identifiers (dict): Dictionary where keys are object IDs and values are lists of dictionaries containing frame numbers and centroids.
#     """
#     identifiers = {}
#     objects = []  

#     for frame, frame_centroids in centroids.items():
#         for centroid in frame_centroids:
#             distances = []
#             color_diffs_r = []
#             color_diffs_g = []
#             color_diffs_b = []
#             matching_object = None

#             for obj in objects:
#                 color_diff_r = abs(centroid[2] - obj['centroid'][2])
#                 color_diffs_r.append(color_diff_r)
#                 color_diff_g = abs(centroid[3] - obj['centroid'][3])
#                 color_diffs_g.append(color_diff_g)
#                 color_diff_b = abs(centroid[4] - obj['centroid'][4])
#                 color_diffs_b.append(color_diff_b)
                
#                 prev_frame, prev_centroid = obj['prev_centroid']
#                 distance = math.sqrt((centroid[0] - prev_centroid[0]) ** 2 + (centroid[1] - prev_centroid[1]) ** 2)
#                 distances.append(distance)
            
#             if distances:
#                 distance_threshold = np.mean(distances) + np.std(distances)
#                 r_threshold = np.mean(color_diffs_r) + np.std(color_diffs_r)
#                 g_threshold = np.mean(color_diffs_g) + np.std(color_diffs_g)
#                 b_threshold = np.mean(color_diffs_b) + np.std(color_diffs_b)
            
#                 for i, obj in enumerate(objects):
#                     if (distances[i] == min(distances)):
#                         matching_object = obj
#                         break

#             if matching_object:
#                 matching_object['centroids'].append({'frame': frame, 'centroid': centroid})
#                 matching_object['centroid'] = centroid
#                 matching_object['prev_centroid'] = (frame, centroid)
#             else:
#                 new_object = {
#                     'id': len(objects),
#                     'centroid': centroid,
#                     'centroids': [{'frame': frame, 'centroid': centroid}],
#                     'prev_centroid': (frame, centroid)
#                 }
#                 objects.append(new_object)

#     for obj in objects:
#         if len(obj['centroids']) > 1:
#             identifiers[obj['id']] = obj['centroids']

#     print(identifiers)

#     return identifiers
