import os

from github import Github, GithubException
from github.GithubObject import NotSet


def get_environment():
    """
    Get required environment variables.
    """
    env_is_ok = True
    github_user = os.environ.get('GITHUB_USER')
    if github_user is None:
        print('GITHUB_USER not found')
        print('Add \'export GITHUB_USER="username"\' to your .bashrc')
        env_is_ok = False
    api_token = os.environ.get('GITHUB_API_TOKEN')
    if api_token is None:
        print('GITHUB_API_TOKEN not found')
        print('Add \'export GITHUB_API_TOKEN"=api_token"\' to your .bashrc')
        env_is_ok = False
    if not env_is_ok:
        return None

    print(github_user, api_token)
    return github_user, api_token

get_environment()
