# Online Clustering with DPGMMs
This repo is still a **work in progress** and **does not yet** work as advertised! This README is also unfinished, and my explanations of various things are frequently either lacking or nonexistent.

## Contents
- [What is this?](#what-is-this?)
  - [Overview](#overview)
  - [Components](#components)
- [Requirements](#requirements)
- [How to use](#how-to-use)
- [Software engineering backgroud](#software-engineering-background)
  - [Make](make)
  - [Docker](#docker)
  - [Kafka](#kafka)
- [Statistics background](#statistics-background)
  - [Mixture models and clustering](#mixture-models-and-clustering)
  - [Dirichlet process priors](#dirichlet-process-priors)
- [Acknowledgements](#acknowledgements)

## What is this?
### Overview
This project is a demonstration of online clustering with streaming data. "Online" here is used in the sense of "online algorithms": Rather than fitting the model in one go on a single batch of data, the model is continuously updated as new data come in. I use mock data fed through a Kafka cluster to simulate a "real software environment", and provide a real-time visualization of the incoming data and their assigned clusters. In addition, everything's containerized and Dockerific!

### Components
This project consists of three services running in Docker containers. The data moves through the containers as follows:
1. Mock data producer
2. Kafka broker
3. Clusterer + webapp server

## Requirements
This project currently assumes...
- You are using some kind of Linux.
- Make and Docker are installed.
- You can use Docker commands [as a non-root user](https://docs.docker.com/install/linux/linux-postinstall/).
- Ports 2181, 5006, and 9092 are free.

If you can help remove some of these requirements, please contribute! :D

## How to use
With the requirements in place, you can...
1. Clone or download this repository.
2. Navigate to the project's root directory.
3. Use `make all` to start everything up.
4. Navigate to `localhost:5006` in your browser. Have fun!
5. You can kill all running containers with `docker kill $(docker ps -q)$`.
6. The images will also take up space on your computer until you delete them.

If you're running other containers and don't want to kill everything, I assume that you already know a thing or two about Docker, and are capable of deleting only those containers corresponding to this project yourself!

## Software engineering background
This project makes use of several pieces of technology which may not be familiar to many data scientists.
### Make
[GNU Make](https://www.gnu.org/software/make/) is a shell program used to execute commands defined in a [makefile](Makefile) (frequently just called "Makefile"). These commands consist of (possibly multiple) standard shell commands, and can also be defined in terms of other commands from the makefile. So, for example, when you run `make test-command` from within the project's root directory, an `echo` command will trigger and print a happy message. If this is your first time using Make, be sure to look inside the [makefile](Makefile) so you know exactly how `make` knows to run that `echo`.

Running `make` by itself will by default run the first command defined in the makefile; it is therefore the same as running `make all` for this repo. The `all` command is itself defined to be the three `run-*` commands defined later in the makefile.

### Docker
[Docker](https://www.docker.com/) enables you to use **containers**, which are basically lightweight virtual machines. Docker has become very popular in the operations space because it allows for clear specifications of program requirements and isolation of different application components.

Containers are built from **images** which are specified in **Dockerfiles**. For example, my [data producer Dockerfile](producer/Dockerfile) builds on top of the `python:latest` image (which comes from the [Docker Hub](https://hub.docker.com/_/python/)). You can see that I use `pip` to upgrade itself, then install the `confluent-kafka` and `scipy` packages.

### Kafka
[Apache Kafka](https://kafka.apache.org/) is, according to its website, a "distributed streaming platform". What that basically means is that Kafka is designed to help programs that produce a continuous stream of data connect with those that consume those streams. This can be done with traditional databases, but for large enough projects, you may encounter problems both organization- and performance-wise.

## Statistics background
### Mixture models and clustering

### Dirichlet process priors

## Acknowledgements
- The Bokeh visualization was created with help from [Matthew Rocklin's blog](http://matthewrocklin.com/blog/work/2017/06/28/simple-bokeh-server). I essentially modified one of his examples to fit my project.
- Confluent's Kafka Python Client [GitHub](https://github.com/confluentinc/confluent-kafka-python) and associated [documentation](https://docs.confluent.io/current/clients/confluent-kafka-python/) were very helpful.
- [This blogpost from Krzysztof Żuraw](https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html) influenced me to start using Make in many of my projects to organize common tasks.
- When using Make, I ran into a problem for which phony targets were the answer. [This Stack Overflow question](https://stackoverflow.com/questions/2145590/what-is-the-purpose-of-phony-in-a-makefile) helped me understand them.
- Thanks to Spotify for creating an easy-to-use [Docker image for Kafka](https://hub.docker.com/r/spotify/kafka/). This saved me a lot of work!
