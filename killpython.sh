#echo "which run you wanna kill?"
read -p "which run you wanna kill?" nRun
echo $nRun
declare DIR="archive/run$nRun"
cd $DIR
echo 0 > com/milano.py.ctrl
echo 0 > com/milano.cc.ctrl
