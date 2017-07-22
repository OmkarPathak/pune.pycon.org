import uuid

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _

from symposion.conference.models import Conference

from cauth.models import EventUser
from root.models import Base


class Ticket(Base):
    """ Model to store the different types of ticket. """

    title = models.CharField(_("name"), max_length=255)
    limit = models.PositiveIntegerField(_("limit"), default=0)
    price = models.PositiveIntegerField(_("price"), default=0, db_index=True)
    description = models.CharField(_("description"), max_length=255, null=True)
    conference = models.ForeignKey(Conference, verbose_name=_("conference"))

    class Meta:
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")

    def __str__(self):
        return u"%s: %s" % (self.conference.title, self.title)


class TicketAddons(Base):
    """ Model for the addons for the tickets, which needs to be bought along
    with the ticket. """
    title = models.CharField(_('name'), max_length=255)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(_('price'), default=0)


class CouponCode(Base):
    """ Model for storing the coupon code, which can be applied on both the
    Ticket & TicketAddons.
    """
    code = models.CharField(_('coupon'), max_length=20)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class UserTicket(Base):
    """ Model for maitaining the ticket entry for all the Users. """

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(EventUser, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("user ticket")
        verbose_name_plural = _("user tickets")
        ordering = ['-timestamp']

    def __str__(self):
        return u'%s:%s' % (self.user.username, self.ticket.title)
