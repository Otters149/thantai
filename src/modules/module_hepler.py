from datetime import datetime

from src.enums import SIDE

BASE_CHANNELS_CODE_OF_WEEK = {
	SIDE.SOUTH :[ ["TG", "KG", "DL"],
				["HCM", "DT", "CM"],
				["BTR", "VT", "BL"],
				["DN", "CT", "ST"],
				["TN", "AG", "BTH"],
				["VL", "BD", "TV"],
				["HCM", "LA", "BP", "HG"] ],
	SIDE.MID :[ ["KT", "KH", "TTH"],
				["PY", "TTH"],
				["DL", "QN"],
				["DN", "KH"],
				["BD", "QT", "QB"],
				["GL", "NT"],
				["DN", "QNG", "DKN"] ],
	SIDE.NORTH : [ ["MB"], ["MB"], ["MB"], ["MB"], ["MB"], ["MB"], ["MB"] ]	
}

__CHANNELS_CODE_OF_WEEK = {
	SIDE.SOUTH:[BASE_CHANNELS_CODE_OF_WEEK[SIDE.SOUTH][0] + ["4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.SOUTH][1] + ["4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.SOUTH][2] + ["4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.SOUTH][3] + ["4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.SOUTH][4] + ["4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.SOUTH][5] + ["4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.SOUTH][6] + ["4D", "DAI4"]],

	SIDE.MID: [ BASE_CHANNELS_CODE_OF_WEEK[SIDE.MID][0] + ["3D", "DAI3", "4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.MID][1] + ["3D", "4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.MID][2] + ["3D", "4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.MID][3] + ["3D", "4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.MID][4] + ["3D", "DAI3", "4D"],
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.MID][5] + ["3D", "4D"],				
				BASE_CHANNELS_CODE_OF_WEEK[SIDE.MID][6] + ["3D", "DAI3", "4D"]],

	SIDE.NORTH : BASE_CHANNELS_CODE_OF_WEEK[SIDE.NORTH]
}
__EXTEND_CHANNEL_CODE_OF_WEEK = {
	SIDE.SOUTH : ["2DP", "2D", "3D", "DC", "DP", "DAI3"],
	SIDE.MID : ["2D", "DC", "DP"],
	SIDE.NORTH : []
}

def get_day_of_week(date: datetime) -> int:
	'''
		Sun=0 Mon=1 Tue=2 Wed=3 Thu=4 Fri=5 Sat=6
	'''
	return int(date.strftime("%w"))

def get_channel_code_by_date(side: SIDE, date: datetime) -> list[str]:
	return __CHANNELS_CODE_OF_WEEK[side][get_day_of_week(date)] + __EXTEND_CHANNEL_CODE_OF_WEEK[side]


__CHANNEL_NAME_CODE_PAIR = {
	"Tiền Giang" : "TG",
	"Kiên Giang": "KG",
	"Đà Lạt": "DL",
	"TP.HCM": "HCM",
	"TP. HCM": "HCM",
	"Đồng Tháp": "DT",
	"Cà Mau": "CM",
	"Bến Tre": "BTR",
	"Vũng Tàu": "VT",
	"Bạc Liêu": "BL",
	"Đồng Nai": "DN",
	"Cần Thơ": "CT",
	"Sóc Trăng": "ST",
	"Tây Ninh": "TN",
	"An Giang": "AG",
	"Bình Thuận": "BTH",
	"Vĩnh Long": "VL",
	"Bình Dương": "BD",
	"Trà Vinh": "TV",
	"Long An": "LA",
	"Bình Phước": "BP",
	"Hậu Giang": "HG",
	"Kom Tum": "KT",
	"Kon Tum": "KT",
	"Khánh Hòa": "KH",
	"Thừa Thiên - Huế": "TTH",
	"Thừa Thiên Huế": "TTH",
	"Thừa T. Huế": "TTH",
	"Phú Yên": "PY",
	"Đắk Lắk": "DL",
	"Đắc Lắc": "DL",
	"Quảng Nam": "QN",
	"Đà Nẵng": "DN",
	"Khánh Hòa": "KH",
	"Bình Định": "BD",
	"Quảng Trị": "QT",
	"Quảng Bình": "QB",
	"Gia Lai": "GL",
	"Ninh Thuận": "NT",
	"Quảng Ngãi": "QNG",
	"Đắk Nông": "DKN",
	"Đắc Nông": "DKN",
	"Miền Bắc": "MB",
	"Hà Nội": "MB",
	"Bắc Ninh": "MB",
	"Hải Phòng": "MB",
	"Nam Định": "MB",
	"Quảng Ninh": "MB",
	"Thái Bình": "MB"
}
def convert_api_channel_name_to_channel_code(input: str):
	return __CHANNEL_NAME_CODE_PAIR[input]

