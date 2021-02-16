#!/usr/bin/env bash

# by providing a path as an argument
BUILD_DIR=build

cmake -E make_directory ${BUILD_DIR}

pushd ${BUILD_DIR}

cmake ..

cmake --build . -j`nproc`

popd

