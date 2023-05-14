#This script was used to split 'train2017' folder into several folders to speed up converting original images to fisheye-looking ones

size = 10000
dirName = "train2017_"
n = $((`find . -maxdepth 1 -type f | wc -l`/$size+1))
for i in `seq 1 $n`;
do
    mkdir -p "$dirName$i";
    find . -maxdepth 1 -type f | head -n $size | xargs -i mv "{}" "$dirName$i"
done