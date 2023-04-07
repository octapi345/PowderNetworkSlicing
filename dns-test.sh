trap "exit;" SIGINT
i=1
for a in {a..z}
do
  for b in {a..z}
  do
    for c in {a..z}
    do
      echo "DNS lookup test"
      dig emailserver $a$b.%c.com
      sleep 0.5
    done
  done    
done
