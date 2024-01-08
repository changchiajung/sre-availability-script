import sys
import time
import yaml
import requests
import logging
import argparse


class EndpointChecker:
    def __init__(self, endpoint, accept_config, logger):
        self.endpoint = endpoint
        self.accept_config = accept_config
        self.logger = logger
        self.domain = self.endpoint['url'].split(".com/")[0]
        self.availability = {'up': 0, 'total': 0}

    def check_health(self):
        try:
            response = requests.request(self.endpoint.get('method', 'GET'), self.endpoint['url'],
                                        headers=self.endpoint.get('headers'), data=self.endpoint.get('body'), timeout=self.accept_config['response_limit'] / 1000)
            return response.status_code in range(200, 300)
        except requests.RequestException:
            self.logger.debug(
                f"[HEALTH CHECK DOWN] Endpoint name: {self.endpoint['name']}")
            return False


def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def main(args, logger):
    endpoints = read_yaml(args.inputfile)
    config = read_yaml(args.configfile)
    domains = set([endpoint['url'].split(".com/")[0]
                  for endpoint in endpoints])
    availability = {domain: {'up': 0, 'total': 0} for domain in domains}
    endpoint_checkers = [EndpointChecker(
        endpoint, config['accept'], logger) for endpoint in endpoints]

    while True:
        for checker in endpoint_checkers:
            is_up = checker.check_health()
            if is_up:
                availability[checker.domain]["up"] += 1
            availability[checker.domain]["total"] += 1

        for domain in domains:
            up_percentage = (
                availability[domain]['up'] / availability[domain]['total']) * 100
            logger.info(
                f"{domain} has {up_percentage:.2f}% availability percentage")

        logger.info(
            "------------------------------------------------------------")
        time.sleep(config['running_period'])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Health check tool',
        description='Check the health of different HTTP endpoints periodically.')

    parser.add_argument('--inputfile', type=str, default='sample.yaml',
                        help='The path of the YAML file with endpoints input. Default as sample.yaml')
    parser.add_argument('--configfile', type=str, default='config.yaml',
                        help='Configuration YAML file, including the running time period, acceptance criteria. Default as config.yaml')
    parser.add_argument('--outputfile', type=str, default='None',
                        help='The path of the output file. Default as stdout.')
    args = parser.parse_args()

    logger = logging.getLogger('health_check_log')
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(levelname)s] %(asctime)s  %(message)s")

    if args.outputfile == "None":
        handler_info = logging.StreamHandler(sys.stdout)
    else:
        handler_info = logging.FileHandler(args.outputfile)

    handler_info.setLevel(logging.INFO)
    handler_info.setFormatter(formatter)

    handler_debug = logging.FileHandler("debug.log")
    handler_debug.setLevel(logging.DEBUG)
    handler_debug.setFormatter(formatter)

    logger.addHandler(handler_info)
    logger.addHandler(handler_debug)

    main(args, logger)
