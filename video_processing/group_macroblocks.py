import numpy as np

def group_macroblocks(macroblocks_data_list, max_distance, total_frames):
    """
    Group macroblocks based on their coordinates and count the sum of macroblocks for each group.
    Eliminate groups that appear in less than a specified percentage of total frames.

    Args:
        macroblocks_data_list (list): List of dictionaries containing macroblock data.
        max_distance (int): Maximum distance to consider macroblocks as part of the same group.
        video_path (str): Path to the video file.
        threshold (float): Minimum percentage of frames a group must appear in to be included.

    Returns:
        grouped_macroblocks (dict): Dictionary where keys are frame numbers and values are lists of grouped macroblocks with sum of macroblocks.
    """
    grouped_macroblocks = {}

    appearance_threshold = len(macroblocks_data_list) * 0.0025

    for data in macroblocks_data_list:
        frame = data['Frame']
        macroblock = data['Macroblock']
        x = data['X']
        y = data['Y']
        mse = data['MSE']
        total_mse = 0
        grouped = False

        if frame not in grouped_macroblocks:
            grouped_macroblocks[frame] = []

        for group in grouped_macroblocks[frame]:
            for mb_data in group:
                dist_x = x - mb_data['X']
                dist_y = y - mb_data['Y']
                if all(dist <= max_distance for dist in (dist_x, dist_y)):
                    group.append(data)
                    grouped = True
                    break
            if grouped:
                break

        if not grouped:
            grouped_macroblocks[frame].append([data])

    for frame, groups in grouped_macroblocks.items():
        for group in groups:
            total_mse = sum(mb_data['MSE'] for mb_data in group)
            for mb_data in group:
                mb_data['MSE'] = total_mse

    if total_frames > 0:
        filtered_groups = {}
        for frame, groups in grouped_macroblocks.items():
            filtered_groups[frame] = [group for group in groups if len(group) >= appearance_threshold]
        grouped_macroblocks = filtered_groups

    return grouped_macroblocks

# def write_grouped_macroblocks_to_csv(grouped_macroblocks, output_csv):
#     """
#     Write grouped macroblocks data to a CSV file.
    
#     Args:
#         grouped_macroblocks (dict): Dictionary where keys are frame numbers and values are lists of grouped macroblocks.
#         output_csv (str): Path to the output CSV file.
#     """
#     with open(output_csv, 'w', newline='') as csvfile:
#         csv_writer = csv.writer(csvfile)
#         csv_writer.writerow(['Frame', 'Group', 'Macroblock', 'MSE', 'X', 'Y', 'R', 'G', 'B'])

#         for frame, groups in grouped_macroblocks.items():
#             for group_idx, group in enumerate(groups):
#                 for mb_data in group:
#                     macroblock = mb_data['Macroblock']
#                     x = mb_data['X']
#                     y = mb_data['Y']
#                     r = mb_data['Red']
#                     g = mb_data['Green']
#                     b = mb_data['Blue']
#                     csv_writer.writerow([frame, group_idx, macroblock, x, y, r, g, b])