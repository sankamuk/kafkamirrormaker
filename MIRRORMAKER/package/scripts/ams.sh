#!/bin/sh
url=http://sandbox.hortonworks.com:6188/ws/v1/timeline/metrics
while [ 1 ]
do
total_connections_received=$(free -k | grep Mem | awk '{ print $4 }')
total_commands_processed=$(free -k | grep Mem | awk '{ print $3 }')
millon_time=$(( $(date +%s%N) / 1000000 ))
json="{
 \"metrics\": [
 {
 \"metricname\": \"usedmem\",
 \"appid\": \"mirrormaker\",
 \"hostname\": \"localhost\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${total_connections_received}
 }
 },
 {
 \"metricname\": \"freemem\",
 \"appid\": \"mirrormaker\",
 \"hostname\": \"localhost\",
 \"timestamp\": ${millon_time},
 \"starttime\": ${millon_time},
 \"metrics\": {
 \"${millon_time}\": ${total_commands_processed}
 }
}
 ]
}"
echo $json | tee -a /root/my_metric.log
curl -i -X POST -H "Content-Type: application/json" -d "${json}" ${url}
sleep 3
done
