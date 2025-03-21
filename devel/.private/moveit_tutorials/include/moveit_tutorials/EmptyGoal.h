// Generated by gencpp from file moveit_tutorials/EmptyGoal.msg
// DO NOT EDIT!


#ifndef MOVEIT_TUTORIALS_MESSAGE_EMPTYGOAL_H
#define MOVEIT_TUTORIALS_MESSAGE_EMPTYGOAL_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace moveit_tutorials
{
template <class ContainerAllocator>
struct EmptyGoal_
{
  typedef EmptyGoal_<ContainerAllocator> Type;

  EmptyGoal_()
    {
    }
  EmptyGoal_(const ContainerAllocator& _alloc)
    {
  (void)_alloc;
    }







  typedef boost::shared_ptr< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> const> ConstPtr;

}; // struct EmptyGoal_

typedef ::moveit_tutorials::EmptyGoal_<std::allocator<void> > EmptyGoal;

typedef boost::shared_ptr< ::moveit_tutorials::EmptyGoal > EmptyGoalPtr;
typedef boost::shared_ptr< ::moveit_tutorials::EmptyGoal const> EmptyGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::moveit_tutorials::EmptyGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}


} // namespace moveit_tutorials

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const ::moveit_tutorials::EmptyGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd41d8cd98f00b204ULL;
  static const uint64_t static_value2 = 0xe9800998ecf8427eULL;
};

template<class ContainerAllocator>
struct DataType< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "moveit_tutorials/EmptyGoal";
  }

  static const char* value(const ::moveit_tutorials::EmptyGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
;
  }

  static const char* value(const ::moveit_tutorials::EmptyGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream&, T)
    {}

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct EmptyGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::moveit_tutorials::EmptyGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream&, const std::string&, const ::moveit_tutorials::EmptyGoal_<ContainerAllocator>&)
  {}
};

} // namespace message_operations
} // namespace ros

#endif // MOVEIT_TUTORIALS_MESSAGE_EMPTYGOAL_H
