#!/bin/bash
TEMPFILE=$(mktemp)
OUTPUT=$(ss -tlpn | awk 'NR>1 {print gensub(/.*"(.+)".*/,"\\1",1,$6)";"gensub(/.*:(.*)/,"\\1",1, $4)}')
echo $OUTPUT | tr -s '[:blank:]' '\n' |
        while IFS=";" read -r process port; do lsof -i :$port -s TCP:LISTEN | awk 'NR>1 { print proc";"$2";"pt }' proc=$process pt=$port; done |
                while IFS=";" read -r process id port; do ps -o thcount $id | awk 'NR>1 { print proc";"pt";"$1 }' proc=$process pt=$port; done >> $TEMPFILE

while IFS=";" read -r process port tdcnt; do find /data/conf/ -name "${process}*" | awk '{ print proc";"pt";"tdcnt";"$0 } END {if (NR == 0) print proc";"pt";"tdcnt";"}' proc=$process pt=$port tdcnt=$tdcnt; done < $TEMPFILE
