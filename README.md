# TimesOfIsrael
TimesOfIsrael Twitter project

This is a simple application that queries Twitter for Tweets with a given search term.
In order to run this application, run (from terminal/command line) "pip install -r requirements.txt". This will install a Python twitter library.
Next, update config.py with your application data. You need to set up a Twitter app (using their development portal). Once you've set up an app, you will find it's API_KEY and API_SECRET_KEY. Add those to config.py.
The application itself is written in main.py. You will see in line 6 the search term - change it to whatever you would like.

Once all that is in place, you can run "python main.py" from command-line, and the application will run and save the output to "output.json". In order to understand what data was retrieved, open that file in program that can read and parse JSON files. If you don't know of a program that does - copy-paste the content of the file to http://jsonviewer.stack.hu/ - you will be able to learn what data was retrieved and plan your next steps from there.
