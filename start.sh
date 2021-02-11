#!/bin/bash

ALL_ARGS="$@"

display_help() {
    echo "Usage: $0 [option...] {-d... -p}" >&2
    echo
    echo "   -d, --development           start development server"
    echo
    echo "   -p, --production            start production server"
    # echo some stuff here for the -a or --add-options
    exit 1
}

start_development () {
  echo "Starting development server"
  docker-compose -f docker-compose.dev.yml build && docker-compose -f docker-compose.dev.yml up
}

start_production () {
  echo "Starting production server"
  docker-compose -f docker-compose.prod.yml build && docker-compose -f docker-compose.prod.yml up
}

setup_staging () {
  echo "Setting up staging environment"
  mkdir -p /opt/bin
  curl -L `curl -s https://api.github.com/repos/docker/compose/releases/latest | jq -r '.assets[].browser_download_url | select(contains("Linux") and contains("x86_64"))'` > /opt/bin/docker-compose
  chmod +x /opt/bin/docker-compose
}

start_staging () {
  echo "Starting staging server"
  docker-compose -f docker-compose.dev.yml build && docker-compose -f docker-compose.dev.yml up
}

for var in "$@"
  do
   case "$var" in
      -h | --help)
          display_help # Call your function
          exit 0
          ;;
      -d | --development)
          start_development
          exit 0
          ;;
      -s | --staging)
          setup_staging
          start_staging
          exit 0
          ;;
      -p | --production)
          start_production
          exit 0
          ;;
      -*)
          echo "Error: Unknown option: $1" >&2
          ## or call function display_help
          exit 1
          ;;
      *)  # No more options
          echo "Need a command."
          DEPLOY_ARGS_SET=true
          ;;
    esac
done