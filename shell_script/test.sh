#!/bin/bash

name="cgt"
echo $name
onlyread_variable="https://www.google.com"
readonly onlyread_variable
echo onlyread_variable
unset onlyread_variable
echo $onlyread_variable

