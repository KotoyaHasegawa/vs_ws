// Generated by gencpp from file moveit_tutorials/GetCurrentCount.msg
// DO NOT EDIT!


#ifndef MOVEIT_TUTORIALS_MESSAGE_GETCURRENTCOUNT_H
#define MOVEIT_TUTORIALS_MESSAGE_GETCURRENTCOUNT_H

#include <ros/service_traits.h>


#include <moveit_tutorials/GetCurrentCountRequest.h>
#include <moveit_tutorials/GetCurrentCountResponse.h>


namespace moveit_tutorials
{

struct GetCurrentCount
{

typedef GetCurrentCountRequest Request;
typedef GetCurrentCountResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct GetCurrentCount
} // namespace moveit_tutorials


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::moveit_tutorials::GetCurrentCount > {
  static const char* value()
  {
    return "602d642babe509c7c59f497c23e716a9";
  }

  static const char* value(const ::moveit_tutorials::GetCurrentCount&) { return value(); }
};

template<>
struct DataType< ::moveit_tutorials::GetCurrentCount > {
  static const char* value()
  {
    return "moveit_tutorials/GetCurrentCount";
  }

  static const char* value(const ::moveit_tutorials::GetCurrentCount&) { return value(); }
};


// service_traits::MD5Sum< ::moveit_tutorials::GetCurrentCountRequest> should match
// service_traits::MD5Sum< ::moveit_tutorials::GetCurrentCount >
template<>
struct MD5Sum< ::moveit_tutorials::GetCurrentCountRequest>
{
  static const char* value()
  {
    return MD5Sum< ::moveit_tutorials::GetCurrentCount >::value();
  }
  static const char* value(const ::moveit_tutorials::GetCurrentCountRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::moveit_tutorials::GetCurrentCountRequest> should match
// service_traits::DataType< ::moveit_tutorials::GetCurrentCount >
template<>
struct DataType< ::moveit_tutorials::GetCurrentCountRequest>
{
  static const char* value()
  {
    return DataType< ::moveit_tutorials::GetCurrentCount >::value();
  }
  static const char* value(const ::moveit_tutorials::GetCurrentCountRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::moveit_tutorials::GetCurrentCountResponse> should match
// service_traits::MD5Sum< ::moveit_tutorials::GetCurrentCount >
template<>
struct MD5Sum< ::moveit_tutorials::GetCurrentCountResponse>
{
  static const char* value()
  {
    return MD5Sum< ::moveit_tutorials::GetCurrentCount >::value();
  }
  static const char* value(const ::moveit_tutorials::GetCurrentCountResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::moveit_tutorials::GetCurrentCountResponse> should match
// service_traits::DataType< ::moveit_tutorials::GetCurrentCount >
template<>
struct DataType< ::moveit_tutorials::GetCurrentCountResponse>
{
  static const char* value()
  {
    return DataType< ::moveit_tutorials::GetCurrentCount >::value();
  }
  static const char* value(const ::moveit_tutorials::GetCurrentCountResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // MOVEIT_TUTORIALS_MESSAGE_GETCURRENTCOUNT_H