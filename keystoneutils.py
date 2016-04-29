from keystoneclient.auth.identity import v3
from keystoneclient import session as ksession
from keystoneclient.v3 import client


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
    auth = v3.Password(auth_url=v['os_auth_url'],
                       password=v['os_password'], username=v['os_username'],
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
