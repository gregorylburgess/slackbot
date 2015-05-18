from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.utils import timezone
from django.utils.timezone import utc
from django.views.decorators.csrf import csrf_exempt
from slackbot.settings import STATIC_URL, SLACK_POST_URL, SLACK_BOT_NAME
import datetime, operator, json, requests


#request the status page
@csrf_exempt
def status(request):
	data = ""	
	if request.method == 'POST':
		# scrape POST data
		command = request.POST.get('command')
		text = request.POST.get('text')
		channel = request.POST.get('channel_name')
		user = request.POST.get('user_name')

		# validate command
		if command == "/google":
			data = google(text)

		elif command == "/roll":
			data = roll(text)

		elif command == "/debug":
			dbg = {'command':command, 'text': text, 'channel': channel, 'user': user}
			

			data = 'a'
			postdata={'text': data, 'channel': channel, 'username': SLACK_BOT_NAME}
			r = requests.post(SLACK_POST_URL, data=json.dumps(postdata))
			print (dbg)
			return HttpResponse( json.dumps({'command':command, 'text': text, 'channel': channel, 'user': user}), content_type="application/json" )

		else:
			print("Invalid command: " + str(command))
			data = "Invalid command."

		postdata={'text': data, 'channel': channel, 'username': SLACK_BOT_NAME}
		r = requests.post(SLACK_POST_URL, data=json.dumps(postdata))
		return (r.status_code)

	else:
		return HttpResponse("Invalid request type.")

#slash command
#https://uhicsr.slack.com/services/4932256860?added=1

#incoming webook
#https://uhicsr.slack.com/services/4954049441?added=1

def google(text):
	response = "http://www.google.com/webhp?#q=" + text + "&btnI=I"
	return response

def roll(text):
	return "4"
