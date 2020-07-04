# Inspired and adapted from https://gist.github.com/pecigonzalo/c147e3f174fca90bec66efbd9eb24ad3

import argparse
import mailbox
import io
import apiclient
import httplib2
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

from imap_tools import MailBox
from tqdm import tqdm


class BaseImporter:
    """
    Base definition of an importer that points to Google Group
    """

    def __init__(self, group_id, *args, **kwargs):
        self.group_id = group_id

        self.client_id = kwargs.get('client_id')
        self.client_secret = kwargs.get('client_secret')

        scope = 'https://www.googleapis.com/auth/apps.groups.migration'
        storage = Storage('.credentials')
        credentials = storage.get()

        if not credentials or credentials.invalid:
            # Request client id and secret if not ready
            if not self.client_id:
                self.client_id = input('Enter client_id: ')
            if not self.client_secret:
                self.client_secret = input('Enter client_secret: ')

            flow = client.OAuth2WebServerFlow(
                self.client_id, self.client_secret, scope
            )

            parser = argparse.ArgumentParser(
                description=__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                parents=[tools.argparser])
            flags, unknown = parser.parse_known_args()
            credentials = tools.run_flow(flow, storage, flags)

        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('groupsmigration', 'v1', http=http)

        # By default list all available emails
        self.query = kwargs.get('query', 'ALL')
        # self.query = Q(seen=False)

        # Create the error mbox
        self.error_mbox = mailbox.mbox('errors.mbox')

    def push_to_group(self, msg_string):
        """
        Push a new msg to the Google Group
        """
        stream = io.BytesIO()
        stream.write(msg_string)

        # Prepare the encoded rfc822 message
        media = apiclient.http.MediaIoBaseUpload(
            stream, mimetype='message/rfc822'
        )

        # Submit and validate the import
        response = self.service.archive().insert(
            groupId=self.group_id, media_body=media
        ).execute()
        assert response.get('responseCode') == 'SUCCESS'
        assert response.get('kind') == 'groupsmigration#groups'

    def handle_error(self, error, uid, msg_string):
        self.error_mbox.add(msg_string)

    def show_errors(self):
        for an_email in self.error_mbox:
            print(
                f"Error processing {an_email.get('Message-ID')}",
                f"'{an_email.get('Subject')}'",
            )


class ImapImporter(BaseImporter):
    """
    Import from an IMAP server to a Google Group
    """

    def __init__(self, group_id, server, email, password, *args, **kwargs):
        super().__init__(group_id,  *args, **kwargs)
        self.server = server
        self.email = email
        self.password = password
        self.process()

    def count_elements(self, remote_mailbox):
        """
        Perform a request to the IMAP server to get all emails instead of 
        inspect the generator
        """
        charset = 'utf-8'
        _, ids = remote_mailbox.box.search(
            charset, remote_mailbox._criteria_encoder(self.query, charset)
        )
        return len(ids[0].split())

    def process(self):
        """
        Try to connect to the IMAP server, and try process all matched emails
        """
        try:
            with MailBox(self.server).login(
                self.email, self.password
            ) as remote_mailbox:
                count = self.count_elements(remote_mailbox)
                if (count == 0):
                    print(
                        "There are'nt emails to be processed",
                        f"with query '{self.query}'"
                    )
                    return

                for an_email in tqdm(
                    remote_mailbox.fetch(self.query),
                    total=count,
                    desc='Processing emails'
                ):
                    try:
                        an_email_str = an_email.obj.as_string().encode('utf-8')
                        self.push_to_group(an_email_str)
                    except Exception as e:
                        self.handle_error(e, an_email.uid, an_email_str)

                self.show_errors()

        except Exception as e:
            print(f"Error while interacting with the IMAP SERVER: '{e}'")


class MboxImporter(BaseImporter):
    """
    Import from a mbox file to a Google Group
    """

    def __init__(self, group_id, mbox, *args, **kwargs):
        super().__init__(group_id,  *args, **kwargs)
        # TODO Validate if file exists
        self.incoming_mbox = mailbox.mbox(mbox)
        self.process()

    def process(self):
        for an_email in tqdm(
            self.incoming_mbox,
            desc='Processing emails',
        ):
            try:
                an_email_str = an_email.as_string().encode('utf-8')
                self.push_to_group(an_email_str)
            except Exception as e:
                self.handle_error(e, an_email.get('Message-ID'), an_email_str)

        self.show_errors()
