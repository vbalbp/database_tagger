# Database tagger
This is a Python script that works with the Dynatrace product. In Dynatrace, we might have automatically detected databases that are not tagged or added into management zones because we are not monitoring the host where they are sitting. In order to increase visibility for the whole environment and make sure that databases are tagged or added to management zones automatically, this script was developed.
### Requirements
This is a very simple script. All you need to have in order to run it:
- `Python 2.7`
- `requests` python library 2.25.0

And of course a working environment of Dynatrace, doesn't matter if it's SaaS or Managed. If it is SaaS, you need to make sure the server where you run the script has an open connection to the Dynatrace API. If it is Managed, you need to make sure that the server where you run the script can connect to the Dynatrace cluster.
### How it works
The script uses the Dynatrace API in order to get a list of all the services in your environment. From this list, it selects the ones that are of type `DATABASE_SERVICE`, and from those, it checks for every single service that calls it. For each one of those services, it gathers all the tags and afterwards adds them to the database, effectively automating the process. If management zones are based on tags (which is a best practice), they will work automatically as well with this script.
## Easy set up guide
This project has been created using the pipenv framework in order to make its installation and execution simple even for non Python users. Follow these simple steps to get it up and running on a Linux system:
1. Install Python 2.7 `sudo apt install python2.7`
2. Install pip `sudo apt install pip`
3. Install pipenv `pip install pipenv`
4. Make sure you move to the project folder at this point. Set up pipenv `pipenv install`
5. Modify the `settings.py` file with the values for your cluster address and your API token
6. Run the script `pipenv run python src/main.py`
You can run the last command as a cronjob once you have done the other 5 steps to make it a recurring execution.
In order to execute the script on a Windows host, you will not be able to use pipenv, you will need to make sure you install Python 2.7, along with the libraries metioned in the requirements, and run the script directly with the Python executable. If it works, you can set up an scheduler, which is the equivalent of cronjob in Windows.
