import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np
from std_msgs.msg import Int16

class ImageSubscriber(Node):
    def __init__(self):
        super().__init__('image_subscriber_node')
        self.subscription = self.create_subscription(
            Image,
            '/cam_publisher',  # Topic to subscribe to
            self.process_frame,  # Callback function
            10  # QoS profile depth
        )
        self.cv_bridge = CvBridge()
        self.error_signal = Int16()
        self.error_publisher = self.create_publisher(Int16, '/line_following_error', 10)
        self.motor_controller = MotorController()

    def process_frame(self, img_msg):
        cv_img = self.cv_bridge.imgmsg_to_cv2(img_msg, 'mono8')
        resized_img = cv2.resize(cv_img, (640, 480), interpolation=cv2.INTER_AREA)
        region_of_interest = resized_img[325:478, 196:531]
        edges_detected = cv2.Canny(region_of_interest, 90, 120)

        line_positions = []
        center_of_line = 0
        for position, intensity in enumerate(edges_detected[:][139]):
            if intensity == 255:
                line_positions.append(position)

        if len(line_positions) == 2:
            center_of_line = sum(line_positions) // 2

        robot_center = 167  # X coordinate of robot's center
        line_error = robot_center - center_of_line
        self.error_signal.data = line_error
        self.error_publisher.publish(self.error_signal)

        # Robot movement based on the error
        self.motor_controller.adjust_movement(line_error)

        # For visual debugging
        cv2.imshow('Original', resized_img)
        cv2.imshow('Edge Detection', edges_detected)
        cv2.waitKey(1)

class MotorController:
    def __init__(self):
        # Initialize your motor control here (GPIO setup or other initializations)
        pass

    def adjust_movement(self, error):
        # Implement motor control logic based on the error value
        if error > 0:
            # Move right
            print("move right")
            pass
        elif error < 0:
            # Move left
            print("move left")
            pass
        else:
            # Move forward
            print("move forward")
            pass
def main():
    rclpy.init()
    node = ImageSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
