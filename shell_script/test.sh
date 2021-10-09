#!/bin/bash

# linux下使用bash test.sh执行，其他系统下sh test.sh执行
name="cgt"
# $ 读取变量值
echo $name
onlyread_variable="https://www.google.com"
# readonly 定义该变量为只读
readonly onlyread_variable
echo $onlyread_variable
# unset 删除变量
unset name
echo $name

your_name="runoob"
str1="Hello,I \"$your_name\" \n"
# echo -e 激活转义字符
# shellcheck disable=SC2090
echo -e "$str1"
# 拼接字符串
echo "hello,my name is $your_name"
# 获取字符串长度
echo ${#your_name}
# 提取子字符串
echo ${your_name:2:5}
# 查找子字符串
label_1="Wechat is the most popular communicate tool in China"
# shellcheck disable=SC2046
# shellcheck disable=SC2005
# shellcheck disable=SC2003
echo $(expr index "$label_1" a)
# 数组 创建数组
name_array=("CGT" "BRUCE" "CAT" "DOG" "APPLE" "BANANA")
# 读取指定位置元素
echo "${name_array[3]}"
# 读取所有元素
echo "${name_array[@]}"
# 获取数组元素个数
array_length=${#name_array[@]}
echo "$array_length"
array_length_2=${#name_array[*]}
echo "$array_length_2"
# 获取单个数组元素长度
cgt_length=${#name_array[0]}
echo "$cgt_length"
:<<EOF
当前上下两行组成多行注释
EOF
# adb shell ls >> show_all_file.txt
# 传递参数
echo "Shell 传递参数："
echo "打印第一个参数（执行的文件名）：$0"
echo "打印第二个参数：$1"
echo "打印第三个参数：$2"
# 传递参数个数
echo "当前传递的参数个数为：$#"
# 获取所有传递的参数
echo "当前所有的传递的参数为：$*"
echo "当前所有的传递的参数为：$@"
# 获取当前脚本运行进程ID号
echo "当前脚本运行Process ID：$$"
# 获取后台运行的最后一个进程ID号
echo "Last Process ID which running in background：$!"
# 获取shell使用的当前选项
echo "shell choose：$-"
# 获取最后命令的退出状态，0表示没有错误，其他值为有错误
echo "Last command exit status is ：$?"
# 使用`expr x + x`完成表达式求值操作
# shellcheck disable=SC2006
# shellcheck disable=SC2003
Bruce=12
# shellcheck disable=SC2006
# shellcheck disable=SC2003
val=`expr $Bruce + 2`
# shellcheck disable=SC2154
echo "2+2=$val"
# 条件表达式要放在方括号之间，并且要有空格，例如: [$a==$b] 是错误的，必须写成 [ $a == $b ]
if [ $Bruce == 12 ]
then
  echo "bruce's value is 12"
fi
  echo "Bruce over"
# 关系运算符只支持数字，不支持字符串，除非字符串的值也是数字
a=1
b=2
if [ $a -eq $b ]
then
  echo "a = b"
elif [ $a -ne $b ]
then
  echo "a != b"
fi
  echo "算数关系运算"

if [ $a -gt $b ]
then
  echo "a > b"
elif [ $a -lt $b ]
then
  echo "a < b"
fi
  echo "算数关系运算"

if [ $a -ge $b ]
then
  echo "a ≥ b"
elif [ $a -le $b ]
then
  echo "a ≤ b"
fi
  echo "算数关系运算"

# ！非运算 -o或运算 -a与运算，&& 逻辑And运算，|| 逻辑Or运算
# shellcheck disable=SC2166
if [ $a -lt $b -a $a -le $b ]
then
  echo "It's -a与运算，两边表达式都为True才执行"
fi

# 字符串运算符
# 检测字符串是否相等
a="ABC"
b="abc"
if [ $a = $b ]
then
  echo "a=b"
elif [ $a != $b ]
then
  echo "a!=b"
fi
# 检测字符串长度是否为0
if [ -z $a ]
then
  echo "a的length为0"
else
  echo "a的length不为0"
fi
if [ -n "$a" ]
then
  echo "a的length不为0"
else
  echo "a的length为0"
fi
# 检测字符串是否为空
if [ $a ]
then
  echo "$a:字符串不为空"
else
  echo "$a:字符串为空"
fi

# 文件测试运算符
file="test.sh"
if [ -e $file ]
then
  echo "$file 文件存在"
  if [ -b $file ]
  then
    echo "$file 是块设备文件"
  elif [ -c $file ]
  then
    echo "$file 是字符设备文件"
  elif [ -d $file ]
  then
    echo "$file 是目录"
  elif [ -g $file ]
  then
    echo "$file 设置了SGID位"
  elif [ -k $file ]
  then
    echo "$file 设置了粘着位"
  elif [ -p $file ]
  then
    echo "$file 是有名管道"
  elif [ -u $file ]
  then
    echo "$file 设置了SUID位"
  elif [ -r $file ]
  then
    echo "$file 可读"
  elif [ -w $file ]
  then
    echo "$file 可写"
  elif [ -x $file ]
  then
    echo "$file 可执行"
  elif [ -s $file ]
  then
    echo "$file 文件不为空，文件大小不为0"
  elif [ -S $file ]
  then
    echo "$file 文件是socket"
  elif [ -L $file ]
  then
    echo "$file 文件存在并且是一个符号链接"
  fi
fi

# echo用于字符串输出
echo string
echo "It is a test"
echo It is a test
echo "\"It is a test\""
# echo 显示变量
#read name
#echo "$name 当前是读取输入的内容并传给变量name，再由echo输出显示"
# 显示换行
echo -e "OK! \n"
# 显示不换行
echo -e "OK! \c"
# 显示结果重定向至文件中
if [ -e "./temp/" ]
then
  echo "temp文件夹已存在，直接读写"
  echo "It is a test" > ./temp/redirect.txt
else
  echo "temp文件夹不存在，先创建文件夹再进行读写"
  mkdir ./temp/
  echo "It is a test" > ./temp/redirect.txt
fi
# 使用单引号 - 原样输出字符串，不进行转义或取变量
# shellcheck disable=SC2016
# shellcheck disable=SC2028
echo '$your_name\n'
# 获取命令执行结果，用反引号
# shellcheck disable=SC2046
# shellcheck disable=SC2006
# shellcheck disable=SC2005
echo `adb devices` > ./temp/redirect.txt
# shellcheck disable=SC2046
# shellcheck disable=SC2006
# shellcheck disable=SC2005
echo `date`

# printf 命令
printf "CGT"
printf "ABC\n"
printf "ZBC"
# shellcheck disable=SC2158
if false
then
  echo "NOK"
elif true
then
  echo "OK"
fi

# for循环
for item in 1 2 3 4 5
do
  echo "The value is: $item"
done

## while循环
#count=1
#while [ $count -le 10 ]
#do
#  echo "$count"
#  SLEEP 0.0000000001
#  # shellcheck disable=SC2219
#  let "count++"
#done
#
## 循环读取键盘输入内容
#echo '按下<CTRL-D>退出'
#echo -n '输入你最喜欢的网站网址：'
#while read WEBSITE
#do
#  echo "This is a fantastic website : $WEBSITE"
#done

## 无限循环
#while true
#do
#  echo "I will not stop!"
#done

## until循环
#number1=0
#until [ ! $number1 -lt 10 ]
#do
#  echo $number1
#  # shellcheck disable=SC2219
#  let "number1++"
#  sleep 0.05
#done

## 多选择语句
#echo '输入数字1~4：'
#echo '你输入的数字为：'
## shellcheck disable=SC2162
#read number2
#case $number2 in
#  1)  echo "你选择了1"
#  ;;
#  2)  echo "你选择了2"
#  ;;
#  3)  echo "你选择了3"
#  ;;
#  4)  echo "你选择了4"
#  ;;
#  *)  echo "你没有输入1~4之间的数字"
#  ;;
#esac

# break,continue用法一致

## Shell函数
#deviceList(){
#  # shellcheck disable=SC2046
#  # shellcheck disable=SC2006
#  # shellcheck disable=SC2005
#  echo `adb devices`
#}
#
#deviceList
#
#returnDevice(){
#  # shellcheck disable=SC2046
#  # shellcheck disable=SC2006
#  # shellcheck disable=SC2005
#  result=$(echo `adb devices`)
#  return 1
#}
#returnDevice
#echo -e "method running result is :$?\nresult is :\n$result"

# Shell输入\输出重定向

# command > file	将输出重定向到 file。
# command < file	将输入重定向到 file。
# command >> file	将输出以追加的方式重定向到 file。
# n > file	将文件描述符为 n 的文件重定向到 file。
# n >> file	将文件描述符为 n 的文件以追加的方式重定向到 file。
# n >& m	将输出文件 m 和 n 合并。
# n <& m	将输入文件 m 和 n 合并。
# << tag	将开始标记 tag 和结束标记 tag 之间的内容作为输入。
# 需要注意的是文件描述符 0 通常是标准输入（STDIN），1 是标准输出（STDOUT），2 是标准错误输出（STDERR）。

source ./outside.sh
# shellcheck disable=SC2154
echo "case1.sh的外部变量调用：$outside_value"


SLEEP 3s
#clear





