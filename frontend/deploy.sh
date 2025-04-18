#!/usr/bin/env bash
set -e

npm run build

# 배포 대상 디렉토리 초기화
sudo rm -rf /var/www/bxl-dev/*

# dist → /var/www/bxl-dev 복사
sudo cp -r dist/* /var/www/bxl-dev/
sudo chown -R www-data:www-data /var/www/bxl-dev
sudo chmod -R 755 /var/www/bxl-dev

# (선택) Nginx 재시작 or reload
sudo systemctl reload nginx
