;; Auto-generated. Do not edit!


(when (boundp 'moveit_tutorials::GettfPose)
  (if (not (find-package "MOVEIT_TUTORIALS"))
    (make-package "MOVEIT_TUTORIALS"))
  (shadow 'GettfPose (find-package "MOVEIT_TUTORIALS")))
(unless (find-package "MOVEIT_TUTORIALS::GETTFPOSE")
  (make-package "MOVEIT_TUTORIALS::GETTFPOSE"))
(unless (find-package "MOVEIT_TUTORIALS::GETTFPOSEREQUEST")
  (make-package "MOVEIT_TUTORIALS::GETTFPOSEREQUEST"))
(unless (find-package "MOVEIT_TUTORIALS::GETTFPOSERESPONSE")
  (make-package "MOVEIT_TUTORIALS::GETTFPOSERESPONSE"))

(in-package "ROS")





(defclass moveit_tutorials::GettfPoseRequest
  :super ros::object
  :slots ())

(defmethod moveit_tutorials::GettfPoseRequest
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

(defclass moveit_tutorials::GettfPoseResponse
  :super ros::object
  :slots (_trans _rot ))

(defmethod moveit_tutorials::GettfPoseResponse
  (:init
   (&key
    ((:trans __trans) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:rot __rot) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _trans __trans)
   (setq _rot __rot)
   self)
  (:trans
   (&optional __trans)
   (if __trans (setq _trans __trans)) _trans)
  (:rot
   (&optional __rot)
   (if __rot (setq _rot __rot)) _rot)
  (:serialization-length
   ()
   (+
    ;; float64[] _trans
    (* 8    (length _trans)) 4
    ;; float64[] _rot
    (* 8    (length _rot)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _trans
     (write-long (length _trans) s)
     (dotimes (i (length _trans))
       (sys::poke (elt _trans i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _rot
     (write-long (length _rot) s)
     (dotimes (i (length _rot))
       (sys::poke (elt _rot i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _trans
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _trans (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _trans i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _rot
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _rot (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _rot i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(defclass moveit_tutorials::GettfPose
  :super ros::object
  :slots ())

(setf (get moveit_tutorials::GettfPose :md5sum-) "a4fcab672ea64ead4d870b0730e4c129")
(setf (get moveit_tutorials::GettfPose :datatype-) "moveit_tutorials/GettfPose")
(setf (get moveit_tutorials::GettfPose :request) moveit_tutorials::GettfPoseRequest)
(setf (get moveit_tutorials::GettfPose :response) moveit_tutorials::GettfPoseResponse)

(defmethod moveit_tutorials::GettfPoseRequest
  (:response () (instance moveit_tutorials::GettfPoseResponse :init)))

(setf (get moveit_tutorials::GettfPoseRequest :md5sum-) "a4fcab672ea64ead4d870b0730e4c129")
(setf (get moveit_tutorials::GettfPoseRequest :datatype-) "moveit_tutorials/GettfPoseRequest")
(setf (get moveit_tutorials::GettfPoseRequest :definition-)
      "---
float64[] trans
float64[] rot

")

(setf (get moveit_tutorials::GettfPoseResponse :md5sum-) "a4fcab672ea64ead4d870b0730e4c129")
(setf (get moveit_tutorials::GettfPoseResponse :datatype-) "moveit_tutorials/GettfPoseResponse")
(setf (get moveit_tutorials::GettfPoseResponse :definition-)
      "---
float64[] trans
float64[] rot

")



(provide :moveit_tutorials/GettfPose "a4fcab672ea64ead4d870b0730e4c129")


