from novaclient import client


def get_client(keystone_session):
    """
    Get a nova client.

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    """
    nc = client.Client(version='2', session=keystone_session)
    return nc

def get_flavors(keystone_session):
    """
    Get a detailed list of flavors.

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    """
    nc = get_client(keystone_session)
    return nc.flavors.list()


def get_instances(keystone_session):
    """
    Get a detailed list of all the instances.

    Ref: http://developer.openstack.org/api-ref-compute-v2.1.html#listServers

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    """

    # len (all) == len(active) + len(error) + len(suspended) + len(shutoff)
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'SHUTOFF'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'ACTIVE'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'ERROR'})
    # nc.servers.list(search_opts={'all_tenants': 1, 'status': 'SUSPENDED'})
    # novaclient.v2.servers.Server

    nc = get_client(keystone_session)
    servers = nc.servers.list(search_opts={'all_tenants': 1})
    return servers


def get_vcpus(keystone_session, overcommit=5):
    """
    Get number of VCPUs consumed and total.

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.

    :param float overcommit: The overcommit ratio to use while printing the
                             VCPU stats.
    """
    nc = get_client(keystone_session)
    stats = nc.hypervisor_stats.statistics().to_dict()
    return (stats['vcpus_used'], stats['vcpus'] * overcommit)


def get_memory(keystone_session, overcommit=1.3):
    """
    Get memory available and total.

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.

    :param float overcommit: The overcommit ratio to use while printing the
                             memory stats.
    """
    nc = get_client(keystone_session)
    stats = nc.hypervisor_stats.statistics().to_dict()
    return (stats['memory_mb_used'], stats['memory_mb'] * overcommit)


def get_instance_count(keystone_session):
    """
    Get number of instances in the cluster.

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    """
    nc = get_client(keystone_session)
    stats = nc.hypervisor_stats.statistics().to_dict()
    return stats['running_vms']
