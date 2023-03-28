import wpilib
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid

from components.drivetrain import DriveTrain
from controllers.gyro import gyro
import wpilib.drive
from robotpy_ext.autonomous import AutonomousModeSelector
from ctre import NeutralMode
import navx

# Download and install stuff on the RoboRIO after imaging
'''
py -3 -m robotpy_installer download-python
py -3 -m robotpy_installer install-python
py -3 -m robotpy_installer download robotpy
py -3 -m robotpy_installer install robotpy
py -3 -m robotpy_installer download robotpy[ctre]
py -3 -m robotpy_installer install robotpy[ctre]
py -3 -m robotpy_installer download robotpy[rev]
py -3 -m robotpy_installer install robotpy[rev]
py -3 -m robotpy_installer download pynetworktables
py -3 -m robotpy_installer install pynetworktables
py -3 -m pip install -U robotpy[ctre]
py -3 -m pip install robotpy[ctre]
'''

# Push code to RoboRIO (only after imaging)
'''
python robot/robot.py deploy --skip-tests
py robot/robot.py deploy --skip-tests --no-version-check
'''


INPUT_SENSITIVITY = 0.05

PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
MagicRobot.control_loop_wait_time = 0.05

SPEED_MULTIPLIER = 1
ANGLE_MULTIPLIER = 1

WINDING_SPEED = .5
NEUTRAL_MODE = NeutralMode(2)

class SpartaBot(MagicRobot):

    # a DriveTrain instance is automatically created by MagicRobot

    drivetrain: DriveTrain
    gyro: gyro

    def createObjects(self):
        '''Create motors and stuff here'''

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')

        self.drive_controller: wpilib.XboxController = wpilib.XboxController(0)  # 0 works for sim?

        self.talon_L_1 = WPI_TalonSRX(1)
        self.talon_L_2 = WPI_TalonSRX(5)

        self.talon_R_1 = WPI_TalonSRX(6)
        self.talon_R_2 = WPI_TalonSRX(9)


    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def teleopInit(self):
        self.sd.putValue("Mode", "Teleop")
        # self.limelight = NetworkTables.getTable("limelight")
        # self.limelight.LEDState(3)
        # print("limelight on")
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''
        Called on each iteration of the control loop\n
        NOTE: all components' execute() methods will be called automatically
        '''

        # drive controls
        # print("tele")
        angle = self.drive_controller.getRightX()
        speed = self.drive_controller.getLeftY()

        if (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):

            self.drivetrain.set_motors(speed, -angle)

            self.sd.putValue('Drivetrain: ', 'moving')

        else:
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')

        
            

if __name__ == '__main__':
    wpilib.run(SpartaBot)