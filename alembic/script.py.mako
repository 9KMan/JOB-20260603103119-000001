from alembic import context

target_metadata = None


def include_object(object, name, type_, *args):
    if type_ == 'table' and object.info.get('is_view'):
        return False
    return True