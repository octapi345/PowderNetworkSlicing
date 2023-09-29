trap "exit;" SIGINT
i=1
while true
do
  echo "sending  email $i"
  mail -s "test $i" $1 < /local/repository/email.txt
  let i++;
  sleep 0.05
done
