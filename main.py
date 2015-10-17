import sys
from util import pp, select
from sc import SoundcloudClient, Abort

# loads config file
from config import auth


# login or report error
try:
    client = SoundcloudClient(auth)
except Abort as a:
	print(a.msg())
	sys.exit(1)

def ppr(s):
	"""pretty result of executing the soundcloud API request s"""
	pp(client.r(s))

group = client.my_groups()[0]

pp(select(group, ["name","id"]))

t = "artwork_url,bpm,comment_count,genre,id,playback_count,tag_list,title"
t = t.split(',')

for track in client.pending(group):
    try:
        pp(select(track,t))
        client.download(track, "pending")
    except Abort as a:
        print(a.msg())
        print(a.cause())
        print("skipping track %s" % track['title'])
