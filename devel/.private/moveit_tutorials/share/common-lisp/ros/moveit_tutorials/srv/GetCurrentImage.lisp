; Auto-generated. Do not edit!


(cl:in-package moveit_tutorials-srv)


;//! \htmlinclude GetCurrentImage-request.msg.html

(cl:defclass <GetCurrentImage-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass GetCurrentImage-request (<GetCurrentImage-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentImage-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentImage-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentImage-request> is deprecated: use moveit_tutorials-srv:GetCurrentImage-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentImage-request>) ostream)
  "Serializes a message object of type '<GetCurrentImage-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentImage-request>) istream)
  "Deserializes a message object of type '<GetCurrentImage-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentImage-request>)))
  "Returns string type for a service object of type '<GetCurrentImage-request>"
  "moveit_tutorials/GetCurrentImageRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentImage-request)))
  "Returns string type for a service object of type 'GetCurrentImage-request"
  "moveit_tutorials/GetCurrentImageRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentImage-request>)))
  "Returns md5sum for a message object of type '<GetCurrentImage-request>"
  "cb21fca2e1d6a2c2ac7fcf25b60e6837")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentImage-request)))
  "Returns md5sum for a message object of type 'GetCurrentImage-request"
  "cb21fca2e1d6a2c2ac7fcf25b60e6837")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentImage-request>)))
  "Returns full string definition for message of type '<GetCurrentImage-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentImage-request)))
  "Returns full string definition for message of type 'GetCurrentImage-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentImage-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentImage-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentImage-request
))
;//! \htmlinclude GetCurrentImage-response.msg.html

(cl:defclass <GetCurrentImage-response> (roslisp-msg-protocol:ros-message)
  ((current_image
    :reader current_image
    :initarg :current_image
    :type sensor_msgs-msg:Image
    :initform (cl:make-instance 'sensor_msgs-msg:Image)))
)

(cl:defclass GetCurrentImage-response (<GetCurrentImage-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentImage-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentImage-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentImage-response> is deprecated: use moveit_tutorials-srv:GetCurrentImage-response instead.")))

(cl:ensure-generic-function 'current_image-val :lambda-list '(m))
(cl:defmethod current_image-val ((m <GetCurrentImage-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader moveit_tutorials-srv:current_image-val is deprecated.  Use moveit_tutorials-srv:current_image instead.")
  (current_image m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentImage-response>) ostream)
  "Serializes a message object of type '<GetCurrentImage-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'current_image) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentImage-response>) istream)
  "Deserializes a message object of type '<GetCurrentImage-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'current_image) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentImage-response>)))
  "Returns string type for a service object of type '<GetCurrentImage-response>"
  "moveit_tutorials/GetCurrentImageResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentImage-response)))
  "Returns string type for a service object of type 'GetCurrentImage-response"
  "moveit_tutorials/GetCurrentImageResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentImage-response>)))
  "Returns md5sum for a message object of type '<GetCurrentImage-response>"
  "cb21fca2e1d6a2c2ac7fcf25b60e6837")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentImage-response)))
  "Returns md5sum for a message object of type 'GetCurrentImage-response"
  "cb21fca2e1d6a2c2ac7fcf25b60e6837")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentImage-response>)))
  "Returns full string definition for message of type '<GetCurrentImage-response>"
  (cl:format cl:nil "sensor_msgs/Image current_image~%~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentImage-response)))
  "Returns full string definition for message of type 'GetCurrentImage-response"
  (cl:format cl:nil "sensor_msgs/Image current_image~%~%================================================================================~%MSG: sensor_msgs/Image~%# This message contains an uncompressed image~%# (0, 0) is at top-left corner of image~%#~%~%Header header        # Header timestamp should be acquisition time of image~%                     # Header frame_id should be optical frame of camera~%                     # origin of frame should be optical center of camera~%                     # +x should point to the right in the image~%                     # +y should point down in the image~%                     # +z should point into to plane of the image~%                     # If the frame_id here and the frame_id of the CameraInfo~%                     # message associated with the image conflict~%                     # the behavior is undefined~%~%uint32 height         # image height, that is, number of rows~%uint32 width          # image width, that is, number of columns~%~%# The legal values for encoding are in file src/image_encodings.cpp~%# If you want to standardize a new string format, join~%# ros-users@lists.sourceforge.net and send an email proposing a new encoding.~%~%string encoding       # Encoding of pixels -- channel meaning, ordering, size~%                      # taken from the list of strings in include/sensor_msgs/image_encodings.h~%~%uint8 is_bigendian    # is this data bigendian?~%uint32 step           # Full row length in bytes~%uint8[] data          # actual matrix data, size is (step * rows)~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentImage-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'current_image))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentImage-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentImage-response
    (cl:cons ':current_image (current_image msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetCurrentImage)))
  'GetCurrentImage-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetCurrentImage)))
  'GetCurrentImage-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentImage)))
  "Returns string type for a service object of type '<GetCurrentImage>"
  "moveit_tutorials/GetCurrentImage")