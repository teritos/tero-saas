ABOUT ME
========

This module provides a FTP Server implementation that lets clients:
    - List files
    - Write files
    - Change directory

It'll fire an event when a file is written complete or incomplete.
For example, you can configure a security camera to upload photos
(using motion detection) to this FTP server, so it will:
    - Store photos from further review
    - Fire an event telling a new photo was uploaded, what means,
      a motion event in the security camera was detected.


RUN
---

Just execute:
    $_: ./manage.py run_ftpd


CONFIGURE
---------

You can modify 'saas/settings.py' the following settings:
FTPD_PORT = 2121                FTPD server will listen in this port
FTPD_ROOT = '/path/to/dir'      All FTPD users will be created 
                                under this path
