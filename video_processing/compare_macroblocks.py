import cv2
import os
import csv
import numpy as np
from scipy.spatial import distance
from video_processing.extract_macroblocks import extract_macroblocks

def compare_macroblocks(video_path, frame_directory, mb_directory):
    """
    Compare macroblocks between frames and extract based on MSE threshold.
    
    Args:
        video_path (str): Path to the video file.
        frame_directory (str): Directory containing frame images.
        output_csv (str): Output CSV file path.
        mb_directory (str): Directory to save extracted macroblocks.
    
    Returns:
        List of dictionaries containing macroblock data.
    """
    vidObj = cv2.VideoCapture(video_path)
    total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
    multiplier = 2.5 # 1.5
    block_size = 16
    frame_nth = 0
    success = 1

    macroblocks_data_list = []
    mse_values = []
    for frame_nth in range(total_frames - 1):
        frame1_path = os.path.join(frame_directory, f"frame{frame_nth}.jpg")
        frame2_path = os.path.join(frame_directory, f"frame{frame_nth + 1}.jpg")

        if os.path.exists(frame1_path) and os.path.exists(frame2_path):
            frame1 = cv2.imread(frame1_path)
            frame2 = cv2.imread(frame2_path)

            if frame1 is not None and frame2 is not None:
                macroblocks1 = extract_macroblocks(frame1)
                macroblocks2 = extract_macroblocks(frame2)

                for i, (mb1, mb2) in enumerate(zip(macroblocks1, macroblocks2)):
                    mb1_gray = cv2.cvtColor(mb1, cv2.COLOR_BGR2GRAY)
                    mb2_gray = cv2.cvtColor(mb2, cv2.COLOR_BGR2GRAY)
                    mse = ((mb1_gray - mb2_gray) ** 2).mean()
                    mse_values.append(mse)  

                mse_threshold = np.mean(mse_values) + multiplier * np.std(mse_values)

                for i, (mb1, mb2) in enumerate(zip(macroblocks1, macroblocks2)):
                    mb1_gray = cv2.cvtColor(mb1, cv2.COLOR_BGR2GRAY)
                    mb2_gray = cv2.cvtColor(mb2, cv2.COLOR_BGR2GRAY)
                    mse = ((mb1_gray - mb2_gray) ** 2).mean()

                    if mse > mse_threshold:  
                        mb_path = os.path.join(mb_directory, f"macroblock_{frame_nth}_{i}.jpg")  
                        cv2.imwrite(mb_path, mb1)
                            
                        current_x = (i % (frame1.shape[1] // block_size)) * block_size
                        current_y = (i // (frame1.shape[1] // block_size)) * block_size
                            
                        red = np.sum(mb1[:, :, 2])  / 16 
                        green = np.sum(mb1[:, :, 1])  / 16 
                        blue = np.sum(mb1[:, :, 0])  /16                         
                            
                        macroblocks_data_list.append({'Frame': frame_nth, 'Macroblock': i, 'MSE': mse, 'X': current_x, 'Y': current_y, 'Red': red, 'Green': green, 'Blue': blue})
                    
            else:
                print(f"Error: Unable to open frame images {frame1_path} or {frame2_path}")
        else:
            print(f"Error: Frame images {frame1_path} or {frame2_path} not found.")

    return macroblocks_data_list    

# import cv2
# import os
# import numpy as np
# from video_processing.extract_macroblocks import extract_macroblocks

# def compare_macroblocks(video_path, frame_directory, mb_directory):
#     """
#     Compare macroblocks between frames and extract based on absolute difference threshold.
    
#     Args:
#         video_path (str): Path to the video file.
#         frame_directory (str): Directory containing frame images.
#         output_csv (str): Output CSV file path.
#         mb_directory (str): Directory to save extracted macroblocks.
    
#     Returns:
#         List of dictionaries containing macroblock data.
#     """
#     vidObj = cv2.VideoCapture(video_path)
#     total_frames = int(vidObj.get(cv2.CAP_PROP_FRAME_COUNT))
#     multiplier = 1.5
#     block_size = 16
#     frame_nth = 0

#     macroblocks_data_list = []
#     abs_diff_values = []
#     for frame_nth in range(total_frames - 1):
#         frame1_path = os.path.join(frame_directory, f"frame{frame_nth}.jpg")
#         frame2_path = os.path.join(frame_directory, f"frame{frame_nth + 1}.jpg")

#         if os.path.exists(frame1_path) and os.path.exists(frame2_path):
#             frame1 = cv2.imread(frame1_path)
#             frame2 = cv2.imread(frame2_path)

#             if frame1 is not None and frame2 is not None:
#                 macroblocks1 = extract_macroblocks(frame1)
#                 macroblocks2 = extract_macroblocks(frame2)

#                 for mb1, mb2 in zip(macroblocks1, macroblocks2):
#                     mb1_gray = cv2.cvtColor(mb1, cv2.COLOR_BGR2GRAY)
#                     mb2_gray = cv2.cvtColor(mb2, cv2.COLOR_BGR2GRAY)
#                     abs_diff = cv2.absdiff(mb1_gray, mb2_gray)
#                     sum_abs_diff = np.sum(abs_diff)
#                     abs_diff_values.append(sum_abs_diff)

#                 abs_diff_threshold = np.mean(abs_diff_values) + multiplier * np.std(abs_diff_values)

#                 for i, (mb1, mb2) in enumerate(zip(macroblocks1, macroblocks2)):
#                     mb1_gray = cv2.cvtColor(mb1, cv2.COLOR_BGR2GRAY)
#                     mb2_gray = cv2.cvtColor(mb2, cv2.COLOR_BGR2GRAY)
#                     abs_diff = cv2.absdiff(mb1_gray, mb2_gray)
#                     sum_abs_diff = np.sum(abs_diff)

#                     if sum_abs_diff > abs_diff_threshold:
#                         mb_path = os.path.join(mb_directory, f"macroblock_{frame_nth}_{i}.jpg")
#                         cv2.imwrite(mb_path, mb1)

#                         current_x = (i % (frame1.shape[1] // block_size)) * block_size
#                         current_y = (i // (frame1.shape[1] // block_size)) * block_size

#                         red = np.sum(mb1[:, :, 2]) / 16
#                         green = np.sum(mb1[:, :, 1]) / 16
#                         blue = np.sum(mb1[:, :, 0]) / 16

#                         macroblocks_data_list.append({'Frame': frame_nth, 'Macroblock': i, 'SumAbsDiff': sum_abs_diff, 'X': current_x, 'Y': current_y, 'Red': red, 'Green': green, 'Blue': blue})

#             else:
#                 print(f"Error: Unable to open frame images {frame1_path} or {frame2_path}")
#         else:
#             print(f"Error: Frame images {frame1_path} or {frame2_path} not found.")

#     return macroblocks_data_list