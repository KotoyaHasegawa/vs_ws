// Auto-generated. Do not edit!

// (in-package moveit_tutorials.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class ValidJointsGoal {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.valid_joint_values = null;
    }
    else {
      if (initObj.hasOwnProperty('valid_joint_values')) {
        this.valid_joint_values = initObj.valid_joint_values
      }
      else {
        this.valid_joint_values = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ValidJointsGoal
    // Serialize message field [valid_joint_values]
    bufferOffset = _arraySerializer.float64(obj.valid_joint_values, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ValidJointsGoal
    let len;
    let data = new ValidJointsGoal(null);
    // Deserialize message field [valid_joint_values]
    data.valid_joint_values = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.valid_joint_values.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'moveit_tutorials/ValidJointsGoal';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '726551018de18a5486e36fb7fd3f6c81';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    float64[] valid_joint_values
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ValidJointsGoal(null);
    if (msg.valid_joint_values !== undefined) {
      resolved.valid_joint_values = msg.valid_joint_values;
    }
    else {
      resolved.valid_joint_values = []
    }

    return resolved;
    }
};

module.exports = ValidJointsGoal;
