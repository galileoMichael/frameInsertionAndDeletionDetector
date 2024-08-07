# import numpy as np

# def detect_deleted_frame(identifiers):
#     """
#     Detects whether a video frame has a deleted frame based on the change in centroids of objects over frames.

#     Args:
#     identifiers (dict): Dictionary containing object IDs as keys and a list of dictionaries with frame and centroid data as values.

#     Returns:
#     dict: Dictionary containing object IDs as keys and a list of frame numbers where a deletion location is detected.
#     """

#     deletion_locations = {} 
#     centroid_changes = []

#     for object_id, data in identifiers.items():
#         threshold = 0  
#         counter = 0
#         deletion_frames = [] 
#         insertion_frames = [] 
#         color_threshold = 5000

#         for i in range(1, len(data)):
#             counter =+ 1
#             change_x = abs(data[i]['centroid'][0] - data[i-1]['centroid'][0])
#             change_y = abs(data[i]['centroid'][1] - data[i-1]['centroid'][1])
#             centroid_change = (change_x ** 2 + change_y ** 2) ** 0.5
#             centroid_changes.append(centroid_change)
#             print(object_id, data[i]['frame'], "ch: ", centroid_change)
#             avg_centroid_change = np.mean(centroid_changes)
#             std_centroid_change = np.std(centroid_changes)
#             threshold = avg_centroid_change + std_centroid_change + 160 
#             print(object_id, data[i]['frame'], "th: ", threshold)            
#             if centroid_change > threshold:
#                 counter = 0
#                 deletion_frames.append(data[i]['frame'])

#         deletion_locations[object_id] = deletion_frames

#     return deletion_locations

import numpy as np

def detect_deleted_frame(identifiers):
    """
    Detects whether a video frame has a deleted frame based on the change in centroids of objects over frames.

    Args:
    identifiers (dict): Dictionary containing object IDs as keys and a list of dictionaries with frame and centroid data as values.

    Returns:
    list: List of frame numbers where a deletion location is detected.
    """

    deletion_frames = set()  
    frame_deleted = []

    for object_id, data in identifiers.items():
        centroid_changes = []

        for i in range(1, len(data)):
            expected_frame_deleted = 0
            change_x = abs(data[i]['centroid'][0] - data[i-1]['centroid'][0])
            change_y = abs(data[i]['centroid'][1] - data[i-1]['centroid'][1])
            centroid_change = np.sqrt(change_x ** 2 + change_y ** 2)
            centroid_changes.append(centroid_change)
        
            if len(centroid_changes) > 1:
                avg_centroid_change = np.mean(centroid_changes)
                std_centroid_change = np.std(centroid_changes)
                threshold = avg_centroid_change + std_centroid_change + 160 # + (avg_centroid_change + std_centroid_change ) * 1.5 + 100
                print(object_id, " ", centroid_change, " ", threshold)
                if centroid_change > threshold:
                    expected_frame_deleted = int(centroid_change / avg_centroid_change)
                    frame_deleted.append(expected_frame_deleted)
                    deletion_frames.add(data[i+1]['frame'])

    if not deletion_frames:
        deletion_frames.add("No deletions detected")
    deletion_locations = deletion_frames                    

    return sorted(deletion_frames), list(frame_deleted)