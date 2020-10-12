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

def process_args(args):
	if re.search("title:", args):
		title_index = args.index("title:")
	if re.search("body:", args):
		body_index = args.index("body:")
	title_args = args[title_index:body_index]
	body_args = args[-body_index:]



if not os.path.isfile("posts_replied_to.txt"):
	posts_replied_to = []
else:
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")
		posts_replied_to = list(filter(None, posts_replied_to))

for comment in subreddit.stream.comments():
	if comment.id not in posts_replied_to:
		if re.search("knowledgebot!", comment.body, re.IGNORECASE):
			args = comment.body.split()
			bot_index = args.index("knowledgebot!")
			del args[:bot_index+1]
			if 'last:' in args:
				num_index = args.index("last:") + 1
				numPosts = int(args[num_index])
			date_index = [i for i, item in enumerate(args) if re.search(r'(\d+/\d+/\d+)', item)]
			del args[date_index[0]+1:]
			date = dt.strptime(args[-1], '%d/%m/%Y')
			del args[-1]
			posts = list(api.search_submissions(after = date, q = args, subreddit = 'pythonforengineers'))
			reply = "There have been " + str(len(posts)) + " post(s) that contain the words " + str(args) + " since " + str(date)
			if 'numPosts' in globals():
				reply = reply + "\nThe last " + str(numPosts) + " are as follows:"
				posts_sublist = posts[:numPosts]
				for submission in posts_sublist:
					reply = reply + "\n[" + str(submission.title)+ "]" + "(" + str(submission.permalink) + ")\n"
			comment.reply(reply)
			print("Bot replying to: ", comment.body)
			posts_replied_to.append(comment.id)
		with open("posts_replied_to.txt", "w") as f:
			for post_id in posts_replied_to:
				f.write(post_id + "\n")




	