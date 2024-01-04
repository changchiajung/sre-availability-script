<a name="readme-top"></a>

[![LinkedIn][linkedin-shield]][linkedin-url]
<h3 align="center">HTTP Endpoints Health Check tool</h3>

<div>
  <p align="center">
    A configurable tool for checking HTTP endpoints' health.
    <br />
    <br />
    <a href="https://fetch-hiring.s3.us-east-1.amazonaws.com/site-reliability-engineer/health-check.pdf"><strong>Tool specification »</strong></a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

To acquire the availability of the web service, it is useful to send multiple HTTP requests to various HTTP endpoints and check the connection status. However, it is time-consuming to repeat this work manually.

In this project, we build a configurable tool that can automatically send HTTP requests to designed HTTP endpoints periodically and calculate the cumulative availability percentage for each domain.

To maximize the usage of this tools, we designed these configuration file that can be modified or extended.

- inputfile (e.g. sample.yaml):
  - A yaml file that contains various HTTP endpoints.
  - Each HTTP endpoint element in the YAML list has the following schema:
    - **name (string, required)** — A free-text name to describe the HTTP endpoint.
    - **url (string, required)** — The URL of the HTTP endpoint.
      - You may assume that the URL is always a valid HTTP or HTTPS address.
    - **method (string, optional)** — The HTTP method of the endpoint.
      - If this field is present, you may assume it’s a valid HTTP method (e.g. GET, POST, etc.).
      - If this field is omitted, the default is GET.
    - **headers (dictionary, optional)** — The HTTP headers to include in the request.
      - If this field is present, you may assume that the keys and values of this dictionary are strings that are valid HTTP header names and values.
      - If this field is omitted, no headers need to be added to or modified in the HTTP request.
    - **body (string, optional)** — The HTTP body to include in the request.
      - If this field is present, you should assume it's a valid JSON-encoded string. You do not need to account for non-JSON request bodies.
      - If this field is omitted, no body is sent in the request.
- configfile (e.g. config.yaml):
  - A yaml file that contains the configuration of this automation tool.
  - Available configuration:
    - running_period: The period between availability test.
    - accept: The acceptance criteria of the connection.
      - response_limit: The limit of response time (ms).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- [![Python][python-shield]][python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To use this tool, it will need an environment that are able to run python script and installed with required python packages.

### Run on local machine

#### Prerequisites

- Python3 +

#### Install the required packages

- ```bash
   pip3 install -r requirements.txt
  ```

#### Usage

##### Run without the parameter, used sample.yaml as input and logging on stdout

- ```bash
   python3 healthCheck.py
  ```

##### Run with the parameter, used inputfile as input and logging in outputfile

- ```bash
    python3 healthCheck.py --inputfile ${inputfile} --configfile ${configfile} --outputfile ${outputfile}
  ```

### Run with Docker container

Replace the health_check with the image name you would like to used.

Build the image from the Dockerfile

- ```bash
    docker build -t health_check .
  ```

Run a container with the image created by previous command, then the script will run the tool automatically.

- ```bash
    docker run health_check
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Chia-Jung - https://www.linkedin.com/in/chiajungchang-ron/ - rabbit20058@gmail.com

Profile Link: [https://changchiajung.github.io/](https://changchiajung.github.io/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/chiajungchang-ron/
[python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[docker-shield]: https://img.shields.io/badge/docker-3670A0?style=for-the-badge&logo=docker&logoColor=ffdd54
[docker-url]: https://www.docker.org/
