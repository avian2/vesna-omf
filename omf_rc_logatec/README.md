OmfRcLogatec
============

This package contains an OMF6 Resource Proxy for use with the VESNA Log-a-tec
testbed. Once installed, it registers a resource type ``cluster`` with the
resource controller.

Each ``cluster`` resource represents one cluster of VESNA sensor nodes. The
``cluster`` OMF resource replaces the usual ``node`` OMF resource in that it
can be used to create ``application`` resources. The applications used in this
way get information via environment on which cluster they are supposed to
operate.

Usage
-----

The usual way to use this package is to use the normal ``omf_rc`` resource
controller that comes in the ``omf_rc`` package. ``config.yaml`` should be
configured to load the ``omf_rc/resource_proxy/cluster`` factory and create as
many ``cluster`` resources as desired.
