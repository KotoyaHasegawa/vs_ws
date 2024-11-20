; Auto-generated. Do not edit!


(cl:in-package moveit_tutorials-srv)


;//! \htmlinclude GetCurrentCount-request.msg.html

(cl:defclass <GetCurrentCount-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass GetCurrentCount-request (<GetCurrentCount-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentCount-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentCount-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentCount-request> is deprecated: use moveit_tutorials-srv:GetCurrentCount-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentCount-request>) ostream)
  "Serializes a message object of type '<GetCurrentCount-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentCount-request>) istream)
  "Deserializes a message object of type '<GetCurrentCount-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentCount-request>)))
  "Returns string type for a service object of type '<GetCurrentCount-request>"
  "moveit_tutorials/GetCurrentCountRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentCount-request)))
  "Returns string type for a service object of type 'GetCurrentCount-request"
  "moveit_tutorials/GetCurrentCountRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentCount-request>)))
  "Returns md5sum for a message object of type '<GetCurrentCount-request>"
  "602d642babe509c7c59f497c23e716a9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentCount-request)))
  "Returns md5sum for a message object of type 'GetCurrentCount-request"
  "602d642babe509c7c59f497c23e716a9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentCount-request>)))
  "Returns full string definition for message of type '<GetCurrentCount-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentCount-request)))
  "Returns full string definition for message of type 'GetCurrentCount-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentCount-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentCount-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentCount-request
))
;//! \htmlinclude GetCurrentCount-response.msg.html

(cl:defclass <GetCurrentCount-response> (roslisp-msg-protocol:ros-message)
  ((count
    :reader count
    :initarg :count
    :type cl:integer
    :initform 0))
)

(cl:defclass GetCurrentCount-response (<GetCurrentCount-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetCurrentCount-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetCurrentCount-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-srv:<GetCurrentCount-response> is deprecated: use moveit_tutorials-srv:GetCurrentCount-response instead.")))

(cl:ensure-generic-function 'count-val :lambda-list '(m))
(cl:defmethod count-val ((m <GetCurrentCount-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader moveit_tutorials-srv:count-val is deprecated.  Use moveit_tutorials-srv:count instead.")
  (count m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetCurrentCount-response>) ostream)
  "Serializes a message object of type '<GetCurrentCount-response>"
  (cl:let* ((signed (cl:slot-value msg 'count)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetCurrentCount-response>) istream)
  "Deserializes a message object of type '<GetCurrentCount-response>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'count) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetCurrentCount-response>)))
  "Returns string type for a service object of type '<GetCurrentCount-response>"
  "moveit_tutorials/GetCurrentCountResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentCount-response)))
  "Returns string type for a service object of type 'GetCurrentCount-response"
  "moveit_tutorials/GetCurrentCountResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetCurrentCount-response>)))
  "Returns md5sum for a message object of type '<GetCurrentCount-response>"
  "602d642babe509c7c59f497c23e716a9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetCurrentCount-response)))
  "Returns md5sum for a message object of type 'GetCurrentCount-response"
  "602d642babe509c7c59f497c23e716a9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetCurrentCount-response>)))
  "Returns full string definition for message of type '<GetCurrentCount-response>"
  (cl:format cl:nil "int32 count~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetCurrentCount-response)))
  "Returns full string definition for message of type 'GetCurrentCount-response"
  (cl:format cl:nil "int32 count~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetCurrentCount-response>))
  (cl:+ 0
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetCurrentCount-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetCurrentCount-response
    (cl:cons ':count (count msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetCurrentCount)))
  'GetCurrentCount-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetCurrentCount)))
  'GetCurrentCount-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetCurrentCount)))
  "Returns string type for a service object of type '<GetCurrentCount>"
  "moveit_tutorials/GetCurrentCount")