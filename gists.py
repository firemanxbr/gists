'''Gists CLI
'''
from argparse import ArgumentParser
from tabulate import tabulate

import json
import requests


'''Config
'''
API = 'https://api.github.com/'
GIT_IO = 'https://git.io/'

# NEED CHANGE
req = requests.get('https://api.github.com/gists')


def list_users_gists(user=None):
    req = requests.get('{0}users/{1}/gists'.format(API, user))

    if req.status_code == 200:
        headers = ['File', 'Size', 'URL', 'Description']

        rows = []

        for output in req.json():
            filename = list(output['files'].keys())[0]
            size = output['files'][filename]['size']
            url = output['html_url']

            gitio = requests.post('{0}create'.format(GIT_IO),
                                  {'url': '{0}'.format(url)}).text

            short_url = '{0}{1}'.format(GIT_IO, gitio)

            description = output['description']

            rows.append(['{0}'.format(filename),
                        '{0}'.format(size),
                        '{0}'.format(short_url),
                        '{0}{1}'.format(description[:30],'...')])

        if len(rows) == 0:
            return "Don't have gists for '{0}'".format(user)

        else:
            return tabulate(rows, headers, tablefmt='grid',
                            showindex='always',
                            numalign='center',
                            stralign='center')

    else:
        return "Don't found the user: '{0}''".format(user)


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
        print(list_users_gists(user=args.user[0]))


if __name__ == '__main__':
    main()
