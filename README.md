# aircrafts

1/ Download files

2/ cd aircrafts (the directory contains requirements.txt, run.sh ...)

3/ create new virtualenv:
	- pip3 install virtualenv

	- virtualenv -p python3 env

	- source env/bin/activate
	
4/ install requirements.txt


5/ change the permissions of run.sh: chmod 777 run.sh

6/open new terminal window and run this command: sudo docker run -p 8053:8050 scrapinghub/splash --max-timeout 85


7/ execute run.sh script: ./run.sh

You will find aircrafts.csv in the same directory.
