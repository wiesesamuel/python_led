# LightStorm

Web Interface for controlling GPIO (and more) connected LEDs on a Raspberry PI.

## Service File

Add a service file on your Raspberry to enable autostart.

```
[Unit]
Description=led
After=mutli-user.target

[Service]
User=root
Type=simple
WorkingDirectory=/home/pi/led-2.0
ExecStart=/usr/bin/python3 /home/pi/led-2.0/main.py
Restart=always
RestartSec=1

[Install]
WantedBy=multi-user.target
```