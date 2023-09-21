trap "exit;" SIGINT
i=1
if [! -e /local/repository/send.txt]; then
  touch /local/repository/send.txt
fi
while true
do
  echo "sending  email $i"
  (time (mail -s "test $i" $1 < /local/repository/email.txt)) /local/repository/send.txt >> 2>1&
  let i++;
  sleep 0.05
done
