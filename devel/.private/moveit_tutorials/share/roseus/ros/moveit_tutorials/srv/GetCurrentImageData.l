;; Auto-generated. Do not edit!


(when (boundp 'moveit_tutorials::GetCurrentImageData)
  (if (not (find-package "MOVEIT_TUTORIALS"))
    (make-package "MOVEIT_TUTORIALS"))
  (shadow 'GetCurrentImageData (find-package "MOVEIT_TUTORIALS")))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEDATA")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEDATA"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEDATAREQUEST")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEDATAREQUEST"))
(unless (find-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEDATARESPONSE")
  (make-package "MOVEIT_TUTORIALS::GETCURRENTIMAGEDATARESPONSE"))

(in-package "ROS")





(defclass moveit_tutorials::GetCurrentImageDataRequest
  :super ros::object
  :slots ())

(defmethod moveit_tutorials::GetCurrentImageDataRequest
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

(defclass moveit_tutorials::GetCurrentImageDataResponse
  :super ros::object
  :slots (_current_image ))

(defmethod moveit_tutorials::GetCurrentImageDataResponse
  (:init
   (&key
    ((:current_image __current_image) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _current_image __current_image)
   self)
  (:current_image
   (&optional __current_image)
   (if __current_image (setq _current_image __current_image)) _current_image)
  (:serialization-length
   ()
   (+
    ;; float32[] _current_image
    (* 4    (length _current_image)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32[] _current_image
     (write-long (length _current_image) s)
     (dotimes (i (length _current_image))
       (sys::poke (elt _current_image i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32[] _current_image
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _current_image (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _current_image i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     ))
   ;;
   self)
  )

(defclass moveit_tutorials::GetCurrentImageData
  :super ros::object
  :slots ())

(setf (get moveit_tutorials::GetCurrentImageData :md5sum-) "06552b34b97c1365790de0d089ef0bec")
(setf (get moveit_tutorials::GetCurrentImageData :datatype-) "moveit_tutorials/GetCurrentImageData")
(setf (get moveit_tutorials::GetCurrentImageData :request) moveit_tutorials::GetCurrentImageDataRequest)
(setf (get moveit_tutorials::GetCurrentImageData :response) moveit_tutorials::GetCurrentImageDataResponse)

(defmethod moveit_tutorials::GetCurrentImageDataRequest
  (:response () (instance moveit_tutorials::GetCurrentImageDataResponse :init)))

(setf (get moveit_tutorials::GetCurrentImageDataRequest :md5sum-) "06552b34b97c1365790de0d089ef0bec")
(setf (get moveit_tutorials::GetCurrentImageDataRequest :datatype-) "moveit_tutorials/GetCurrentImageDataRequest")
(setf (get moveit_tutorials::GetCurrentImageDataRequest :definition-)
      "---
float32[] current_image

")

(setf (get moveit_tutorials::GetCurrentImageDataResponse :md5sum-) "06552b34b97c1365790de0d089ef0bec")
(setf (get moveit_tutorials::GetCurrentImageDataResponse :datatype-) "moveit_tutorials/GetCurrentImageDataResponse")
(setf (get moveit_tutorials::GetCurrentImageDataResponse :definition-)
      "---
float32[] current_image

")



(provide :moveit_tutorials/GetCurrentImageData "06552b34b97c1365790de0d089ef0bec")


