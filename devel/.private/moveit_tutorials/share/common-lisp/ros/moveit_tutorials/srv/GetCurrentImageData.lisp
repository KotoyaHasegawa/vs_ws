; Auto-generated. Do not edit!


(cl:in-package moveit_tutorials-srv)


;//! \htmlinclude GetCurrentImageData-request.msg.html

(cl:defclass <GetCurrentImageData-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass GetCurrentImageData-request (<GetCurrentImageData-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentImageData-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentImageData-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentImageData-request> is deprecated: use moveit_tutorials-srv:GetCurrentImageData-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentImageData-request>) ostream)
  "Serializes a message object of type '<GetCurrentImageData-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentImageData-request>) istream)
  "Deserializes a message object of type '<GetCurrentImageData-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentImageData-request>)))
  "Returns string type for a service object of type '<GetCurrentImageData-request>"
  "moveit_tutorials/GetCurrentImageDataRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentImageData-request)))
  "Returns string type for a service object of type 'GetCurrentImageData-request"
  "moveit_tutorials/GetCurrentImageDataRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentImageData-request>)))
  "Returns md5sum for a message object of type '<GetCurrentImageData-request>"
  "06552b34b97c1365790de0d089ef0bec")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentImageData-request)))
  "Returns md5sum for a message object of type 'GetCurrentImageData-request"
  "06552b34b97c1365790de0d089ef0bec")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentImageData-request>)))
  "Returns full string definition for message of type '<GetCurrentImageData-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentImageData-request)))
  "Returns full string definition for message of type 'GetCurrentImageData-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentImageData-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentImageData-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentImageData-request
))
;//! \htmlinclude GetCurrentImageData-response.msg.html

(cl:defclass <GetCurrentImageData-response> (roslisp-msg-protocol:ros-message)
  ((current_image
    :reader current_image
    :initarg :current_image
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass GetCurrentImageData-response (<GetCurrentImageData-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentImageData-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentImageData-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentImageData-response> is deprecated: use moveit_tutorials-srv:GetCurrentImageData-response instead.")))

(cl:ensure-generic-function 'current_image-val :lambda-list '(m))
(cl:defmethod current_image-val ((m <GetCurrentImageData-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader moveit_tutorials-srv:current_image-val is deprecated.  Use moveit_tutorials-srv:current_image instead.")
  (current_image m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentImageData-response>) ostream)
  "Serializes a message object of type '<GetCurrentImageData-response>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'current_image))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'current_image))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentImageData-response>) istream)
  "Deserializes a message object of type '<GetCurrentImageData-response>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'current_image) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'current_image)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentImageData-response>)))
  "Returns string type for a service object of type '<GetCurrentImageData-response>"
  "moveit_tutorials/GetCurrentImageDataResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentImageData-response)))
  "Returns string type for a service object of type 'GetCurrentImageData-response"
  "moveit_tutorials/GetCurrentImageDataResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentImageData-response>)))
  "Returns md5sum for a message object of type '<GetCurrentImageData-response>"
  "06552b34b97c1365790de0d089ef0bec")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentImageData-response)))
  "Returns md5sum for a message object of type 'GetCurrentImageData-response"
  "06552b34b97c1365790de0d089ef0bec")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentImageData-response>)))
  "Returns full string definition for message of type '<GetCurrentImageData-response>"
  (cl:format cl:nil "float32[] current_image~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentImageData-response)))
  "Returns full string definition for message of type 'GetCurrentImageData-response"
  (cl:format cl:nil "float32[] current_image~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentImageData-response>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'current_image) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentImageData-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentImageData-response
    (cl:cons ':current_image (current_image msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetCurrentImageData)))
  'GetCurrentImageData-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetCurrentImageData)))
  'GetCurrentImageData-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentImageData)))
  "Returns string type for a service object of type '<GetCurrentImageData>"
  "moveit_tutorials/GetCurrentImageData")