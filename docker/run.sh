#!/usr/bin/env bash

COMMAND=${1:-}
shift

function usage {
    cat <<EOF
Usage: $0 <COMMAND> <ARGUMENT>

Commands:
  build     Build carto image
  start     Start the HTTP server
  test      Run tests


Examples:

   $0 build
   $0 start
   $0 test
EOF
}

case "$COMMAND" in
    build)
    docker-compose build
    ;;

    start)
    docker-compose up
    ;;

    test)
    docker-compose run carto python -m pytest
    ;;

    "")
    echo "Missing command" >&2
    usage
    exit 1
    ;;
    *)

    echo "Unknown command: $COMMAND" >&2
    usage
    exit 1
    ;;
esac
