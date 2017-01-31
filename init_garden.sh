#init lights
nohup python /home/pi/git/growroom/legacy/lights.py &

#init basic soil sensor and water pump integration
nohup python /home/pi/git/growroom/legacy/Main.py &

#initialize django webserver for growroom
python /home/pi/git/growroom/MyGarden/manage.py runserver 192.168.69:8000

