from threading import Thread
from queue import Queue
from pathlib import Path
import os
import shutil 
import time

from video_processing.extract_frames import extract_frames
from video_processing.compare_macroblocks import compare_macroblocks
from video_processing.group_macroblocks import group_macroblocks
from video_processing.calculate_centroids import calculate_centroids
from video_processing.assign_identifiers import assign_macroblock_identifiers
from video_processing.detect_deleted_frame import detect_deleted_frame
from video_processing.detect_inserted_frame import detect_inserted_frame
from video_processing.plot_trajectory_object import plot_trajectory_object

def clear_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)  
    os.makedirs(directory_path, exist_ok=True)

def main(video_path, gui_queue):

    gui_queue.put(f'show_image_1')
    time.sleep(1)

    frame_directory = r"D:\Polban\TA\PROGRAM\Aplikasi_Sistem_Pendeteksian_Penyisipan_dan_Penghapusan_Frame\data\frames"
    mb_directory = r"D:\Polban\TA\PROGRAM\Aplikasi_Sistem_Pendeteksian_Penyisipan_dan_Penghapusan_Frame\data\macroblocks"

    clear_directory(frame_directory)
    clear_directory(mb_directory)

    print("Extracting frame(s)...")
    extract_frames(video_path, frame_directory)
    print("Frame(s) extraction completed.")

    gui_queue.put(f'show_image_2')
    time.sleep(1)   

    print("Comparing macroblock(s)")
    macroblocks_data_list = compare_macroblocks(video_path, frame_directory, mb_directory)
    print("Macroblock(s) comparison completed.")

    gui_queue.put(f'show_image_3')
    time.sleep(1)  

    print("Grouping Cluster of Macrooblck(s)...")
    max_distance = 16
    total_frames = len(os.listdir(frame_directory))
    grouped_macroblocks = group_macroblocks(macroblocks_data_list, max_distance, total_frames)
    print("Grouping completed.")

    gui_queue.put(f'show_image_4')
    time.sleep(1)    

    centroids = calculate_centroids(grouped_macroblocks)
    print("Centroids calculation completed.")  

    gui_queue.put(f'show_image_5')
    time.sleep(1)        

    print("Tracking objects...")
    identifiers = assign_macroblock_identifiers(centroids)
    print("Tracking objects completed.")  

    gui_queue.put(f'show_image_6')
    time.sleep(1)  

    print("Detecting deleted frames...")
    deletion_locations, deleted_frames = detect_deleted_frame(identifiers)
    print("Deleted frames detection complete")

    print("Detecting inserted frames...")
    insertion_locations = detect_inserted_frame(identifiers)
    print("Inserted frames detection comple")

    gui_queue.put(f'show_image_7')
    time.sleep(1)  

    print("Deletion Locations: ", deletion_locations)
    print("Insertion Location: ", insertion_locations)

    gui_queue.put(f'show_image_8')
    time.sleep(1)  

    gui_queue.put(('show_results', deletion_locations, deleted_frames, insertion_locations))
    gui_queue.put(f'restart_app')

    print("Drawing trajectory lines...")
    plot_trajectory_object(identifiers) 
    print("Drawing trajectory completed.")

if __name__ == "__main__":
    main()