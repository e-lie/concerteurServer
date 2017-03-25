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
#echo "$sms" >> /var/www/html/RaspiSMS/receiveds/"$date".txt
wget "http://localhost:9000/addsms/$sms_num/$sms" -o /dev/null

