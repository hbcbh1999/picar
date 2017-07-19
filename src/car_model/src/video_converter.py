#!/usr/bin/env python
import roslib;
roslib.load_manifest('car_model')
import cv2, os, rospy, signal, sys
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from std_msgs.msg import String, Header
from time import sleep

#from __future__ import print_function

class video_converter:

    def __init__(self):
        self.bridge = CvBridge()

        self.image_pub = rospy.Publisher("/sensor_msgs/Image",Image, queue_size=50)
        #self.image_sub = rospy.Subscriber("image_topic",Image,self.callback)
        self.test_video = cv2.VideoCapture("example.avi")


    def vid_to_images(self):

        self.test_video = cv2.VideoCapture("example.avi")
        success, image = self.test_video.read()
        try:
            while success:

                cv2.imshow("Image window", image)
                cv2.waitKey(2)

                """
                pub_image = self.bridge.cv2_to_imgmsg(image, "bgr8")
                pub_image.header = Header()
                pub_image.header.frame_id = "odom"
                pub_image.header.stamp = rospy.Time.now()

                try:
                    self.image_pub.publish(pub_image)
                except CvBridgeError as e:
                    rospy.loginfo(e)
                """

                #cv2.imwrite("frames/frame%d.jpg"%count, image)
                success, image = self.test_video.read()
                sleep(0.03)

            return 1

        except KeyboardInterrupt:
            return 100

        self.test_video.release()
        rospy.loginfo("Done")
        #os.system("rm frames/*")


def signal_handler(signal, frame):
    rospy.signal_shutdown("Shutting down")
    sys.exit(0)



def main(args):
    vc = video_converter()
    for var in range(0,5):
        ret = vc.vid_to_images()
        if ret == 100:
            cv2.destroyAllWindows()
            break


if __name__ == '__main__':
    rospy.init_node('video_converter', anonymous=True)
    signal.signal(signal.SIGINT, signal_handler)
    main(sys.argv)
    rospy.spin()
