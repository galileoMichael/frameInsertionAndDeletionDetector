import matplotlib.pyplot as plt
import os

def plot_trajectory_object(identifiers):
    """
    Plot centroid changes over frames for each identified object.
    
    Args:
        identifiers (dict): Dictionary where keys are object IDs and values are lists of dictionaries containing frame numbers and centroids.
        
    Returns:
        None
    """

    trajectory_directory = r"D:\Polban\TA\PROGRAM\Aplikasi_Sistem_Pendeteksian_Penyisipan_dan_Penghapusan_Frame\data\trajectory graph"
    num_objects = len(identifiers)
    num_cols = 2 
    num_rows = -(-num_objects // num_cols)
    
    fig, axs = plt.subplots(num_rows, num_cols, figsize=(15, 5*num_rows))
    
    for idx, (object_id, centroid_data) in enumerate(identifiers.items()):
        row = idx // num_cols
        col = idx % num_cols
        
        ax = axs[row, col] if num_rows > 1 else axs[col]
        
        frame_numbers = [data['frame'] for data in centroid_data]
        x_centroids = [data['centroid'][0] for data in centroid_data]
        y_centroids = [data['centroid'][1] for data in centroid_data]
        
        ax.scatter(frame_numbers, x_centroids, color='blue', label='X Centroid')
        ax.scatter(frame_numbers, y_centroids, color='red', label='Y Centroid')
        ax.set_xlabel('Frame Number')
        ax.set_ylabel('Centroid Position')
        ax.set_title(f'Trajectory for Object {object_id}')
        ax.legend()
        ax.grid(True)
    

    if not os.path.exists(trajectory_directory):
        os.makedirs(trajectory_directory)
    plot_path = os.path.join(trajectory_directory, 'trajectory_plot.png')
    plt.savefig(plot_path)
    plt.close(fig)