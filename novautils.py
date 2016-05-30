from . import keystoneutils
from .. import datetimeutils
from . import mysqlwrapper
from novaclient import client
from .. import parser


def get_flavors(keystone_session=None):
    """
    Get a detailed list of flavors.
    """
    if keystone_session is None:
        p = parser.get_parser()
        args = p.parse_args()
        keystone_session = keystoneutils.get_session(args)
    nc = client.Client(version='2', session=keystone_session)
    return nc.flavors.list()


def get_instances_created(keystone_session, from_date, till_date):
    """
    Get a detailed list of the instances created from from_date to till_date.

    Ref: http://developer.openstack.org/api-ref-compute-v2.1.html#listServers

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    :param datetime.datetime from_date: The date from when to list the
                                        instances.
                                        Default: today
    :param datetime.datetime till_date: The date till when to list the
                                        instances.
                                        Default: today
    """

    # len (all) == len(active) + len(error) + len(suspended) + len(shutoff)
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'SHUTOFF'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'ACTIVE'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'ERROR'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'SUSPENDED'})
    # novaclient.v2.servers.Server

    nc = client.Client(version='2', session=keystone_session)
    servers = nc.servers.list(search_opts={'all_tenants': 1})

    cservers = []
    for server in servers:
        cdate = datetimeutils.parse_date(server.created, strftime=False)
        cdate = cdate.replace(tzinfo=None)
        if cdate >= from_date and cdate <= till_date:
            cservers.append(server)

    return cservers


def get_instances_deleted(keystone_session, from_date, till_date):
    """
    Get a detailed list of the instances deleted from from_date to till_date.

    Ref: http://developer.openstack.org/api-ref-compute-v2.1.html#listServers

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    :param datetime.datetime from_date: The date from when to list the
                                        instances.
    :param datetime.datetime till_date: The date till when to list the
                                        instances.
    """
    # nc = client.Client(version='2', session=keystone_session)
    # nc.servers.list(search_opts={'all_tenants': 1})

    dservers_mysql = mysqlwrapper.get_instances_mysql(
        deleted_at_FROM=from_date.date().isoformat(),
        deleted_at_TO=till_date.date().isoformat())
    return dservers_mysql


def get_instances(keystone_session=None, from_date=None, till_date=None):
    """
    Get a detailed list of the instances created and deleted from from_date to
    till_date.

    Ref: http://developer.openstack.org/api-ref-compute-v2.1.html#listServers

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    :param string from_date: The date from when to list the instances.
                             eg. 04-25-2016, 3d, 6w
                             Default: today
    :param string till_date: The date till when to list the instances.
                             eg. 04-25-2016, 3d, 6w
                             Default: today
    """

    # len (all) == len(active) + len(error) + len(suspended) + len(shutoff)
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'SHUTOFF'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'ACTIVE'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'ERROR'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'SUSPENDED'})
    # novaclient.v2.servers.Server
    # novaclient.v2.flavors.Flavor
    # nc.networks.list()
    # nc.flavors.list()

    if keystone_session is None:
        p = parser.get_parser()
        args = p.parse_args()
        keystone_session = keystoneutils.get_session(args)

    if from_date is None:
        from_date = datetimeutils.today(strftime=False)
    else:
        from_date = datetimeutils.parse_date(from_date, strftime=False)

    if till_date is None:
        till_date = datetimeutils.today(strftime=False)
    else:
        till_date = datetimeutils.parse_date(till_date, strftime=False)

    if from_date > till_date:
        raise Exception("FROM date is greater than TILL date!!!")

    cservers = get_instances_created(keystone_session, from_date, till_date)
    dservers = get_instances_deleted(keystone_session, from_date, till_date)
    return cservers, dservers


def get_vcpus(keystone_session=None, overcommit=5):
    """
    Get number of vcpus consumed and total.
    """
    if keystone_session is None:
        p = parser.get_parser()
        args = p.parse_args()
        keystone_session = keystoneutils.get_session(args)
    nc = client.Client(version='2', session=keystone_session)
    stats = nc.hypervisor_stats.statistics().to_dict()
    return (stats['vcpus_used'], stats['vcpus'] * overcommit)


def get_memory(keystone_session=None, overcommit=1.3):
    """
    Get memory available and total.
    """
    if keystone_session is None:
        p = parser.get_parser()
        args = p.parse_args()
        keystone_session = keystoneutils.get_session(args)
    nc = client.Client(version='2', session=keystone_session)
    stats = nc.hypervisor_stats.statistics().to_dict()
    return (stats['memory_mb_used'], stats['memory_mb'] * overcommit)


def get_instance_count(keystone_session=None):
    """
    Get number of instances in the cluster.
    """
    if keystone_session is None:
        p = parser.get_parser()
        args = p.parse_args()
        keystone_session = keystoneutils.get_session(args)
    nc = client.Client(version='2', session=keystone_session)
    stats = nc.hypervisor_stats.statistics().to_dict()
    return stats['running_vms']

