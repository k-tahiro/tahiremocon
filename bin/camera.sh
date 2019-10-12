#!/bin/bash

readonly CAMERA_APP="com.huawei.camera/com.huawei.camera"
readonly CAMERA_DIR="/sdcard/DCIM/Camera"
readonly DATA_DIR="$(cd $(dirname $0) && pwd)/../data"
readonly LOG_DIR="$(cd $(dirname $0) && pwd)/../log"
readonly ADB_LOG_FILE="${LOG_DIR}/adb.log"
readonly ERR_LOG_FILE="${LOG_DIR}/err.log"

{
  adb shell touch "${CAMERA_DIR}/newer"
  adb shell input keyevent 82 # unlock
  adb shell am start -n "${CAMERA_APP}" # start camera app
  adb shell input keyevent 80 # forcus
  adb shell input keyevent 27 # release the shutter
  adb shell input keyevent 3 # back to home
  adb shell input keyevent 223 # sleep
} >>"${ADB_LOG_FILE}" 2>&1

while :
do
  FILENAME=$(adb shell find ${CAMERA_DIR} -type f -newer ${CAMERA_DIR}/newer | grep jpg)
  if [ "${FILENAME}" != "" ]; then
    if [ $(echo "${FILENAME}" | wc -l) -eq 1 ]; then
      adb pull "${FILENAME}" "${DATA_DIR}" >>"${ADB_LOG_FILE}" 2>&1
      adb shell rm -f "${FILENAME}" >>"${ADB_LOG_FILE}" 2>&1
      break
    else
      {
        echo "Unexpected state!!"
        echo "There are too many files."
        echo "${FILENAME}"
      } | tee -a "${ERR_LOG_FILE}" 1>&2
      exit 1
    fi
  fi
  sleep 1
done
adb shell rm -f "${CAMERA_DIR}/newer" >>"${ADB_LOG_FILE}" 2>&1

basename "${FILENAME}" | tr -d '\n'
