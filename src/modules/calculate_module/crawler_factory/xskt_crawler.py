import urllib.request
from html_table_parser import HTMLTableParser
from datetime import datetime

from src.enums import SIDE
from src.modules.calculate_module.crawler_factory.crawler import Crawler, AppLogger

class XSKTCrawler(Crawler):
	def __init__(self) -> None:
		super().__init__()
		self._base_url = "https://xskt.com.vn"

	def __get_week_day_str(self, date: datetime, side: SIDE) -> str:
		index = date.weekday()
		week_days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ Nhật']
		if index == 6 and side != SIDE.NORTH:
			return f'CN {date.day:02}/{date.month:02}' 
		return week_days[index]

	def _crawling(self, side: SIDE, date: datetime) -> tuple[bool, dict]:
		'''
			https://xskt.com.vn/xsmb/ngay-20-02-2023
			date-format: dd-MM-yyyy
		'''

		if side == SIDE.NORTH:
			crawl_url = f"{self._base_url}/xsmb/ngay-{date.day:02}-{date.month:02}-{date.year:04}"
		elif side == SIDE.MID:
			crawl_url = f"{self._base_url}/xsmt/ngay-{date.day:02}-{date.month:02}-{date.year:04}"
		else:
			crawl_url = f"{self._base_url}/xsmn/ngay-{date.day:02}-{date.month:02}-{date.year:04}"

		try:
			is_spinning_flag = "tự động cập nhật"
			week_day_str = self.__get_week_day_str(date, side)

			req = urllib.request.Request(url=crawl_url)
			content = urllib.request.urlopen(req)
			xhtml = content.read().decode('utf-8')

			parser = HTMLTableParser()
			parser.feed(xhtml)
			raw_data = parser.tables[0]

			if len(raw_data) < 8 or is_spinning_flag in str(raw_data[0][0]).lower() or is_spinning_flag in str(raw_data[0][1]).lower():
				return False, None
			
			is_date_found = False
			for line in raw_data:
				for element in line:
					if week_day_str in element:
						is_date_found = True
						break
				if is_date_found:
					break

			if not is_date_found:
				return False, None
			
			if side == SIDE.NORTH:
				json_data = {}
				prizes = ['ĐB', 'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7']
				for index in range(1, len(raw_data)):
					for prize in prizes:
						if prize == raw_data[index][0]:
							if '.' in raw_data[index][1] or raw_data[index][1] == '':
								return False, None
							if prize == "ĐB":
								json_data["db"] = raw_data[index][1]
							else:
								json_data[prize.lower()] = raw_data[index][1]
							break
				json_data['g8'] = ""
				return True, {"Miền Bắc": json_data}
			else:
				result = {}
				raw_channels = raw_data[0][1:]
				for ch in raw_channels:
					result[ch] = {} # init
				prizes = ['ĐB', 'G.1', 'G.2', 'G.3', 'G.4', 'G.5', 'G.6', 'G.7', 'G.8']
				for index in range(1, len(raw_data)):
					for prize in prizes:
						if prize == raw_data[index][0]:
							if '.' in raw_data[index][1] or raw_data[index][1] == '':
								return False, None
							if prize == 'ĐB':
								for channel_index in range(len(raw_channels)):
									result[raw_channels[channel_index]]["db"] = raw_data[index][channel_index + 1]
							else:
								for channel_index in range(len(raw_channels)):
									result[raw_channels[channel_index]][prize.replace(".", "").lower()] = raw_data[index][channel_index + 1]
							break
				return True, result
		except Exception as e:
			AppLogger.e(f"[GET_LOTTERY_RESULT] {e}")
			return False, None