trap "exit;" SIGINT
for a in {a..z}
do
  for b in {a..z}
  do
    for c in {a..z}
    do
      for d in {a..z}
      do  
        echo "DNS lookup test"
        ( time ( dig $1 $a$b$d.$c.com )) >> /local/repository/dnstimes.txt 2>&1
        sleep 0.5
      done
    done
  done    
done
