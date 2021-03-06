"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
from t0mm0.common.net import Net
import urllib2
import urlresolver
from urlresolver import common
from urlresolver.plugnplay.interfaces import UrlResolver
from urlresolver.plugnplay import Plugin

class TubeplusResolver(Plugin, UrlResolver):
    implements = [UrlResolver]
    name = "tubeplus.me"
    
    def __init__(self):
        self.net = Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        #get list
        try:
            html = self.net.http_GET(web_url).content
        except urllib2.URLError, e:
            common.addon.log_error('tubeplus: got http error %d fetching %s' %
                                    (e.code, web_url))
            return False
            
        r = '"none" href="(.+?)"'
        sources = []
        regex = re.finditer(r, html, re.DOTALL)

        for s in regex:
            sources.append(urlresolver.HostedMediaFile(url=s.group(1))) 
        
        source = urlresolver.choose_source(sources)
        
        if source:
            stream_url = source.resolve()
        else:
            stream_url = ''
        return stream_url


    def get_url(self, host, media_id):
        return 'http://tubeplus.me/player/%s/' % media_id
        
        
    def get_host_and_id(self, url):
        r = re.search('//(.+?)/player/(\d+)', url)
        if r:
            return r.groups()
        else:
            return False


    def valid_url(self, url, host):
        return re.match('http://(www.)?tubeplus.me/player/\d+', 
                        url) or 'tubeplus' in host

