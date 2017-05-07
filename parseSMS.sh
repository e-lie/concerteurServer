#!/bin/sh

date=$(date +%Y%m%d%H%M%S%N)
first_time=1
for i in `seq $SMS_MESSAGES` ; do
	eval "sms_number=\"\${SMS_${i}_NUMBER}\""
	eval "sms_text=\"\${SMS_${i}_TEXT}\""
	if [ $first_time -eq 1 ]
	then
		first_time=0
		sms_num="$sms_number"
		sms=""
	fi
	sms="$sms$sms_text"
done
echo "test $sms_num $sms" >> /tmp/parseSMSout.txt
python3 /home/elie/Bureau/concerteurServer/messageReception.py "$sms_num" "$sms"


exit 0
