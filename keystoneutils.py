from keystoneclient.auth.identity import v3
from keystoneclient import session as ksession
from keystoneclient.v3 import client


def get_auth(args=None, **kwargs):
    """Get the auth object to authenticate a session.
       Gathers information from args if passed, else from the keyword
       arguments.

       :param argparse.Namespace args: argparse.Namespace object obtained after
                                       parsing the commandline args containing
                                       the openstack variables.
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
    if args:
        os_auth_url = args.os_auth_url
        os_password = args.os_password
        os_username = args.os_username
        os_project_name = args.os_project_name
        if 'os_user_domain_id' in args:
            os_user_domain_id = args.os_user_domain_id
        else:
            os_user_domain_id = 'default'
        if 'os_project_domain_id' in args:
            os_project_domain_id = args.os_project_domain_id
        else:
            os_project_domain_id = 'default'
    else:
        if 'os_auth_url' in kwargs:
            os_auth_url = kwargs['os_auth_url']
        else:
            raise Exception('Key \'%s\' not found!!!' % 'os_auth_url')
        if 'os_password' in kwargs:
            os_password = kwargs['os_password']
        else:
            raise Exception('Key \'%s\' not found!!!' % 'os_password')
        if 'os_username' in kwargs:
            os_username = kwargs['os_username']
        else:
            raise Exception('Key \'%s\' not found!!!' % 'os_username')
        if 'os_project_name' in kwargs:
            os_project_name = kwargs['os_project_name']
        else:
            raise Exception('Key \'%s\' not found!!!' % 'os_project_name')
        if 'os_user_domain_id' in kwargs:
            os_user_domain_id = kwargs['os_user_domain_id']
        else:
            os_user_domain_id = 'default'
        if 'os_project_domain_id' in kwargs:
            os_project_domain_id = kwargs['os_project_domain_id']
        else:
            os_project_domain_id = 'default'

    auth = v3.Password(auth_url=os_auth_url,
                       password=os_password, username=os_username,
                       user_domain_id=os_user_domain_id,
                       project_name=os_project_name,
                       project_domain_id=os_project_domain_id)
    return auth


def get_session(args=None, os_auth=None):
    """Establish a session from the auth object to connect to the OpenStack
       services.
       Gathers information from args if passed, else from the auth object.

       :param argparse.Namespace args: argparse.Namespace object obtained after
                                       parsing the commandline args containing
                                       the openstack variables.
       :param keystoneclient.auth.identity.v3.Password os_auth: The auth object
                                                                to authenticate
                                                                the session
                                                                with.
    """
    if not os_auth:
        os_auth = get_auth(args)
    session = ksession.Session(auth=os_auth)
    return session


def get_client(os_auth_url, os_password, os_username, os_project_name):
    """Get a keystone client.
       :param string os_auth_url: Auth URL to use for OpenStack service access.
       :param string os_password: Password to use for OpenStack service access.
       :param string os_username: User name to use for OpenStack service
                                  access.
       :param string os_project_name: Project name to use for OpenStack service
                                      access.
    """
    os_auth = get_auth(os_auth_url, os_password, os_username, os_project_name)
    session = get_session(os_auth)
    keystone = client.Client(session=session)
    return keystone
