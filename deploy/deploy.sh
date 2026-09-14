#!/usr/bin/env bash

set -u
set -o pipefail

: "${IMAGE_NAME:?IMAGE_NAME is required}"
: "${IMAGE_TAG:?IMAGE_TAG is required}"

APP_DIR="$HOME/devops-lab"

cd "$APP_DIR"

source ./health_checks.sh


echo "================================="
echo "DEPLOYMENT START"
echo "================================="

echo "Target image:"
echo "${IMAGE_NAME}:${IMAGE_TAG}"


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

    echo
    echo "Previous deployment configuration:"

    cat .env

    echo
    echo "Loading previous deployment environment..."

    set -a
    source .env
    set +a

    echo
    echo "Rollback target:"

    echo "${IMAGE_NAME}:${IMAGE_TAG}"

    echo
    echo "Pulling previous image..."

    if ! docker compose pull api; then
        echo "CRITICAL: failed to pull rollback image"
        return 1
    fi

    echo
    echo "Restoring previous API version..."

    if ! docker compose up -d --force-recreate api; then
        echo "CRITICAL: failed to restore previous API"
        return 1
    fi

    echo
    echo "Checking rolled-back application..."

    if api_health_check && edge_health_check; then

        echo
        echo "================================="
        echo "ROLLBACK SUCCESSFUL"
        echo "================================="

        docker compose ps
        return 0
    fi

    echo
    echo "CRITICAL: rollback health check failed"

    echo
    echo "Rollback container logs:"

    docker logs devops-lab-api || true

    return 1
}


echo
echo "Saving current deployment..."

if [ -f .env ]; then
    cp .env .env.previous
fi


echo
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

    echo
    echo "ERROR: failed to pull new API image"

    if [ -f .env.previous ]; then
        echo "Restoring previous .env file..."
        cp .env.previous .env
    fi

    exit 1
fi


echo
echo "Deploying new API version..."

if ! docker compose up -d; then

    echo
    echo "================================="
    echo "NEW DEPLOYMENT FAILED DURING STARTUP"
    echo "================================="

    rollback_result=0
    rollback || rollback_result=$?

    if [ "$rollback_result" -ne 0 ]; then
        echo
        echo "================================="
        echo "CRITICAL: ROLLBACK FAILED"
        echo "================================="
    fi

    exit 1
fi


echo
echo "Waiting for application health checks..."

if api_health_check && edge_health_check; then

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

echo
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