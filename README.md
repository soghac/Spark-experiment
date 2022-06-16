# Spark-experiment

 You need Linux OS, as the instruction is for linux.

First, on your terminal go to your path that the folder test_with_2_3_4 worker is placed and run:

1) Python3.8 –m venv venv

Then run the command:

2)source venv/bin/activate

Then install the required packages by running the command:

3)pip install -r requirement.txt

The next step is to open another terminal, and go to the root by running the cd command, and then go to the spark folder, so by running ls command you can see the docker-compose file. Then, you can run the following command:

4)sudo docker-compose up

So, as you can see the spark and flask app is up and running.

The next step is to open another terminal and again create a venv environment to run the request-file script, so as I mentioned you need to run source /bin/activate, and then run the command python request_file.py After that go to the first terminal ( test_with_2_3_4 worker) and run python docker_monitoring.py So, you can see all the information from the running container. And from request_file script you can see all the request at the time.
