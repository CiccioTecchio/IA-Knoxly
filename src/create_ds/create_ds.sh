echo "text,tipo,sensibile" >> ds200.csv
python3 crea.py ds200.csv 200
echo "#############"
echo "text,tipo" >> ds1000.csv
python3 crea.py ds1000.csv 1000
echo "#############"
echo "text,tipo" >> ds10000.csv
python3 crea.py ds10000.csv 10000
echo "#############"
