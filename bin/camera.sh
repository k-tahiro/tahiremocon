#!/bin/bash

readonly CAMERA_APP="com.huawei.camera/com.huawei.camera"
readonly CAMERA_DIR="/sdcard/DCIM/Camera"

: "${DATA_DIR:="$(cd $(dirname $0) && pwd)/../data"}"
: "${LOG_DIR:="$(cd $(dirname $0) && pwd)/../log"}"
ADB_LOG_FILE="${LOG_DIR}/adb.log"
ERR_LOG_FILE="${LOG_DIR}/err.log"

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
  FILE=$(adb shell find ${CAMERA_DIR} -type f -newer ${CAMERA_DIR}/newer | grep jpg)
  if [ "${FILE}" != "" ]; then
    if [ $(echo "${FILE}" | wc -l) -eq 1 ]; then
      adb pull "${FILE}" "${DATA_DIR}" >>"${ADB_LOG_FILE}" 2>&1
      adb shell rm -f "${FILE}" >>"${ADB_LOG_FILE}" 2>&1
      break
    else
      {
        echo "Unexpected state!!"
        echo "There are too many files."
        echo "${FILE}"
      } | tee -a "${ERR_LOG_FILE}" 1>&2
      exit 1
    fi
  fi
  sleep 1
done
adb shell rm -f "${CAMERA_DIR}/newer" >>"${ADB_LOG_FILE}" 2>&1

FILENAME="$(basename ${FILE})"
FILE="${DATA_DIR}/${FILENAME}"
echo -n "${FILE}"
