#!/bin/bash

add_services() {
  for i in $(seq 1 $1); do
    cat <<EOF >>docker-compose.yml
  node$i:
    build: .
    container_name: node$i
    hostname: node$i
    networks:
      - gossip-net
EOF
  done
}

add_network() {
  cat <<EOF >>docker-compose.yml
networks:
  gossip-net:
    driver: bridge
EOF
}

echo "services:" >docker-compose.yml
add_services "$1"
add_network
