rm -rf channel_v3.json
curl -O https://packagecontrol.io/channel_v3.json
git add .
git commit -m 'update'
git push
