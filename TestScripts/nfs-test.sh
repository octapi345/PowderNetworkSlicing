trap "exit;" SIGINT
cd /nfs
i=1
text="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea re"
if ! [ -e /local/repository/read.txt ]
then
  touch /local/repository/read.txt
elif ! [ -e /local/repository/write.txt ]
then
  touch /local/repository/write.txt
fi
while true
do
  touch $1_$i.txt
  (time (echo "$text" >> "${1}_${i}.txt")) >> /local/repository/write.txt 2>&1
  sleep 0.5
  (time (cp $1_$i.txt /home/copy/)) >> /local/repository/read.txt 2>&1
  sleep 0.5
  let i++
done
  
