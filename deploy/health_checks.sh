#!/usr/bin/env bash

api_health_check() {

    echo "Checking API health..."

    for attempt in 1 2 3 4 5 6 7 8 9 10; do

        if docker exec devops-lab-api \
            python -c \
            "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"; then

            echo
            echo "API health check passed"
            return 0
        fi

        echo "API health check attempt ${attempt} failed..."
        sleep 3
    done

    echo "API health check failed"
    return 1
}


edge_health_check() {

    echo "Checking edge health through Caddy..."

    for attempt in 1 2 3 4 5 6 7 8 9 10; do

        if curl -fsS http://localhost/health > /dev/null; then

            echo
            echo "Edge health check passed"
            return 0
        fi

        echo "Edge health check attempt ${attempt} failed..."
        sleep 3
    done

    echo "Edge health check failed"
    return 1
}