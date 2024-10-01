from enum import Enum

class SIDE:
	NORTH = 0
	MID = 1
	SOUTH = 2

class MONEY_UNIT:
	NONE = 0
	NGHIN = 1
	TRIEU = 2

class LINK_NUMBER(Enum):
	HANG = 0
	DONVI = 1

class IMPLICIT_NUMBER(Enum):
	CAP = 0
	CHUC = 1
	LE = 2
	CHAN = 3
	LELE = 4
	CHANCHAN = 5
	LECHAN = 6
	CHANLE = 7
	VINHO = 8
	VILON = 9
	CHUCLON = 10
	CHUCNHO = 11
	NHOLE = 12
	LONLE = 13
	NHOCHAN = 14
	LONCHAN = 15
	LENHO = 16
	CHANNHO = 17
	CHUCLE = 18
	CHUCCHAN = 19
	GIAP = 20
	NGUOCGIAP = 21
	GIAP37 = 22
	GIAP44 = 23
	HE28 = 24
	HE39 = 25
	HE44 = 26
	HE48 = 27
	HE56 = 28
	HE58 = 29
	TONGNHO = 30