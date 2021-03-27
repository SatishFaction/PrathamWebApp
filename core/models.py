from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import datetime


class CANDIDATE(AbstractUser):

	location = models.CharField(max_length = 100, null = True)
	isDeleted = models.BooleanField(default = False, null = False)
	
	def __str__(self):
	
		return "Id : {7} username : {0} first_name : {1}  : last_name : {2} email : {3} password : {4} location : {5} is_deleted : {6}".format(self.username, self.first_name, self.last_name, self.email, self.password, self.location, self.isDeleted, self.id)
		#return "username : {0}".format(self.username)


class INTERVIEW(models.Model):

	candidateId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.DO_NOTHING, null = False, related_name = "Candidate_ID")
	
	dateOfSubmission = models.DateField(null = False, auto_now_add = True)
	timeOfSubmission = models.TimeField(auto_now = False, auto_now_add = True)
	
	languageOfSubmission = models.CharField(max_length = 100, null = True)
	
	isVideo = models.BooleanField(null = True)
	isReportGenerated = models.BooleanField(null = True, default = False)
	
	videoFilePath = models.TextField(null = True)
	videoFileName = models.TextField(null = True)
	audioFilePath = models.TextField(null = True)
	audioFileName = models.TextField(null = True)
	transcriptFilePath = models.TextField(null = True)
	transcriptFileName = models.TextField(null = True)
	
	eyeContactIndex = models.CharField(null = True, max_length = 50)
	smileIndex = models.CharField(null = True, max_length = 50)
	lipBiteIndex = models.CharField(null = True, max_length = 50)
	faceObstructionIndex = models.CharField(null = True, max_length = 50)
	nlpPositivityIndex = models.CharField(null = True, max_length = 50)
	voiceConfidenceIndex = models.CharField(null = True, max_length = 50)
	
	reportFilePath = models.TextField(null = True)
	reportFileName = models.TextField(null = True)
	
	def __str__(self):
	
		return "Id : {0}, Candidate : {1}, dateOfSubmission : {2}, timeOfSubmission : {3}, languageOfSubmission : {4}, isVideo : {5}, isReportGenerated : {6}, videoFilePath : {7}, videoFileName : {8}, audioFilePath : {9}, audioFileName : {10}, transcriptFilePath : {11}, transcriptFileName : {12}, eyeContactIndex : {13}, smileIndex : {14}, lipBiteIndex : {15}, faceObstructionIndex : {16}, nlpPositivityIndex {17}, voiceConfidenceIndex : {18}, reportFilePath : {19}, reportFileName : {20}\n".format(self.id, self.candidateId, self.dateOfSubmission, self.timeOfSubmission, self.languageOfSubmission, self.isVideo, self.isReportGenerated, self.videoFilePath, self.videoFileName, self.audioFilePath, self.audioFileName, self.transcriptFilePath, self.transcriptFileName, self.eyeContactIndex, self.smileIndex, self.lipBiteIndex, self.faceObstructionIndex, self.nlpPositivityIndex, self.voiceConfidenceIndex, self.reportFilePath, self.reportFileName)
		
		
		
				
