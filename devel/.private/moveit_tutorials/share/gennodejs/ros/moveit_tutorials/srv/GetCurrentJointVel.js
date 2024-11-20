// Auto-generated. Do not edit!

// (in-package moveit_tutorials.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------


//-----------------------------------------------------------

class GetCurrentJointVelRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
    }
    else {
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetCurrentJointVelRequest
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetCurrentJointVelRequest
    let len;
    let data = new GetCurrentJointVelRequest(null);
    return data;
  }

  static getMessageSize(object) {
    return 0;
  }

  static datatype() {
    // Returns string type for a service object
    return 'moveit_tutorials/GetCurrentJointVelRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'd41d8cd98f00b204e9800998ecf8427e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetCurrentJointVelRequest(null);
    return resolved;
    }
};

class GetCurrentJointVelResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.current_joint_vel = null;
    }
    else {
      if (initObj.hasOwnProperty('current_joint_vel')) {
        this.current_joint_vel = initObj.current_joint_vel
      }
      else {
        this.current_joint_vel = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetCurrentJointVelResponse
    // Serialize message field [current_joint_vel]
    bufferOffset = _arraySerializer.float64(obj.current_joint_vel, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetCurrentJointVelResponse
    let len;
    let data = new GetCurrentJointVelResponse(null);
    // Deserialize message field [current_joint_vel]
    data.current_joint_vel = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.current_joint_vel.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'moveit_tutorials/GetCurrentJointVelResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '1d32d78f4d7ef4d386bfa163951babe5';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] current_joint_vel
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetCurrentJointVelResponse(null);
    if (msg.current_joint_vel !== undefined) {
      resolved.current_joint_vel = msg.current_joint_vel;
    }
    else {
      resolved.current_joint_vel = []
    }

    return resolved;
    }
};

module.exports = {
  Request: GetCurrentJointVelRequest,
  Response: GetCurrentJointVelResponse,
  md5sum() { return '1d32d78f4d7ef4d386bfa163951babe5'; },
  datatype() { return 'moveit_tutorials/GetCurrentJointVel'; }
};
