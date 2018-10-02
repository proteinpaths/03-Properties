# It uses the mmtsb rmsd program "rms.pl"
res=`rms.pl -fit -out ca $1 $2`
echo $res|cut -d" " -f1
