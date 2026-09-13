#!/usr/bin/env bash

set -u
set -o pipefail


: "${IMAGE_NAME:?IMAGE_NAME is required}"
: "${IMAGE_TAG:?IMAGE_TAG is required}"


APP_DIR="$HOME/devops-lab"

cd "$APP_DIR"


echo "================================="
echo "DEPLOYMENT START"
echo "================================="

echo "Target image:"
echo "${IMAGE_NAME}:${IMAGE_TAG}"


health_check() {

    echo "Checking application health..."

    for attempt in 1 2 3 4 5 6 7 8 9 10; do

        if curl -fsS http://localhost:8000/health; then
            echo
            echo "Health check passed"
            return 0
        fi

        echo "Health check attempt ${attempt} failed..."
        sleep 3

    done

    echo "Health check failed"
    return 1
}


rollback() {

    echo
    echo "================================="
    echo "STARTING AUTOMATIC ROLLBACK"
    echo "================================="

    if [ ! -f .env.previous ]; then
        echo "ERROR: no previous deployment configuration found"
        return 1
    fi


    echo "Restoring previous environment..."

    cp .env.previous .env


    echo "Previous deployment configuration:"

    cat .env


    echo "Pulling previous image..."

    if ! docker compose pull api; then
        echo "CRITICAL: failed to pull rollback image"
        return 1
    fi


    echo "Restoring previous API version..."

    if ! docker compose up -d api; then
        echo "CRITICAL: failed to restore previous API"
        return 1
    fi


    echo "Checking rolled-back application..."

    if health_check; then

        echo
        echo "Rollback successful"

        docker compose ps

        return 0

    fi


    echo "CRITICAL: rollback health check failed"

    docker logs devops-lab-api || true

    return 1
}


echo
echo "Saving current deployment..."

if [ -f .env ]; then
    cp .env .env.previous
fi


echo "Writing new deployment configuration..."

printf 'IMAGE_NAME=%s\nIMAGE_TAG=%s\n' \
    "$IMAGE_NAME" \
    "$IMAGE_TAG" \
    > .env


echo
echo "New deployment configuration:"

cat .env


echo
echo "Pulling new API image..."

if ! docker compose pull api; then

    echo "ERROR: failed to pull new API image"

    if [ -f .env.previous ]; then
        cp .env.previous .env
    fi

    exit 1
fi


echo
echo "Deploying new API version..."

if ! docker compose up -d api; then

    echo
    echo "NEW DEPLOYMENT FAILED DURING STARTUP"

    rollback || true

    exit 1
fi


echo
echo "Waiting for application health check..."

if health_check; then

    echo
    echo "================================="
    echo "DEPLOYMENT SUCCESSFUL"
    echo "================================="

    docker compose ps

    exit 0

fi


echo
echo "================================="
echo "NEW DEPLOYMENT FAILED"
echo "================================="


echo "Failed container logs:"

docker logs devops-lab-api || true


rollback_result=0

rollback || rollback_result=$?


if [ "$rollback_result" -ne 0 ]; then

    echo
    echo "================================="
    echo "CRITICAL: ROLLBACK FAILED"
    echo "================================="

fi


exit 1