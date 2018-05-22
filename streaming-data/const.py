
# Seriously, don't put a '/' at the end of the address, or ZeroMQ will not see
# the port number...
BISON = "tcp://pubsub.besteffort.ndovloket.nl:7658"


class Envelopes:
    KV6_RIG     = b"/RIG/KV6posinfo"
    KV6_ARR     = b"/ARR/KV6posinfo"
    KV6_CXX     = b"/CXX/KV6posinfo"
    KV6_DITP    = b"/DITP/KV6posinfo"
    KV6_EBS     = b"/EBS/KV6posinfo"
    KV6_GVB     = b"/GVB/KV6posinfo"
    KV6_QBUZZ   = b"/QBUZZ/KV6posinfo"
