# OpenTAKServer

OpenTAKServer (OTS) is yet another open source TAK Server for ATAK, iTAK, and WinTAK. OTS's goal is to be easy to install and use, and to run on both servers and SBCs (ie Raspberry Pi).

This project is just beginning and not yet suitable for production.

## Current Features
- Connect via TCP from ATAK
- Send and receive messages
- Send and receive points
- Share location with other users

## Planned Features
- WinTAK and iTAK support (This may already work, just needs to be tested)
- SSL Support
- Authentication
- Save CoT messages to a database (either SQLite or MySQL via SQLAlchemy)
- API to query saved CoT messages
- WebUI
  - Live Map
  - View saved CoT messages
  - Chat with EUDs
- Android app
- Mission support

## Requirements
- python = "^3.10"
- flask = "^3.0.0"
- colorlog = "^6.7.0"
- flask-socketio = "^5.3.6"
- bs4 = "^0.0.1"
- datetime = "^5.3"
- pika = "^1.3.2"
- RabbitMQ