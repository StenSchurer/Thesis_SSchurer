"""
Stabilization of videos using OpenCV.
Stabilized video will be saved in the same directory as the original video.

Sources:
--------
http://nghiaho.com/uploads/code/videostab.cpp
https://www.learnopencv.com/video-stabilization-using-point-feature-matching-in-opencv/

"""

import os
import cv2
import numpy as np
from tqdm import tqdm
import stabilization as stb

videopath = r'C:/Users/SSchurer/Documents/TU_Delft/Thesis/LSPIV/Edited/After rain/After_rain_original_stabilized2.mp4'

def movingAverage(curve, radius):
    """Moving average filter that takes in any curve as an input and
    returns the smoothed version of the curve.

    Arguments:
        curve {list} -- Any curve to be smoothed (i.e. 1-D of numbers)
        radius {int} -- Padding of the curve

    Returns:
        curve_smoothed {array} -- Smoothed curve
    """
    window_size = 2 * radius + 1
    # Define the filter
    f = np.ones(window_size)/window_size
    # Add padding to the boundaries
    curve_pad = np.lib.pad(curve, (radius, radius), 'edge')
    # Apply convolution
    curve_smoothed = np.convolve(curve_pad, f, mode='same')
    # Remove padding
    curve_smoothed = curve_smoothed[radius:-radius]
    # return smoothed curve
    return curve_smoothed


def smooth(trajectory, smoothing_radius):
    """Smooth x, y and angles individually"""
    smoothed_trajectory = np.copy(trajectory)
    # Filter the x, y and angle curves
    for i in range(3):
        smoothed_trajectory[:, i] = movingAverage(trajectory[:, i],
                                                  radius=smoothing_radius)

    return smoothed_trajectory


def fixBorder(frame):
    """Adjust border to remove as much of black borders as possible"""
    s = frame.shape
    # Scale the image 2% without moving the center
    T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, 1.02)
    frame = cv2.warpAffine(frame, T, (s[1], s[0]))
    return frame


def stabilization(videopath,
                  smoothing_radius=50,
                  fixed_area=[0, -1, 0, -1],
                  stab_points=200):
    """Stabilization of a video. Saved at the same directory as the original
    video. Using fixed_area it is possible to adress an area in which fixed
    spots are located.

    Arguments:
        videopath {str} -- Path to video (example: r'C:/example_video.mp4')

    Keyword Arguments:
        smoothing_radius {int} -- Strength of smoothing effect (default: {50})
        fixed_area {[x0, x1, y0, y1]} --  Reference area which is fixed
        (default: {[0, -1, 0, -1]})
        stab_points {int} -- Number of points used to apply stabilization on
        (default: {200})
    """

    # Read original video
    # Extract directory and videoname for saving purposes
    capture = cv2.VideoCapture(videopath)
    directory, videoname = os.path.split(videopath)
    videoname = os.path.splitext(videoname)[0]

    # Get number of frames
    # Get width and height of video stream
    # Get frames per second (fps)
    n_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    w = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = capture.get(cv2.CAP_PROP_FPS)

    # Set up output video
    out = cv2.VideoWriter(os.path.join(directory, str(videoname)+'_stabilized.mp4'),
                          -1,
                          fps,
                          (w, h))

    # Read first frame
    # Convert frame to grayscale and extract part of image
    _, prev = capture.read()
    xmin, xmax, ymin, ymax = fixed_area
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)[ymin:ymax, xmin:xmax]

    # Pre-define transformation-store array
    transforms = np.zeros((n_frames-1, 3), np.float32)

    # Filling in transformation array per frameset
    with tqdm(total=2*(n_frames-2), ncols=50) as pbar:
        for i in range(n_frames-2):
            # Detect feature points in previous frame
            prev_pts = cv2.goodFeaturesToTrack(prev_gray,
                                               maxCorners=stab_points,
                                               qualityLevel=0.1,
                                               minDistance=100,
                                               blockSize=10)
            # Read next frame
            # If not success: break loop
            success, curr = capture.read()
            if not success:
                break

            # Convert to grayscale and extract part of image
            # Calculate optical flow (i.e. track feature points)
            # Sanity check
            curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)[ymin:ymax,
                                                               xmin:xmax]
            curr_pts, status, err = cv2.calcOpticalFlowPyrLK(prev_gray,
                                                             curr_gray,
                                                             prev_pts,
                                                             None)
            assert prev_pts.shape == curr_pts.shape

            # Filter only valid points
            idx = np.where(status == 1)[0]
            prev_pts = prev_pts[idx]
            curr_pts = curr_pts[idx]

            # Find transformation matrix
            m = cv2.estimateAffinePartial2D(prev_pts, curr_pts)[0]

            # Extract translation
            # Extract rotation angle
            dx = m[0, 2]
            dy = m[1, 2]
            da = np.arctan2(m[1, 0], m[0, 0])

            # Store transformation
            transforms[i] = [dx, dy, da]

            # Move to next frame
            prev_gray = curr_gray

            pbar.update(1)

        # Compute trajectory using cumulative sum of transformations
        # Create variable to store smoothed trajectory
        # Calculate diference in smoothed_trajectory and trajectory
        trajectory = np.cumsum(transforms, axis=0)
        smoothed_trajectory = smooth(trajectory, smoothing_radius)
        difference = smoothed_trajectory - trajectory

        # Calculate newer transformation array
        transform_smooth = transforms + difference

        # Reset stream to first frame
        capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # Apply transformations to video
        for i in range(n_frames-2):
            # Read next frame
            success, frame = capture.read()
            if not success:
                break

            # Extract transformations from the new transformation array
            dx = transform_smooth[i, 0]
            dy = transform_smooth[i, 1]
            da = transform_smooth[i, 2]

            # Reconstruct transformation matrix accordingly to new values
            m = np.zeros((2, 3), np.float32)
            m[0, 0] = np.cos(da)
            m[0, 1] = -np.sin(da)
            m[1, 0] = np.sin(da)
            m[1, 1] = np.cos(da)
            m[0, 2] = dx
            m[1, 2] = dy

            # Apply affine wrapping to the given frame
            # Fix border artifacts
            frame_stabilized = cv2.warpAffine(frame, m, (w, h))
            frame_stabilized = fixBorder(frame_stabilized)

            # Save new frame
            out.write(frame_stabilized)

            pbar.update(1)

    # Release original and stabilized video
    capture.release()
    out.release()

stb.stabilization(videopath,
                  smoothing_radius=200,
                  fixed_area=[0, -1, 0, -1],
                  stab_points=200)