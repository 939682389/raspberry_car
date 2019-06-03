from main.Rotation import Rotation

class Steering:
    def __init__(self,channelH,min_thetaH,max_thetaH,
            channelV,min_thetaV,max_thetaV,init_thetaH=0,init_thetaV=0):
        '''
        构造函数
            channelH: 水平舵机的信号通道
            min_thetaH: 水平舵机最小转角
            max_thetaH: 水平舵机最大转角
            channelV: 垂直舵机的信号通道
            min_thetaV: 垂直舵机最小转角
            max_thetaV: 垂直舵机最大转角
            init_thetaH: 水平舵机初始转角
            init_thetaV: 垂直舵机初始转角
        '''
        self.hRotation=Rotation(channelH,min_thetaH,max_thetaH,init_thetaH)
        self.vRotation=Rotation(channelV,min_thetaV,max_thetaV,init_thetaV)

    def setup(self):
        self.hRotation.setup()
        self.vRotation.setup()

    def Up(self):
        '''
        向上步进转动（每次调用只转动0.2度）
        '''
        self.vRotation.positiveRotation()

    def Down(self):
        '''
        向下步进转动（每次调用只转动0.2度）
        '''
        self.vRotation.reverseRotation()

    def Left(self):
        '''
        向左步进转动（每次调用只转动0.2度）
        '''
        self.hRotation.positiveRotation()

    def Right(self):
        '''
        向右步进转动（每次调用只转动0.2度）
        '''
        self.hRotation.reverseRotation()

    def specify(self,thetaH,thetaV):
        '''
        转动到指定的角度
        '''
        self.hRotation.specifyRotation(thetaH)
        self.vRotation.specifyRotation(thetaV)

    def cleanup(self):
        self.hRotation.cleanup()
        self.vRotation.cleanup()