;; Auto-generated. Do not edit!


(when (boundp 'moveit_tutorials::GetCurrentJointVel)
  (if (not (find-package "MOVEIT_TUTORIALS"))
    (make-package "MOVEIT_TUTORIALS"))
  (shadow 'GetCurrentJointVel (find-package "MOVEIT_TUTORIALS")))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTJOINTVEL")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTJOINTVEL"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTJOINTVELREQUEST")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTJOINTVELREQUEST"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTJOINTVELRESPONSE")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTJOINTVELRESPONSE"))

(in-package "ROS")





(defclass moveit_tutorials::GetCurrentJointVelRequest
  :super ros::object
  :slots ())

(defmethod moveit_tutorials::GetCurrentJointVelRequest
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

(defclass moveit_tutorials::GetCurrentJointVelResponse
  :super ros::object
  :slots (_current_joint_vel ))

(defmethod moveit_tutorials::GetCurrentJointVelResponse
  (:init
   (&key
    ((:current_joint_vel __current_joint_vel) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _current_joint_vel __current_joint_vel)
   self)
  (:current_joint_vel
   (&optional __current_joint_vel)
   (if __current_joint_vel (setq _current_joint_vel __current_joint_vel)) _current_joint_vel)
  (:serialization-length
   ()
   (+
    ;; float64[] _current_joint_vel
    (* 8    (length _current_joint_vel)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _current_joint_vel
     (write-long (length _current_joint_vel) s)
     (dotimes (i (length _current_joint_vel))
       (sys::poke (elt _current_joint_vel i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _current_joint_vel
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _current_joint_vel (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _current_joint_vel i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(defclass moveit_tutorials::GetCurrentJointVel
  :super ros::object
  :slots ())

(setf (get moveit_tutorials::GetCurrentJointVel :md5sum-) "1d32d78f4d7ef4d386bfa163951babe5")
(setf (get moveit_tutorials::GetCurrentJointVel :datatype-) "moveit_tutorials/GetCurrentJointVel")
(setf (get moveit_tutorials::GetCurrentJointVel :request) moveit_tutorials::GetCurrentJointVelRequest)
(setf (get moveit_tutorials::GetCurrentJointVel :response) moveit_tutorials::GetCurrentJointVelResponse)

(defmethod moveit_tutorials::GetCurrentJointVelRequest
  (:response () (instance moveit_tutorials::GetCurrentJointVelResponse :init)))

(setf (get moveit_tutorials::GetCurrentJointVelRequest :md5sum-) "1d32d78f4d7ef4d386bfa163951babe5")
(setf (get moveit_tutorials::GetCurrentJointVelRequest :datatype-) "moveit_tutorials/GetCurrentJointVelRequest")
(setf (get moveit_tutorials::GetCurrentJointVelRequest :definition-)
      "---
float64[] current_joint_vel
")

(setf (get moveit_tutorials::GetCurrentJointVelResponse :md5sum-) "1d32d78f4d7ef4d386bfa163951babe5")
(setf (get moveit_tutorials::GetCurrentJointVelResponse :datatype-) "moveit_tutorials/GetCurrentJointVelResponse")
(setf (get moveit_tutorials::GetCurrentJointVelResponse :definition-)
      "---
float64[] current_joint_vel
")



(provide :moveit_tutorials/GetCurrentJointVel "1d32d78f4d7ef4d386bfa163951babe5")


