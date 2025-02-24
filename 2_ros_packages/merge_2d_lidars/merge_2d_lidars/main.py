#! /bin/python3
import rclpy
from sensor_msgs.msg import LaserScan
from tf2_ros import Buffer, TransformListener
import tf_transformations as transformations
from time import time
import copy

from rclpy.node import Node
from rclpy.action import ActionClient
from geometry_msgs.msg import Twist, Point
import sys
import os
import numpy as np

from rclpy.qos import QoSProfile, ReliabilityPolicy

class MergeScan(Node):

    def __init__(self):
        super().__init__("robot_node")
        # scan1 : main lidar to be merged from another scan
        # scan2 : sub lidar
        self.declare_parameter('tname1', "/scan1")
        tname1 = self.get_parameter('tname1').value
        self.declare_parameter('tname2', "/scan2")
        tname2 = self.get_parameter('tname2').value
        self.declare_parameter('oname', "/scan")
        oname = self.get_parameter('oname').value

        self.declare_parameter('disable_update', False)
        self.disable_update = self.get_parameter('disable_update').value
                
        self.declare_parameter('angle1_range', [-3.1241390705108643,3.1415925533510745])
        self.angle1_range = self.get_parameter('angle1_range').value
        self.declare_parameter('angle1_increment', 0.005806980188935995 )
        self.angle1_increment = self.get_parameter('angle1_increment').value
        self.declare_parameter('target1_range', [-np.pi/4,np.pi/4])
        self.target1_range = self.get_parameter('target1_range').value
        self.declare_parameter('target1_dir', 0)
        self.target1_dir = self.get_parameter('target1_dir').value
        self.declare_parameter('lidar1_max', 40)
        self.lidar1_max = self.get_parameter('lidar1_max').value
        
        self.declare_parameter('angle2_range', [-3.1241390705108643,3.1415925533510745])
        self.angle2_range = self.get_parameter('angle2_range').value
        self.declare_parameter('angle2_increment', 0.5806980188935995 )
        self.angle2_increment = self.get_parameter('angle2_increment').value
        self.declare_parameter('target2_range', [-np.pi/2,np.pi/2])
        self.target2_range = self.get_parameter('target2_range').value
        self.declare_parameter('target2_dir', 0)
        self.target2_dir = self.get_parameter('target2_dir').value
        
        self.declare_parameter('len_lidars', 0.44)
        self.L = self.get_parameter('len_lidars').value # two rplidar distance [m]
        self.declare_parameter('matching_threshold', 0.1)  # threshold for matching d2 and d2* [m]
        self.tld = self.get_parameter('matching_threshold').value
      
        qos_profile = QoSProfile(depth=1)
        qos_profile.reliability = ReliabilityPolicy.RELIABLE
        self.scan = self.robot.create_publisher(LaserScan, oname, qos_profile)
        self.lidar1 = self.robot.create_subscription(
            LaserScan,
            tname1,
            self.lidar1_callback,
            qos_profile,
        )
        self.lidar2 = self.robot.create_subscription(
            LaserScan,
            tname2,
            self.lidar2_callback,
            qos_profile,
        )

        # RPLiDAR : [-pi, pi]を1080に反時計回りに分割
        #           pi がインデックス1080 で前
        self.scan = None
        self.scan1 = None
        self.scan2 = None
                
        if not self.disable_update:
          self.calc_constants()
          self.flag = [False,False,False]
        else:
          self.flag = [True,True,True]
        
        hz = 10
        self.create_timer(1 / hz, self.merged_scan)  # TODO

    def set_constants(self,msg,i):
      if i == 0:
        self.angle1_increment = msg.angle_increment # 0.005806980188935995 
        self.angle1_range[0] = msg.angle_min # -3.1241390705108643
        self.angle1_range[1] = msg.angle_max # 3.1241390705108643
      else:
        self.angle2_increment = msg.angle_increment # 0.005806980188935995 
        self.angle2_range[0] = msg.angle_min # -3.1241390705108643
        self.angle2_range[1] = msg.angle_max # 3.1241390705108643

    def lidar1_callback(self, msg):
        if self.flag[0]:
          self.set_constants(msg,0)
          self.flag[0] = False # 排他処理をしなくてよいようにこの順番：保守的だが確実
        self.scan1 = msg

    def lidar2_callback(self, msg):
        if self.flag[1]:
          self.set_constants(msg,1)
          self.flag[1] = False
        self.scan2 = msg

    def calc_constants(self):
        # Set scan1 range to be merged
        # frontから見てボディで隠れる領域：レーザーindexの範囲
        # RPLiDARでは540 が真後ろ 90個で30度
        a1 = np.arange(self.angle1_range[0],self.angle1_range[1],self.angle1_increment)
        angle1 = np.append(a1,a1[-1]+self.angle1_increment)
        a1ids = np.arange(len(angle1))
        t1r=[np.where(angle1>self.target1_range[0])[0][0],np.where(angle1<self.target1_range[1])[0][-1]]
        if t1r[0] < t1r[1]: # 例：t1_range = [405,406,...685] 
          self.t1_range = np.arange(t1r[0],t1r[1])
        else:
          self.t1_range = np.append(np.arange(t1r[0],a1ids[-1]),np.arange(0,t1r[1]))
        t1d = np.argmin(np.abs(angle1 - self.target1_dir))
        self.t1_dir = np.argmin(np.abs(self.t1_range - t1d)) # t1_rangeの中でのインデックス t1_range[t1_dir]
        
        a2 = np.arange(self.angle2_range[0],self.angle2_range[1],self.angle2_increment)
        angle2 = np.append(a2,a2[-1]+self.angle2_increment)
        a2ids = np.arange(len(angle2))
        t2r=[np.where(angle2>self.target2_range[0])[0][0],np.where(angle2<self.target2_range[1])[0][-1]]
        if t2r[0] < t2r[1]: # 例：t2_range = [270,271,...,810]
          self.t2_range = np.arange(t2r[0],t2r[1])
        else:
          self.t2_range = np.append(np.arange(t2r[0],a2ids[-1]),np.arange(0,t2r[1]))
        t2d = np.argmin(np.abs(angle2 - self.target2_dir))
        self.t2_dir = np.argmin(np.abs(self.t2_range - t2d)) # t2_rangeの中でのインデックス t2_range[t2_dir]
        
        # N: negative part, P: positive part
        
        # calc constants once from scan topic 
        # legend: RPLiDAR S1
        # alpha: angle in front_rplidar frame ( same dir with robot )
        # [al_min, 0]
        # alN = (self.angle1_increment * np.arange(self.t1_range[0] - 1, self.t1_dir - 1) + self.angle1_range[0]).reshape(-1, 1)
        alN = angle1[self.t1_range[:self.t1_dir]].reshape(-1,1)
        # [0, al_max]
        #alP = (self.angle1_increment * np.arange(self.t1_dir , self.t1_range[1]) + self.angle1_range[0]).reshape(-1, 1)
        alP = angle1[self.t1_range[self.t1_dir:]].reshape(-1,1)

        # theta: angle in back_rplidar frame ( inverse dir with robot )
        # [-pi/2, 0]
        #thN = self.angle2_increment * np.arange(self.t2_range[0] - 1 , self.t2_dir - 1)+ self.angle2_range[0] - np.pi
        thN = angle2[self.t2_range[:self.t2_dir]]
        # [0, pi/2]
        #thP = self.angle2_increment * np.arange( self.t2_dir, self.t2_range[1]) + self.angle2_range[0] + np.pi
        thP = angle2[self.t2_range[self.t2_dir:]]

        phiN = thN - alN
        phiP = thP - alP
        # phi = th - al # matrix: row: alpha, col: th
        sinphiN = np.sin(phiN)
        cosphiN = np.cos(phiP)
        sinalN = np.sin(alN)
        sinthN = np.sin(thN)
        # cosalN = np.cos(alN)
        # costhN = np.cos(thN)
        # Confirm element-wise calculation
        self.AN = self.L *  sinalN / sinphiN  # d2* : geometric intersection
        self.BN = self.L *  (sinthN - sinalN * cosphiN) / sinphiN
        self.CN = cosphiN
        # self.BN = np.hstack([L / cosalN] * len(thN))
        # self.CN = costhN / cosalN
        # self.BN = np.zeros(phiN.shape)
        # self.CN = sinthN / sinalN
        self.IDMN = np.matlib.repmat(
            np.arange(0, self.AN.shape[1]), self.AN.shape[0], 1
        )  # = [[0,1,2,3,...],[0,1,2,3,...],...]

        sinphiP = np.sin(phiP)
        cosphiP = np.cos(phiP)
        sinalP = np.sin(alP)
        sinthP = np.sin(thP)
        # cosalP = np.cos(alP)
        # costhP = np.cos(thP)
        # Confirm element-wise calculation
        self.AP = self.L *  sinalP / sinphiP  # d2
        self.BP = self.L *  (sinthP - sinalP * cosphiP) / sinphiP
        self.CP = cosphiP
        # self.BP = np.hstack([L / cosalP] * len(thP))
        # self.CP = costhP / cosalP
        # self.BP = np.zeros(phiP.shape)
        # self.CP = sinthP / sinalP
        self.IDMP = np.matlib.repmat(
            np.arange(0, self.AP.shape[1]), self.AP.shape[0], 1
        )  # = [[0,1,2,3,...],[0,1,2,3,...],...]

    def merged_scan(self):
        if self.scan1 is None or self.scan2 is None:
          print("RPLidar is down!!!!!!!!!!!!!!!!")
          return
        elif not self.flag[0] and not self.flag[1] and self.flag[2]: 
          self.calc_constants()
          self.flag[2] = False

        merged_scan = copy.deepcopy(self.scan1)
        ranges = np.array([copy.deepcopy(self.scan1.ranges)])
        ranges[0, self.t1_range] = np.inf  # initialize hidden range

        # al: [al_min, 0]  th: [-pi/2, 0 ] の範囲
        DN = np.array([self.scan2.ranges[self.t2_range[:self.t2_dir]]])  # distance by scan2
        condN = (DN < self.AN) & (
            self.AN - DN < self.tld
        )  # same size with AN: AN - tld < DN < AN
        nonzero_idN = np.any(condN, axis=1)  # True: satisfy condition
        if np.any(nonzero_idN) > 0:  # True case
            JN = np.argmin(
                np.where(condN[nonzero_idN, :], self.IDMN[nonzero_idN, :], len(self.angle2_range)+1), # 第３引数は十分大きい値であれば良い
                axis=1
            )
            # J1 = np.argmax(cond1[nonzero_id1, :], axis=1)
            ranges[0, self.t1_range[:self.t1_dir]][nonzero_idN] = (
                DN[0, JN] * self.CN[nonzero_idN, JN] + self.BN[nonzero_idN, JN]
            )

        # al: [0, al_max]  th: [ 0, pi/2 ] の範囲
        DP = np.array([self.scan2.ranges[self.t2_range[self.t2_dir:]]])
        condP = (DP < self.AP) & (
            self.AP - DP < self.tld
        )  # same size with AP = al x th
        nonzero_idP = np.any(condP, axis=1)  # row: boolean,  True: al satisfy cond2
        # print(f"DP: {DP.shape}, inf:{nonzero_id2}, cond:{cond2}")
        if np.any(nonzero_idP) > 0:  # for al that satisfy cond2
            JP = np.argmax(
                np.where(condP[nonzero_idP, :], self.IDMP[nonzero_idP, :], -1), axis=1
            )
            # print(f" J2: {J2.shape}, DP[J2]: {DP[0,J2].shape}")
            ranges[0, self.t1_range[self.t1_dir:]][nonzero_idP] = (
                DP[0, JP] * self.CP[nonzero_idP, JP] + self.BP[nonzero_idP, JP]
            )

        ranges[0, ranges[0] == np.inf] = merged_scan.range_max + 20
        ranges[0, ranges[0] < merged_scan.range_min] = merged_scan.range_max + 20
        merged_scan.ranges = [float(value) for value in ranges[0]]
        merged_scan.header.stamp = self.get_clock().now().to_msg()
        self.pub.scan.publish(merged_scan)

    def destroy_subscription(self):
        self.destroy_subscription()
        
        
def main(args=None):
    rclpy.init(args=args)

    scan = MergeScan()
    try: 
        rclpy.spin(scan) 
    except KeyboardInterrupt: 
        pass 
    except Exception as e: 
        scan.get_logger().error(f"Unexpected error: {e}") 
    finally: 
        scan.destroy_node() 
        rclpy.shutdown()

if __name__ == "__main__":
    main()
