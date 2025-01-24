# Docker and SQL Homework

## Question 1: Understanding Docker First Run

### Overview
the goal is to run a docker container using python 3.12.8 image in interactive mode, using `bash` shell as the entry point

### steps to solve 

1. pulled the python image (python: 3.12.8) and run the image interactively with the following command
-
```bash
docker run it --entrypoint bash python:3.12.8
```
2. **Check `pip` version**
  - run the following command inside the container
  ```bash
      pip  --version 
  ```
  - output: 
  ```
  pip 24.3.1 from /usr/local/lib/python3.12/site-packages/pip (python 3.12)

  ```
### output
**Answer** the version of `pip` in the `python:3.12.8` image is **24.3.1**