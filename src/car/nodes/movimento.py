#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PointStamped
from nav_msgs.msg import Odometry

class Movimento:
    def __init__(self):
        rospy.init_node('movimento_carro', anonymous=True)
        rospy.Subscriber('sonar_data', PointStamped, self.movimentarCarro)
        rospy.Subscriber('odom', Odometry, self.posicaoCarro)
        self.pubMovimentacao = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        self.radar = PointStamped()
        self.posicaoRelativaCarros = PointStamped()
        self.posicaoCarro = PointStamped()

    def posicaoCarro(self,odom):

        rate = rospy.Rate(500)

        self.posicaoCarro.point.x = odom.pose.pose.position.x
        self.posicaoCarro.point.y = odom.pose.pose.position.y
        self.posicaoCarro.point.z = odom.pose.pose.position.z

        rate.sleep()

    def direcaoLado(self, posicaoCarro , distancia):
        if(abs(distancia) > 3.0):
            posicaoCarroVerde = posicaoCarro + distancia
            if(posicaoCarroVerde < posicaoCarro):
             return 0 - 1.5
            else:
             return 1.5
        else:
            return 0.0

    def direcaoFrente(self, posicaoCarro , distancia):
        if(abs(distancia) > 3.0):
            posicaoCarroVerde = posicaoCarro + distancia
            if(posicaoCarroVerde > posicaoCarro):
             return 1.5
            else:
             return 0 - 1.5
        else:
            return 0.0


    def movimentarCarro(self,sonar):

        rate = rospy.Rate(500)

        v = Twist()
        v.linear.x = self.direcaoLado(self.posicaoCarro.point.x, sonar.point.x)
        v.linear.y = self.direcaoFrente(self.posicaoCarro.point.y, sonar.point.y)
        v.linear.z = 0.0

        v.angular.x = 0.0
        v.angular.y = 0.0

        v.angular.z = 0.0

        self.pubMovimentacao.publish(v)
        
        rate.sleep()


if __name__ == '__main__':
    try:
        t = Movimento()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass    