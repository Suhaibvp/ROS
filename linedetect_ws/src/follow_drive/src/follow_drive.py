import rclpy
from rclpy.node import Node
from std_msgs.msg import Int16
import pigpio

class VisionbotDriver(Node):
    def __init__(self):
        super().__init__('Visionbot_driver')
        self.line_error_subscriber = self.create_subscription(Int16, '/line_following_error', self.update_motor_speed, 10)
        self.motor_controller = MotorSetup(24, 23, 25, 20, 16, 21)
        self.standard_speed = 128  # Base speed for the wheels
        self.velocity_right_wheel = 0
        self.velocity_left_wheel = 0

    def update_motor_speed(self, error_msg):
        if error_msg.data < 0:  # Turn right
            self.velocity_right_wheel = self.standard_speed - 10
            self.velocity_left_wheel = self.standard_speed + 10
        else:  # Turn left
            self.velocity_right_wheel = self.standard_speed + 10
            self.velocity_left_wheel = self.standard_speed - 10

        self.motor_controller.set_speeds(self.velocity_left_wheel, self.velocity_right_wheel)

class MotorSetup:
    def __init__(self, pin_right_a, pin_right_b, pin_right_enable, pin_left_a, pin_left_b, pin_left_enable):
        self.pi = pigpio.pi()
        self.pin_right_enable = pin_right_enable
        self.pin_left_enable = pin_left_enable

        self.pi.set_mode(pin_right_enable, pigpio.OUTPUT)
        self.pi.set_mode(pin_left_enable, pigpio.OUTPUT)

        self.pi.set_PWM_frequency(pin_right_enable, 1000)
        self.pi.set_PWM_frequency(pin_left_enable, 1000)

    def set_speeds(self, left_wheel_speed, right_wheel_speed):
        self.pi.set_PWM_dutycycle(self.pin_right_enable, right_wheel_speed)
        self.pi.set_PWM_dutycycle(self.pin_left_enable, left_wheel_speed)

    def stop_motors(self):
        self.pi.set_PWM_dutycycle(self.pin_right_enable, 0)
        self.pi.set_PWM_dutycycle(self.pin_left_enable, 0)

    def cleanup(self):
        self.pi.stop()

def main(args=None):
    rclpy.init(args=args)
    robot_controller = VisionbotDriver()
    rclpy.spin(robot_controller)
    robot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
