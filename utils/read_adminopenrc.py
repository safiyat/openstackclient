import os


def read_adminopenrc(path=None):
    """Read the OpenStack environment variables from the specified path.

       If the path is a directory, the file admin-openrc.sh inside the
       directory is read.
       If the path is not specified, the current working directory is searched
       for admin-openrc.sh. If not found, the admin-openrc.sh in HOME directory
       is used.

       :param string path: Path to the admin-openrc file.
    """
    if path is not None:
        path = os.path.abspath(os.path.expanduser(path))
        if os.path.isdir(path):
            admin_openrc_path = os.path.join(path, 'admin-openrc.sh')
        else:
            admin_openrc_path = path
    else:
        admin_openrc_path = os.path.join('.', 'admin-openrc.sh')
        if os.path.isfile(admin_openrc_path) is False:
            admin_openrc_path = os.path.join(os.environ['HOME'],
                                             'admin-openrc.sh')

    admin_openrc = open(admin_openrc_path).read()

    OS_ENVIRON = {}
    for line in admin_openrc.splitlines():
        key, value = line.split()[1].split('=')
        if value.startswith('\'') and value.endswith('\''):
            value = value[1:-1]
        elif value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        OS_ENVIRON[key] = value

    return OS_ENVIRON
