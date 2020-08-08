import praw
import pdb
import re
import os
from datetime import datetime as dt
from psaw import PushshiftAPI

reddit = praw.Reddit('bot1')
api = PushshiftAPI(reddit)
subreddit = reddit.subreddit("pythonforengineers")

def num_posts(date, args):
	posts = list(api.search_submissions(after = date, q = args, subreddit = 'pythonforengineers'))
	return len(posts)

if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
else:
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

for comment in subreddit.stream.comments():
	if comment.id not in posts_replied_to:
		if re.search("maidenbot!", comment.body, re.IGNORECASE):
			args = comment.body.split()
			del args[0]
			date = dt.strptime(args[-1], '%d/%m/%Y')
			del args[-1]
			#num_posts = num_posts(date, args)
			comment.reply("There have been " + str(num_posts(date, args)) + " post(s) that contain the words" + str(args) + "since" + str(date))
			print("Bot replying to: ", comment.body)
			posts_replied_to.append(comment.id)
		with open("posts_replied_to.txt", "w") as f:
			for post_id in posts_replied_to:
				f.write(post_id + "\n")




	