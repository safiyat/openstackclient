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
