import cv2

def find_available_cameras():
    available_cameras = []
    for i in range(10):  # Check up to 10 cameras
        cap = cv2.VideoCapture(i)
        if not cap.isOpened():
            break
        else:
            available_cameras.append(i)
            cap.release()
    return available_cameras

if __name__ == "__main__":
    cameras = find_available_cameras()
    if cameras:
        print("Available cameras:")
        for cam in cameras:
            print(f"Camera {cam}")
    else:
        print("No cameras found.")
