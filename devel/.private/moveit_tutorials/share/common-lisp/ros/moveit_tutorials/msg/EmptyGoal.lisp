; Auto-generated. Do not edit!


(cl:in-package moveit_tutorials-msg)


;//! \htmlinclude EmptyGoal.msg.html

(cl:defclass <EmptyGoal> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass EmptyGoal (<EmptyGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <EmptyGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'EmptyGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name moveit_tutorials-msg:<EmptyGoal> is deprecated: use moveit_tutorials-msg:EmptyGoal instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <EmptyGoal>) ostream)
  "Serializes a message object of type '<EmptyGoal>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <EmptyGoal>) istream)
  "Deserializes a message object of type '<EmptyGoal>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<EmptyGoal>)))
  "Returns string type for a message object of type '<EmptyGoal>"
  "moveit_tutorials/EmptyGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'EmptyGoal)))
  "Returns string type for a message object of type 'EmptyGoal"
  "moveit_tutorials/EmptyGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<EmptyGoal>)))
  "Returns md5sum for a message object of type '<EmptyGoal>"
  "d41d8cd98f00b204e9800998ecf8427e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'EmptyGoal)))
  "Returns md5sum for a message object of type 'EmptyGoal"
  "d41d8cd98f00b204e9800998ecf8427e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<EmptyGoal>)))
  "Returns full string definition for message of type '<EmptyGoal>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'EmptyGoal)))
  "Returns full string definition for message of type 'EmptyGoal"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <EmptyGoal>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <EmptyGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'EmptyGoal
))