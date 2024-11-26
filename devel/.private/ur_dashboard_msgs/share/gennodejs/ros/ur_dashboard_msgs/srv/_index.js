
"use strict";

let RawRequest = require('./RawRequest.js')
let IsProgramRunning = require('./IsProgramRunning.js')
let GetLoadedProgram = require('./GetLoadedProgram.js')
let IsInRemoteControl = require('./IsInRemoteControl.js')
let GetRobotMode = require('./GetRobotMode.js')
let IsProgramSaved = require('./IsProgramSaved.js')
let Load = require('./Load.js')
let GetSafetyMode = require('./GetSafetyMode.js')
let AddToLog = require('./AddToLog.js')
let Popup = require('./Popup.js')
let GetProgramState = require('./GetProgramState.js')

module.exports = {
  RawRequest: RawRequest,
  IsProgramRunning: IsProgramRunning,
  GetLoadedProgram: GetLoadedProgram,
  IsInRemoteControl: IsInRemoteControl,
  GetRobotMode: GetRobotMode,
  IsProgramSaved: IsProgramSaved,
  Load: Load,
  GetSafetyMode: GetSafetyMode,
  AddToLog: AddToLog,
  Popup: Popup,
  GetProgramState: GetProgramState,
};
