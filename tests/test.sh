#!/usr/bin/env bash

alias nots="./main.py"
space="        -"

echo "$space reset nots"
nots reset system -v3

echo "$space setup nots"
nots setup system -v3

echo "$space add our first resource"
nots create resource --name=todo --plural=todos -v3

echo "$space cannot add the same resource"
nots create resource --name=todo --plural=todos -v3

echo "$space add a few fields."
nots create field --resource=todo --name=done --type=boolean --default=false -v3
nots create field --resource=todo --name=name -v3

echo "$space cannot add same field twice"
nots create field --resource=todo --name=name -v3

echo "$space now insert some records"
nots create todo --name="Do some stuff" -v3
nots create todo --name="Do some more stuff!" --done=true -v3

echo "$space list the resources we just created"
nots list todos -v3 -v3

echo "$space add a new resource"
nots create field --resource=todo --name=date --default=NOW -v3

echo "$space list the resources we just created"
nots list todos -v3 -v3