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
    navx = navx.AHRS.create_spi()
    
    def balancing(self):
        angle = self.navx.getPitch()
        if angle > 0:
            self.drivetrain.set_motors(0.2, 0.0)
            self.sd.putValue("Mode: ", "Moving Forward")
        elif angle < 0:
            self.drivetrain.set_motors(-0.2, 0.0)
            self.sd.putValue("Mode: ", "Moving Backward")
        else:
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue("Mode: ", "Balanced!")
            print("balanced!")
        print(self.navx.getPitch())

        
        