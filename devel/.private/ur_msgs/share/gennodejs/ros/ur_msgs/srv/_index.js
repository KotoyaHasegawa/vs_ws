
"use strict";

let GetRobotSoftwareVersion = require('./GetRobotSoftwareVersion.js')
let SetSpeedSliderFraction = require('./SetSpeedSliderFraction.js')
let SetAnalogOutput = require('./SetAnalogOutput.js')
let SetIO = require('./SetIO.js')
let SetPayload = require('./SetPayload.js')

module.exports = {
  GetRobotSoftwareVersion: GetRobotSoftwareVersion,
  SetSpeedSliderFraction: SetSpeedSliderFraction,
  SetAnalogOutput: SetAnalogOutput,
  SetIO: SetIO,
  SetPayload: SetPayload,
};
