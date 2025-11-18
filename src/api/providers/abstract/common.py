def session_provider():
    raise NotImplementedError


def redis_pool_provider():
    raise NotImplementedError


def redis_db_provider():
    raise NotImplementedError


def hasher_provider():
    raise NotImplementedError


def tm_provider():
    """
    This is transaction manager provider
    """
    raise NotImplementedError


def fm_provider():
    """
    This is files manager provider
    """
    raise NotImplementedError


def notification_email_provider():
    raise NotImplementedError
