from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
import requests
from django.template.defaultfilters import title

# Use the C ElementTree implementation where possible
try:
	from xml.etree.cElementTree import ElementTree, fromstring
except ImportError:
	from xml.etree.ElementTree import ElementTree, fromstring

API_PREFIX = 'https://www.warwicksu.com/membershipapi/listMembers/'

def send_signup_mail():
	pass

class Command(BaseCommand):
	help = 'Updates the list of members from the Warwick SU member API'

	def handle(self, *args, **options):
		api_url = '{prefix}{key}/'.format(
			prefix=API_PREFIX,key=settings.SU_API_KEY
		)
		print('Retrieving member list from: ' + api_url)
		members_xml = requests.get(api_url)
		active_member_ids = []
		members_root = fromstring(members_xml.text.encode('utf-8'))
		print('Checking list for members')
		for member in members_root:
			try:
				# Add existing members to the active list
				current_member = User.objects.get(
					username=member.find('UniqueID').text
				)
				active_member_ids.append(current_member.id)
				print('Existing member: ' + current_member.username)
			except User.DoesNotExist:
				# Create new members and add them to the active list
				password = User.objects.make_random_password()
				new_user = User.objects.create_user(
					username=member.find('UniqueID').text,
					email=member.find('EmailAddress').text,
					password=password
				)
				new_user.first_name = title(member.find('FirstName').text)
				new_user.last_name = title(member.find('LastName').text)
				new_user.save()
				active_member_ids.append(new_user.id)
				print('New member: ' + new_user.username)

		# Ensure all accounts that are to be activate are so
		activated = User.objects.filter(id__in=active_member_ids).all()
		activated.update(is_active=True)
		print(str(activated.count()) + ' users active')

		# Deactivate old accounts
		deactivated = User.objects.exclude(id__in=active_member_ids).all()
		deactivated.update(is_active=False)
		print(str(deactivated.count()) + ' users deactivated')