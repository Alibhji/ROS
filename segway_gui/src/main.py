import os , sys
print("test")


os.system('pyuic4 main_ui.ui > main_ui.py  ')
# !/usr/bin/env python
# license removed for brevity
import rospy

from main_ui import Ui_MainWindow

from  PyQt4.QtGui import QMainWindow, QApplication
from PyQt4  import QtCore
from std_msgs.msg import String


class appWin(QMainWindow):
    def __init__(self):
        super(appWin , self).__init__()
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        self.config()

    def config(self):
        self.ui.btn_segway_gazebo_rviz.clicked.connect(self.btn)
        self.ui.btn_topics.clicked.connect(self.btn)
        self.ui.btn_topics.setEnabled(False)

        self.genericThread = GenericThread(command_run, delay=0.3)






    def btn(self,sender):
        if(self.sender().objectName() == 'btn_segway_gazebo_rviz'):
            cmd='gazebo'
            self.genericThread = GenericThread(command_run,cmd, delay=0.3)
            self.genericThread.start()
            self.ui.btn_topics.setEnabled(True)

        elif(self.sender().objectName() == 'btn_topics'):
            cmd = 'topics'

            self.genericThread = GenericThread(command_run,cmd, delay=0.3)
            self.genericThread.start()
        print(cmd)


def command_run(cmd,delay=0.5):

    # if(self.sender().objectName() == 'btn_segway_gazebo_rviz'):
    if cmd=='gazebo':
        os.system( '{} {} {}'.format('roslaunch' ,'segway_gazebo','stanley_innovation_system_sim.launch'))
    elif cmd=='topics':
        os.system('{} {} {}'.format('rosrun', 'rqt_topic', 'rqt_topic'))


class GenericThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def __del__(self):
        self.wait()

    def run(self):
        self.function(*self.args, **self.kwargs)
        # self.function()
        return




def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)  # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()


if __name__ == '__main__':

    app = QApplication([])
    win=appWin()
    win.show()
    sys.exit(app.exec_())

    try:
        talker()
    except rospy.ROSInterruptException:
        pass