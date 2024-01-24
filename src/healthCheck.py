import sys
import time
import yaml
import requests
import logging
import argparse
from urllib.parse import urlparse
import httpx
import asyncio


def read_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def check_health(endpoint, accept_config):
    try:
        response = requests.request(endpoint.get('method', 'GET'), endpoint['url'],
                                    headers=endpoint.get('headers'), data=endpoint.get('body'), timeout=accept_config['response_limit'] / 1000)
        return 200 <= response.status_code < 300
    except requests.RequestException:
        return False


async def async_check_health(endpoint, accept_config, availability, domain):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                endpoint.get('method', 'GET'),
                endpoint['url'],
                headers=endpoint.get('headers'),
                data=endpoint.get('body'),
                timeout=accept_config['response_limit'] / 1000
            )
            availability[domain]['total'] += 1
            if 200 <= response.status_code < 300:
                availability[domain]['up'] += 1

        except requests.RequestException:
            return False


def argument_init(args):
    endpoints = read_yaml(args.inputfile)
    config = read_yaml(args.configfile)
    domains = set([urlparse(endpoint['url']).netloc
                   for endpoint in endpoints])
    availability = {domain: {'up': 0, 'total': 0} for domain in domains}
    return endpoints, config, domains, availability


def availability_logger(availability, domains, logger):

    for domain in domains:
        up_percentage = (
            availability[domain]['up'] / availability[domain]['total']) * 100
        logger.info(
            f"{domain} has {up_percentage:.2f}% availability percentage")

    logger.info(
        f"------------------------------------------------------------")


async def async_main(args, logger):
    endpoints, config, domains, availability = argument_init(args)
    while True:
        sync_start = time.time()

        tasks = [async_check_health(
            endpoint, config['accept'], availability, urlparse(endpoint['url']).netloc) for endpoint in endpoints]
        await asyncio.gather(*tasks)

        availability_logger(availability, domains, logger)

        sync_end = time.time()
        # print(f"ASYNC: Time lapsed is: {sync_end - sync_start}")
        time.sleep(config['running_period'])


def main(args, logger):
    endpoints, config, domains, availability = argument_init(args)
    while True:
        sync_start = time.time()
        for endpoint in endpoints:
            is_up = check_health(endpoint, config['accept'])
            domain = urlparse(endpoint['url']).netloc
            availability[domain]['total'] += 1
            if is_up:
                availability[domain]['up'] += 1
            else:
                logger.debug(
                    f"[HEALTH CHECK DOWN] Endpoint name: {endpoint['name']}")

        availability_logger(availability, domains, logger)

        sync_end = time.time()
        # print(f"Time lapsed is: {sync_end - sync_start}")
        time.sleep(config['running_period'])


def handler():
    parser = argparse.ArgumentParser(
        prog='Health check tool',
        description='Check the health of different HTTP endpoints periodically.')

    parser.add_argument('--inputfile', type=str, default='sample.yaml',
                        help='The path of the YAML file with endpoints input. Default as sample.yaml')
    parser.add_argument('--configfile', type=str, default='config.yaml',
                        help='Configuration YAML file, including the running time period, acceptance criteria. Default as config.yaml')
    parser.add_argument('--outputfile', type=str, default='None',
                        help='The path of the output file. Default as stdout.')
    parser.add_argument('--nodebug', action='store_true',
                        help='Set True to deactivate output debug logging.')
    parser.add_argument('--ifasync', action='store_true',
                        help='Set True if run the script in async mode.')
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

    if not args.nodebug:
        handler_debug = logging.FileHandler("/tmp/debug.log")
        handler_debug.setLevel(logging.DEBUG)
        handler_debug.setFormatter(formatter)
        logger.addHandler(handler_debug)

    logger.addHandler(handler_info)
    if args.ifasync:
        logger.info(f"Running in Async mode...")
        asyncio.run(async_main(args, logger))
    else:
        logger.info(f"Running in Sync mode...")
        main(args, logger)


if __name__ == "__main__":
    handler()
