#coding: utf-8
from django.db import models
from django.utils.translation import ugettext_lazy as _
from facebook.models import User, FACEBOOK_APPS_CHOICE
from facebook.utils import get_graph, get_static_graph
from facebook.fields import JSONField

class Score(models.Model):
    """ The score object stores a game score for a user. It is automatically
        posted in the user's activity feed. 
        To get or set scores use the app access token.
    """
    user = models.ForeignKey(User)
    score = models.PositiveIntegerField(_('Score'))
    application_id = models.BigIntegerField(_('Application'), max_length=30, choices=FACEBOOK_APPS_CHOICE, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Score')
        verbose_name_plural = _('Scores')
        ordering = ['-score']
        
    class Facebook:
        access_token_type = 'app'
        type = 'score'
    
    def __unicode__(self):
        return u'%s, %s' % (self.user, self.score)
    
    def send_to_facebook(self, app_name=None, graph=None):
        if not graph:
            graph = get_graph(request=None, app_name=app_name)
        if self.score < 0:
            raise AttributeError, 'The score must be an integer >= 0.'
        return graph.request('%s/scores' % self.user.id ,'', {'score': str(self.score) })

    def save(self, facebook=True, app_name=None, graph=None, *args, **kwargs):
        super(Score, self).save(*args, **kwargs)
        if facebook:
            return self.send_to_facebook(app_name=app_name, graph=graph) 

    def delete(self, app_name=None, *args, **kwargs):
        graph = get_static_graph(app_name=app_name)
        graph.request('%s/scores' % self.user.id, post_args={'method': 'delete'})
        super(Score, self).delete(*args, **kwargs)
        
        
class Achievment(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(_('Title'), max_length=255)
    url = models.URLField(_('url'))
    description = models.CharField(_('Description'), max_length=255)
    image = JSONField(_('image'), blank=True)
    points = models.SmallIntegerField(_('Points'))
    updated_time = models.DateTimeField(_('updated_time'), auto_now=True)
    context = JSONField(_('context'), blank=True)
    
    class Meta:
        verbose_name = _('Achievment')
        verbose_name_plural = _('Achievments')
        
    class Facebook:
        type = 'games.achievement'
    
    def __unicode__(self):
        return unicode(self.title)
    
    