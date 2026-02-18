# Ansible Role: mongodb_install

[![CI](https://github.com/trfore/ansible-role-mongodb-install/actions/workflows/ci.yml/badge.svg)](https://github.com/trfore/ansible-role-mongodb-install/actions/workflows/ci.yml)
[![Prerelease](https://github.com/trfore/ansible-role-mongodb-install/actions/workflows/prerelease.yml/badge.svg)](https://github.com/trfore/ansible-role-mongodb-install/actions/workflows/prerelease.yml)
[![Galaxy Release](https://github.com/trfore/ansible-role-mongodb-install/actions/workflows/release.yml/badge.svg)](https://github.com/trfore/ansible-role-mongodb-install/actions/workflows/release.yml)

This role installs the MongoDB Community edition server metapackage, `mongodb-org`, via the OS's package manager. It currently defaults to `mongodb_version: 8.2.5`, while still allowing major/minor tracking (for example, `mongodb_version: 8.2`) or exact package pinning (for example, `mongodb_version: 8.2.5`), see 'Tested Platforms and Versions' section for a compatibility matrix.

See [Example Playbooks](#example-playbooks) for working examples. **The default settings do not configure the server**, it uses the default configuration values and minimal recommended `ulimit` settings. Its recommended to configure the server for production use, for details see: https://www.mongodb.com/docs/manual/administration/production-notes/

### Install the Role

You can install this role with the Ansible Galaxy CLI:

```bash
ansible-galaxy install trfore.mongodb_install
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy install -r requirements.yml`, using the format:

```yaml
---
roles:
  - name: trfore.mongodb_install
    version: v3.0.4 # optional

collections:
  # required when targeting CentOS & RHEL host
  - name: community.general
    source: https://galaxy.ansible.com

  # required if using Transparent HugePages, e.g. 'mongodb_security_authorization: enable'
  - name: community.mongodb
    source: https://galaxy.ansible.com
```

## Tested Platforms and Versions

### MongoDB Community `8.2.5`

- CentOS Stream 9
- Debian 12 & 13
- Ubuntu 22.04 & 24.04

### MongoDB Community `7.0.30`

- CentOS Stream 9
- Debian 11 & 12
- Ubuntu 22.04

### MongoDB Community `6.0.25` (EOL July 2025)

- CentOS Stream 9
- Debian 11
- Ubuntu 22.04

### MongoDB Community `5.0.31` (EOL October 2024)

- CentOS Stream 8
- Debian 10 & 11
- Ubuntu 20.04

### MongoDB Community `4.4.29` (EOL February 2024)

- CentOS Stream 8
- Debian 10
- Ubuntu 20.04

## Requirements

- `ansible-core>=2.17.0`

## Dependencies

- `community.general.yum_versionlock` required when targeting CentOS & RHEL host.
- `community.mongodb` required when `mongodb_security_authorization: enable`, [see detail below](#user-creation-variables).

  ```bash
  ansible-galaxy collection install community.general community.mongodb
  ```

## Role Variables

### Common Variables

Common variables are listed below, along with default values (see `defaults/main.yml`):

| Variable                                   | Default    | Description                                                                                               | Required  |
| ------------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------- | --------- |
| mongodb_version                            | `8.2.5`    | MongoDB Community stable releases `v4.4`, `v5`, `v6`, `v7`, `v8`                                          | No        |
| mongodb_version_maj                        | Automatic  | Extracts major value from `mongodb_version`                                                               | Automatic |
| mongodb_version_maj_minor                  | Automatic  | Extracts major and minor values from `mongodb_version`                                                    | Automatic |
| mongodb_transparent_hugepages_optimization | `false`    | Disable Transparent HugePages (THP) for MongoDB ≤ 7 or enable Transparent HugePages (THP) for MongoDB ≥ 8 | No        |
| mongodb_security_authorization             | `disabled` | MongoDB `authorization` setting in `mongod.conf`, e.g. `enabled` or `disabled`                            | No        |
| hostname                                   | ``         | Set the hostname for the MongoDB server (useful for some monitoring tools).                               | No        |

### Package Install Variables

`defaults/main.yml`:

| Variable              | Default          | Description                                                           | Required |
| --------------------- | ---------------- | --------------------------------------------------------------------- | -------- |
| mongodb_gpg_key       | URL              | MongoDB GPG Key                                                       | No       |
| mongodb_pkg_hold      | `true`           | Boolean, `true` to hold package version                               | No       |
| mongodb_pkg_hold_list | MongoDB Packages | List of MongoDB packages installed from `mongodb-org`, `v4.4` to `v7` | No       |

### User Creation Variables

Set these to automatically create users during provisioning. If `mongodb_security_authorization` is set to `enabled`, the users will be created after mongod starts (see `defaults/main.yml`).

| Variable                     | Default      | Description                                                     | Required |
| ---------------------------- | ------------ | --------------------------------------------------------------- | -------- |
| disable_logging_for_auth     | `false`      | Boolean, suppress auth info in Ansible output (e.g., passwords) | No       |
| mongodb_user_admin_name      | `UserAdmin`  | Administrative user name                                        | No       |
| mongodb_user_admin_password  | `passw01d`   | Administrative user password                                    | No       |
| mongodb_root_admin_name      | `RootAdmin`  | Root user name                                                  | No       |
| mongodb_root_admin_password  | `passw01d`   | Root user password                                              | No       |
| mongodb_root_backup_name     | `BackupUser` | Backup user name                                                | No       |
| mongodb_root_backup_password | `passw01d`   | Backup user password                                            | No       |
| mongodb_client_tls_enabled   | `false`      | Enable TLS for client-side auth/user/replica-set mongosh operations | No   |
| mongodb_client_tls_ca_file   | `""`         | CA file path used when `mongodb_client_tls_enabled: true`       | No       |
| mongodb_client_tls_cert_key_file | `""`     | Client certificate+key PEM used when mTLS is required           | No       |

### Replica Set Variables

Use these when deploying multi-node replica sets with this role.

| Variable                     | Default | Description                                                                 | Required |
| ---------------------------- | ------- | --------------------------------------------------------------------------- | -------- |
| mongodb_replica_set_enabled  | `false` | Boolean, enable replica set configuration                                   | No       |
| mongodb_replica_set_name     | `rs0`   | Replica set name written to `mongod.conf`                                   | No       |
| mongodb_replica_set_topology | `pss`   | Replica set topology, one of `pss` or `psa`                                 | No       |
| mongodb_replica_set_members  | `[]`    | Data-bearing members in `host:port` format                                  | Yes\*    |
| mongodb_replica_set_arbiter  | `""`    | Arbiter member in `host:port` format, required when topology is `psa`       | Yes\*\*  |
| mongodb_replica_set_initiator_host | `""` | Optional inventory hostname where `rs.initiate`/`rs.reconfig` is executed | No       |

\* Required when `mongodb_replica_set_enabled: true`  
\*\* Required when `mongodb_replica_set_enabled: true` and `mongodb_replica_set_topology: psa`

### Systemd Resource Limits

`defaults/main.yml`:

| Variable                          | Default | Description           | Required |
| --------------------------------- | ------- | --------------------- | -------- |
| mongodb_systemd_unit_limit_nofile | `64000` | File descriptor limit | No       |
| mongodb_systemd_unit_limit_nproc  | `64000` | Process count limit   | No       |

### Other OS Specific Variables

`vars/debian.yml`:

| Variable              | Default                             | Description                                           | Required |
| --------------------- | ----------------------------------- | ----------------------------------------------------- | -------- |
| mongodb_path_db       | `/var/lib/mongodb`                  | PATH, MongoDB database folder                         | No       |
| mongodb_path_log      | `/var/log/mongodb`                  | PATH, MongoDB log folder                              | No       |
| mongodb_dependencies  | `["libcurl4","openssl","liblzma5"]` | Required packages for MongoDB                         | No       |
| mongodb_pkg_hold_list | MongoDB Packages                    | List of MongoDB packages installed from `mongodb-org` | No       |

`vars/redhat.yml` and `vars/redhat_mongo_v{4-8}.yml`:

| Variable              | Default                 | Description                                           | Required |
| --------------------- | ----------------------- | ----------------------------------------------------- | -------- |
| mongodb_path_db       | `/var/lib/mongo`        | PATH, MongoDB database folder                         | No       |
| mongodb_path_log      | `/var/log/mongodb`      | PATH, MongoDB log folder                              | No       |
| mongodb_dependencies  | `["openssl","xz-libs"]` | Required packages for MongoDB                         | No       |
| mongodb_pkg_hold_list | MongoDB Packages        | List of MongoDB packages installed from `mongodb-org` | No       |

## Example Playbooks

- Package install via distribution's package manager.

```yaml
- hosts: servers
  become: true
  roles:
    - name: Install MongoDB
      role: trfore.mongodb_install
```

- Replica set topology examples

  Client certificate authentication for node bootstrap is optional and disabled by default. Set `mongodb_client_tls_enabled: true` and provide `mongodb_client_tls_ca_file` (and `mongodb_client_tls_cert_key_file` when required) to enable it.

```yaml
# PSS (3 data-bearing members)
- hosts: mongo_nodes
  become: true
  vars:
    mongodb_security_authorization: "enabled"
    mongodb_replica_set_enabled: true
    mongodb_replica_set_name: rs0
    mongodb_replica_set_topology: pss
    mongodb_replica_set_members:
      - "mongo1.example.com:27017"
      - "mongo2.example.com:27017"
      - "mongo3.example.com:27017"
  roles:
    - role: trfore.mongodb_install
```

```yaml
# PSA (2 data-bearing members + 1 arbiter)
- hosts: mongo_nodes
  become: true
  vars:
    mongodb_security_authorization: "enabled"
    mongodb_replica_set_enabled: true
    mongodb_replica_set_name: rs0
    mongodb_replica_set_topology: psa
    mongodb_replica_set_members:
      - "mongo1.example.com:27017"
      - "mongo2.example.com:27017"
    mongodb_replica_set_arbiter: "mongo-arbiter.example.com:27017"
  roles:
    - role: trfore.mongodb_install
```

```yaml
- hosts: servers
  become: true
  vars:
    mongodb_version: "8.2.5"
  roles:
    - name: Install MongoDB
      role: trfore.mongodb_install
```

- With authorization, user creation, and THP settings

```yaml
- hosts: servers
  become: true
  vars:
    hostname: "mongodb-test"
    mongodb_version: "8.2.5"
    mongodb_net_bindip: "127.0.30.1"
    mongodb_net_port: "27017"

    mongodb_user_admin_name: main-admin
    mongodb_user_admin_password: "mainpassw01d"

    mongodb_root_admin_name: root-admin
    mongodb_root_admin_password: "rootpassw01d"

    mongodb_root_backup_name: backup-user
    mongodb_root_backup_password: "backuppassw01d"

    mongodb_security_authorization: "enabled"
    disable_logging_for_auth: true

    mongodb_systemd_unit_limit_nofile: 64000
    mongodb_systemd_unit_limit_nproc: 64000

    # In MongoDB 8.0 and later, ensure that THP is enabled before mongod starts by creating a service file for your platform's initialization system. If you are using MongoDB 7.0 or earlier, disable THP.
    mongodb_transparent_hugepages_optimization: true

    # Example of how to add a custom configuration to the mongod.conf file (experimental)
    mongodb_config:
      processManagement:
        fork: false
      systemLog:
        verbosity: 0
  roles:
    - name: Install MongoDB
      role: trfore.mongodb_install
```

## License

This Ansible role is MIT.

MongoDB Community is Server Side Public License software from MongoDB, Inc. For additional information see: https://www.mongodb.com/licensing/server-side-public-license

## Contributors

- [trfore](https://github.com/trfore) - original author and maintainer

Special thanks to all those who have [contributed to the project](https://github.com/trfore/ansible-role-mongodb-install/graphs/contributors)!
Interested in adding a feature or fixing a bug? Checkout the [contributing guide](CONTRIBUTING.md).

## Related Roles & Playbooks

| Github                         | Ansible Galaxy           |
| ------------------------------ | ------------------------ |
| [ansible-role-jsvc]            | [trfore.jsvc]            |
| [ansible-role-mongodb-install] | [trfore.mongodb_install] |
| [ansible-role-omada-install]   | [trfore.omada_install]   |

## References

### MongoDB

- <https://www.mongodb.com/docs/manual/release-notes/>
- <https://www.mongodb.com/download-center/community/releases>
- <https://www.mongodb.com/docs/manual/administration/install-on-linux/>
- <https://www.mongodb.com/docs/manual/administration/production-notes/>
- <https://www.mongodb.com/docs/manual/reference/configuration-options/>
- <https://www.mongodb.com/docs/manual/reference/ulimit/>
- [MongoDB Docs: Disabling Transparent Hugepages (THP) for MongoDB 7 or Earlier]
- [MongoDB Docs: Enabling Transparent Hugepages (THP) for MongoDB 8]

[ansible-role-jsvc]: https://github.com/trfore/ansible-role-jsvc
[trfore.jsvc]: https://galaxy.ansible.com/trfore/jsvc
[ansible-role-mongodb-install]: https://github.com/trfore/ansible-role-mongodb-install
[trfore.mongodb_install]: https://galaxy.ansible.com/trfore/mongodb_install
[ansible-role-omada-install]: https://github.com/trfore/ansible-role-omada-install
[trfore.omada_install]: https://galaxy.ansible.com/trfore/omada_install
[MongoDB Docs: Enabling Transparent Hugepages (THP) for MongoDB 8]: https://www.mongodb.com/docs/manual/administration/tcmalloc-performance/
[MongoDB Docs: Disabling Transparent Hugepages (THP) for MongoDB 7 or Earlier]: https://www.mongodb.com/docs/manual/tutorial/disable-transparent-huge-pages/
