import logging
from operator import itemgetter
import random
import requests
import time

# cElementTree is faster and uses less memory -Sorc
try:
    from xml.etree.cElementTree import ElementTree, fromstring
except ImportError:
    from xml.etree.ElementTree import ElementTree, fromstring

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.template.defaultfilters import title

from aniMango.settings import EMAIL_HOST_USER


def getMembers():
    try:
        request = requests.get('https://www.warwicksu.com/membershipapi/listmembers/c76aa4b2-ae70-43e7-b59f-'
                               '81d680deb1c5/')  # TODO: take key from settings file
    except Exception as e:
        raise

    xml_tree = fromstring(request.text.encode('utf-8'))
    members = []
    for xml_member in xml_tree:
        members.append({
            'id': xml_member.find('UniqueID').text,
            'f_name': title(xml_member.find('FirstName').text),
            'l_name': title(xml_member.find('LastName').text),
            'email': xml_member.find('EmailAddress').text,
        })
    members.sort(key=itemgetter('id'))
    return members


def removeExistingMembers(members_list):
    ret_members = []
    for item in members_list:
        if not User.objects.filter(username=item['id']).exists():
            ret_members.append(item)
    return ret_members


def removeAllBut(members_list, id_list):
    # use for testing or some unusual circumstances -Sorc
    ret_members = []
    for item in members_list:
        if item['id'] in id_list:
            ret_members.append(item)
    return ret_members


def validate_format(members_list):
    if not len(members_list[0]['id']) == 7:  # TODO: make sure they are also ints -Sorc
        raise ValueError(
            'IDs provided by SU should be strings of 7 digits. Duplicate accounts may be created otherwise. Take that '
            'in consideration if overriding.')
    return True


# def createUsersSimulated(logger, members_list):
# 	for item in members_list:
# 		temp_password = ''.join(random.choice('0123456789abcdef') for n in range(16))
# 		try:
# 			print('Create user here')
# 		except Exception as e:
# 			raise
# 		logger.info('Simulated | Created user: {0} {1} ({2}) - {3} | {4}'.format(
# 			item['f_name'].encode('utf-8'),
# 			item['l_name'].encode('utf-8'),
# 			item['id'],
# 			temp_password,
# 			item['email'].encode('utf-8'),
# 		))
# 		try:
# 			print('Sending email here to: '+item['email'].encode('utf-8'))
# 		except Exception as e:
# 			print('Delete user here')
# 			raise
# 		logger.info('Simulated | Email sent to {0}'.format(
# 			item['email'].encode('utf-8'),
# 		))
# 		time.sleep(5)

def createUsersReal(logger, members_list):
    for item in members_list:
        temp_password = ''.join(random.choice('0123456789abcdef') for n in range(16))
        try:
            usr = User.objects.create_user(
                username=item['id'],
                password=temp_password,
                email=item['email'],
                first_name=item['f_name'],
                last_name=item['l_name'],
            )
            usr.save()
        except Exception as e:
            raise
        logger.info('Created user: {0} {1} ({2}) | {3}'.format(
            item['f_name'].encode('utf-8'),
            item['l_name'].encode('utf-8'),
            item['id'],
            item['email'].encode('utf-8'),
        ))

        try:
            send_signup_mail(usr, temp_password)
        except Exception as e:
            usr.delete()
            raise
        logger.info('Email sent to {0}'.format(
            item['email'].encode('utf-8'),
        ))
    # time.sleep(5)


def send_signup_mail(user, password):
    subject = 'Welcome to the University of Warwick Anime and Manga Society'
    message = 'Hi,\n\n' \
              'Welcome to the University of Warwick Anime and Manga Society! Your login details are as follows:\n\n' \
              'Username: {username}\n' \
              'Password: {password}\n\n' \
              'You can log in at https://animesoc.co.uk/members/login/. We suggest you change your \n' \
              'password as soon as you log in. Do that by clicking on your temporary nickname (top right corner)\n' \
              'and then selecting profile. Don\'t forget to change your nickname, too!\n\n' \
              'Regards,\n' \
              'Warwick Anime and Manga Society\n\n'.format(username=user.username, password=password)
    send_mail(subject, message, EMAIL_HOST_USER, [user.email], fail_silently=False)


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            logger = logging.getLogger('user_creator_logger')
            while True:
                try:
                    members_list = getMembers()
                except Exception as e:
                    logger.exception(e)
                    time.sleep(5 * 60)
                    continue

                try:
                    validate_format(members_list)
                    members_list_new = removeExistingMembers(members_list)
                except Exception as e:
                    logger.exception(e)
                    return

                # members_list_new = removeAllBut(members_list_new, ['1705896','1701133'])

                number_total = len(members_list)
                number_new = len(members_list_new)
                logger.info('Synced with SU. Total members:{0!s} | New members: {1!s}'.format(number_total, number_new))

                if number_new > 0:
                    try:
                        createUsersReal(logger, members_list_new)
                        return  # FOR TESTING
                    except Exception as e:
                        logger.exception(e)
                        return

                time.sleep(5 * 60)
        except KeyboardInterrupt as k:
            print("Exiting")
