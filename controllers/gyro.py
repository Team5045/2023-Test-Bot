# time for a pro gyroscope no :billed_cap:
import navx
from components.drivetrain import DriveTrain
import wpilib
import ctre
import networktables
from networktables import NetworkTable
from magicbot import MagicRobot

class gyro():

    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    
    def setup(self):
        self.navx = navx.AHRS.create_spi()

    def balancing(self):
        ABSOLUTE_ANGLE = abs(angle)
        MAX_RANGE_LIM = 180
        angle = self.navx.getPitch()

        ''' Just making things a bit easier to read here with variables'''
        motor_set = angle/MAX_RANGE_LIM
        # This should provide constant adjustment to the speeds so it won't jerk the robot

        if (ABSOLUTE_ANGLE > 0) and (ABSOLUTE_ANGLE < MAX_RANGE_LIM):
            if angle > 0.0:
                self.drivetrain.set_motors(0.2, 0.0)
                self.sd.putValue("Mode: ", "Moving Forward")

            elif angle < 0.0:
                self.drivetrain.set_motors(motor_set, 0.0)
                self.sd.putValue("Mode: ", "Moving Backward")

            else:
                self.drivetrain.set_motors(0.2, 0.0)
                self.sd.putValue("Mode: ", "Balanced!")
                print("balanced!")

            ''' Conditional Statements after prereqs are checked '''
        else:
            self.drivetrain.set_motors(0.0, 0.0)
            

        
        