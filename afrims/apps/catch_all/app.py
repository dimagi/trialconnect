import datetime
import logging

from django.core.exceptions import ObjectDoesNotExist

from rapidsms.apps.base import AppBase
from afrims.apps.reminders.models import Patient
from models import CatchallMessage

# In RapidSMS, message translation is done in OutgoingMessage, so no need
# to attempt the real translation here.  Use _ so that ./manage.py makemessages
# finds our text.
_ = lambda s: s

class CatchAllApp(AppBase):
    """ RapidSMS app to reply to unhandled messages """

    # Which message we send when we don't recognize the message
    # depends on who sent it.
    # Translators: This message is sent to patients
    patient_template = _("""Thank you for contacting us. Please reply with 2 to be """ \
                         """called back within 2 days.""")
    # Translators: This message is sent to non-patients (staff)
    non_patient_template = _("""Sorry, that message was not recognized""")

    def default(self, msg):
        """ If we reach the default phase here, respond with an appropriate
        message"""

        identity = msg.connection.identity
        contact = msg.connection.contact

        logging.debug("In catch_all.default(msg=%r, identity=%r)" % (msg,identity))

        # Have we sent them several catchalls recently?
        five_minutes_ago = datetime.datetime.now() - datetime.timedelta(minutes=5)
        recent_message_count = CatchallMessage.objects.filter(identity=identity,
                                                              timestamp__gte=five_minutes_ago).count()
        if recent_message_count >= 3:
            # Just ignore
            logging.debug("Not sending another 'did not understand' message")
            return True

        # are they a patient?
        patient = None
        if contact is not None:
            try:
                patient = Patient.objects.get(contact=contact)
            except ObjectDoesNotExist, e:
                pass

        if patient is None:
            msg.respond(self.non_patient_template)
            logging.debug("Sent non-patient do not understand message")
        else:
            msg.respond(self.patient_template)
            logging.debug("Sent patient do not understand message")

        # Remember that we sent a message
        logging.debug("Create CatchallMessage")
        try:
            CatchallMessage.objects.create(identity=identity)
        except e:
            logging.error(e)

        return True
