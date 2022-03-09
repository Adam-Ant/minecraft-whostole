# WhoStole

[![Build Status](https://drone.spritsail.io/api/badges/Adam-Ant/minecraft-whostole/status.svg)](https://drone.spritsail.io/Adam-Ant/minecraft-whostole)

A hacky minecraft telegram bot to find items in inventories.

This was created to fufill a need for a small collaborative survival server - people logging off with key resources in their inventories. This allows anyone to query items in anyone's inventory, using a telegram command.

## How to use
The bot has two arguments:
 * `-t` or `--token` specifies the telegram bot token
 * `-w` or `--world` specifies the full path to the world folder. Defaults to `/world` for Docker purposes.

## Docker

This program also comes with an associated Docker container for ease of deployment:

```sh
docker run -d --name WhoStole -v /host/path/to/world:/world adamant/minecraft-whostole -t <telegram token>
```

## Disclaimer
This bot was thrown together in an evening after too much beer. Stability, security and/or spontaneous combustion of any players, inventories or soft furnishings not guaranteed. 