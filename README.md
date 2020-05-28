# mail2gg

Email to Google Group migration tool

It provides simple cli tools devised to support migrations or email imports to a Google Group:

- [imap2gg](#imap2gg)
- [mbox2gg](#mbox2gg)

It uses the [Groups Migration API](https://developers.google.com/admin-sdk/groups-migration/index), a `Google Developers Console project` with the `Google Groups service` enabled will be needed. For more information review the [prerequisites](https://developers.google.com/admin-sdk/groups-migration/v1/guides/prerequisites).

The first execution will start an [OAuth2 Google Authentication Flow](https://developers.google.com/identity/protocols/oauth2) to initialize and store your grants.

Highly inspired by https://gist.github.com/pecigonzalo/c147e3f174fca90bec66efbd9eb24ad3.

## Install

Just use pip to install it!

```
pip install mail2gg
```

## imap2gg

```
 __                        ______
|__|.--------.---.-.-----.|__    |.-----.-----.
|  ||        |  _  |  _  ||    __||  _  |  _  |
|__||__|__|__|___._|   __||______||___  |___  |
                   |__|           |_____|_____|
```

Import an IMAP mailbox to a Google Group

If `password` is not provided will prompt for it
`client_id` and `client_secret` are just needed the first time. The authorization file `.credentials` will be created and reused
Default query is 'ALL'. Examples: 'SEEN', 'UNSEEN'. See https://github.com/ikvk/imap_tools/blob/master/README.rst#search-criteria for more filters

Errors are logged to stdout and embeded into `error.mbox` file.

For more info run `$ imap2gg --help`

### Examples

- Import everything from my IMAP server

```
$ imap2gg example@googlegroups.com myimapserver.com example@myimapserver.com aPassword --client_id=11111111-asjdhasjdkhasdjkhasjkh12.apps.googleusercontent.com --client_secret=4JHsadhj23jhasdj
```

- Import everything from a gmail account

```
$ imap2gg another@googlegroups.com imap.gmail.com example@gmail.com aPassword --client_id=11111111-asjdhasjdkhasdjkhasjkh12.apps.googleusercontent.com --client_secret=4JHsadhj23jhasdj
```

- Import just unseen emails:

```
$ imap2gg another@googlegroups.com imap.gmail.com example@gmail.com aPassword --query='UNSEEN'
```

## mbox2gg

```
           __                 ______
.--------.|  |--.-----.--.--.|__    |.-----.-----.
|        ||  _  |  _  |_   _||    __||  _  |  _  |
|__|__|__||_____|_____|__.__||______||___  |___  |
                                     |_____|_____|
```

Import an mbox file to a Google Group

`client_id` and `client_secret` are just needed the first time. The authorization file `.credentials` will be created and reused

Errors are logged to stdout and embeded into `error.mbox` file.

For more info run `$ mbox2gg --help`

### Examples

- Import everything from mailbox.mbox to example@googlegroups.com

```
$ mbox2gg example@googlegroups.com mailbox.mbox --client_id=11111111-asjdhasjdkhasdjkhasjkh12.apps.googleusercontent.com --client_secret=4JHsadhj23jhasdj
```
