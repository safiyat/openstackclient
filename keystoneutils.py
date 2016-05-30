import sys
try:
    from keystoneclient.auth.identity import v3
    from keystoneclient import session as ksession
    from keystoneclient.v3 import client
except ImportError:
    from keystoneauth1 import loading
from utils import get_osvars, dict_to_args


def get_auth(args=None, **kwargs):
    """Get the auth object to authenticate a session.
       Gathers information from args if passed, else from the keyword
       arguments.

       :param argparse.Namespace args: argparse.Namespace object obtained after
                                       parsing the commandline args containing
                                       the openstack variables.
                                        OR
       :param string os_auth_url: Auth URL to use for OpenStack service access.
       :param string os_password: Password to use for OpenStack service access.
       :param string os_username: User name to use for OpenStack service
                                  access.
       :param string os_project_name: Project name to use for OpenStack service
                                      access.
       :param string os_user_domain_id: User Domain ID to use for OpenStack
                                        service access.
       :param string os_project_domain_id: Project Domain ID to use for
                                           OpenStack service access.
    """
    v = get_osvars(args, **kwargs)

    if 'keystoneauth1' in sys.modules:
        auth = loading.load_auth_from_argparse_arguments(dict_to_args(v))
    else:
        auth = v3.Password(auth_url=v['os_auth_url'],
                           password=v['os_password'],
                           username=v['os_username'],
                           user_domain_id=v['os_user_domain_id'],
                           project_name=v['os_project_name'],
                           project_domain_id=v['os_project_domain_id'])
    return auth


def get_session(args=None, **kwargs):
    """Establish a session from the auth object to connect to the OpenStack
       services.
       Gathers information from args if passed, else from the auth object.

       :param argparse.Namespace args: argparse.Namespace object obtained after
                                       parsing the commandline args containing
                                       the openstack variables.
                                        OR
       :param keystoneclient.auth.identity.v3.Password os_auth: The auth object
                                                                to authenticate
                                                                the session
                                                                with.
                                        OR
       :param string os_auth_url: Auth URL to use for OpenStack service access.
       :param string os_password: Password to use for OpenStack service access.
       :param string os_username: User name to use for OpenStack service
                                  access.
       :param string os_project_name: Project name to use for OpenStack service
                                      access.
    """
    if 'keystoneauth1' in sys.modules:
        v = get_osvars(args, **kwargs)
        args = dict_to_args(v)
        session = loading.load_session_from_argparse_arguments(args)
    else:
        if 'os_auth' in kwargs:
            os_auth = kwargs['os_auth']
        else:
            os_auth = get_auth(args, **kwargs)
        session = ksession.Session(auth=os_auth)
    return session


def get_client(args=None, **kwargs):
    """Get a keystone client.

       :param argparse.Namespace args: argparse.Namespace object obtained after
                                       parsing the commandline args containing
                                       the openstack variables.
                                        OR
       :param keystoneclient.session.Session session: Session object to
                                                      associate the client
                                                      with.
                                        OR
       :param keystoneclient.auth.identity.v3.Password os_auth: The auth object
                                                                to authenticate
                                                                the session
                                                                with.
                                        OR
       :param string os_auth_url: Auth URL to use for OpenStack service access.
       :param string os_password: Password to use for OpenStack service access.
       :param string os_username: User name to use for OpenStack service
                                  access.
       :param string os_project_name: Project name to use for OpenStack service
                                      access.
    """
    if 'session' in kwargs:
        session = kwargs['session']
    else:
        session = get_session(args, **kwargs)
    keystone = client.Client(session=session)
    return keystone
