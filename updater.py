#!/usr/bin/env python3

import requests
import argparse


def create_cpanel(cpanel_user, cpanel_pass, cpanel_url, dns_domain, dns_sub):
    cpanel = {
        'url': cpanel_url + '/json-api/cpanel',
        'params': {
            'cpanel_jsonapi_user': cpanel_user,
            'cpanel_jsonapi_apiversion': '2',
            'cpanel_jsonapi_module': 'ZoneEdit',
            'domain': dns_domain,
            'name': dns_sub + '.' + dns_domain + '.'  # NB! note the dot at the end of full subdomain
        }, 
        'user': cpanel_user,
        'pass': cpanel_pass
    }
    
    return cpanel


def get_subdomain_property(cpanel, setting):
    params = cpanel['params']
    params['cpanel_jsonapi_func'] = 'fetchzone'
    
    response = requests.get(cpanel['url'], params, auth=(cpanel['user'], cpanel['pass']),  verify=True)
    
    result = response.json()['cpanelresult']['data'][0]['record']
    
    if result:
            return result[0][setting]
    
    return None


def edit_subdomain_address(cpanel, dns_line, dns_address):
    params = cpanel['params']
    params['cpanel_jsonapi_func'] = 'edit_zone_record'
    params['type'] = 'A'
    params['Line'] = dns_line
    params['address'] = dns_address
    
    requests.get(cpanel['url'], params, auth=(cpanel['user'], cpanel['pass']),  verify=True)


def get_ip_address():
    """
    Use external service to get IP address
    :return:
    """
    return requests.get('https://ipinfo.io/ip', verify=True).text


def main():
    parser = argparse.ArgumentParser(description="Dynamic DNS updater")
    parser.add_argument("-u",  "--username",  help="cPanel username")
    parser.add_argument("-p",  "--password",  help="cPanel password")
    parser.add_argument("domain",  help="Domain to be modified")
    parser.add_argument("sub_domain", nargs='+', help="List of sub-domain names to be updated (excluding the "
                                                      "qualified domain suffix). eg. hello.example.com would "
                                                      "simply translate to hello")
    parser.add_argument("url", help="cPanel URL e.g. https://example.com:2083")
    
    args = parser.parse_args()
    
    cpanel_user = args.username
    cpanel_pass = args.password
    cpanel_url = args.url
    dns_domain = args.domain
    dns_subs = args.sub_domain
    
    ip_address = get_ip_address()
    
    # Each subdomain shares the same address above
    for dns_sub in dns_subs:
        cpanel = create_cpanel(cpanel_user, cpanel_pass, cpanel_url, dns_domain, dns_sub)
        dns_address = get_subdomain_property(cpanel, 'address')
        
        # Check if IP address has changed
        if ip_address != dns_address:
            dns_line = get_subdomain_property(cpanel, 'line')
            edit_subdomain_address(cpanel, dns_line, ip_address)
        

if __name__ == '__main__':
    main()
