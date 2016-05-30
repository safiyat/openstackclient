"""Utility functions to access OpenStack API."""

import os
import argparse


def read_adminopenrc(path=None):
    """Read the OpenStack environment variables from the specified path."""
    if path is not None:
        if os.path.isdir(path):
            admin_openrc_path = os.path.join(path, 'admin-openrc.sh')
        else:
            admin_openrc_path = path
    else:
        admin_openrc_path = os.path.join(os.environ['HOME'], 'admin-openrc.sh')
        if os.path.isfile(admin_openrc_path) is False:
            admin_openrc_path = os.path.join('.', 'admin-openrc.sh')
    admin_openrc = open(admin_openrc_path).read()
    ENVIRON = {}
    for line in admin_openrc.splitlines():
        key, value = line.split()[1].split('=', 1)
        if value.startswith('\'') and value.endswith('\''):
            value = value[1:-1]
        elif value.startswith('\"') and value.endswith('\"'):
            value = value[1:-1]
        ENVIRON[key] = value
    return ENVIRON


def get_parser():
    '''Creates a parser to parse the OpenStack arguments'''
    p = argparse.ArgumentParser()
    p.add_argument('--os-username',
                   default=os.environ.get('OS_USERNAME'),
                   help='User name to use for OpenStack service access.')
    p.add_argument('--os-user-domain-id',
                   default=os.environ.get('OS_USER_DOMAIN_ID', 'default'),
                   help='User Domain ID to use for OpenStack service access.')
    p.add_argument('--os-password',
                   default=os.environ.get('OS_PASSWORD'),
                   help='Password to use for OpenStack service access.')
    p.add_argument('--os-tenant-name',
                   default=os.environ.get('OS_TENANT_NAME'),
                   help='Tenant name to use for OpenStack service access.')
    p.add_argument('--os-tenant-id',
                   default=os.environ.get('OS_TENANT_ID'),
                   help='Tenant ID to use for OpenStack service access.')
    p.add_argument('--os-project-name',
                   default=os.environ.get('OS_PROJECT_NAME'),
                   help='Project name to use for OpenStack service access.')
    p.add_argument('--os-project-domain-id',
                   default=os.environ.get('OS_PROJECT_DOMAIN_ID', 'default'),
                   help='Project Domain ID to use for OpenStack service '
                   'access.')
    p.add_argument('--os-region-name',
                   default=os.environ.get('OS_REGION_NAME'),
                   help='Region name to use for OpenStack service endpoints.')
    p.add_argument('--os-auth-url',
                   default=os.environ.get('OS_AUTH_URL'),
                   help='Auth URL to use for OpenStack service access.')
    p.add_argument('--os-image-api-version',
                   default=os.environ.get('OS_IMAGE_API_VERSION', '2'),
                   help='Image API version to use for OpenStack service '
                   'access.')
    p.add_argument('--os-volume-api-version',
                   default=os.environ.get('OS_VOLUME_API_VERSION', '2'),
                   help='Volume API version to use for OpenStack service '
                   'access.')
    p.add_argument('--os-compute-api-version',
                   default=os.environ.get('OS_COMPUTE_API_VERSION', '2'),
                   help='Compute API version to use for OpenStack service '
                   'access.')
    p.add_argument('--os-endpoint-type',
                   default=os.environ.get('OS_ENDPOINT_TYPE', 'publicURL'),
                   help='Type of endpoint in Identity service catalog to use '
                   'for communication with OpenStack services.')
    p.add_argument('--insecure',
                   default=os.environ.get('OS_INSECURE', False),
                   help='Use insecure SSL for communication.')
    p.add_argument('--os-cacert',
                   default=os.environ.get('OS_CACERT', None),
                   help='Specify a CA Cert, in case the cert is signed by an '
                   'unknown CA.')
    p.add_argument('--os-cert',
                   default=os.environ.get('OS_CERT', None),
                   help='Specify a Cert, in case the cert is signed by an '
                   'unknown CA.')
    p.add_argument('--os-key',
                   default=os.environ.get('OS_KEY', None),
                   help='')
    p.add_argument('--timeout',
                   default=os.environ.get('OS_TIMEOUT', 600),
                   help='Set request timeout (in seconds).')
    return p


def get_osvars(args=None, **kwargs):
    """Extract OpenStack variables from args or kwargs."""
    osvars = {}
    if args:
        osvars['os_auth_url'] = args.os_auth_url
        osvars['os_password'] = args.os_password
        osvars['os_username'] = args.os_username
        osvars['os_project_name'] = args.os_project_name
        if 'os_user_domain_id' in args:
            osvars['os_user_domain_id'] = args.os_user_domain_id
        else:
            osvars['os_user_domain_id'] = 'default'
        if 'os_project_domain_id' in args:
            osvars['os_project_domain_id'] = args.os_project_domain_id
        else:
            osvars['os_project_domain_id'] = 'default'
    elif kwargs:
        if 'os_auth_url' in kwargs:
            osvars['os_auth_url'] = kwargs['os_auth_url']
        else:
            raise Exception('Key "os_auth_url" not found!!!')
        if 'os_password' in kwargs:
            osvars['os_password'] = kwargs['os_password']
        else:
            raise Exception('Key "os_password" not found!!!')
        if 'os_username' in kwargs:
            osvars['os_username'] = kwargs['os_username']
        else:
            raise Exception('Key "os_username" not found!!!')
        if 'os_project_name' in kwargs:
            osvars['os_project_name'] = kwargs['os_project_name']
        else:
            raise Exception('Key "os_project_name" not found!!!')
        if 'os_user_domain_id' in kwargs:
            osvars['os_user_domain_id'] = kwargs['os_user_domain_id']
        else:
            osvars['os_user_domain_id'] = 'default'
        if 'os_project_domain_id' in kwargs:
            osvars['os_project_domain_id'] = kwargs['os_project_domain_id']
        else:
            osvars['os_project_domain_id'] = 'default'
    return osvars


def dict_to_args(d):
    args = argparse.Namespace()
    for key in d.keys():
        setattr(args, key, d[key])
    return args


def tuple2dict(keys, tuple):
    d = {}
    for key, value in zip(keys, tuple):
        d[key] = value
    return d


def get(list_of_dict, key, value):
    o = filter(lambda dictionary: dictionary.__dict__[key] == value,
               list_of_dict)
    return o
