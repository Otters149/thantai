from abc import ABC, abstractmethod
from datetime import datetime

import requests
import urllib.request
from html_table_parser import HTMLTableParser

from src.gvals import app_timezone
from src.enums import SIDE
from src.modules.module_hepler import BASE_CHANNELS_CODE_OF_WEEK, convert_api_channel_name_to_channel_code
from src.logger import AppLogger
from configure import time_to_get_lottery_result


class Crawler(ABC):
	@abstractmethod
	def _crawling(self, side: SIDE, date: datetime) -> tuple[bool, dict]:
		'''
			Return:
				bool: success
				dict: lottery resule crawled from website
					dict format: {"Channel Vietnamese String" : {"Prize Name" : "Prize Values"}}
		'''

	def __get_empty_result(self, side: SIDE, date: datetime) -> tuple[bool, dict]:
		'''
			Return:
				bool: success
				dict: {"Channel Code" : {"Prize Name" : "Prize Values"}}
		'''
		channel_code_of_week = BASE_CHANNELS_CODE_OF_WEEK 
		if side == SIDE.NORTH:
			return {
						"MB":{
							"g8":"",
							"g7":"** ** ** **",
							"g6":"*** *** ***",
							"g5":"**** **** **** **** **** ****",
							"g4":"**** **** **** ****",
							"g3":"***** ***** ***** ***** ***** *****",
							"g2":"***** *****",
							"g1":"*****",
							"db":"*****"
						}
					}
		else:
			channels = channel_code_of_week[side][int(date.strftime("%w"))]
			rs = {}
			for channel in channels:
				rs[channel] = {
					"g8":"**",
					"g7":"***",
					"g6":"**** **** ****",
					"g5":"****",
					"g4":"***** ***** ***** ***** ***** ***** *****",
					"g3":"***** *****",
					"g2":"*****",
					"g1":"*****",
					"db":"******"
				}
			return rs

	def crawl_result(self, side: SIDE, date_get: datetime, force_result_not_available: bool) -> tuple[bool, dict, str]:
		'''
			Return:
				bool: success
				dict: lottery result
				str:  error
		'''
		if force_result_not_available:
			return False, self.__get_empty_result(side, date_get)
		try:
			today = datetime.now(tz=app_timezone)
			if date_get.year == today.year and date_get.month == today.month and date_get.day == today.day:
				if today.hour < time_to_get_lottery_result[side][0]:
					return False, self.__get_empty_result(side, date_get)
				elif today.hour == time_to_get_lottery_result[side][0]:
					if today.minute < time_to_get_lottery_result[side][1]:
						return False, self.__get_empty_result(side, date_get)
					
			success, lottery_result = self._crawling(side, date_get)
			if success:
				result_handled = {}
				for channel_name in lottery_result:
					channel_code = convert_api_channel_name_to_channel_code(channel_name)
					result_handled[channel_code] = lottery_result[channel_name]
				return True, result_handled
			return False, self.__get_empty_result(side, date_get)
		except Exception as e:
			AppLogger.e(f"[CRAWLER] Get lottery exception: {e}")
			return False, self.__get_empty_result(side, date_get)