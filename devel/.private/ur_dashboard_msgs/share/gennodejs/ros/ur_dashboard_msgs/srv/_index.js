
"use strict";

let GetRobotMode = require('./GetRobotMode.js')
let AddToLog = require('./AddToLog.js')
let Popup = require('./Popup.js')
let GetLoadedProgram = require('./GetLoadedProgram.js')
let IsProgramSaved = require('./IsProgramSaved.js')
let IsInRemoteControl = require('./IsInRemoteControl.js')
let RawRequest = require('./RawRequest.js')
let GetProgramState = require('./GetProgramState.js')
let IsProgramRunning = require('./IsProgramRunning.js')
let Load = require('./Load.js')
let GetSafetyMode = require('./GetSafetyMode.js')

module.exports = {
  GetRobotMode: GetRobotMode,
  AddToLog: AddToLog,
  Popup: Popup,
  GetLoadedProgram: GetLoadedProgram,
  IsProgramSaved: IsProgramSaved,
  IsInRemoteControl: IsInRemoteControl,
  RawRequest: RawRequest,
  GetProgramState: GetProgramState,
  IsProgramRunning: IsProgramRunning,
  Load: Load,
  GetSafetyMode: GetSafetyMode,
};
