import fire
from .loaders import imap_importer, mbox_importer


def execute_imap_importer():
    fire.Fire(imap_importer)


def execute_mbox_importer():
    fire.Fire(mbox_importer)
