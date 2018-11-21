#!/bin/sh
#goto project root
curpath=$(cd "$(dirname "$0")"; pwd)
cd $curpath
nohup python3 server.py > server.log 2>&1 &
cd ..
echo "server is running in background"
echo "yixue:port=8002(public)"
exit 0
