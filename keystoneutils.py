from keystoneclient.auth.identity import v3
from keystoneclient import session as ksession
from keystoneclient.v3 import client


def get_auth():
    auth = v3.Password(auth_url='http://controller:35357/v3',
                       password='snapdeal@1234', username='osadmin',
                       user_domain_id='default', project_name='admin',
                       project_domain_id='default')
    return auth


def get_session(auth):
    session = ksession.Session(auth=auth)
    return session


def get_client():
    auth = get_auth()
    session = get_session(auth)
    keystone = client.Client(session=session)
    return keystone
