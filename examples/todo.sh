#!/usr/bin/env bash

todo() {

  if [ "$1" = "list" ]; then
    nots list todos
  fi

  if [ "$1" = "list-done" ]; then
    nots list todos --done__eq=true
  fi

  if [ "$1" = "list-todo" ]; then
    nots list todos --done__eq=false
  fi

  if [ "$1" = "mark-done" ]; then
    nots update todos --done=true --id__eq="$2"
  fi

  if [ "$1" = "add" ]; then
    nots create todo --description="$2"
  fi

}
