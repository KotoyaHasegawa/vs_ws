; Auto-generated. Do not edit!


(cl:in-package moveit_tutorials-srv)


;//! \htmlinclude GetCurrentJointVel-request.msg.html

(cl:defclass <GetCurrentJointVel-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass GetCurrentJointVel-request (<GetCurrentJointVel-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentJointVel-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentJointVel-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentJointVel-request> is deprecated: use moveit_tutorials-srv:GetCurrentJointVel-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentJointVel-request>) ostream)
  "Serializes a message object of type '<GetCurrentJointVel-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentJointVel-request>) istream)
  "Deserializes a message object of type '<GetCurrentJointVel-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentJointVel-request>)))
  "Returns string type for a service object of type '<GetCurrentJointVel-request>"
  "moveit_tutorials/GetCurrentJointVelRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentJointVel-request)))
  "Returns string type for a service object of type 'GetCurrentJointVel-request"
  "moveit_tutorials/GetCurrentJointVelRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentJointVel-request>)))
  "Returns md5sum for a message object of type '<GetCurrentJointVel-request>"
  "1d32d78f4d7ef4d386bfa163951babe5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentJointVel-request)))
  "Returns md5sum for a message object of type 'GetCurrentJointVel-request"
  "1d32d78f4d7ef4d386bfa163951babe5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentJointVel-request>)))
  "Returns full string definition for message of type '<GetCurrentJointVel-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentJointVel-request)))
  "Returns full string definition for message of type 'GetCurrentJointVel-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentJointVel-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentJointVel-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentJointVel-request
))
;//! \htmlinclude GetCurrentJointVel-response.msg.html

(cl:defclass <GetCurrentJointVel-response> (roslisp-msg-protocol:ros-message)
  ((current_joint_vel
    :reader current_joint_vel
    :initarg :current_joint_vel
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass GetCurrentJointVel-response (<GetCurrentJointVel-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentJointVel-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentJointVel-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentJointVel-response> is deprecated: use moveit_tutorials-srv:GetCurrentJointVel-response instead.")))

(cl:ensure-generic-function 'current_joint_vel-val :lambda-list '(m))
(cl:defmethod current_joint_vel-val ((m <GetCurrentJointVel-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader moveit_tutorials-srv:current_joint_vel-val is deprecated.  Use moveit_tutorials-srv:current_joint_vel instead.")
  (current_joint_vel m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentJointVel-response>) ostream)
  "Serializes a message object of type '<GetCurrentJointVel-response>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'current_joint_vel))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'current_joint_vel))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentJointVel-response>) istream)
  "Deserializes a message object of type '<GetCurrentJointVel-response>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'current_joint_vel) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'current_joint_vel)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentJointVel-response>)))
  "Returns string type for a service object of type '<GetCurrentJointVel-response>"
  "moveit_tutorials/GetCurrentJointVelResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentJointVel-response)))
  "Returns string type for a service object of type 'GetCurrentJointVel-response"
  "moveit_tutorials/GetCurrentJointVelResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentJointVel-response>)))
  "Returns md5sum for a message object of type '<GetCurrentJointVel-response>"
  "1d32d78f4d7ef4d386bfa163951babe5")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentJointVel-response)))
  "Returns md5sum for a message object of type 'GetCurrentJointVel-response"
  "1d32d78f4d7ef4d386bfa163951babe5")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentJointVel-response>)))
  "Returns full string definition for message of type '<GetCurrentJointVel-response>"
  (cl:format cl:nil "float64[] current_joint_vel~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentJointVel-response)))
  "Returns full string definition for message of type 'GetCurrentJointVel-response"
  (cl:format cl:nil "float64[] current_joint_vel~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentJointVel-response>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'current_joint_vel) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentJointVel-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentJointVel-response
    (cl:cons ':current_joint_vel (current_joint_vel msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetCurrentJointVel)))
  'GetCurrentJointVel-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetCurrentJointVel)))
  'GetCurrentJointVel-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentJointVel)))
  "Returns string type for a service object of type '<GetCurrentJointVel>"
  "moveit_tutorials/GetCurrentJointVel")