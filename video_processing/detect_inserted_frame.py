# # def detect_inserted_frame(identifiers):
# #     """
# #     Detects potential insertions of objects based on their appearance and disappearance patterns.

# #     Args:
# #     identifiers (dict): Dictionary containing object IDs as keys and a list of dictionaries with frame and centroid data as values.

# #     Returns:
# #     dict: Dictionary containing object IDs as keys and a list of tuples where each tuple contains the start and end frame of a potential insertion.
# #     """

# #     insertions = {}

# #     object_presence = {}
# #     for object_id, data in identifiers.items():
# #         for frame_data in data:
# #             frame = frame_data['frame']
# #             if frame not in object_presence:
# #                 object_presence[frame] = set()
# #             object_presence[frame].add(object_id)

# #     for frame, objects_in_frame in object_presence.items():
# #         next_frame = frame + 1
# #         if next_frame in object_presence:
# #             objects_in_next_frame = object_presence[next_frame]
# #             disappeared_objects = objects_in_frame - objects_in_next_frame
# #             reappeared_objects = objects_in_next_frame - objects_in_frame
# #             for reappeared_object in reappeared_objects:
# #                 start_frame = None
# #                 for prev_frame in range(frame - 1, 0, -1):
# #                     if prev_frame in object_presence:
# #                         if reappeared_object in object_presence[prev_frame]:
# #                             start_frame = prev_frame
# #                             break
# #                 if start_frame is not None:
# #                     end_frame = frame
# #                     insertions.setdefault(reappeared_object, []).append((start_frame, end_frame))

# #     for object_id in identifiers.keys():
# #         if object_id not in insertions:
# #             insertions[object_id] = ["No insertions detected"]
                    

# #     return insertions

# def detect_inserted_frame(identifiers):
#     """
#     Detects potential insertions of objects based on their appearance and disappearance patterns.

#     Args:
#     identifiers (dict): Dictionary containing object IDs as keys and a list of dictionaries with frame and centroid data as values.

#     Returns:
#     list: List of tuples where each tuple contains the start and end frame of a potential insertion.
#     """
    
#     insertions = []

#     object_presence = {}
#     for object_id, data in identifiers.items():
#         for frame_data in data:
#             frame = frame_data['frame']
#             if frame not in object_presence:
#                 object_presence[frame] = set()
#             object_presence[frame].add(object_id)

#     for frame, objects_in_frame in object_presence.items():
#         next_frame = frame + 1
#         if next_frame in object_presence:
#             objects_in_next_frame = object_presence[next_frame]
#             reappeared_objects = objects_in_next_frame - objects_in_frame
#             for reappeared_object in reappeared_objects:
#                 start_frame = None
#                 for prev_frame in range(frame - 1, 0, -1):
#                     if prev_frame in object_presence:
#                         if reappeared_object in object_presence[prev_frame]:
#                             start_frame = prev_frame
#                             break
#                 if start_frame is not None:
#                     end_frame = frame
#                     insertions.append((start_frame, end_frame))

#     if not insertions:
#         insertions.append("No insertions detected")
    
#     return insertions

def detect_inserted_frame(identifiers):
    """
    Detects potential insertions of objects based on their appearance and disappearance patterns.

    Args:
    identifiers (dict): Dictionary containing object IDs as keys and a list of dictionaries with frame and centroid data as values.

    Returns:
    list: List of tuples where each tuple contains the start and end frame of a potential insertion.
    """
    
    insertions = set()  # Use a set to store unique insertions

    object_presence = {}
    for object_id, data in identifiers.items():
        for frame_data in data:
            frame = frame_data['frame']
            if frame not in object_presence:
                object_presence[frame] = set()
            object_presence[frame].add(object_id)

    for frame, objects_in_frame in object_presence.items():
        next_frame = frame + 1
        if next_frame in object_presence:
            objects_in_next_frame = object_presence[next_frame]
            reappeared_objects = objects_in_next_frame - objects_in_frame
            for reappeared_object in reappeared_objects:
                start_frame = None
                for prev_frame in range(frame - 1, 0, -1):
                    if prev_frame in object_presence:
                        if reappeared_object in object_presence[prev_frame]:
                            start_frame = prev_frame
                            break
                if start_frame is not None:
                    end_frame = frame
                    insertions.add((start_frame+1, end_frame+1))  # Add the tuple to the set

    if not insertions:
        return ["No insertions detected"]
    
    return list(insertions)  # Convert the set back to a list before returning
