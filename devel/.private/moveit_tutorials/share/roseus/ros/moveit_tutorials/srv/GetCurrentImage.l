;; Auto-generated. Do not edit!


(when (boundp 'moveit_tutorials::GetCurrentImage)
  (if (not (find-package "MOVEIT_TUTORIALS"))
    (make-package "MOVEIT_TUTORIALS"))
  (shadow 'GetCurrentImage (find-package "MOVEIT_TUTORIALS")))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTIMAGE")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTIMAGE"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEREQUEST")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEREQUEST"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTIMAGERESPONSE")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTIMAGERESPONSE"))

(in-package "ROS")



(if (not (find-package "SENSOR_MSGS"))
  (ros::roseus-add-msgs "sensor_msgs"))


(defclass moveit_tutorials::GetCurrentImageRequest
  :super ros::object
  :slots ())

(defmethod moveit_tutorials::GetCurrentImageRequest
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass moveit_tutorials::GetCurrentImageResponse
  :super ros::object
  :slots (_current_image ))

(defmethod moveit_tutorials::GetCurrentImageResponse
  (:init
   (&key
    ((:current_image __current_image) (instance sensor_msgs::Image :init))
    )
   (send-super :init)
   (setq _current_image __current_image)
   self)
  (:current_image
   (&rest __current_image)
   (if (keywordp (car __current_image))
       (send* _current_image __current_image)
     (progn
       (if __current_image (setq _current_image (car __current_image)))
       _current_image)))
  (:serialization-length
   ()
   (+
    ;; sensor_msgs/Image _current_image
    (send _current_image :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; sensor_msgs/Image _current_image
       (send _current_image :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; sensor_msgs/Image _current_image
     (send _current_image :deserialize buf ptr-) (incf ptr- (send _current_image :serialization-length))
   ;;
   self)
  )

(defclass moveit_tutorials::GetCurrentImage
  :super ros::object
  :slots ())

(setf (get moveit_tutorials::GetCurrentImage :md5sum-) "cb21fca2e1d6a2c2ac7fcf25b60e6837")
(setf (get moveit_tutorials::GetCurrentImage :datatype-) "moveit_tutorials/GetCurrentImage")
(setf (get moveit_tutorials::GetCurrentImage :request) moveit_tutorials::GetCurrentImageRequest)
(setf (get moveit_tutorials::GetCurrentImage :response) moveit_tutorials::GetCurrentImageResponse)

(defmethod moveit_tutorials::GetCurrentImageRequest
  (:response () (instance moveit_tutorials::GetCurrentImageResponse :init)))

(setf (get moveit_tutorials::GetCurrentImageRequest :md5sum-) "cb21fca2e1d6a2c2ac7fcf25b60e6837")
(setf (get moveit_tutorials::GetCurrentImageRequest :datatype-) "moveit_tutorials/GetCurrentImageRequest")
(setf (get moveit_tutorials::GetCurrentImageRequest :definition-)
      "---
sensor_msgs/Image current_image

================================================================================
MSG: sensor_msgs/Image
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image
#

Header header        # Header timestamp should be acquisition time of image
                     # Header frame_id should be optical frame of camera
                     # origin of frame should be optical center of camera
                     # +x should point to the right in the image
                     # +y should point down in the image
                     # +z should point into to plane of the image
                     # If the frame_id here and the frame_id of the CameraInfo
                     # message associated with the image conflict
                     # the behavior is undefined

uint32 height         # image height, that is, number of rows
uint32 width          # image width, that is, number of columns

# The legal values for encoding are in file src/image_encodings.cpp
# If you want to standardize a new string format, join
# ros-users@lists.sourceforge.net and send an email proposing a new encoding.

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.h

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id
")

(setf (get moveit_tutorials::GetCurrentImageResponse :md5sum-) "cb21fca2e1d6a2c2ac7fcf25b60e6837")
(setf (get moveit_tutorials::GetCurrentImageResponse :datatype-) "moveit_tutorials/GetCurrentImageResponse")
(setf (get moveit_tutorials::GetCurrentImageResponse :definition-)
      "---
sensor_msgs/Image current_image

================================================================================
MSG: sensor_msgs/Image
# This message contains an uncompressed image
# (0, 0) is at top-left corner of image
#

Header header        # Header timestamp should be acquisition time of image
                     # Header frame_id should be optical frame of camera
                     # origin of frame should be optical center of camera
                     # +x should point to the right in the image
                     # +y should point down in the image
                     # +z should point into to plane of the image
                     # If the frame_id here and the frame_id of the CameraInfo
                     # message associated with the image conflict
                     # the behavior is undefined

uint32 height         # image height, that is, number of rows
uint32 width          # image width, that is, number of columns

# The legal values for encoding are in file src/image_encodings.cpp
# If you want to standardize a new string format, join
# ros-users@lists.sourceforge.net and send an email proposing a new encoding.

string encoding       # Encoding of pixels -- channel meaning, ordering, size
                      # taken from the list of strings in include/sensor_msgs/image_encodings.h

uint8 is_bigendian    # is this data bigendian?
uint32 step           # Full row length in bytes
uint8[] data          # actual matrix data, size is (step * rows)

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id
")



(provide :moveit_tutorials/GetCurrentImage "cb21fca2e1d6a2c2ac7fcf25b60e6837")


