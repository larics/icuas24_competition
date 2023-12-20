#!/bin/bash

echo "Building icuas24_competition Docker image"

distro="focal"
build_args=""
for (( i=1; i<=$#; i++));
do
  param="${!i}"
  echo $param

  if [ "$param" == "--bionic" ]; then
    distro="bionic"
  fi

  if [ "$param" == "--focal" ]; then
    distro="focal"
  fi

  if [ "$param" == "--focal-nogpu" ]; then
    distro="focal-nogpu"
  fi

  if [ "$param" == "--build-args" ]; then
    j=$((i+1))
    build_args="${!j}"
  fi

done

echo "Building for $distro with additional docker arguments $build_args."

docker build \
    $build_args \
    -f Dockerfile.$distro \
    -t icuas24_competition:$distro .
