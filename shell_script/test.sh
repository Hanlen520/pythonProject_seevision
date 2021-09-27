#!/bin/bash

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

