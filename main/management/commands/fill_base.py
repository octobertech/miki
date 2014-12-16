from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


from mezzanine.generic.models import Rating, ThreadedComment

from main.models import Link


class Command(BaseCommand):

    def handle(self, *args, **options):

        try:
            user_id = User.objects.get(username='miki').id
        except User.DoesNotExist:
            return
        mikis=self.extract()
        for miki in mikis:
            miki["user_id"] = user_id
            try:
                obj = Link.objects.create(title=miki['title'], body=miki["body"], user_id=user_id)
                obj.rating.add(Rating(value=1, user_id=user_id))
                obj.comments.add(ThreadedComment(comment=miki["example"], user_id=user_id))
            except: 
                pass
        print "The operation accomplished"

    def extract(self):
        """extracts word data from txt file into list of dictionaries/mikis"""
        wordbase=[]
        title=""
        hyper=""
        word_type=""
        body=""
        example=""
        miki={}
        for line in open("wordbase.txt"):
            line = line.strip()
            title, body, example = line.split(" - ")
            miki={"title": title, "body": body, "example": example}
            wordbase.append(miki)
        return wordbase
    
