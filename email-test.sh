for i in {1..100}
do
  echo "send email $i"
  mail -s "test $i" $1 < /local/repository/email.txt
done
