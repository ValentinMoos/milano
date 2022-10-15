echo "starting run management."
#what we wanna do is
# A) keep track of run - logistics: this includes 
#	A1) find out the number of this run
#	A2) create the directory for this run, and CHANGE into it (such that there is no interference between active runs)
#	A3) find out the variables: nOrder, and version of artemide and possibly also other parameters such as the order of the TMDPDF and TMDFF evolution order....
#	A4) create com dir, copy the correct constfile into this one / this can be done by python...
# B) initialize Python... this will take some time.
# C) initialize C++... this is fast. 
# B + C should run in parallel... so after A) is completed, essentially one should call for C++ and Python to launch... and they should find all their requirements in the folder we are then. 
# D) just end both processes and return to section.

#A
#A1
declare -i max=99

declare -i nRun
#for i in `seq 1 $max`
for ((i=0; i<=$max;++i));
#for i in {$1..$max..1}
do
	#echo $i
	nRun=$i+200
	#echo "$nRun"
	declare DIR="archive/run$nRun"
	#echo $DIR
	#echo "above was directory"
	#ls $DIR
#	ls archive/run"$a"
	if [ !  -d "$DIR" ]; then
	#	echo "$nRun"
		echo "the run will be $nRun. Now we create the directory."
		mkdir $DIR
		cp milano2.py $DIR
		cp milano2 $DIR
		cd $DIR
		echo "now we are in the run directory."
#		pwd
		break
	fi
done


#A2 is done in A1..

#A3
#declare -i norder, version, evolutionorder

read -p "type in order for cross section and TMDR evoltion: " norder
echo ""
echo ""

read -p "type in version for artemide file ( amount of parameters depends on this ): " version
echo ""
echo ""

read -p "type in order for TMD - evolution order: " evolutionorder
echo ""
echo ""


declare file4settings="settingsfile"
touch $file4settings
echo "settings for run$nRun" > $file4settings
echo $norder >> $file4settings
echo $version >> $file4settings
echo $evolutionorder >> $file4settings


#echo "settings for run$a > $file4settings

#A4
mkdir com
touch com/milano.cc.parameters
#start with c++ running and python waiting.. python should initialize itself first anyway. and until then c++ will be calling for python already.
echo 1 > com/milano.cc.ctrl
echo 2 > com/milano.py.ctrl

#B&C)
#run python and run c++

#sleep(10)

echo "setup read to launch python and others others."
python milano2.py &
./milano2
echo "c++ finished!"
#D)
touch cppstopper
touch pystopper
echo 0 > com/milano.cc.ctrl
echo 0 > com/milano.py.ctrl
rm cppstopper pystopper -f
cd ../..
