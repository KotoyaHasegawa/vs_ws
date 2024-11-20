
(cl:in-package :asdf)

(defsystem "moveit_tutorials-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :sensor_msgs-msg
)
  :components ((:file "_package")
    (:file "GetCurrentCount" :depends-on ("_package_GetCurrentCount"))
    (:file "_package_GetCurrentCount" :depends-on ("_package"))
    (:file "GetCurrentImage" :depends-on ("_package_GetCurrentImage"))
    (:file "_package_GetCurrentImage" :depends-on ("_package"))
    (:file "GetCurrentImageData" :depends-on ("_package_GetCurrentImageData"))
    (:file "_package_GetCurrentImageData" :depends-on ("_package"))
    (:file "GetCurrentJointVel" :depends-on ("_package_GetCurrentJointVel"))
    (:file "_package_GetCurrentJointVel" :depends-on ("_package"))
    (:file "GettfPose" :depends-on ("_package_GettfPose"))
    (:file "_package_GettfPose" :depends-on ("_package"))
  ))