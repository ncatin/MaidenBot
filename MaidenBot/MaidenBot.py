import praw
import pdb
import re
import os
import sqlite3
from datetime import datetime as dt
from psaw import PushshiftAPI

reddit = praw.Reddit('bot1')
api = PushshiftAPI(reddit)
subreddit = reddit.subreddit("pythonforengineers")
conn = sqlite3.connect('JinnBotDB.db')
cursor = conn.cursor()



def process_args(args):
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
	return reply

def episode_table(args):
	query = args[1:]
	listtoStr= " "

	placeholder= '?'
	placeholders= ', '.join([placeholder]*len(query))
	statement = 'SELECT * FROM RWBY_Episode_Table WHERE ? LIKE tags'
	cursor.execute(statement, (listtoStr.join(query), ))
	results = cursor.fetchall()
	reply = "The episodes you're looking for are as follows:"
	for result in results:
		reply = reply + "\n[" + result[0]+ "]" + "(" + result[2] + ")\n"
	return reply


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
			del args[:bot_index+1] # deletes everything before the call to KnowledgeBot
			
			if 'last:' in args:
				num_index = args.index("last:") + 1
				numPosts = int(args[num_index])
			
			if 'episodetable' in args:
				comment.reply(episode_table(args))
			else:
				comment.reply(process_args(args))
			print("Bot replying to: ", comment.body)
			posts_replied_to.append(comment.id)
		with open("posts_replied_to.txt", "w") as f:
			for post_id in posts_replied_to:
				f.write(post_id + "\n")




	