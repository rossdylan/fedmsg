# This file is part of fedmsg.
# Copyright (C) 2012 Red Hat, Inc.
#
# fedmsg is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# fedmsg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with fedmsg; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  Ralph Bean <rbean@redhat.com>
#
from fedmsg.text.base import BaseProcessor

class WikiProcessor(BaseProcessor):
    def handle_subtitle(self, msg, **config):
        return any([
            target in msg['topic'] for target in [
                'wiki.article.edit',
                'wiki.upload.complete',
            ]
        ])

    def subtitle(self, msg, **config):
        if 'wiki.article.edit' in msg['topic']:
            user = msg['msg']['user']
            title = msg['msg']['title']
            url = msg['msg']['url']
            tmpl = self._('{user} made a wiki edit to "{title}".  {url}')
            return tmpl.format(user=user, title=title, url=url)
        elif 'wiki.upload.complete' in msg['topic']:
            user = msg['msg']['user_text']
            filename = msg['msg']['title']['mPrefixedText']
            description = msg['msg']['description'][:35]
            tmpl = self._(
                '{user} uploaded {filename} to the wiki: "{description}..."'
            )
            return tmpl.format(user=user, filename=filename,
                               description=description)
        else:
            raise NotImplementedError
