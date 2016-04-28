import os
import sys
import argparse


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

    return p
