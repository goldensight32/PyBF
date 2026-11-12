'''

I kinda just dont know any brainfuck so im copy and pasting this from wikipedia

>  	Increment the data pointer by one (to point to the next cell to the right).
< 	Decrement the data pointer by one (to point to the next cell to the left). Undefined if at 0.
+ 	Increment the byte at the data pointer by one modulo 256.
- 	Decrement the byte at the data pointer by one modulo 256.
. 	Output the byte at the data pointer.
, 	Accept one byte of input, storing its value in the byte at the data pointer.
[ 	If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching ] command.
] 	If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching [ command.

'''

import tty
import termios
import sys

if len(sys.argv) < 2:
    print("Specify file")
    sys.exit(1)

filename = sys.argv[1]

def get_char():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)

	try:
		tty.setraw(fd)
		char = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

	return char

with open(filename, "r") as file:
    code = file.read()

debug = False

commands = "><+-.,[]"
code = "".join(char for char in code if char in commands)
 #hello world ++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.>---.+++++++..+++.>>.<-.<.+++.------.--------.>>+.>++.
tape = [0]
pointer = 0
instruction = 0
bracket_stack = []
bracket_pairs = {}

for position, char in enumerate(code):
	if char == "[":
		bracket_stack.append(position)

	elif char == "]":
		opening = bracket_stack.pop()

		bracket_pairs[opening] = position
		bracket_pairs[position] = opening

if bracket_stack:
	print("Unmatched opening bracket!")
	exit()

while instruction < len(code): 

	char = code[instruction]
	if debug == True:
		print(tape)

	if char == ">":
		pointer += 1
		if pointer == len(tape):
			tape.append(0)

	if char == "<":
		if pointer != 0:
			pointer -= 1

	if char == "+":
		tape[pointer] = (tape[pointer] + 1) % 256

	if char == "-":
		tape[pointer] = (tape[pointer] - 1) % 256

	if char == ".":
		print(chr(tape[pointer]), end="")

	if char == ",":
		inputc = get_char()

		if inputc == "\x03":
			raise KeyboardInterrupt
		tape[pointer] = ord(get_char()) % 256
		print("\nInput value:", tape[pointer])

	if char == "[" and tape[pointer] == 0:
		instruction = bracket_pairs[instruction]

	if char == "]" and tape[pointer] != 0:
		instruction = bracket_pairs[instruction]


	instruction += 1
