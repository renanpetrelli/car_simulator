#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Odometry

class Movimento:
    def __init__(self):
        rospy.init_node('movimento_carro', anonymous=True)
        rospy.Subscriber('sonar_data', PointStamped, self.movimentarCarro)
        self.pubMovimentacao = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.radar = PointStamped()
        self.posicaoRelativaCarros = PointStamped()
        self.odomCarro = Odometry()

    def movimentarCarro(self,sonar):

        rate = rospy.Rate(10)

        v = Twist()
        v.linear.x = sonar.point.x
        v.linear.y = sonar.point.y
        v.linear.z = 0.0

        v.angular.x = 0.0
        v.angular.y = 0.0

        if(v.linear.x == sonar.point.x):
         v.angular.z = 0.0
        elif(int(v.linear.x) == int(sonar.point.x)):
         v.linear.x = 0.0
         v.linear.y = 0.0
         v.angular.z = 180.0
        else
         v.angular.z = 0.0

        self.pubMovimentacao.publish(v)
        
        rate.sleep()


if __name__ == '__main__':
    try:
        t = Movimento()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass    