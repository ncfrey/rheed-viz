# rheed-viz

Database, dimensionality reduction, and visualization dashboard for RHEED data

To setup the environment, run conda env update --file env.cpu.yml, which will create a conda environment called rheed-viz

Next setup the default local database, responding to the commands as follows (blank means hit enter):

molarcli install local  
Where do you want to install Molar 🦷 (./molar_data_dir): 
Password for Postgres admin: rheed  
Server url (http://localhost):  
Allow the backend to send email? [y/n]: n 
Backend port (8000):  
Number of workers for the backend (2):  
Full name: default  
Email: default@rheed.com  
Password: rheed 


If you get a permissions error on linux, you can change the user group of docker using the below command.
sudo usermod -G docker your_username; su - your_username

