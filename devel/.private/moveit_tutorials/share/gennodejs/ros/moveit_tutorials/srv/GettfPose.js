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

class GettfPoseRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
    }
    else {
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GettfPoseRequest
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GettfPoseRequest
    let len;
    let data = new GettfPoseRequest(null);
    return data;
  }

  static getMessageSize(object) {
    return 0;
  }

  static datatype() {
    // Returns string type for a service object
    return 'moveit_tutorials/GettfPoseRequest';
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
    const resolved = new GettfPoseRequest(null);
    return resolved;
    }
};

class GettfPoseResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.trans = null;
      this.rot = null;
    }
    else {
      if (initObj.hasOwnProperty('trans')) {
        this.trans = initObj.trans
      }
      else {
        this.trans = [];
      }
      if (initObj.hasOwnProperty('rot')) {
        this.rot = initObj.rot
      }
      else {
        this.rot = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GettfPoseResponse
    // Serialize message field [trans]
    bufferOffset = _arraySerializer.float64(obj.trans, buffer, bufferOffset, null);
    // Serialize message field [rot]
    bufferOffset = _arraySerializer.float64(obj.rot, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GettfPoseResponse
    let len;
    let data = new GettfPoseResponse(null);
    // Deserialize message field [trans]
    data.trans = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [rot]
    data.rot = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.trans.length;
    length += 8 * object.rot.length;
    return length + 8;
  }

  static datatype() {
    // Returns string type for a service object
    return 'moveit_tutorials/GettfPoseResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'a4fcab672ea64ead4d870b0730e4c129';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64[] trans
    float64[] rot
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GettfPoseResponse(null);
    if (msg.trans !== undefined) {
      resolved.trans = msg.trans;
    }
    else {
      resolved.trans = []
    }

    if (msg.rot !== undefined) {
      resolved.rot = msg.rot;
    }
    else {
      resolved.rot = []
    }

    return resolved;
    }
};

module.exports = {
  Request: GettfPoseRequest,
  Response: GettfPoseResponse,
  md5sum() { return 'a4fcab672ea64ead4d870b0730e4c129'; },
  datatype() { return 'moveit_tutorials/GettfPose'; }
};
