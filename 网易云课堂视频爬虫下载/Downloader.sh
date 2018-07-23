#write by ctipsy

i=1
grep  '<div class="down"><a href='    *.html | while read line
do
    urldl=$(echo $line | cut  -d '"' -f4)
    echo $urldl
    filename=$(echo $line | cut -d '"' -f5 | cut -d '<' -f1 | sed  's/^>//')
    fn="$i-${filename}.flv"
    echo "$fn"
    if [  -e  "$fn".st  -o  ! -f   "$fn"  ] ; then
    axel -n 10  -o  "$fn"  -av  $urldl
    else
    echo "$fn  已存在"
    fi  
    i=$(($i+1))
done

echo "所有资料下载完毕！"
