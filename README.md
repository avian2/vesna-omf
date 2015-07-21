# VESNA OMF bits and pieces

This repository contains various bits and pieces required to setup [OMF][1]
with clusters of VESNA sensor nodes.

[1]: http://omf.mytestbed.net/projects/omf/wiki/OMF_Main_Page


## Installation

(Note: these instructions are for the testbed administrator. Normal testbed
users don't need to do any of this)

These instructions are based on [OMF 6 installation guide][2]. They have been
verified on Ubuntu 14.04 (Trusty Tahr) and OMF 6.2.2.

In the command-lines below, a hash sign (`#`) denotes commands that need to be
run as root. A dollar sign (`$`) denotes commands that can be run as a normal
user.

[2]: http://mytestbed.net/doc/omf/file.INSTALLATION.html

First install some Ubuntu packages that we will need later on. This also
installs the RabbitMQ server which is used for communication between OMF
components (it is available as `amqp://localhost` by default).

    # apt-get install ruby-dev build-essential libssl-dev git rabbitmq-server python-pip

### OMF Resource Controller

Install the OMF Resource Controller (note that the `install_omf_rc` command
overwrites any existing RC configuration).

    # gem install omf_rc --no-ri --no-rdoc
    # install_omf_rc -i -c

Install the Resource Proxies for accessing VESNA Log-a-tec-style testbeds.

    $ git clone FIXME
    $ cd vesna-omf/omf_rc_logatec
    $ gem build omf_rc_logatec.gemspec
    # gem install omf_rc_logatec-1.0.0.gem

Put the following configuration into `/etc/omf_rc/config.yaml`. This registers
two VESNA clusters with names  `lgt01` and `lgt02` with the OMF Resource
Controller.

    ---
    communication:
      url: amqp://localhost

    factories:
      load:
        - omf_rc/resource_proxy/cluster

    resources:
    - type: node
      uid: <%= Socket.gethostname %>
    - type: cluster
      uid: lgt01
    - type: cluster
      uid: lgt02

Start the resource controller.

    $ start omf_rc

To check that OMF Resource Controller works, you can query the properties of
one of the clusters. Note that this does not check whether any other component
works as well. OMF RC writes to a log at `/var/log/omf_rc.log` which might be
useful in debugging problems.

    $ omf_send_request -r amqp://localhost/lgt01
    lgt01
      supported_children_type: ["application"]
      uid: lgt01
      type: cluster
      membership: []
      child_resources: []
    -----------------

### Authentication proxy

Install the proxy server that handles request authentication between the
OMF/SFA and the VESNA ALH worlds.

    # cd vesna-omf/vesna_alhauthproxy
    # pip install .
    # pip install vesna-spectrumsensor
    # cp -i initrc /etc/init.d/vesna_alh_auth_proxy

Put the following configuration into `/etc/vesna_alh_auth_proxy.conf`. This
maps OMF resources `lgt01` and `lgt02` to ALH cluster IDs 10001 and 10002.

    log_file = "/var/log/vesna_alh_auth_proxy.log"

    socket = "/var/run/vesna_alh_auth_proxy.socket"
    pid_file = "/var/run/vesna_alh_auth_proxy.pid"

    clusters = {
        "lgt01": {
            "base_url": "https://crn.log-a-tec.eu/communicator",
            "cluster_id": 10001
        },
        "lgt02": {
            "base_url": "https://crn.log-a-tec.eu/communicator",
            "cluster_id": 10002
        }
    }

Now start the proxy

    # /etc/init.d/vesna_alh_auth_proxy start

You can check if it started successfully in its log file at
`/var/log/vesna_alh_auth_proxy.log`.

If the proxy doesn't start with errors referring to `urllib3`, it might be
necessary to upgrade it:

    # pip install -U urllib3

Finally, put ALH credentials for clusters mentioned in
`vesna_alh_auth_proxy.conf` into `/etc/alhrc`. Make sure the file is only
readable by root!

### OMF Experiment Controller

To install the OMF Experiment Controller:

    # gem install omf_ec --no-ri --no-rdoc


## Running an experiment

To test the OMF setup, the a simple experiment can be performed.

    $ cd vesna-omf/examples
    $ omf_ec oedl_hello.rb -- --cluster lgt02
    INFO	OML4R Client 2.10.6 [OMSPv4; Ruby 1.9.3] Copyright 2009-2014, NICTA
    Warning: OML4R: Missing values for parameter :domain (--oml-domain, OML_DOMAIN)! to instrument, so it will run without instrumentation. (see --oml-help)
    15:30:50  INFO OmfEc::Runner: OMF Experiment Controller 6.2.2 - Start
    15:30:50  INFO OmfEc::Runner: Connected using {:proto=>:amqp, :user=>"guest", :domain=>"127.0.0.1"}
    15:30:50  INFO OmfEc::Runner: Execute: /home/tsolc/vesna-omf/example/oedl_hello.rb
    15:30:50  INFO OmfEc::Runner: Properties: {:cluster=>"lgt02"}
    15:30:50  INFO OmfEc::ExperimentProperty: cluster = "lgt02" (String)
    15:30:50  INFO OmfEc::Experiment: Experiment: 2015-07-21T13:30:50.182Z starts
    15:30:50  INFO OmfEc::Experiment: CONFIGURE 1 resources to join group Actor
    15:30:50  INFO OmfEc::Experiment: TOTAL resources: 1. Events check interval: 1.
    15:30:51  INFO OmfEc::Experiment: Event triggered: 'ALL_NODES_UP, ALL_UP'
    15:30:52  INFO OmfEc::Experiment: Event triggered: 'Actor_application_fa173538-6af5-41bf-8b30-c612f4fdae04_created'
    15:30:52  INFO OmfEc: APP_EVENT STARTED from app fa173538-6af5-41bf-8b30-c612f4fdae04-7d937465-59a9-4c05-899d-dc9979488b63 - msg: env -i CLUSTER_UID='lgt02' python /home/tsolc/vesna-omf/example/hello.py 
    15:31:04  INFO OmfEc: APP_EVENT STDERR from app fa173538-6af5-41bf-8b30-c612f4fdae04-7d937465-59a9-4c05-899d-dc9979488b63 - msg: INFO:vesna.alh:     GET: hello?
    15:31:04  INFO OmfEc: APP_EVENT STDERR from app fa173538-6af5-41bf-8b30-c612f4fdae04-7d937465-59a9-4c05-899d-dc9979488b63 - msg: INFO:vesna.alh:response: Coordinator version 2.44
    15:31:04  INFO OmfEc: APP_EVENT STDOUT from app fa173538-6af5-41bf-8b30-c612f4fdae04-7d937465-59a9-4c05-899d-dc9979488b63 - msg: Coordinator version 2.44
    15:31:04  INFO OmfEc: APP_EVENT STDOUT from app fa173538-6af5-41bf-8b30-c612f4fdae04-7d937465-59a9-4c05-899d-dc9979488b63 - msg: 
    15:31:05  INFO OmfEc: APP_EVENT EXIT from app fa173538-6af5-41bf-8b30-c612f4fdae04-7d937465-59a9-4c05-899d-dc9979488b63 - msg: 0
    15:31:05  INFO OmfEc::Experiment: Event triggered: 'ALL_APPS_DONE'
    15:31:05  INFO OmfEc::Experiment: Experiment: 2015-07-21T13:30:50.182Z finished
    15:31:05  INFO OmfEc::Experiment: Exit in 15 seconds...
    15:31:16  INFO OmfEc::Experiment: Configure resources to leave Actor
    15:31:19  INFO OmfEc::Experiment: OMF Experiment Controller 6.2.2 - Exit.
    15:31:20  INFO OmfCommon: Disconnecting...

This queries the coordinator node of the selected cluster (`lgt02`) for its firmware version (`Coordinator version 2.44`).
