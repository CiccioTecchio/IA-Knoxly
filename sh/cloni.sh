rm output/*.txt
rm copie/*.csv

skip=0
limit=1000
ds=copie/ds_$limit.csv
out=output/out_$limit.txt
echo text,tipo >> $ds
python3 crea.py $ds #$limit $skip
python3 modello.py $ds 2> $out
echo fatto $ds
