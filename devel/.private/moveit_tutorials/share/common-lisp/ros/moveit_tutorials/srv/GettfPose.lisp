; Auto-generated. Do not edit!


(cl:in-package moveit_tutorials-srv)


;//! \htmlinclude GettfPose-request.msg.html

(cl:defclass <GettfPose-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass GettfPose-request (<GettfPose-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GettfPose-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GettfPose-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GettfPose-request> is deprecated: use moveit_tutorials-srv:GettfPose-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GettfPose-request>) ostream)
  "Serializes a message object of type '<GettfPose-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GettfPose-request>) istream)
  "Deserializes a message object of type '<GettfPose-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GettfPose-request>)))
  "Returns string type for a service object of type '<GettfPose-request>"
  "moveit_tutorials/GettfPoseRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GettfPose-request)))
  "Returns string type for a service object of type 'GettfPose-request"
  "moveit_tutorials/GettfPoseRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GettfPose-request>)))
  "Returns md5sum for a message object of type '<GettfPose-request>"
  "a4fcab672ea64ead4d870b0730e4c129")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GettfPose-request)))
  "Returns md5sum for a message object of type 'GettfPose-request"
  "a4fcab672ea64ead4d870b0730e4c129")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GettfPose-request>)))
  "Returns full string definition for message of type '<GettfPose-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GettfPose-request)))
  "Returns full string definition for message of type 'GettfPose-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GettfPose-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GettfPose-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GettfPose-request
))
;//! \htmlinclude GettfPose-response.msg.html

(cl:defclass <GettfPose-response> (roslisp-msg-protocol:ros-message)
  ((trans
    :reader trans
    :initarg :trans
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0))
   (rot
    :reader rot
    :initarg :rot
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass GettfPose-response (<GettfPose-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GettfPose-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GettfPose-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GettfPose-response> is deprecated: use moveit_tutorials-srv:GettfPose-response instead.")))

(cl:ensure-generic-function 'trans-val :lambda-list '(m))
(cl:defmethod trans-val ((m <GettfPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader moveit_tutorials-srv:trans-val is deprecated.  Use moveit_tutorials-srv:trans instead.")
  (trans m))

(cl:ensure-generic-function 'rot-val :lambda-list '(m))
(cl:defmethod rot-val ((m <GettfPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader moveit_tutorials-srv:rot-val is deprecated.  Use moveit_tutorials-srv:rot instead.")
  (rot m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GettfPose-response>) ostream)
  "Serializes a message object of type '<GettfPose-response>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'trans))))
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
   (cl:slot-value msg 'trans))
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'rot))))
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
   (cl:slot-value msg 'rot))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GettfPose-response>) istream)
  "Deserializes a message object of type '<GettfPose-response>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'trans) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'trans)))
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
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'rot) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'rot)))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GettfPose-response>)))
  "Returns string type for a service object of type '<GettfPose-response>"
  "moveit_tutorials/GettfPoseResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GettfPose-response)))
  "Returns string type for a service object of type 'GettfPose-response"
  "moveit_tutorials/GettfPoseResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GettfPose-response>)))
  "Returns md5sum for a message object of type '<GettfPose-response>"
  "a4fcab672ea64ead4d870b0730e4c129")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GettfPose-response)))
  "Returns md5sum for a message object of type 'GettfPose-response"
  "a4fcab672ea64ead4d870b0730e4c129")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GettfPose-response>)))
  "Returns full string definition for message of type '<GettfPose-response>"
  (cl:format cl:nil "float64[] trans~%float64[] rot~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GettfPose-response)))
  "Returns full string definition for message of type 'GettfPose-response"
  (cl:format cl:nil "float64[] trans~%float64[] rot~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GettfPose-response>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'trans) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'rot) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GettfPose-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GettfPose-response
    (cl:cons ':trans (trans msg))
    (cl:cons ':rot (rot msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GettfPose)))
  'GettfPose-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GettfPose)))
  'GettfPose-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GettfPose)))
  "Returns string type for a service object of type '<GettfPose>"
  "moveit_tutorials/GettfPose")