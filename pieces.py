import struct
import sys
from math import ceil

def pieces(message):
	if len(message) <= 64:
                pieces = [message]
                return pieces
	# Gets the number of pieces required
	count = int(ceil(len(message) / 64))
	pieces = []
	for x in range(0,count):
		tempList = []
		for y in range(x * 64, (x+1)*64):
			# Copy chars from message until end of message
			try:
				tempList.append(message[y])
			# End of message throws IndexError
			except IndexError:
				#Exit inner for loop
				break
		# Join chars in tempList into a string
		piece = "".join(tempList)	
		# Appends string to list
		pieces.append(piece)
	return pieces
	
def parse_message(pieces):
    parsed_message = ""
    for x in pieces:
        parsed_message = parsed_message + x
    return parsed_message
