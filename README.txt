How to install
------------------

To run this service, Python and pip is required.
The following links will have instructions on how to install these.

Python: https://www.python.org/downloads/

pip: https://pip.pypa.io/en/stable/installation/


Installing the requirements
-------------------------------

Using the terminal (command line), navigate to the directory of this folder.

e.g cd C:\Users\example\Documents\SSBE-Backend

To install the requirements, enter the command: python setup.py

NOTE: 
    - Your use of the "python" command may vary, dependent on installation. e.g. you might have to use command "python3" instead
    - If there is errors relating to pip, please go to line 4 of the setup.py file and change comamnd "pip install -r requirements.txt" to "pip3 install -r requirements.txt"
    - If there are any other error, please search online for solution.

Using and running the service
--------------------------------

Using the terminal (command line), navigate to the directory of this folder.

e.g cd C:\Users\example\Documents\SSBE-Backend

To run the service, enter: python main.py

As it loads, a URL link is shown which will allow you to connect the extension to the service. There is quite a bit of text printed on the screen so you will be able to find it by scrolling up.

The default host url will most likely be: http://127.0.0.1:5000

By entering the settings page on the extension and selecting the "Backend Service" provider option, enter the host url.

Although it is to be used locally on users' machines, a login / signup system has been implemented for those who would like to use this as an actual service. To connect normally, the default option to connect is:

Username: default
Password: default

Reading the documentation
--------------------------------

Markdown is required to read the documentation.



Running the unit and integration tests
--------------------------------

Run testing.py file within this directory e.g. python testing.py

Do not exit when the testing is running.