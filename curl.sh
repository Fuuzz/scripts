set -e

# API Key Test
KEY=""

# Address Test
ADDRESS=""

HOSTNAME=$1
HOSTADDRESS=$2
SERVICEDESC=$3
STATE=$4
OUTPUT=$5

# Proxies
PROXY='http://user:pass@domain:8080'

# Buil monitored item
if [ -z $SERVIDESC];then
        MONITORED_ITEM="$SERVICEDESC service of $HOSTNAME"
else
        MONITORED_ITEM="$HOSTNAME with IP $HOSTADDRESS"
fi

# Build the json payload
generate_post_data()
{
  cat <<EOF
{
   "monitored_item": "$MONITORED_ITEM",
   "alert_summary": "$STATE",
   "detailed_description": "$OUTPUT",
   "apikey": "$KEY",
   "monitoring_system": "NAGIOSXI"
}
EOF
}

curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-x "$PROXY" \
-X POST --data "$(generate_post_data)" "$ADDRESS"

