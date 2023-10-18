trap "exit;" SIGINT
for a in {a..z}
do
  for b in {a..z}
  do
    for c in {a..z}
    do
      echo "DNS lookup test"
      ( time ( dig $1 $a$b.$c.com )) >> /local/repository/dnstimes.txt
      sleep 0.5
    done
  done    
done
