# video_processing/__init__.py

# Import modules to be available when importing the package
from .extract_frames import extract_frames
from .compare_macroblocks import compare_macroblocks
from .group_macroblocks import group_macroblocks
from .calculate_centroids import calculate_centroids
from .assign_identifiers import assign_macroblock_identifiers
from .detect_deleted_frame import detect_deleted_frame
from .detect_inserted_frame import detect_inserted_frame
from .plot_trajectory_object import plot_trajectory_object

# Explicitly specify symbols to be exported when using 'from video_processing import *'
__all__ = [
    'extract_frames',
    'compare_macroblocks',
    'group_macroblocks',
    'calculate_centroids',
    'assign_macroblock_identifiers',
    'detect_deleted_frame',
    'detect_inserted_frame',
    'plot_trajectory_object'
]