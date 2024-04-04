# Essato_internship
Application allows user to add a new patient,  delete a patient and list patients into a database.

# The application can be started in two ways:

    1. Using only CLI
    2. Using docker

### Using only CLI

On linux machine open up terminal. Alternatively, on windows any IDE's should work too. My reccomendation is Visual Studio Code

##    Downloading files
        
        Clone this repository to your local machine using:
        ```bash
        git clone https://github.com/Hbrtjm/Essato_internship
        ```
## Install dependencies
        
        Install dependencies from requirements.txt:
        ```bash
        python -m pip install --no-cache-dir -r requirements.txt
        ```

## Start the app

        To start the application run:
        ```bash
        python -m flask run
        ```

## Accessing the page

        After running the app in terminal there should be a url to localhost. Use this link in any browser.


### Using docker 

## Note: this requires Docker to be installed. Installation guide here: https://docs.docker.com/get-docker/ 

## Building the Docker Image

1. Open a terminal.

2. Navigate to the directory containing your Flask application and the Dockerfile. This directory should also include the `requirements.txt` file listing all necessary Python dependencies.

3. Build your Docker image by running:

    ```bash
    docker build -t flask-app .
    ```

    This command creates a Docker image named `flask-app`. The `.` at the end of the command denotes the current directory as the build context.

## Running the Docker Container

Once the image has been successfully built, you can run it:

1. Execute the following command:

    ```bash
    docker run -p 5000:5000 flask-app
    ```

    The `-p 5000:5000` option maps port 5000 of the container to port 5000 on your host machine.

2. Access your Flask application by navigating to `http://0.0.0.0:5000` in your web browser.
