from django.db import models
from django.utils.translation import ugettext as _
import reversion

@reversion.register()
class Media(models.Model):
    IMAGE = _(u'image')
    VIDEO = _(u'video')
    MEDIA_TYPES = (
        (IMAGE, _(u'Image')),
        (VIDEO, _(u'Video')),
        )

    OG_METATAG = u'<meta property="og:{0}" content="{1}" />'

    name = models.CharField(max_length=255)
    url = models.URLField(max_length=500, null=True, blank=True)
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPES)
    content = models.FileField(upload_to=u'site/', null=True, blank=True)
    content_type = models.CharField(max_length=255, null=True, blank=True)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    class Meta:
        verbose_name = _(u'Media')
        verbose_name_plural = _(u'Medias')

    def __unicode__(self):
        return self.name

    def get_fb_og_image_metatags(self):
        return u'{0}\n{1}\n{2}\n{3}\n{4}'.format(
                self.OG_METATAG.format('image', self.url),
                self.OG_METATAG.format('image:secure_url', self.url),
                self.OG_METATAG.format('image:type', self.content_type),
                self.OG_METATAG.format('image:width', self.width),
                self.OG_METATAG.format('image:height', self.height)
                )

    def get_fb_og_video_metatags(self):
        return u'{0}\n{1}\n{2}\n{3}\n{4}\n{5}'.format(
                self.OG_METATAG.format('video', self.url),
                self.OG_METATAG.format('video:secure_url', self.url),
                self.OG_METATAG.format('video:type', self.content_type),
                self.OG_METATAG.format('video:width', self.width),
                self.OG_METATAG.format('video:height', self.height),
                self.OG_METATAG.format('image', self.content.url)
                )

    def get_fb_og_metatags(self):
        if self.media_type == self.IMAGE:
            return self.get_fb_og_image_metatags()
        elif self.media_type == self.VIDEO:
            return self.get_fb_og_video_metatags()
        else:
            return u''
