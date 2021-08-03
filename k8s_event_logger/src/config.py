# TODO: we can't combine denylist and allow list
NAMESPACE_DENYLIST = {'kube-system'}
NAMESPACE_ALLOWLIST = {''}
if NAMESPACE_DENYLIST & NAMESPACE_ALLOWLIST:  # Set intersection
    raise ValueError("NAMESPACE_DENYLIST cannot contain the same entries as NAMESPACE_ALLOWLIST")