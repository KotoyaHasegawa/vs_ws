;; Auto-generated. Do not edit!


(when (boundp 'moveit_tutorials::GetCurrentCount)
  (if (not (find-package "MOVEIT_TUTORIALS"))
    (make-package "MOVEIT_TUTORIALS"))
  (shadow 'GetCurrentCount (find-package "MOVEIT_TUTORIALS")))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTCOUNT")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTCOUNT"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTCOUNTREQUEST")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTCOUNTREQUEST"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTCOUNTRESPONSE")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTCOUNTRESPONSE"))

(in-package "ROS")





(defclass moveit_tutorials::GetCurrentCountRequest
  :super ros::object
  :slots ())

(defmethod moveit_tutorials::GetCurrentCountRequest
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

(defclass moveit_tutorials::GetCurrentCountResponse
  :super ros::object
  :slots (_count ))

(defmethod moveit_tutorials::GetCurrentCountResponse
  (:init
   (&key
    ((:count __count) 0)
    )
   (send-super :init)
   (setq _count (round __count))
   self)
  (:count
   (&optional __count)
   (if __count (setq _count __count)) _count)
  (:serialization-length
   ()
   (+
    ;; int32 _count
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _count
       (write-long _count s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _count
     (setq _count (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(defclass moveit_tutorials::GetCurrentCount
  :super ros::object
  :slots ())

(setf (get moveit_tutorials::GetCurrentCount :md5sum-) "602d642babe509c7c59f497c23e716a9")
(setf (get moveit_tutorials::GetCurrentCount :datatype-) "moveit_tutorials/GetCurrentCount")
(setf (get moveit_tutorials::GetCurrentCount :request) moveit_tutorials::GetCurrentCountRequest)
(setf (get moveit_tutorials::GetCurrentCount :response) moveit_tutorials::GetCurrentCountResponse)

(defmethod moveit_tutorials::GetCurrentCountRequest
  (:response () (instance moveit_tutorials::GetCurrentCountResponse :init)))

(setf (get moveit_tutorials::GetCurrentCountRequest :md5sum-) "602d642babe509c7c59f497c23e716a9")
(setf (get moveit_tutorials::GetCurrentCountRequest :datatype-) "moveit_tutorials/GetCurrentCountRequest")
(setf (get moveit_tutorials::GetCurrentCountRequest :definition-)
      "---
int32 count
")

(setf (get moveit_tutorials::GetCurrentCountResponse :md5sum-) "602d642babe509c7c59f497c23e716a9")
(setf (get moveit_tutorials::GetCurrentCountResponse :datatype-) "moveit_tutorials/GetCurrentCountResponse")
(setf (get moveit_tutorials::GetCurrentCountResponse :definition-)
      "---
int32 count
")



(provide :moveit_tutorials/GetCurrentCount "602d642babe509c7c59f497c23e716a9")


