# Online Clustering with DPGMMs

## Contents
- [What is this?](#what-is-this?)
  - [Overview](#overview)
  - [Components](#components)
- [Requirements](#requirements)
- [How to use](#how-to-use)
  - [Startup](#startup)
  - [Cleanup](#cleanup)
- [Software engineering backgroud](#software-engineering-background)
  - [Make](make)
  - [Docker](#docker)
  - [Kafka](#kafka)
- [Statistics background](#statistics-background)
  - [Finite mixture models and clustering](#finite-mixture-models-and-clustering)
  - [Dirichlet priors](#dirichlet-priors)
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
### Startup
With the requirements in place, you can...
1. Clone or download this repository.
2. Navigate to the project's root directory.
3. Use `make all` to start everything up.
4. Navigate to `localhost:5006` in your browser. Have fun!

Note that you may need to wait a few seconds between starting up the containers in step 3 and actually being able to access the webapp in step 4. Once you get to the plot, everything will be working, but you'll also need to be patient before the first points appear in the scatterplot.

### Cleanup
5. *You can kill all running containers with `docker kill $(docker ps -q)`.
6. *Delete all stopped containers with `docker rm $(docker ps -aq)`.
7. *Delete all images with `docker rmi $(docker image ls -q)`.

*If you're using Docker for other things as well, you probably ought not to run these commands. In this case, I assume that you already know a thing or two about Docker, and are capable of killing/deleting only those containers/images corresponding to this project yourself!

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
### Finite mixture models and clustering
In a **finite mixture model**, we view each data point as being a member of one of K **components**, where K is typically an integer chosen as a hyperparameter before fitting (but see below). In a Gaussian mixture like what we use here, data points are modeled as being normal/Gaussian distributed within each component. Therefore, the model has 3 sets of parameters that need to be estimated/learned:

1. The K **component weights**, which must sum to 1. In the generative process, you might imagine the i-th weight as the probability that a new data point comes from component i.
2. The K **mean vectors** of the normal distributions, one for each component.
3. The K **covariance matrices** of the normal distributions. Again, one for each component.

Finite mixture models are frequently used for clustering, because the clustering task can be viewed as determining which of the K components each data point came from. Indeed, the popular K-means algorithm taught in "Machine Learning 101" can be viewed as fitting a finite mixture model under the hood.

### Dirichlet priors
In a Bayesian setup, inference is performed by putting a **prior distribution** on the parameter vector in the model representing our "beliefs" about the parameter values. Bayes' rule is then used to get a **posterior distribution**, representing our beliefs about the parameter values after having seen the data.

Disregarding the mean and covariance parameters for now, the [**Dirichlet distribution**](https://en.wikipedia.org/wiki/Dirichlet_distribution) is the most commonly used distribution for the K-vector of component weights. They must be positive and sum to 1, and this is exactly what we'd get from a draw from the Dirichlet distribution. Moreover, because the Dirichlet distribution is **conjugate** in this case (specifically, conjugate to the underlying Categorical distribution representing each point's component), the posterior distribution resulting from Bayes' rule will also be a Dirichlet distribution, albeit with different parameters.

### Dirichlet process priors
When using a Dirichlet prior, it's possible to specify a K so large that not all of the components will have points in them. If you don't know the number of components ahead of time, specifying a large number of *potential components* can be beneficial because your model will be able to "determine for itself" how many clusters are appropriate. (Note that this only works when doing Bayesian inference; doing this with likelihood based approaches would result in the fitting procedure "choosing" to use as many components as possible).

Dirichlet process priors extend this logic to the extreme by setting K as infinity. The actual definition of a Dirichlet process is fairly involved (it requires graduate-level probability theory), but the essential points are that...
- We are using an infinite number of "potential components".
- All but a finite number of them will have no corresponding data points.
- We have computational tricks that allow us to only worry about a finite number of components.
- Even for a Dirichlet distribution with K = infinity, we still benefit from conjugacy with the (in this case, also infinite) Categorical distribution.

## Acknowledgements
- The Bokeh visualization was created with help from [Matthew Rocklin's blog](http://matthewrocklin.com/blog/work/2017/06/28/simple-bokeh-server). I essentially modified one of his examples to fit my project.
- Confluent's Kafka Python Client [GitHub](https://github.com/confluentinc/confluent-kafka-python) and associated [documentation](https://docs.confluent.io/current/clients/confluent-kafka-python/) were very helpful.
- [This blogpost from Krzysztof Żuraw](https://krzysztofzuraw.com/blog/2016/makefiles-in-python-projects.html) influenced me to start using Make in many of my projects to organize common tasks.
- When using Make, I ran into a problem for which phony targets were the answer. [This Stack Overflow question](https://stackoverflow.com/questions/2145590/what-is-the-purpose-of-phony-in-a-makefile) helped me understand them.
- Thanks to Spotify for creating an easy-to-use [Docker image for Kafka](https://hub.docker.com/r/spotify/kafka/). This saved me a lot of work!
- Gershman and Blei's [tutorial on Bayesian nonparametrics](https://arxiv.org/abs/1106.2697) was very helpful while trying to wrap my head around the fundamental concepts.
- Tamara Broderick's [ML Summer School 2015](https://www.youtube.com/watch?v=FUL1DcjOjwo) videos on Dirichlet processes are also highly recommended. My description of the large-K-but-still-finite Dirichlet distribution is basically stolen from these videos. This is the link to the first of 3 videos. (More generally, almost every MLSS video is probably useful for learning advanced ML and statistics concepts).
