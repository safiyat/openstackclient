from glanceclient import client


def get_client(keystone_session):
    """
    Get a glance client.

    :param keystoneclient.session.Session keystone_session: Session object to
                                                            associate the
                                                            client with.
    """
    gc = client.Client(version='2', session=keystone_session)
    return gc
