import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

class CameraPublisher(Node):
    def __init__(self):
        super().__init__('cam_publish_node')
        self.publisher = self.create_publisher(Image, '/cam_publisher', 10)
        self.bridge = CvBridge()

    def capture_images(self):
        cap = cv2.VideoCapture(1)
        while True:
            ret, frame = cap.read()
            if ret:
                image_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")
                self.publisher.publish(image_msg)

def main():
    rclpy.init()
    node = CameraPublisher()
    node.capture_images()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
