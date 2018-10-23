# ansible-ambari-manager

[![Docker Pulls](https://img.shields.io/docker/pulls/oleewere/ansible-ambari-manager.svg)](https://hub.docker.com/r/oleewere/ansible-ambari-manager/)
[![](https://images.microbadger.com/badges/image/oleewere/ansible-ambari-manager.svg)](https://microbadger.com/images/oleewere/ansible-ambari-manager "")

## Requirements:

Update hostname on each host
see [Set the Hostname](https://docs.hortonworks.com/HDPDocuments/Ambari-2.2.1.0/bk_Installing_HDP_AMB/content/_set_the_hostname.html)

Install ansible (2.4.x -) 
```bash
pip install ansible
```
You can use docker as well:
```bash
# pull the docker image
docker pull oleewere/ansible-ambari-manager:latest
# or build it to yourself
docker build -t oleewere/ansible-ambari-manager:latest .
```

From that point you can use docker-compose or docker to run ansible commands like:
```bash
# use docker run
docker run --rm oleewere/ansible-ambari-manager:latest ansible -i hosts.sample ambari-server -m shell -a 'echo hello'
# or use with docker-compose (files are on volume)
docker-compose run ansible-ambari-manager ansible -i hosts.sample ambari-server -m shell -a 'echo hello'
```
 - Note 1.: the examples does not contain the docker or docker-compose prefixes. 
 - Note 2: `.env` file can be defined in the project folder, there you can set `SSH_KEYS_LOCATION`, which will be passed as a volume folder with the docker-compose command.
## Setup

Create an invertory file (based on hosts.sample) with proper hosts/variables which can be used for the playbooks.
Also make sure the default variables (group_vars/all) is redefined in your inventory file if it's required

Please use the right hostname for each hosts.

## Examples

### Run command on group
```bash
ansible -i hosts ambari-server -m shell -a "echo hello"
```

### Install 

install Ambari 2.7:
```bash
ansible-playbook -i hosts.sample playbooks/install-ambari-2_7.yml --extra-vars "ambari_build_number=103"
```

Install Ambari 2.7 to be run as non-root user:

```bash
ansible-playbook playbooks/install-ambari-2_7.yml --extra-vars "remote_ambari_server_user=ambari-server remote_ambari_agent_user=ambari-agent"
#  (`libselinux-python` may be required if using SELinux)
```

 Install Solr Metrics Sink mpack:
[AMS Solr Sink for Ambari Infra Solr](https://github.com/oleewere/ams-solr-metrics-mpack)
(not compatible with Ambari 2.7.0+, but metrics sink is built-in for Infra Solr from 2.7.0)

```bash
ansible-playbook -i hosts.sample playbooks/mpacks/install-infra-solr-metrics-mpack.yml
```

Install Solr Metrics Sink service/components:
```bash
ansible-playbook -i hosts.sample playbooks/mpacks/add-infra-solr-metrics-mpack.yml
```

Install Ambari from base repo url
```bash
# it will ask ambari_repo_base_url parameter with a prompt (value can be like: http://s3.amazonaws.com/dev.hortonworks.com/ambari/centos7/2.x/BUILDS/2.7.0.0-180)
ansible-playbook -i hosts.sample playbooks/install-ambari.yml
```

### Upgarde 

Upgarde Ambari (e.g.: 2.6.0.0 -> 3.0.0.0)
```bash
ansible-playbook -i hosts.sample playbooks/upgrade-ambari-packages.yml -v --extra-vars "ambari_base_url=http://s3.amazonaws.com/dev.hortonworks.com/ambari/centos6/3.x/BUILDS/3.0.0.0-1116 ambari_version=3.0.0.0 ambari_build_number=1116"
```

Upgarde Ambari - build number change only (2.6.0.0-102 -> 2.6.0.0-113)
```bash
ansible-playbook -i hosts.sample playbooks/upgrade-ambari-packages.yml -v --extra-vars "ambari_base_url=http://s3.amazonaws.com/dev.hortonworks.com/ambari/centos6/2.x/BUILDS/2.6.0.0-113 ambari_version=2.6.0.0 ambari_build_number=113 skip_ambari_server_upgrade_command=True"
```


### Install Ambari cluster with blueprint

```bash
ansible-playbook -i hosts.sample playbooks/blueprint/install-cluster.yml
```
Right now there are 2 host groups: master and slave, you can control those with 2 ansible groups like that:
```bash
[bp-master-host-group]
c6401.ambari.apache.org

[bp-slave-host-group]
c6402.ambari.apache.org
c6403.ambari.apache.org
```
You can specify the master and slave components as well with comma separated lists (ZOOKEEPER_SERVER for master and ZOOKEEPER_CLIENT for slave are defaults + Ranger added differently)
```bash
bp_master_components=INFRA_SOLR,INFRA_SOLR_CLIENT
bp_slave_components=INFRA_SOLR_CLIENT
```

### Upload

Upload local stack to remote (common-services and stack)
```bash
# required: local_ambari_location in inventory file
ansible-playbook -i hosts.sample playbooks/local/upload-stack.yml -v
```
Or you can upload only one service as well: (add stack_service var)
```bash
ansible-playbook -i hosts playbooks/local/upload-stack.yml -v --extra-vars "stack_service=AMBARI_INFRA"
```

 Upload local Ambari agent python files to remote

```bash
ansible-playbook -i hosts.sample playbooks/local/upload-ambari-agent-python.yml -v
```

### Restart an Ambari service

```bash
ansible-playbook -i hosts.sample playbooks/service/restart.yml --extra-vars "service_name=AMBARI_INFRA" -v
```

### Save internal hostname and public IP addresses file from GCE cluster
```bash
# save to out/gce_hostnames file with internal hostname ip address pairs (you can put that into /etc/hosts)
ansible-playbook -i hosts playbooks/gce/gce-get-hosts.yml -v --extra-vars="gce_cluster_name=mycluster"
# save to out/gce_hostname file with only internal hostnames (you can put that into your inventory file)
ansible-playbook -i hosts playbooks/gce/gce-get-hosts.yml -v --extra-vars="gce_cluster_name=perf-solr gce_only_internal_address=true"
# or you can just print a public address to one hostname
ansible-playbook -i hosts playbooks/gce/print-public-ip.yml --extra-vars="gce_cluster_name=mycluster gce_hostname=hostname.internal"
```


## Authentication examples

now only for centos


### Setup Kerberos:


```bash
ansible-playbook -i hosts.sample playbooks/setup-kerberos.yml --extra-vars "kerberos_domain_realm=ambari.apache.org"
```
### Install Ambari cluster with blueprint + kerberos

```bash
ansible-playbook -i hosts.sample playbooks/blueprint/install-secure-cluster.yml
```

Make sure you defined the following variables:
```bash
kerberos_realm=AMBARI.APACHE.ORG
kerberos_domain_realm=ambari.apache.org
kdc_hostname=c7401.ambari.apache.org
```

### Install Ambari cluster with blueprint + kerberos + Ranger

```bash
ansible-playbook -i hosts.sample playbooks/blueprint/install-ranger-cluster.yml
```
Note: Ranger Admin will be installed on Ambari Server host.

### Local kinit to access Kerberized Solr UI from browsers
```bash
# important parameters: (you can set as --extra-vars or in the inventory file)
# - kerberos_realm: kerberos realm (default: EXAMPLE.COM)
# - kerberos_domain_realm: kerberos domain realm (default: ambari.apache.org)
# - kdc_hostname: used as --kdc-hostname parameter in the kinit command
# - keytab_file_name: filename of the keytab (saved to /tmp/<keytab_file_name>)
# - kerberos_service_user: kerberos principal name part
# - kerberos_service_host: kerberos principal host part
# (note: make sure kinit group points to that host where the service running)

ansible-playbook -i hosts.sample playbooks/local-kinit.yml -v
```

### Ranger/Solr scale testing

#### Upload Ranger scripts (e.g.: to /opt/ranger)
First set the following params in your inventory files (or use them as extra-params):
```bash
ranger_zookeeper_quorum=localhost1:2181,localhost2:2181
ranger_sam_password=sam-password
ranger_tom_password=tom-password
ranger_admin_password=admin-password

ranger_admin_host=ranger_admin_hostname

ranger_kms_host=kms_hostname
ranger_kms_userlist=ambari-qa,hdfs,ranger

ranger_hive_host=hive_hostname
ranger_hive_userlist=hive,ambari-qa,hdfs

ranger_kafka_host=kafka_hostname
ranger_kafka_userlist=kafka

ranger_knox_host=knox_hostname

ranger_hbase_host=localhost
ranger_hbase_userlist=hbase

ranger_yarn_host=localhost
ranger_yarn_userlist=ambari-qa,yarn

ranger_scale_test_folder=/opt
```
Then you can run (on different hosts, if hive, kafka, kms etc. are on different hosts, you can set the host with ranger_scale_test_hostname, make sure that hostname is located in your inventory somewhere):
```bash
ansible-playbook -i hosts.sample playbooks/ranger/upload-ranger-scripts.yml --extra-vars "ranger_scale_test_hostname=selected_hostname"
```
Note: libselinux-python package is required on the remote machine to generate config.ini file

#### Start ranger python scripts 
```bash
ansible-playbook -i hosts.sample playbooks/ranger/start-ranger-command.yml --extra-vars "ranger_scale_test_hostname=selected_hostname ranger_command_type=kafka ranger_command_param_days=1 ranger_command_param_threads=1 ranger_command_param_executions=1000"
```
Note: make sure you will using the right host for `ranger_scale_test_hostname` (like if you will use kafka commands, kafka should exist on that host)

#### Stop running ranger python scripts
```bash
ansible-playbook -i hosts.sample playbooks/ranger/stop-ranger-command.yml --extra-vars "ranger_scale_test_hostname=selected_hostname ranger_command_type=kafka"
```
