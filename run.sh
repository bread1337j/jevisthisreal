TYPESAFE_API_KEY="$(cat .env | sed -n 1p)" DISCORD_TOKEN="$(cat .env | sed -n 2p)" ./bin/python main.py
