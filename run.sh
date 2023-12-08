#!/bin/bash
cd $(dirname "$(realpath "$0")")
docker cp eddeapp_django:/app/media .
docker compose up -d --build
