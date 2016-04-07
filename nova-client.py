#! /usr/bin/env python

import os
from argparse import Namespace
from keystoneauth1 import loading
from novaclient import client
from novaclient import api_versions


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
    admin_openrc=open(admin_openrc_path).read()
    ENVIRON={}
    for line in admin_openrc.splitlines():
        key, value = line.split()[1].split('=')
        ENVIRON[key] = value
    return ENVIRON


env = read_adminopenrc()
args = Namespace()

args.bypass_url=''
args.debug=False
if 'OS_ENDPOINT_TYPE' in env:
    args.endpoint_type=env['OS_ENDPOINT_TYPE']
else:
    args.endpoint_type='publicURL'

args.help=False
args.insecure=False
args.os_auth_system=''
args.os_auth_type='password'
if 'OS_AUTH_URL' in env:
    args.os_auth_url=env['OS_AUTH_URL']
else:
    args.os_auth_url='http://controller:35357/v3'

args.os_cacert=None
args.os_cache=False
args.os_cert=None
args.os_compute_api_version='2.latest'
args.os_default_domain_id=None
args.os_default_domain_name=None
args.os_domain_id=None
args.os_domain_name=None
args.os_key=None
if 'OS_PASSWORD' in env:
    args.os_password=env['OS_PASSWORD']
else:
    args.os_password=''

if 'OS_PROJECT_DOMAIN_ID' in env:
    args.os_project_domain_id=env['OS_PROJECT_DOMAIN_ID']
else:
    args.os_project_domain_id='default'

args.os_project_domain_name=None
args.os_project_id=''
if 'OS_PROJECT_NAME' in env:
    args.os_project_name=env['OS_PROJECT_NAME']
else:
    args.os_project_name='admin'

args.os_region_name=''
if 'OS_TENANT_NAME' in env:
    args.os_tenant_name=env['OS_TENANT_NAME']
else:
    args.os_tenant_name=None

args.os_trust_id=None
if 'OS_USER_DOMAIN_ID' in env:
    args.os_user_domain_id=env['OS_USER_DOMAIN_ID']
else:
    args.os_user_domain_id='default'

args.os_user_domain_name=None
args.os_user_id=None
if 'OS_USERNAME' in env:
    args.os_username=env['OS_USERNAME']
else:
    args.os_username='osadmin'

args.service_name=''
args.service_type=None
args.timeout=600
args.timings=False
args.volume_service_name=''

keystone_session = (loading.load_session_from_argparse_arguments(args))
keystone_auth = (loading.load_auth_from_argparse_arguments(args))


cs = client.Client(api_versions.APIVersion("2.0"), env['OS_USERNAME'],
                   env['OS_PASSWORD'], env['OS_PROJECT_NAME'], tenant_id='',
                   user_id=None, auth_url=env['OS_AUTH_URL'], insecure=False,
                   region_name='', endpoint_type=env['OS_ENDPOINT_TYPE'],
                   extensions=[], service_type='compute', service_name='',
                   auth_system='', auth_plugin=None, auth_token=None,
                   volume_service_name='', timings=False, bypass_url='',
                   os_cache=False, http_log_debug=False, cacert=None,
                   timeout=600, session=keystone_session, auth=keystone_auth)

cs.servers.list()
cs.flavors.list()
