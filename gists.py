"""Gists CLI
"""
from argparse import ArgumentParser

import json
import requests


req = requests.get('https://api.github.com/gists')


def list_users_gists(user=None):
    req = requests.get('https://api.github.com/users/{0}/gists'.format(user))

    if req.status_code == 200:
        return req.json()
    else:
        return None


def main():
    '''
    gists CLI
    '''
    parser = ArgumentParser()
    parser.add_argument('-a', '--all', help="public gists",
                        action='store_true')
    parser.add_argument('-u', '--user', nargs=1,
                        help='List public gists for the specified user')
    args = parser.parse_args()

    if args.all:
        print(json.dumps(req.json(), sort_keys=True, indent=4))

    if args.user:

        query = list_users_gists(user=args.user[0])

        for output in query:
            filename = list(output['files'].keys())[0]
            url = output['html_url']
            description = output['description']
            print('File: \t\t{0}'.format(filename))
            print('Description: \t{0}'.format(description))
            print('URL: \t\t{0}\n'.format(url))


if __name__ == '__main__':
    main()
