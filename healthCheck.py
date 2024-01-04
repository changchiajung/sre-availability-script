import sys
import time
import yaml
import requests
import logging
import argparse


def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def check_health(endpoint, accept_config):
    try:
        response = requests.request(endpoint.get('method', 'GET'), endpoint['url'],
                                    headers=endpoint.get('headers'), data=endpoint.get('body'), timeout=accept_config['response_limit'] / 1000)
        return response.status_code in range(200, 300)
    except requests.RequestException:
        return False


def main(args, logger):
    endpoints = read_yaml(args.inputfile)
    config = read_yaml(args.configfile)
    domains = set([endpoint['url'].split(".com/")[0]
                  for endpoint in endpoints])
    availability = {domain: {'up': 0, 'total': 0} for domain in domains}
    while True:
        for endpoint in endpoints:
            is_up = check_health(endpoint, config['accept'])
            domain = endpoint['url'].split(".com/")[0]
            availability[domain]['total'] += 1
            if is_up:
                availability[domain]['up'] += 1
            else:
                logger.debug(
                    f"[HEALTH CHECK DOWN] Endpoint name: {endpoint['name']}")

        for domain in domains:
            up_percentage = (
                availability[domain]['up'] / availability[domain]['total']) * 100
            logger.info(
                f"{domain} has {up_percentage:.2f}% availability percentage")

        logger.info(
            f"------------------------------------------------------------")

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
