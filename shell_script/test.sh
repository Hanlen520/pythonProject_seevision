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
echo -e $str1
# 拼接字符串
echo "hello,my name is $your_name"
# 获取字符串长度
echo ${#your_name}
# 提取子字符串
