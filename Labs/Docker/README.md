# docker

## Part 1: Introduction to docker
In this first part of the lab you will build and run your first docker.

### Step 1: Introduction to Docker
- Docker is a platform that enables developers to easily create, deploy, and run applications in containers.
- Containers are isolated environments that contain everything an application needs to run, including the code, runtime, system tools, libraries, and settings.
### Step 2: Installing Docker
- Docker is available for Windows, macOS, and various Linux distributions.
- To install Docker on your system, follow the instructions for your operating system at this URL: https://docs.docker.com/engine/install/
- You can also use docker installed on one of the compute nodes of the cluster. If you are going this route please tell your TA beforehand so he can enable docker for you
### Step 3: Running your first Docker container
- To verify that Docker is installed and running correctly, run the following command in your terminal: docker run hello-world
- This command downloads and runs the “hello-world” image from the Docker hub, which displays a message indicating that Docker is installed and working correctly.
### Step 4: Creating a Docker container
- To create a Docker container, you'll first need to download an image from the Docker hub or create your own.
- For this lab, we'll use the Ubuntu image. To download and run the image, run the following command: 

```
docker run -it ubuntu
```

- The -it flag specifies that we want to run the container interactively and allocate a TTY for the container process.

### Step 5: Exploring the Docker container
- You are now inside the Docker container and have a  shell prompt.
- Try running some Linux commands to familiarize yourself with the environment.
- To exit the container, type exit at the prompt.

### Step 6: Stopping and removing containers
- To stop a running Docker container, run the following command: docker stop [container_id]
- To remove a stopped Docker container, run the following command: docker rm [container_id]

## Part 2: Building a website
In the next part of the lab you will build a very simple website.  This will teach you how port mapping and directory mapping work in docker.

### Step 1: Setting up the development environment

- To set up a development environment using Docker, we'll need to create a Docker container with all the tools and libraries required to build a website.
- For this lab, we'll use a pre-built image that contains the required tools. To download and run the image, run the following command:

```
docker run -it --name website-dev -v $(pwd)/web:/app -p 8080:80 node:14 bash
```

- The -it flag specifies that we want to run the container interactively and allocate a TTY for the container process.
- The --name flag assigns a name to the container for easy identification.
- The -v flag maps the current directory to /app in the container. This allows us to access our code from within the container.
- The -p flag maps port 8080 on the host to port 80 in the container, allowing us to access our website from a web browser.
- The last part of the command specifies the image to use, in this case, node:14.

### Step 2: Building the website

- You are now inside the Docker container and have a shell prompt.
- To create the code for our website, run the following commands:
```
cd /app
mkdir website
cd website
touch index.html
touch style.css
touch script.js
```

- The first line changes to the /app directory, which is mapped to the current directory on the host.
- The next three lines create a new directory for our website, change to that directory, and create three files for our HTML, CSS, and JavaScript code.

### Step 3: Writing the code
- Open the index.html file using your preferred text editor and add the following code:

```
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="style.css">
  </head>
  <body>
    <h1>My Website</h1>
    <p>Welcome to my website!</p>
    <script src="script.js"></script>
  </body>
</html>
```
- Open the style.css file and add the following code:

```
body {
  font-family: Arial, sans-serif;
  text-align: center;
}
```
- Open the script.js file and add the following code:

```
console.log("Hello, world!");
```
### Step 4: Running the website

- To run the website, you'll need to serve the HTML file using a web server. There are many options for serving HTML files, but for this lab, we'll use a simple HTTP server.
- To start the HTTP server, run the following command in the terminal
```
npx http-server . -p 80
```
- The npx command runs the http-server package, which serves the current directory on port 80.
- Open a web browser and navigate to http://localhost:8080. You should see the website you just built, displaying the text "My Website" and "Welcome to my website!".

### Step 5: Stopping the container
- To stop the container, you can use the exit command or type CTRL + D.
- To restart the container, run the following command:
```
docker start -ai website-dev
```
Congratulations! You have successfully built a website using Docker! In this lab, you learned how to set up a development environment using Docker, build a simple website using HTML, CSS, and JavaScript, and run the website using a web server.


## Part 3:  Introduction to dockerfiles

Docker containers are normally built from Dockerfiles. Dockerfiles contain a step by step instructions on how to build the desired environment.

### Step 1: Creating a Dockerfile
- Create a new directory for the project and navigate to that directory in the terminal.
- Create a new file in the directory named Dockerfile without an extension.
- Add the following lines to the Dockerfile:


```
FROM jupyter/base-notebook:latest
RUN pip install scikit-learn
```

- The first line specifies the base image to use, in this case, the jupyter/base-notebook image with the latest tag.
- The second line runs the pip command to install the scikit-learn package.

### Step 2: Building the Docker image
To build the Docker image, run the following command in the terminal:

```
docker build -t jupyter-scikit-learn .
```

- The -t flag specifies the name and tag to give the image, in this case, jupyter-scikit-learn.
- The . at the end of the command specifies the context, which is the current directory.

### Step 3: Running the Jupyter Notebook
To run the Jupyter Notebook, run the following command in the terminal:

```

docker run -it -p 8888:8888 -v $(pwd)/jupyter:/app -v $(pwd)/user:/home/jovyan jupyter-scikit-learn
```

- The -it flag specifies that we want to run the container interactively and allocate a TTY for the container process.
- The -p flag maps port 8888 on the host to port 8888 in the container, allowing us to access the Jupyter Notebook from a web browser.
- The first -v flag maps the current subdirectory jupyter  to /app in the container. This allows us to access our code from within the Jupyter Notebook.
- The second -v flag maps the current subdirectory user to /home/jovyan in the container. By default notebooks are run in the /home/jovyan directory of the container. We are mapping the user directory to that directory so we can save our notebook files.
- The last part of the command specifies the image to use, in this case, jupyter-scikit-learn.

### Step 4: Using scikit-learn in the Jupyter Notebook

- Open a web browser and navigate to http://localhost:8888. You should see the Jupyter Notebook login page.
- Enter the token displayed in the terminal to log in.
- Once you are logged in, create a new Jupyter Notebook by clicking on the "New" button in the top right corner and selecting "Python 3".
In the new Jupyter Notebook, run the following code to test scikit-learn:

```
import sklearn
print(sklearn.__version__)
```

- The output should show the version of scikit-learn that is installed in the Jupyter Notebook.

### Part 5: Get creative

Use what you’ve learned to make your own notebook environment using packages you commonly use day to day. Store your new dockerfile in a directory called my_notebook and create a notebook to test it.

You now know how to create a notebook environment that you can use anywhere!

