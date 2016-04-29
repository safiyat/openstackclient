#! /usr/bin/env python

import sys
from utils.parser import get_parser
import keystoneutils
from novaclient import client


def keystone_example():
    parser = get_parser()
    args = parser.parse_args()
    kclient = keystoneutils.get_client(os_auth_url=args.os_auth_url,
                                       os_password=args.os_password,
                                       os_username=args.os_username,
                                       os_project_name=args.os_project_name)
    print kclient.projects.list()


def nova_example():
    p = get_parser()
    args = p.parse_args()
    auth = keystoneutils.get_auth(os_auth_url=args.os_auth_url,
                                  os_username=args.os_username,
                                  os_password=args.os_password,
                                  os_project_name=args.os_project_name)
    sess = keystoneutils.get_session(auth)
    nc = client.Client(version=args.os_compute_api_version, session=sess)
    print nc.servers.list(search_opts={'all_tenants': 1})


def main():
    keystone_example()
    nova_example()


if __name__ == '__main__':
    sys.exit(main())
