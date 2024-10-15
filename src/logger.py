import platform
import pkg_resources
import logging

from enum import Enum
from preprocessor import IS_DEV_BUILD

coloramaAvailable = False
package = "colorama"

try:
	dist = pkg_resources.get_distribution(package)
	print('{} ({}) is installed'.format(dist.key, dist.version))
	coloramaAvailable = True
except pkg_resources.DistributionNotFound:
	print('{} is NOT installed'.format(package))

if coloramaAvailable:
	from colorama import Fore, Back, Style # type: ignore

if platform.system()=='Windows':
	# See http://msdn.microsoft.com/library/default.asp?url=/library/en-us/winprog/winprog/windows_api_reference.asp
	# for information on Windows APIs.
	STD_INPUT_HANDLE = -10
	STD_OUTPUT_HANDLE= -11
	STD_ERROR_HANDLE = -12

	FOREGROUND_BLACK     = 0x0000
	FOREGROUND_BLUE      = 0x0001
	FOREGROUND_GREEN     = 0x0002
	FOREGROUND_CYAN      = 0x0003
	FOREGROUND_RED       = 0x0004
	FOREGROUND_MAGENTA   = 0x0005
	FOREGROUND_YELLOW    = 0x0006
	FOREGROUND_GREY      = 0x0007
	FOREGROUND_INTENSITY = 0x0008 # foreground color is intensified.

	BACKGROUND_BLACK     = 0x0000
	BACKGROUND_BLUE      = 0x0010
	BACKGROUND_GREEN     = 0x0020
	BACKGROUND_CYAN      = 0x0030
	BACKGROUND_RED       = 0x0040
	BACKGROUND_MAGENTA   = 0x0050
	BACKGROUND_YELLOW    = 0x0060
	BACKGROUND_GREY      = 0x0070
	BACKGROUND_INTENSITY = 0x0080 # background color is intensified.

	import ctypes
	std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)  # type: ignore

	def set_color(color, handle=std_out_handle):
		"""(color) -> BOOL

		Example: set_color(FOREGROUND_GREEN | FOREGROUND_INTENSITY)
		"""
		bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
		return bool

class Colors(Enum): # You may need to change color settings in iPython
	BLACK = 1,
	RED = 2,
	GREEN = 3,
	YELLOW = 4,
	BLUE = 5,
	PURPLE = 6,
	CYAN = 7,
	WHITE = 8,

def ColorSimplePrint(color: Colors, message: str) -> None:
	if coloramaAvailable:
		colorama_switcher = {
			Colors.BLACK: Fore.BLACK,
			Colors.RED: Fore.RED,
			Colors.GREEN: Fore.GREEN,
			Colors.YELLOW: Fore.YELLOW,
			Colors.BLUE: Fore.BLUE,
			Colors.PURPLE: Fore.MAGENTA,
			Colors.CYAN: Fore.CYAN,
			Colors.WHITE: Fore.WHITE
		}
		prefix = colorama_switcher[color]
		print("{}{}{}".format(prefix, message, Style.RESET_ALL))
	else:
		if platform.system()=='Windows':
			windows_switcher = {
				Colors.BLACK: FOREGROUND_BLACK | BACKGROUND_GREY,
				Colors.RED: FOREGROUND_RED | BACKGROUND_BLACK,
				Colors.GREEN: FOREGROUND_GREEN |  BACKGROUND_BLACK,
				Colors.YELLOW: FOREGROUND_YELLOW |  BACKGROUND_BLACK,
				Colors.BLUE: FOREGROUND_BLUE |  BACKGROUND_BLACK,
				Colors.PURPLE: FOREGROUND_MAGENTA |  BACKGROUND_BLACK,
				Colors.CYAN: FOREGROUND_CYAN |  BACKGROUND_BLACK,
				Colors.WHITE: FOREGROUND_GREY | BACKGROUND_BLACK
			}
			_color = windows_switcher[color]
			set_color(_color)
			print(message)
			set_color(FOREGROUND_GREY | BACKGROUND_BLACK)
		else:
			ansi_switcher = {
				Colors.BLACK: '\033[30m',
				Colors.RED: '\033[31m',
				Colors.GREEN: '\033[32m',
				Colors.YELLOW: '\033[33m',
				Colors.BLUE: '\033[34m',
				Colors.PURPLE: '\033[35m',
				Colors.CYAN: '\033[36m',
				Colors.WHITE: '\033[37m'
			}
			prefix = ansi_switcher[color]
			print("{}{}{}".format(prefix, message, '\033[m'))

def ColorPrint(color: Colors, message: str, *args) -> None:
	ColorSimplePrint(color, message.format(*args))
	


logging.basicConfig(
	format='%(asctime)s,%(msecs)d %(levelname)-8s [%(pathname)s:%(lineno)d in ' \
			'function %(funcName)s] %(message)s',
	datefmt='%Y-%m-%d:%H:%M:%S',
	level=logging.DEBUG
)
logger = logging.getLogger(__name__)
class AppLogger:
	def d(log):
		if IS_DEV_BUILD:
			print(f"[DEBUG] {log}")
			# ColorPrint(Colors.WHITE, f"[DEBUG] {log}")

	def i(log):
		print(f"[INFO]: {log}")
		# ColorPrint(Colors.GREEN, f"[INFO]: {log}")

	def w(log):
		print(f"[WARN]: {log}")
		# ColorPrint(Colors.YELLOW, f"[WARN]: {log}")

	def e(log):
		print(f"[ERROR]: {log}")
		# ColorPrint(Colors.RED, f"[ERROR]: {log}")

	def wtf(log):
		print(f"[WTF]: {log}")
		# ColorPrint(Colors.PURPLE, f"[WTF]: {log}")

