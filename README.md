# rheed-viz

Database, dimensionality reduction, and visualization dashboard for RHEED data

To setup the environment, run conda env update --file env.cpu.yml, which will create a conda environment called rheed-viz

Next, use conda activate rheed-viz and run molarcli install local to install a local version of the postgres database.

If you get a permissions error on linux, you can change the user group of docker using the below command.
sudo usermod -G docker your_username; su - your_username
