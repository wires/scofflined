# wrapper around the python soundcloud API client
import sys
import time, random

import os
import json
import soundcloud
import requests

def log(wut):
    sys.stdout.write('\r%s' % wut)
    sys.stdout.flush()

class Abort(Exception):
    def msg(self):
        return self.args[0]
    def cause(self):
        return self.args[1]

class SoundcloudClient:
    def __init__(self, auth):
        self.client = soundcloud.Client(**auth)

        if not self.client:
            Abort("failed to login to soundcloud")

    def get_resource(self, s, **kwargs):
        """Retrieve a resource from the soundcloud api."""
        obj = self.client.get(s, **kwargs)

        # single resource
        if type(obj) == soundcloud.resource.Resource:
            return obj.fields()

        # list of resources
        return [r.fields() for r in obj]

    # page over list of resources
    # TODO use itertools!! do this lazy
    def rs(self, s, maximum=10**5, k=200):
        rs = []
        for i in range(0,maximum,k):
            r = self.get_resource(s,limit=k,offset=i)
            if(len(r)==0):
                break
            rs += r
            time.sleep(random.random() + 0.7);
            log("loading %s: %d" % (s, len(rs)))
            if len(rs) % k:
                break
            log("loaded %d items from %s\n" % (len(rs),s))
        return rs

    def stream(self, track_id):
        try:
            track = '/tracks/%d/stream' % track_id
            stream = self.get_resource(track, allow_redirects=False)
            r = requests.get(stream['location'], stream=True)
            return r.raw
        except HTTPError as e:
            raise Abort('error reading stream', e)

    def download(self, track, destdir):
        user = track['user']['permalink']
        track_id = track['id']
        fn = lambda ext: "%s/%s-%d.%s" % (destdir, user, track_id, ext)

        # filenames for audio and metadata target files
        audio = fn('mp3')
        meta = fn('meta.json')

        if nos.path.exists(audio):
            print("file already exists, skipping %s" % audio)
            return

        print("downloading %s" % audio)

        # save metadata
        with open(meta, 'w+') as f:
            json.dump(track, f)

        # save audio stream
        with open(audio, 'wb+') as f:
            f.write(self.stream(track_id).read())

    def my_groups(self):
        return self.get_resource('/me/groups')

    def pending(self, group):
        return self.client.rs('/groups/%d/pending_tracks' % group['id'])#,  maximum=300)
