#!/bin/bash

if [ $1 = "run_local" ]; then
    export IID=${2? Container ID not supplied}
fi

function destroy() {
    remove_container "stock_db"
}

function remove_container() {
    local container=$1
    echo "Removing container ${container}..."
    test $(docker ps -a | grep ${container} | wc -l) -ge 1 && docker rm -f ${container}
}

function run_local() {
    local local_dir="$(pwd)"

    # remove_container "stock_db"
    docker run --rm -d -t \
        --name stock_db \
        -e ENV=DEBUG \
        -p 4446:4444 \
        -p 8000:8000 \
        -p 8022:22 \
        ${IID}
        # -p 22:22 \

    echo "Started container listening to ports 5500"
}

function for_manifest() {
    fun_name=$1
    echo "Running stock db ${fun_name}..."
    $fun_name
}

function status() {
    docker ps | grep -E "stock_db"
}

for_manifest ${1:-status}
