from keystoneclient.auth.identity import v3
from keystoneclient import session as ksession
from keystoneclient.v3 import client


def get_auth(os_auth_url, os_password, os_username, os_project_name,
             os_user_domain_id='default', os_project_domain_id='default'):
    """Get the auth object to authenticate a session.

       :param string os_auth_url: Auth URL to use for OpenStack service access.
       :param string os_password: Password to use for OpenStack service access.
       :param string os_username: User name to use for OpenStack service access.
       :param string os_project_name: Project name to use for OpenStack service
                                      access.
       :param string os_user_domain_id: User Domain ID to use for OpenStack
                                        service access.
       :param string os_project_domain_id: Project Domain ID to use for
                                           OpenStack service access.
    """
    auth = v3.Password(auth_url=os_auth_url,
                       password=os_password, username=os_username,
                       user_domain_id=os_user_domain_id,
                       project_name=os_project_name,
                       project_domain_id=os_project_domain_id)
    return auth


def get_session(os_auth):
    """Establish a session from the auth object to connect to the OpenStack
       services.

       :param keystoneclient.auth.identity.v3.Password os_auth: The auth object
                                                                to authenticate
                                                                the session
                                                                with.
    """
    session = ksession.Session(auth=os_auth)
    return session


def get_client(os_auth_url, os_password, os_username, os_project_name):
    """Get a keystone client.

       :param string os_auth_url: Auth URL to use for OpenStack service access.
       :param string os_password: Password to use for OpenStack service access.
       :param string os_username: User name to use for OpenStack service access.
       :param string os_project_name: Project name to use for OpenStack service
                                      access.
    """
    os_auth = get_auth(os_auth_url, os_password, os_username, os_project_name)
    session = get_session(os_auth)
    keystone = client.Client(session=session)
    return keystone
