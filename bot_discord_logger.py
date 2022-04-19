# Helium add-on: log discord messages to Minecraft

import sys
import os
sys.path.append(os.path.abspath('./pyCraft'))
from minecraft.networking.connection import Connection
from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.packets import Packet, clientbound, serverbound

from optparse import OptionParser
import getpass
import re
import json
import socket
import requests


class DiscordBot:
	def __init__(self):
		options = self.get_options()

		self.commands = {
			'chat': self.log_discord_msg,
			'quit': self.quit
		}

		self.players = clientbound.play.player_list_item_packet.PlayerListItemPacket.PlayerList()

		self.sock_addr = ('', 14444)
		self.webhook = options.webhook

		if options.offline:
			print("Connecting in offline mode...")
			self.connection = Connection(
				options.address, options.port, username=options.username)

		self.connection.register_packet_listener(
			self.handle_join_game, clientbound.play.JoinGamePacket)

		self.connection.register_packet_listener(
			self.print_chat, clientbound.play.ChatMessagePacket)

		self.connection.register_packet_listener(
			self.update_players, clientbound.play.player_list_item_packet.PlayerListItemPacket)

		if False:
			def print_incoming(packet):
				if type(packet) is Packet:
					# This is a direct instance of the base Packet type, meaning
					# that it is a packet of unknown type, so we do not print it
					# unless explicitly requested by the user.
					if options.dump_unknown:
						print('--> [unknown packet] %s' % packet, file=sys.stderr)
				else:
					ignore = [
						clientbound.play.EntityPositionDeltaPacket, 
						clientbound.play.EntityVelocityPacket, 
						clientbound.play.TimeUpdatePacket, 
						clientbound.play.KeepAlivePacket, 
						clientbound.play.EntityLookPacket, 
						clientbound.play.block_change_packet.MultiBlockChangePacket, 
						clientbound.play.sound_effect_packet.SoundEffectPacket,
						clientbound.play.block_change_packet.BlockChangePacket,
					]
					if type(packet) not in ignore:
						print('--> %s' % packet, type(packet), file=sys.stderr)

			def print_outgoing(packet):
				print('<-- %s' % packet, file=sys.stderr)

			self.connection.register_packet_listener(
				print_incoming, Packet, early=True)
			# self.connection.register_packet_listener(
			# 	print_outgoing, Packet, outgoing=True)

		self.connection.connect()

		self.start_server()

	def get_options(self):
		parser = OptionParser()

		parser.add_option("-u", "--username", dest="username", default=None,
						help="username to log in with")

		parser.add_option("-p", "--password", dest="password", default=None,
						help="password to log in with")

		parser.add_option("-s", "--server", dest="server", default=None,
						help="server host or host:port "
							"(enclose IPv6 addresses in square brackets)")

		parser.add_option("-o", "--offline", dest="offline", action="store_true",
						help="connect to a server in offline mode "
							"(no password required)")

		parser.add_option("-d", "--dump-packets", dest="dump_packets",
						action="store_true",
						help="print sent and received packets to standard error")

		parser.add_option("-v", "--dump-unknown-packets", dest="dump_unknown",
						action="store_true",
						help="include unknown packets in --dump-packets output")
		
		parser.add_option("-w", "--webhook", dest="webhook", default=None,
						help="webhook url ")

		(options, args) = parser.parse_args()

		if not options.username:
			options.username = input("Enter your username: ")

		if not options.password and not options.offline:
			options.password = getpass.getpass("Enter your password (leave "
											"blank for offline mode): ")
			options.offline = options.offline or (options.password == "")

		if not options.server:
			options.server = input("Enter server host or host:port "
								"(enclose IPv6 addresses in square brackets): ")
		# Try to split out port and address
		match = re.match(r"((?P<host>[^\[\]:]+)|\[(?P<addr>[^\[\]]+)\])"
						r"(:(?P<port>\d+))?$", options.server)
		if match is None:
			raise ValueError("Invalid server address: '%s'." % options.server)
		options.address = match.group("host") or match.group("addr")
		options.port = int(match.group("port") or 25565)

		if not options.webhook:
			options.webhook = input("Enter the webhook url: ")

		return options

	def start_server(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
			self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)	
			self.socket.bind(self.sock_addr)
			print('Server started!')
			try:
				self.socket.listen(5)
				while True:
					(client, (ip, port)) = self.socket.accept()

					try:
						data = client.recv(1024).decode('utf-8').strip()
						
						if not data:
							continue

						data = json.loads(data)

						command = data.pop('command')
						self.commands[command](**data)
					finally:
						client.close()
			finally:
				self.socket.close()

	def update_players(self, packet):
		packet.apply(self.players)
		print(self.players.players_by_uuid)

	def print_chat(self, chat_packet):
		# Todo: Parse chat with chat.type in (text, me, action)
		packet_data = json.loads(chat_packet.json_data)
		if chat_packet.position == clientbound.play.ChatMessagePacket.Position.CHAT:
			data = self.parse_msg(packet_data)
			author, content = data['author'], data['content']

			if content is None or len(content.strip()) == 0:
				print('EMPTY', packet_data)
				return

			if author is None and content is not None:
				match = re.match(r'^<(?P<author>\w+)> (?P<content>.*)$', content)
				if match is not None:
					author = match.group('author')
					content = match.group('content')
				print(match, content)

			if author is None:
				author = 'MC Logger'

			data = {
				'username': author,
				'content': content
			}

			print(f'{author}: "{content}"')

			requests.post(self.webhook, data)
		else:
			data = self.parse_msg(packet_data)
			author, content = data['author'], data['content']
			print("Message (%s): %s" % (
				chat_packet.field_string('position'), content))
		
	def log_discord_msg(self, author, msg, col = None):
		if col is None:
			col = 'gray'
		text = [
			{'text':author,'color':col},
			{'text':': ', 'color': 'white'},
			{'text':msg, 'color': 'white'}
		]

		cmd = f'/tellraw @a ' + json.dumps(text)
		self.send_chat(cmd)

	def send_chat(self, text):
		packet = serverbound.play.ChatPacket()
		packet.message = text
		self.connection.write_packet(packet)
	
	def handle_join_game(self, join_game_packet):
		print('Connected.')

	def quit(self):
		raise SystemExit

	def parse_msg(self, data):
		author, content = None, None
		if type(data) is str:
			content = data
		elif 'translate' in data:
			if data['translate'] == 'chat.type.text':
				txts = [self.parse_msg(sub)['content'] for sub in data['with']]
				author, content = txts
		else:
			content = data['text']
			if 'extra' in data:
				content += ' '.join(self.parse_msg(c)['content'] for c in data['extra'])

		return {
			'author': author, 
			'content': content
		}

if __name__ == "__main__":
	DiscordBot()  
