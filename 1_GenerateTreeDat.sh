cd $1
for SubDir in *_v
do
	echo ""
	cd $SubDir
	for DataFile in sub*.txt
	do
		echo "dir",$SubDir,"datafile",$DataFile
		MDataFile=${DataFile%*.txt}
		python ../../7* -r $MDataFile
	done
	echo "OK"
	cd ..
done

