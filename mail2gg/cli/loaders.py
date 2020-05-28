from .. import ImapImporter, MboxImporter
from getpass import getpass


def imap_importer(google_group, imap_server, email, password=None, query='ALL', client_id=None, client_secret=None, **kwargs):
    """
    Import an IMAP mailbox to a Google Group

     __                        ______              
    |__|.--------.---.-.-----.|__    |.-----.-----.
    |  ||        |  _  |  _  ||    __||  _  |  _  |
    |__||__|__|__|___._|   __||______||___  |___  |
                       |__|           |_____|_____|

    If `password` is not provided will prompt for it
    `client_id` and `client_secret` are just needed the first time. The authorization file `.credentials` will be created and reused
    Default query is 'ALL'. Examples: 'SEEN', 'UNSEEN'. See https://github.com/ikvk/imap_tools/blob/master/README.rst#search-criteria for more filters

    Examples
    - Import everything from my IMAP server
    `$ imap2gg example@googlegroups.com myimapserver.com example@myimapserver.com aPassword --client_id=11111111-asjdhasjdkhasdjkhasjkh12.apps.googleusercontent.com --client_secret=4JHsadhj23jhasdj`

    - Import everything from a gmail account
    `$ imap2gg another@googlegroups.com imap.gmail.com example@gmail.com aPassword --client_id=11111111-asjdhasjdkhasdjkhasjkh12.apps.googleusercontent.com --client_secret=4JHsadhj23jhasdj`

    - Import just unseen emails:
    `$ imap2gg another@googlegroups.com imap.gmail.com example@gmail.com aPassword --query='UNSEEN'

    Errors are logged to stdout and embeded into `error.mbox` file.

    Issues and contributions to https://github.com/XaviTorello/mail2gg
    """

    if not password:
        password = getpass('Enter password: ')
    ImapImporter(
        group_id=google_group,
        server=imap_server,
        email=email,
        password=password,
        query=query,
        client_id=client_id,
        client_secret=client_secret,
        **kwargs,
    )


def mbox_importer(google_group, mbox, client_id=None, client_secret=None, **kwargs):
    """
    Import an mbox file to a Google Group

               __                 ______              
    .--------.|  |--.-----.--.--.|__    |.-----.-----.
    |        ||  _  |  _  |_   _||    __||  _  |  _  |
    |__|__|__||_____|_____|__.__||______||___  |___  |
                                         |_____|_____|

    `client_id` and `client_secret` are just needed the first time. The authorization file `.credentials` will be created and reused

    Examples
    - Import everything from mailbox.mbox to example@googlegroups.com
    `$ mbox2gg example@googlegroups.com mailbox.mbox --client_id=11111111-asjdhasjdkhasdjkhasjkh12.apps.googleusercontent.com --client_secret=4JHsadhj23jhasdj`

    Errors are logged to stdout and embeded into `error.mbox` file.

    Issues and contributions to https://github.com/XaviTorello/mail2gg
    """

    MboxImporter(
        group_id=google_group,
        mbox=mbox,
        client_id=client_id,
        client_secret=client_secret,
        **kwargs,
    )
