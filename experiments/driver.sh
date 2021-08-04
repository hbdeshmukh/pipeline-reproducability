#!/bin/bash

mkdir -p /fastdisk/qs-data

echo "Loading data ..."
for i in tmp-load*.cfg; do
  cmd="./run-benchmark.sh $i"
  echo ${cmd}
  eval ${cmd}
done

echo "Running queries ..."
for i in tmp-run*.cfg; do
  cmd="./run-benchmark.sh $i"
  echo ${cmd}
  eval ${cmd}
done
