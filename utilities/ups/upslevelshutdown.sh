#!/bin/bash
DEBUG=0
# This is the IP Address the SNMP Server daemon is running on:
SERVERIP=192.168.85.100
# SNMP Community
SNMPCOMMUNITY=mynasups
# This shouldn't ever change:
OIDBASE=.1.3.6.1.4.1
# This will be defined from the SNMP Server's MIB file:
UPSOFFSET=.44738.6
# UPS Battery Level Field
UPSFIELDOFFSET=7

# Shutdown Threshold in percentage
NOTIFICATIONTHRESHOLD=92
SHUTDOWNTHRESHOLD=60

# Call the SNMP Command
UPSLEVEL=$(snmpwalk -v2c -c ${SNMPCOMMUNITY} ${SERVERIP} ${OIDBASE}${UPSOFFSET} | head -n${UPSFIELDOFFSET} | tail -n1 | sed -e 's/ /~/g' | sed -e 's/:~/ /g' | awk '{print $2}')

# Messages
NOMINALMESSAGE="UPS Battery level is ${UPSLEVEL}%."
DISCHARGEMESSAGE="UPS Battery level has dropped to ${UPSLEVEL}%..."
SHUTDOWNMESSAGE="The UPS Battery level of ${UPSLEVEL}% is lower than the defined shutdown threshold of ${SHUTDOWNTHRESHOLD}%."

# Debug
if [ "${DEBUG}" -eq "1" ]; then
  echo "${DISCHARGEMESSAGE}"
  echo "${SHUTDOWNMESSAGE}"
fi

# Determine if the UPS Battery Level is under the threshold
if [ "${UPSLEVEL}" -lt "${SHUTDOWNTHRESHOLD}" ]; then
  echo "${SHUTDOWNMESSAGE}" | tee /dev/kmsg
  shutdown now "${SHUTDOWNMESSAGE}"
elif [ "${UPSLEVEL}" -lt "${NOTIFICATIONTHRESHOLD}" ]; then
  echo "${DISCHARGEMESSAGE}" | tee /dev/kmsg
else
  if [ "${DEBUG}" -eq "1" ]; then
    echo "${NOMINALMESSAGE}" | tee /dev/kmsg
  fi
fi
