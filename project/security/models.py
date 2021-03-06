
from django.db import models
from djangotoolbox.fields import ListField
from ifc.rwlabel import RWFM,LabelManager
import os
from django.contrib.auth.models import User
#from django.contrib.auth import models
# Create your models here.



#####################################################Dummy Function for upload_to##################################    
def dummyfunction(self,filename):
    return
####################################################Upload to #####################################################
def get_upload_file_name(self,filename):
    return "uploads/%s/%s" % (self.user_name,filename)


################################################## Models ##########################################################
class Document_mongo(models.Model):
    title=models.CharField(max_length=200)
    user_id=models.CharField(max_length=200)
    docfile = models.FileField(upload_to=dummyfunction,default='00000')
    data_created=models.DateTimeField(auto_now_add=True, blank=True)
    entities=models.CharField(max_length=200)
    is_public = models.BooleanField(default=False)
    assignee = ListField()
    class Meta:
        app_label='mongodb'
    def assignees(self):
        """Returns assigned users or empty list"""
        return self.get('assignee') or []

    def is_visible(self, user_id=None):
        """Indicates whether the document is visible to user"""
        # assignees=[]
        # print self.assignees
        # for user in self.assignees:
        #     assignees.append(user["id"])
        assignees = [user["id"] for user in self.assignees]
        return (self.is_public or
                user_id == self.user_id or
                user_id in assignees)
    def is_editable(self, user_id=None,session=None):
        """Indicates the user can edit this document"""
        # access control.

        print "is_editable"
        #print session["rwlabel"]
        # self is document object
        # user_id is user id of requesting user..
        # also check if user requesting is a writer of document
        # get label for document
        print "document_id"
        lm = LabelManager()
        rw = RWFM()
        print self.pk
        doc_label = lm.getLabel(self.pk)
        print "edit"
        print "before edit doclabel",doc_label
        print "before edit sublabel",session["rwlabel"]
        temp = rw.checkWrite(session["rwlabel"],doc_label)

        print "after edit doclabel",doc_label
        print "after edit sublabel",session["rwlabel"]
        if temp:
            testwriter = True
        else:
            testwriter = False
        print 'testwriter',testwriter
        if ((str(user_id) == str(self.user_id)) and testwriter):# it is the user who created the document..
            return True
        #print "user_id self.user_id",user_id,self.user_id

        assignees=[]
        ##for user in self.assignee:
        for permission in self.assignee:
            print "in for loop of assignee",permission.get("id"),permission.get("permission")
            if (str(permission.get("id")) == str(user_id) and
                    permission.get('permission')=='can_edit' and testwriter):
                return True

        return False


class SignUp(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length = 200)
    password = models.CharField(max_length = 200)
    timestamp = models.DateTimeField(auto_now_add = True)       

class Document(models.Model):
    user_name = models.CharField(max_length=200)
    grantor = models.CharField(max_length=200,default='00000')
    docfile = models.FileField(upload_to=get_upload_file_name,default='00000')   
    read = models.BooleanField(default=1)
    write = models.BooleanField(default=0)
    owner = models.BooleanField(default=0)
    object_id = models.CharField(max_length=200)
    #privacy = models.CharField(default='0',max_length='2')
    class Meta:
        db_table="documents"
    def filename(self):
        #print os.path.basename(self.docfile.name)
        return os.path.basename(self.docfile.name)

class Friends(models.Model):
    user_name=models.CharField(max_length=200)
    friend_name = models.CharField(max_length=200)


    
class Request_send(models.Model):
    user_name= models.CharField(max_length=200,default='00000')
    friend_req= models.CharField(max_length=200,default='00000')
    document_name = models.FileField(default='00000',upload_to=dummyfunction)
    class Meta:
        db_table="request_send"


class Shared(models.Model):
    user_name = models.CharField(max_length=200)
    docfile = models.CharField(max_length=200)   
    read = models.BooleanField(default=False)
    write = models.BooleanField(default=False)
    owner = models.BooleanField(default=False)

class Details(models.Model):
    user_name = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    phnumber = models.CharField(max_length=200)
    email = models.EmailField()
    class Meta:
        db_table="profile_details"

class PrivacyDetails(models.Model):
    user_name = models.CharField(max_length=200)
    name = models.CharField(max_length=2)
    age = models.CharField(max_length=2)
    location = models.CharField(max_length=2)
    phnumber = models.CharField(max_length=2)
    email = models.EmailField()
    class Meta:
        db_table="profile_privacy"

class PrivacyFriend(models.Model):
    user_name = models.CharField(max_length=200)
    privacy = models.CharField(max_length=2)
    class Meta:
        db_table="friend_privacy"

class PrivacyDocs(models.Model):
    user_name = models.CharField(max_length=200)
    docfile = models.FileField(default='00000',upload_to=dummyfunction)
    privacy = models.CharField(max_length=2,default='0')
    class Meta:
        db_table = "document_privacy"