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

class GetCurrentImageDataRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
    }
    else {
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetCurrentImageDataRequest
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetCurrentImageDataRequest
    let len;
    let data = new GetCurrentImageDataRequest(null);
    return data;
  }

  static getMessageSize(object) {
    return 0;
  }

  static datatype() {
    // Returns string type for a service object
    return 'moveit_tutorials/GetCurrentImageDataRequest';
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
    const resolved = new GetCurrentImageDataRequest(null);
    return resolved;
    }
};

class GetCurrentImageDataResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.current_image = null;
    }
    else {
      if (initObj.hasOwnProperty('current_image')) {
        this.current_image = initObj.current_image
      }
      else {
        this.current_image = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetCurrentImageDataResponse
    // Serialize message field [current_image]
    bufferOffset = _arraySerializer.float32(obj.current_image, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetCurrentImageDataResponse
    let len;
    let data = new GetCurrentImageDataResponse(null);
    // Deserialize message field [current_image]
    data.current_image = _arrayDeserializer.float32(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 4 * object.current_image.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a service object
    return 'moveit_tutorials/GetCurrentImageDataResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '06552b34b97c1365790de0d089ef0bec';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32[] current_image
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetCurrentImageDataResponse(null);
    if (msg.current_image !== undefined) {
      resolved.current_image = msg.current_image;
    }
    else {
      resolved.current_image = []
    }

    return resolved;
    }
};

module.exports = {
  Request: GetCurrentImageDataRequest,
  Response: GetCurrentImageDataResponse,
  md5sum() { return '06552b34b97c1365790de0d089ef0bec'; },
  datatype() { return 'moveit_tutorials/GetCurrentImageData'; }
};
