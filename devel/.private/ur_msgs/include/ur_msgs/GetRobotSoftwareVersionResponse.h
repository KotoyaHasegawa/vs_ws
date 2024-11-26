// Generated by gencpp from file ur_msgs/GetRobotSoftwareVersionResponse.msg
// DO NOT EDIT!


#ifndef UR_MSGS_MESSAGE_GETROBOTSOFTWAREVERSIONRESPONSE_H
#define UR_MSGS_MESSAGE_GETROBOTSOFTWAREVERSIONRESPONSE_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace ur_msgs
{
template <class ContainerAllocator>
struct GetRobotSoftwareVersionResponse_
{
  typedef GetRobotSoftwareVersionResponse_<ContainerAllocator> Type;

  GetRobotSoftwareVersionResponse_()
    : major(0)
    , minor(0)
    , bugfix(0)
    , build(0)  {
    }
  GetRobotSoftwareVersionResponse_(const ContainerAllocator& _alloc)
    : major(0)
    , minor(0)
    , bugfix(0)
    , build(0)  {
  (void)_alloc;
    }



   typedef uint32_t _major_type;
  _major_type major;

   typedef uint32_t _minor_type;
  _minor_type minor;

   typedef uint32_t _bugfix_type;
  _bugfix_type bugfix;

   typedef uint32_t _build_type;
  _build_type build;





  typedef boost::shared_ptr< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> const> ConstPtr;

}; // struct GetRobotSoftwareVersionResponse_

typedef ::ur_msgs::GetRobotSoftwareVersionResponse_<std::allocator<void> > GetRobotSoftwareVersionResponse;

typedef boost::shared_ptr< ::ur_msgs::GetRobotSoftwareVersionResponse > GetRobotSoftwareVersionResponsePtr;
typedef boost::shared_ptr< ::ur_msgs::GetRobotSoftwareVersionResponse const> GetRobotSoftwareVersionResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator1> & lhs, const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator2> & rhs)
{
  return lhs.major == rhs.major &&
    lhs.minor == rhs.minor &&
    lhs.bugfix == rhs.bugfix &&
    lhs.build == rhs.build;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator1> & lhs, const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace ur_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "eea0f1664f7955042558cb2bf2c766ad";
  }

  static const char* value(const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xeea0f1664f795504ULL;
  static const uint64_t static_value2 = 0x2558cb2bf2c766adULL;
};

template<class ContainerAllocator>
struct DataType< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "ur_msgs/GetRobotSoftwareVersionResponse";
  }

  static const char* value(const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "uint32 major    # Major version number\n"
"uint32 minor    # Minor version number\n"
"uint32 bugfix   # Bugfix version number\n"
"uint32 build    # Build number\n"
"\n"
;
  }

  static const char* value(const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.major);
      stream.next(m.minor);
      stream.next(m.bugfix);
      stream.next(m.build);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GetRobotSoftwareVersionResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::ur_msgs::GetRobotSoftwareVersionResponse_<ContainerAllocator>& v)
  {
    s << indent << "major: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.major);
    s << indent << "minor: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.minor);
    s << indent << "bugfix: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.bugfix);
    s << indent << "build: ";
    Printer<uint32_t>::stream(s, indent + "  ", v.build);
  }
};

} // namespace message_operations
} // namespace ros

#endif // UR_MSGS_MESSAGE_GETROBOTSOFTWAREVERSIONRESPONSE_H
