'''Gists CLI
'''
from argparse import ArgumentParser
from tabulate import tabulate

import requests
import sys


'''Config
'''
API = 'https://api.github.com/'
GIT_IO = 'https://git.io/'


def handle_data(request, message):

    if request.status_code == 200:
        headers = ['File', 'Size', 'short URL', 'Description']

        rows = []

        for output in request.json():
            filename = list(output['files'].keys())[0]
            size = output['files'][filename]['size']
            url = output['html_url']

            gitio = requests.post('{0}create'.format(GIT_IO),
                                  {'url': '{0}'.format(url)}).text

            short_url = '{0}{1}'.format(GIT_IO, gitio)

            if len(rows) == 0:
                print("+ creating short urls...")

            description = output['description']

            if description is None:
                description = '...'
            elif len(description) > 30:
                description = '{0}{1}'.format(output['description'][:30],
                                              '...')

            rows.append(['{0}'.format(filename),
                         '{0}'.format(size),
                         '{0}'.format(short_url),
                         '{0}'.format(description)])

        if len(rows) == 0:
            return message

        return tabulate(rows, headers, tablefmt='grid',
                        showindex='always',
                        numalign='center',
                        stralign='center')
    else:
        return message


def list_public_gists():
    req = requests.get('{0}gists/public'.format(API))
    msg = "Don't found any public gists!"
    return handle_data(request=req, message=msg)


def list_users_gists(user=None):
    req = requests.get('{0}users/{1}/gists'.format(API, user))

    if req.status_code == 404:
        return "Don't found the user '{0}'".format(user)

    msg = "Don't have gists for '{0}'".format(user)
    return handle_data(request=req, message=msg)


def list_starred_gists(user=None, passwd=None):
    req = requests.get('{0}gists/starred'.format(API),
                       auth=(user, passwd))

    if req.status_code == 401:
        return "Authentication problem: Unauthorized"

    msg = "Don't found any starred gists   !"
    return handle_data(request=req, message=msg)


def main():
    '''
    gists CLI
    '''
    parser = ArgumentParser()
    parser.add_argument('-a', '--all',
                        help="List the last 30 public gists sorted by most \
                              recently",
                        action='store_true')
    parser.add_argument('-u', '--username', nargs=1,
                        help='username for authentication OR select user \
                             to get gists from him')
    parser.add_argument('-p', '--password', nargs=1,
                        help='password for authentication')
    parser.add_argument('-s', '--starred',
                        help='List the authenticated user\'s starred gists',
                        action='store_true')
    args = parser.parse_args()

    if args.all:
        print(list_public_gists())

    if len(sys.argv) == 3 and args.username:
        print((list_users_gists(user=args.username[0])))

    if args.starred:
        if args.username and args.password:
            print(list_starred_gists(user=args.username[0],
                                     passwd=args.password[0]))
        else:
            print("Require authentication!")

    if len(sys.argv) == 1:
        print(parser.parse_args(['-h']))


if __name__ == '__main__':
    main()
