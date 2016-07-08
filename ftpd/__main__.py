#!/usr/bin/env python
import os
from ftpd import main


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.webapp.settings")
    main()
