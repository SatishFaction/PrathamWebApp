from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import CANDIDATE, INTERVIEW
from .forms import UserLoginForm, INTERVIEWForm

import csv, io
import datetime
import cv2
import numpy as np 
from dateutil.relativedelta import relativedelta

questionFilePath = "/home/shriniwas/UBSPratham/PrathamWebApp/media/"
questionFileName = "questionFile.txt"

videoFilePath = "/home/shriniwas/UBSPratham/PrathamWebApp/media/videos/"
audioFilePath = "/home/shriniwas/UBSPratham/PrathamWebApp/media/audios/"
transcriptFilePath = "/home/shriniwas/UBSPratham/PrathamWebApp/media/transcripts/"


def authenticate(request, candidateUsername, candidatePassword):

	try:
	
		candidateObj = CANDIDATE.objects.get(username = candidateUsername)
		
		if(candidateObj.password == candidatePassword):
		
			return candidateObj
			
	except:
	
		print("Candidate username does not exist")
		
	return None
		

def userLogin(request):

	print("In user login console")
	
	if(request.method == "POST"):
	
		form = UserLoginForm(request.POST, request.FILES)
		
		if(form.is_valid()):
		
			dataDict = form.cleaned_data	
			request.user = authenticate(request, candidateUsername = form.cleaned_data["username"], candidatePassword = form.cleaned_data["password"])

			user = request.user

			if(request.user != None):
				
				login(request, user)
				
				return redirect('core-home')
				
			else:
			
				messages.error(request, "INVALID CREDENTIALS")
	
	else:
	
		form = UserLoginForm()
		
	context = {'userLoginForm' : form}

	return render(request, "core/userLogin.html", context)



@login_required
def home(request):

	candidateName = request.user.first_name + " " + request.user.last_name

	contextDict = {'candidateName' : candidateName}

	return render(request, "core/home.html", context = contextDict)
	
	

@login_required
def viewGuidelines(request):

	contextDict = dict()

	return render(request, "core/guidelines.html", context = contextDict)


@login_required
def viewQuestions(request):

	try:
	
		questionData = open(questionFilePath + questionFileName).read()
		
		questionData = questionData.split('\n')
		
	except:
	
		print("Error in reading : {0}\n".format(questionFileName))

	contextDict = {'questions' : questionData}

	return render(request, "core/viewQuestions.html", context = contextDict)



def saveUploadedFile(fileData, isVideoVal, interviewObj, extension):   

	global videoFilePath
	global audioFilePath
	
	fileName = ""
	
	if(isVideoVal):
	
		path = videoFilePath
		
		interviewObj.videoFilePath = videoFilePath
		
		fileName = str(interviewObj.id) + "_" + "Video" + "." + extension
		
		interviewObj.videoFileName = fileName
		
	else:
	
		path = audioFilePath
		
		interviewObj.audioFilePath = audioFilePath
	
		fileName = str(interviewObj.id) + "_" + "Audio" + "." + extension
		
		interviewObj.audioFileName = fileName
	
	try:
	
		fileObj = open(path + fileName, "wb+")
			
		for chunk in fileData.chunks():
			
			fileObj.write(chunk)
			
	except:
			
		print("Unable to save file")
		raise
	
	interviewObj.save()



@login_required
def uploadVideo(request):

	if(request.method == "POST"):
	
		form = INTERVIEWForm(request.POST, request.FILES)
		
		if(form.is_valid()):
	
			isVideoVal = False
			
			extension = form.cleaned_data['interview_File'].name.split(".")[-1]
			
			if(extension == "mp4"):
			
				isVideoVal = True


			interviewObj = INTERVIEW(candidateId = request.user, languageOfSubmission = form.cleaned_data['language_Of_Submission'], isVideo = isVideoVal)
			interviewObj.save()
			
			try:		
	
				saveUploadedFile(form.cleaned_data['interview_File'], isVideoVal, interviewObj, extension)
				
			except:
			
				print("Unable to save the file : {0}".format(form.cleaned_data['interview_File'].name))
				exit(1)
				messages.error(request, "Cannot Save File")	
				
					
			messages.success(request, "Interview Submitted Successfully, Please note Reference ID : {0}".format(interviewObj.id))
			
		else:
		
			messages.error(request, "Please Use file format : mp3, mp4 OR wav")	
		
	else:
	
		form = INTERVIEWForm()
		
	context = {'INTERVIEWForm' : form}

	return render(request, "core/uploadVideo.html", context)	
	
	

@login_required	
def recordVideo(request):

	global videoFilePath
	global audioFilePath

	if(request.method == "POST"):

		if(request.POST.get("START") == "START"):

			cap = cv2.VideoCapture(0)
			
			fourcc = cv2.VideoWriter_fourcc(*'MPEG') 
			out = cv2.VideoWriter(videoFilePath + 'output.mp4', fourcc, 20.0, (640, 480)) 
	  
			while(True): 
				
				ret, frame = cap.read()  
	  
				out.write(frame)  
		  
				cv2.imshow('Frame', frame) 
	  
				if( cv2.waitKey(1) & 0xFF == ord('q') ): 
					
					break
	  
			cap.release() 
	  
			out.release()  
	  
			cv2.destroyAllWindows()
			
	return render(request, "core/recordVideo.html", context = dict())



def showReport(request, interviewObj):

	path = interviewObj.reportFilePath
	
	fileName = interviewObj.reportFileName
	
	try:
	
		fileObj = open(path + fileName, "r")
	
	except:
	
		print("Unable to open : {0}".format(path + fileName))
		
		exit(1)
	
	context = {'reportData' : fileObj.readlines()}
	
	return render(request, "core/showReport.html", context)
	

@login_required	
def viewResults(request):

	interviewQuerySet = None

	interviewQuerySet = []

	if(request.method == "POST"):
	
		interviewId = int(request.POST["interviewId"])

		interviewObj = INTERVIEW.objects.get(id = interviewId)
		
		renderObj = showReport(request, interviewObj)
		
		return renderObj
		
	else:
	
		interviewQuerySet = INTERVIEW.objects.filter(candidateId = request.user).order_by('-dateOfSubmission')
		
		if(len(interviewQuerySet) == 0):
		
			messages.error(request, "No Results to Display")
			
	
	context = {'interviewQuerySet' : interviewQuerySet}	

	return render(request, "core/viewResults.html", context)
	
	
	
@login_required	
def about(request):

	context = dict()

	return render(request, "core/about.html", context)


	
@login_required
def userLogout(request):

	logout(request)

	print(request.user)

	messages.success(request, "Logout Successful")
	
	return redirect('core-userLogin')
	
