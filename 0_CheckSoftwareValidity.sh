# This is a pre-operation code. Since not all the software are handled well by IDA, this script check all the software in the database, and mark those who are successfully reverse-engineered by add a suffix "_v".
echo $1 > $2
cd $1
for SubDir in *;
do	
	sign=0
	cd $SubDir 
	for SubFile in *;
	do
		if [ $sign -eq 1 ]
		then 
			break
		elif [[ $SubFile =~ txt$ ]]
		then
			sign=1
		fi
	done
	cd ..
	if [ $sign -eq 1 ]
	then
		echo $SubDir >> ../$2;
		Dest=$SubDir'_v'
		mv $SubDir $Dest
	fi
done

