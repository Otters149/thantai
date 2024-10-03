from src.enums import SIDE, LINK_NUMBER, IMPLICIT_NUMBER, MONEY_UNIT

#region CONFIG
CHILD_ORDER = ["t@", "t @", "tin@", "tin @"]

__IMPLICIT_CHANNELS = {
	"DC": ["dai chanh", "daichanh", "dchanh", "dai chinh", "daichinh", "daich", "dchinh", "chanh", "chinh", "dch", "dc", "ch"],
	"DP": ["dai phu", "daiphu","d phu", "dphu", "dph", "phu", "ph", "dp", "fu"],
	"DAI3": ["dai thu 3", "dai thu3", "daithu3", "dthu3", "dai 3", "dai3"],
	"DAI4": ["dai thu 4", "dai thu4", "daithu4", "dthu4", "dai 4", "dai4"],
	"2D": ["2 dai", "2 d", "2 daj", "2daj", "2dai", "2da", "2d", "hai dai", "haidai", "haidaj"],
	"2DP": ["2 dai phu", "2 dp", "2 daj phu", "2dajphu", "2daiphu","2d phu", "2dphu", "2phu", "2daph", "2dph", "2ph", "2dp", "2fu", "hai dai phu", "haidaiphu", "hdp"],
	"3D": ["3 dai", "3 d", "3 daj", "3daj", "3dai", "3da", "3d", "ba dai", "badai"],
	"4D": ["4 dai", "4 d", "4 daj", "4daj", "4dai", "4da", "4d", "bon dai", "bondai"],
}
CHANNELS = {
	SIDE.SOUTH:{
		"DAI3": __IMPLICIT_CHANNELS["DAI3"],
		"DAI4": __IMPLICIT_CHANNELS["DAI4"],        
		"TG": ["dai tien giang","tien giang va","tien giang v", "tien giang","tien gian","t giang v", "t giang", "tiengiang", "tgiang", "tgiag", "tgi", "tg"],
		"KG": ["dai kieng giang", "dai kien giang", "kieng giang","kien giang v", "kien giang","k giang v", "k giang","kien gian", "k g","kgiang v", "kiengiang", "kgiang", "kgiag", "kgi", "kg"],
		"DL": ["dai da lat","da lat", "dalat","da lac", "d lat","dai dl","dalac", "dlat", "dl", "ld"],
		"HCM": ["ho chi minh", "sai gon", "hochi minh", "ho chiminh", "hochiminh", "hchiminh", "hcminh","dai thanh pho","thanh pho va","thanh pho v", "thanh pho","dai tp", "t ph","tp va","dai hcm", "thanhpho","dai sai gon", "sai gon", "saigon", "thahpho", "tpho","tp v","thphcm", "tph", "tphcm", "hcm", "tp", "sg"],
		"DT": ["dai dong thap", "dong thap","d thap v", "d thap", "dongthap", "dogthap", "donthap", "dthap","ddth", "thap", "dth","d t", "dt"], # thap is special name for workdaround while parsing currency "dong" conflict vs "dong thap"
		"CM": ["dai ca mau", "ca mau v", "ca mau", "ca mao", "c mau", "camau", "camao", "cmau", "cmao", "cm"],
		"VT": ["dai vung tau","vung tau v","vung tau", "vung tao", "vun tau", "vug tau", "v tau","v t", "vungtau", "vungtao", "vugtau", "vugtau", "vtau", "vt"],
		"BL": ["dai bac lieu", "bac lieu", "b lieu","bac liu", "baclieu", "bliuiu", "bclieu","bacliu", "bloieu", "bllieu", "blieu", "bliiu", "bloeu", "bleu", "blii", "bliu", "bli"],
		"DN": ["dai dong nai","dong nai va", "dong nai","d nai v", "d nai", "dongnai", "dognai", "dongai", "dnai", "nai", "dn"], # nai is special name for workdaround while parsing currency "dong" conflict vs "dong nai"
		"ST": ["dai soc trang", "soc trang", "soctrang","soc trag", "soctrag","s trang", "strang", "strag", "str","s t", "st"],
		"CT": ["dai can tho","can tho v", "can tho", "cantho", "cantho","c tho v", "c tho", "catho", "ctho", "cth","c t", "ct"],
		"TN": ["dai tay ninh","tay ninh v","tay ninh","t ninh v", "t ninh", "t n", "tayninh","tninh v","tninh", "tn"],
		"AG": ["dai an giang", "an giang", "angiang", "angian","a giang","agiang v", "agiang", "agian", "agi","a g", "ag"],
		"BTH": ["dai binh thuan","binh thuan", "b thuan", "binhthuan", "binhthun", "bthuan", "bthh", "bth","dai bt", "bt"],
		"BTR": ["dai ben tre","ben tre va","ben tre v", "ben tre", "b tre v",  "b tre", "bentre", "bentr", "btre", "btr","dai bt","b t", "bt"],
		"VL": ["dai vinh long","vinh long va","vinh long v","vinh long","v long v" ,"v long","dai vl","v l", "vinhlong", "vlong", "vlog", "vlog", "vlo", "vl"],
		"BD": ["dai binh duong","binh duong","b duong v", "b duong", "binhduong", "binhduog", "bduong", "bduog", "bdu", "bdg","b d", "bd", "song be", "songbe", "sbe", "sb"],
		"TV": ["dai tra vinh", "tra vinh", "tr vinh","travinh", "trvinh", "tvinh","t vinh", "tvih", "trv", "tv"],
		"LA": ["dai long an", "long an", "log an", "longan", "logan","longa",  "l an", "lan", "la"],
		"BP": ["binh phuoc", "binhphuoc", "binhpuoc","b phuoc v" ,"b phuoc","dai bp", "b ph", "bphuoc", "bpuoc", "bph", "bp"],
		"HG": ["hau giang","hau gian", "h giang", "haugiang", "haugian","hau gian","haugiag", "hgiang", "hgiag","dai hg", "hgi", "hg"],
		"2DP": __IMPLICIT_CHANNELS["2DP"],
		"2D": __IMPLICIT_CHANNELS["2D"],
		"3D": __IMPLICIT_CHANNELS["3D"],
		"4D": __IMPLICIT_CHANNELS["4D"],
		"DC": __IMPLICIT_CHANNELS["DC"],
		"DP": __IMPLICIT_CHANNELS["DP"],
	},
	SIDE.MID:{
		"DAI3": __IMPLICIT_CHANNELS["DAI3"],         
		"KT": ["dai komtum","kom tum", "kom tom", "kom tun", "kon tum", "kun tum", "kum tun","k tum v", "kum tum","k tum", "komtom", "komtum", "kumtum", "kontum","contum", "ktum", "kt"],
		"TTH":["thua thien hue","thuathien hue","thuathienhue","t t hue", "thua t hue","t t hue","dai hue",  "hue", "tthue", "tth", "h"],
		"PY": ["dai phu yen","phu yen", "p yen", "phuyen", "phyen", "pyen", "py"],
		"DL": ["dak lak","dai dac lak","dai dac lac", "dac lac", "dac lat", "dat lak", "dat lat","dac lak", "daklak", "daclak", "datlak", "dalak", "daclat", "daclac","d lac", "dlak", "dlac", "dlat", "dalk", "dlk", "dkl", "dl"],
		"KH": ["dai khanh hoa", "khanh hoa", "khah hoa", "kah hoa","k hoa v",  "k hoa","khanhhoa", "khanhoa", "khanh","kh hoa", "khhoa", "khoa v", "khoa", "kh v", "k h", "kh"],
		"BD": ["dai binh dinh","binh dinh", "binh din", "bin din", "bih din", "dih din", "b d", "binhdinh","b dinh v", "b dinh", "bdinh", "bdin", "bdih", "bdi", "bd"],
		"QT": ["dai quang tri","quang tri", "quag tri", "qang tri", "quan tri", "q tri", "quangtri", "quantri","qtri v", "qtri", "qtr", "qt"],
		"QB": ["quang binh", "quag binh", "quang bin", "qang binh", "quan binh","q binh v", "q binh", "quangbinh", "quanbinh","qbih", "qbinh", "qbi", "qb"],
		"GL": ["dai gia lai", "gia lai", "g lai", "gialai", "gilai", "glai", "gl"],
		"NT": ["ninh thuan", "nih thuan", "ninh thua", "n thuan", "ninhthuan", "nthuan","thuan", "nth", "nt"],
		"QNG":["dai quang ngai", "quang ngai", "qang ngai", "quan ngai","qua ngai", "qu ngai", "q ngai", "quangngai", "qngai", "qng", "qn"],
		"QN": ["dai quang nam","quang nam", "quang nom", "quan nam", "quan nom", "quangnam", "qgnam","q nam", "qnam", "qnm", "qn"],
		"DKN":["dak nong", "dak nog", "dat nong", "dac nong", "dat nog", "dac nog", "dk nong", "d nong", "datnong", "daknong", "dacnong", "dnong", "dnog", "dno", "no", "dkn"],
		"DN": ["dai da nang","da nang va", "da nang v","da nang", "d nang", "da nan", "danang","da nag", "danag", "dnang","dnan", "dang", "dnag", "dng", "dna", "dn"], # "dn" only equal "Da Nang"
		"2D": __IMPLICIT_CHANNELS["2D"],
		"3D": __IMPLICIT_CHANNELS["3D"],
		"4D": __IMPLICIT_CHANNELS["4D"],
		"DC": __IMPLICIT_CHANNELS["DC"],
		"DP": __IMPLICIT_CHANNELS["DP"],
	},
	SIDE.NORTH:{
		"MB": [ "mien bac", "mienbac", "mbac", "dai mb", "dai hn", "mb",
				"ha noi", "ha loi", "hanoi", "haloi", "hnoi", "hloi", "dai hn", "hn", "hanuiii", "hnuii",
				"bac ninh", "bacninh", "bninh", "bacnih", "bn",
				"hai phong", "haiphong", "hphong", "hphog", "hp",
				"nam dinh", "namdinh", "ndinh", "ndih", "nd",
				"quang ninh", "quangninh", "qninh", "qn",
				"thai binh", "thaibinh", "thbinh", "thb",] + 
				__IMPLICIT_CHANNELS["2D"] +
				__IMPLICIT_CHANNELS["3D"] +
				__IMPLICIT_CHANNELS["4D"] +
				__IMPLICIT_CHANNELS["DC"] +
				__IMPLICIT_CHANNELS["DP"]
	}
}

IMPLICIT_NUMBERS = {
	IMPLICIT_NUMBER.CAP: ["so cap", "socap", "scap", "socp", "cap so", "capso", "cap"],
	IMPLICIT_NUMBER.CHUCLON: ["so chuc lon", "sochuclon", "schuclon", "chuc lon", "chuclon"],
	IMPLICIT_NUMBER.CHUCNHO: ["so chuc nho", "sochucnho", "schucnho", "chuc nho", "chucnho"],
	IMPLICIT_NUMBER.CHUCLE: ["chuc le", "chucle"],
	IMPLICIT_NUMBER.CHUCCHAN: ["chuc chan", "chucchan"],
	IMPLICIT_NUMBER.CHUC: ["so chuc", "sochuc", "schuc", "chuc"],
	IMPLICIT_NUMBER.LELE: ["le le", "lele", "lel", "lle", "ll"],
	IMPLICIT_NUMBER.CHANCHAN: ["chan chan", "chanchan", "chanc", "cchan", "cc"],
	IMPLICIT_NUMBER.LECHAN: ["le chan", "lechan", "lchan", "lec", "lech", "lc"],
	IMPLICIT_NUMBER.CHANLE: ["chan le", "chanle", "chanl", "chle", "cle", "cl"],
	IMPLICIT_NUMBER.NHOLE: ["so nho le", "nho le", "nhole"],
	IMPLICIT_NUMBER.LENHO: ["so le nho", "le nho", "lenho"],
	IMPLICIT_NUMBER.NHOCHAN: ["nho chan", "nhochan"],
	IMPLICIT_NUMBER.CHANNHO: ["chan nho", "channho"],
	IMPLICIT_NUMBER.LONLE: ["lon le", "lonle"],
	IMPLICIT_NUMBER.LONCHAN: ["lon chan", "lonchan"],
	IMPLICIT_NUMBER.LE: ["le don vi", "don vi le", "so le", "sole", "ledonvi", "ldonvi", "ledv", "le", "ldv"],
	IMPLICIT_NUMBER.CHAN: ["chan don vi", "don vi chan", "so chan", "sochan", "chandonvi", "cdonvi", "chandv", "chan", "cdv"],
	IMPLICIT_NUMBER.VILON: ["don vi lon", "donvilon", "dvlon", "vi lon", "vilon", "vlon", "lon", "dvl", "vln"],  # vl same as (vinh long)
	IMPLICIT_NUMBER.VINHO: ["don vi nho", "donvinho", "dvnho", "vi nho", "vinho", "vnho", "nho", "dvn", "vn"],
	IMPLICIT_NUMBER.TONGNHO: ["tong nho", "tongnho", "tognho", "tnho", "tongnh"],
	IMPLICIT_NUMBER.NGUOCGIAP: ["nguoc giap", "khong giap", "nghich giap", "ngich giap", "khgiap", "kgiap", "bgiap"],
	IMPLICIT_NUMBER.GIAP37: ["giap 37 so", "giap 37so", "giap37so", "con giap he 37", "giap lay he 37", "giap lay he37", "giap lay h37", "giap he 37", "giaphe37"],
	IMPLICIT_NUMBER.GIAP44: ["giap 44 so", "giap 44so", "giap44so", "con giap he 44", "giap lay he 44", "giap lay he44", "giap lay h44", "giap he 44", "giaphe44"],
	IMPLICIT_NUMBER.GIAP: ["con giap", "giap"],
	IMPLICIT_NUMBER.HE28: ["he 28 so", "he 28so", "he28so", "he nuoc 28", "he nuoc28", "hnuoc28", "he nuoc", "he 28", "he28"],
	IMPLICIT_NUMBER.HE39: ["he 39 so", "he 39so", "he39so", "he 39", "he39"],
	IMPLICIT_NUMBER.HE44: ["he 44 so", "he 44so", "he44so", "he 44", "he44"],
	IMPLICIT_NUMBER.HE48: ["he 48 so", "he 48so", "he48so", "he 48", "he48"],
	IMPLICIT_NUMBER.HE56: ["he 56 so", "he 56so", "he56so", "he 56", "he56"],
	IMPLICIT_NUMBER.HE58: ["he 58 so", "he 58so", "he58so", "he 58", "he58"]  
}

TYPES_BET = {
	# 4D 
	"DAODACBIET": ["dao dac biet", "daodacbiet","daodacbiet", "ddb","dbd"],	

	# 3D
	"DAOXIUDAU": ["dao xiu dau", "daoxiu dau", "daoxcdau", "daoxiudau", "dxiu dau", "xcdaudao", "dxiudau", "dxiudao", "daoxdau", "dxcdau", "dxdau", "xiudaodau", "xiuddau", "xcdaodau", "xdaudao", "xddau"],
	"DAOXIUDUOI": ["dao xiu dui", "dao xdui", "daoxiu dui", "daoxc dui", "xcd dui", "xcdui dao", "xcdao dui","dui daoxc","dao xcdui", "xduidaodui", "daoxiudui", "daoduixiu", "daoduix", "daoxcduoi", "daoxcdui", "daoxdui", "duixdao", "duixd", "dxiu dui", "dxiudui", "dxcduoi", "dxcdui", "dxdui", "xcdaoduoi", "xcdaodui", "xcduidao", "xcduoidao", "xduoidao", "xduidao", "xdaodui", "xcduid", "xddui","duidao"],
	"DAOXIU": ["daoxiu daudui","xiu chu dao", "dao xiu", "xiu dao", "xc dao", "dao xc", "dao x","xiuchudao", "daoxiuchu", "daoxiu", "daxiu", "dasiu", "daoxc", "daxc", "daox", "doxc", "dox", "dxdaudui" "dxiudd", "dxiu", "dxdd", "dxc", "xiudao", "xcdao", "xcdo", "xdao", "xdo","dao dd", "dao.xc"],
	"XIUCHU": ["xiu chu dau dui","xc dau duoi", "xiuchu dau dui", "xiuchu daudui", "xiuchudaudui","xcdauduoi", "xchu dau dui","xc chu", "xiuchudd","ab xc","ab.xc","abxc", "siuchu", "schu", "siu", "sui",  "xieu", "xcdd", "tc", "cs", "cx", "sc", "s"],
	"XDAU": ["dau xiu chu", "dau xiuchu","xchu a", "dau xc", "dau x", "xiu chu dau", "xiuchu dau", "xiuchudau", "xchu dau", "xchudau", "xc dau", "xcdau", "xiu dau", "xiudau", "xdau", "dauxc", "daux", "xde", "dq", "q"],
	"XDUOI":["duoi xiu chu", "duoi xiuchu", "duoi xc", "dui xiu chu", "dui xiuchu", "dui xc", "duoi x", "x dui", "dui x", "xiu chu dui", "xiuchu dui", "xiuchudui", "xchu dui", "xchudui", "xc duoi", "xc dui", "xcduoi", "xcdui", "xiu dui","xiudui", "xuidui", "xduoi", "xdui", "duixc", "duix", "xdu", "bw", "dw", "w"],
	"DAOXIU2": ["xcd", "xd"],
	"XIUCHU2": ["xiu chu","xiuchu", "xchu", "xiu", "xch", "xc"],

	# BAO LO
	"BAYLODAO": ["bao dao bay lo", "dao bay lo", "baodaobaylo", "baodaobayl", "bdaobaylo", "bdbaylo", "baylodao", "bdblo", "baodbaylo", "bdbl", "bd7lo", "bd7l"],
	"BAOLO7": ["bao bay lo", "baobaylo", "baobayl", "bbaylo", "bbayl", " bay lo", "baylo", "bayl","bao 7 lo", "bao 7 lo", "bao7lo", "bao7l", "b7lo", "b7l", "pao 7 lo", "pao 7lo", "pao7lo", "p7lo", "p7l"],
	"BAODAO": ["dao bao lo", "dao bl", "dao lo", "dao bao", "bao lo da", "bao lo dao", "bao dao","bl bdao", "blao dao","bl dao", "b dao","dao b","baolodao", "baoloda", "baodao", "daobao", "baodo", "baod", "blodao", "bldao", "daoblo", "daolo", "daobl", "daob", "dalo", "dolo", "daob", "dbao", "bdao", "dlo", "dab", "bdo", "bdl", "bld", "bd", "db", "pao dao", "paodao", "pdao", "pd", "dl"],
	"BAOLO": ["bao lo con ","bao lo","lo bao", "b lo", "baolo", "bao", "blo", "bl", "pao lo", "paolo", "pao", "plo", "loo", "lo", "pl"],

	# DA
	"DATHANGVONG":["da vong thang", "dv thang", "davthag"],
	"DATHANG": ["da thang","d thang", "da th", "da t", "d t", "dathang", "dathag", "dthang", "dthag","thang", "dath", "dtg", "dth", "dat", "dt"],
	"DAXIENVONG": ["da vong xien", "da xien vong", "daaxienvong",  "dxvog", "daxv", "davx", "dxv", "dvx", "xv"],
	"DAXIEN": ["da moi cap", "da cap", "dacheo xien", "dacheoxien", "da cheo","cheo da", "dacheo", "dache", "da xieng", "da xien", "da xuyen","da xjen", "da x", "daxieng","daxjen", "daxien", "daxuyen", "daxi", "daxc", "dax", "dxien", "xien", "xi","dcheo", "cheo", "che"],
	"DAVONG": ["da vong con" ,"da vong" , "da dong", "da vog", "davong", "dvong", "dvog", "dadong","vong", "cheov", "da v", "d v", "dav", "dv", "v"],
    
	#
	"XDUOI2": ["xu"],

	# North
	"AM": ["amot", "amt", "amo", "am"],
	"AH": ["ahai", "aha", "ahi", "ah"],
	"AB": ["aba"],
	"AT": ["abon", "abo", "atu", "at"],
	"XL": ["xo lien", "xolien", "xol", "xolen", "xlien", "xlin", "xln", "xl"],

	# 2D
	"DAUDUOI": ["dau duoi", "dau dui", "a b", "dauduoi", "daudui", "ddui", "deu","d d", "dd", "ab", "z"],
	"DAU": ["dau", "de", "a"],
	"DUOI": ["duoi dac biet moi con", "duoi", "duoj", "dupi", "duii","duj", "duo", "dui", "di", "bu", "u"],

	#
	"BAOLO2": ["c"],
	"DA": ["da"],
	"UNDETERMINED": ["dx", "d", "b"],
	"XIUCHU3": ["x"],
}

MONEY_UNITS = {
	MONEY_UNIT.NGHIN: ["nghin", "ngan", "ngin", "ng", "nn", "n", "dong"],
	MONEY_UNIT.TRIEU: ["trieu", "triu", "tri", "tr"]
}

NUMBER_LINK_UNIT = ["keo vi", "keovi", "keo v", "keov", "den vi", "denvi", "den v", "denv", "toi vi", "toivi", "toi v", "toiv", "tiv", "kv"]
NUMBER_LINK_CONTINUOUS = ["keo", "toi", "den", "khc", "kht", "k"]
NUMBER_IGNORE = ["bchuc", "bcap", "bo", "tru", "loai"]

LINK_NUMBERS = {
	LINK_NUMBER.HANG: ["hang @", "hang@", "hag @", "hag@", "ha@", "h@"],
	LINK_NUMBER.DONVI: ["don vi @", "don vi@", "donvi @", "donv @", "dvi @", "vi @", "dich @", "dit @", "duoiv @", "duiv @", "donvi@", "donv@", "dvi@", "vi@", "dich@", "dit @", "duoiv@", "duiv@"],
}

'''
SOUTH
cn: Tiền Giang; Kiên Giang; Đà Lạt	
t2: Thành phố; Đồng Tháp; Cà Mau
t3: Bến Tre; Vũng Tàu; Bạc Liêu
t4: Đồng Nai; Cần Thơ; Sóc Trăng
t5: Tây Ninh; An Giang; Bình Thuận
t6: Vĩnh Long; Bình Dương (Sông Bé); Trà Vinh
t7: Thành Phố; Long An; Bình Phước; Hậu Giang
MID
cn: Kom Tum; Khánh Hòa, Thừa Thiên - Huế
t2: Phú Yên, Thừa Thiên - Huế
t3: Đắk Lắk, Quảng Nam
t4: Đà Nẵng, Khánh Hòa
t5: Bình Định, Quảng Trị, Quảng Bình
t6: Gia Lai, Ninh Thuận
t7: Đà Nẵng, Quảng Ngãi, Đắk Nông
'''



#endregion

#region HELPER
class PairInt:
	def __init__(self, first = 0, second = 0) -> None:
		self._value = [first, second]

	def get_first(self) -> int:
		return self._value[0]

	def get_second(self) -> int:
		return self._value[1]

	def set_first(self, intVal: int):
		self._value[0] = intVal

	def set_second(self, intVal: int):
		self._value[1] = intVal

	first: int = property(get_first, set_first)
	second: int = property(get_second, set_second)

class ParseMessagePartIndexes:
	def __init__(self, order_index = PairInt(), channel_index = PairInt(), number_index = PairInt(), type_bet_index = PairInt(), point_bet_index = PairInt()) -> None:
		self._value = [order_index, channel_index, number_index, type_bet_index, point_bet_index]

	def get_order_pair_index(self) -> PairInt:
		return self._value[0]
	def get_channel_pair_index(self) -> PairInt:
		return self._value[1]
	def get_number_pair_index(self) -> PairInt:
		return self._value[2]
	def get_type_bet_pair_index(self) -> PairInt:
		return self._value[3]
	def get_point_bet_pair_index(self) -> PairInt:
		return self._value[4]
	
	def set_order_pair_index(self, value: PairInt) -> PairInt:
		self._value[0] = value
	def set_channel_pair_index(self, value: PairInt) -> PairInt:
		self._value[1] = value
	def set_number_pair_index(self, value: PairInt) -> PairInt:
		self._value[2] = value
	def set_type_bet_pair_index(self, value: PairInt) -> PairInt:
		self._value[3] = value
	def set_point_bet_pair_index(self, value: PairInt) -> PairInt:
		self._value[4] = value

	order_pair_index: PairInt = property(get_order_pair_index, set_order_pair_index)
	channel_pair_index: PairInt = property(get_channel_pair_index, set_channel_pair_index)
	number_pair_index: PairInt = property(get_number_pair_index, set_number_pair_index)
	type_bet_pair_index: PairInt = property(get_type_bet_pair_index, set_type_bet_pair_index)
	point_bet_pair_index: PairInt = property(get_point_bet_pair_index, set_point_bet_pair_index)

def get_link_numbers_by_config(code: LINK_NUMBER, suffix: int):
	if code == LINK_NUMBER.HANG:
		return [f'{suffix}{i}' for i in range(10)]
	elif code == LINK_NUMBER.DONVI:
		return [f'{i}{suffix}' for i in range(10)]
	
def get_implicit_numbers_by_config(code: IMPLICIT_NUMBER):
	if code == IMPLICIT_NUMBER.CAP:
		return [f'{i}{i}' for i in range(10)]
	elif code == IMPLICIT_NUMBER.CHUC:
		return [f'{i}0' for i in range(10)]
	elif code == IMPLICIT_NUMBER.LE:
		return ["{0:02}".format(i) for i in range(1, 100, 2)]
	elif code == IMPLICIT_NUMBER.CHAN:
		return ["{0:02}".format(i) for i in range(0, 100, 2)]
	elif code == IMPLICIT_NUMBER.LELE:
		return ["{0:02}".format(i) for i in range(0, 100) if (i // 10) % 2 == 1 and (i % 10) % 2 == 1]
	elif code == IMPLICIT_NUMBER.CHANCHAN:
		return ["{0:02}".format(i) for i in range(0, 100) if (i // 10) % 2 == 0 and (i % 10) % 2 == 0]
	elif code == IMPLICIT_NUMBER.LECHAN:
		return ["{0:02}".format(i) for i in range(0, 100) if (i // 10) % 2 == 1 and (i % 10) % 2 == 0]
	elif code == IMPLICIT_NUMBER.CHANLE:
		return ["{0:02}".format(i) for i in range(0, 100) if (i // 10) % 2 == 0 and (i % 10) % 2 == 1]
	elif code == IMPLICIT_NUMBER.VINHO:
		return ["{0:02}".format(i) for i in range(0, 100) if (i % 10) < 5]
	elif code == IMPLICIT_NUMBER.VILON:
		return ["{0:02}".format(i) for i in range(0, 100) if (i % 10) > 4]
	elif code == IMPLICIT_NUMBER.CHUCLON:
		return ["{0:02}".format(i) for i in range(50, 100)]
	elif code == IMPLICIT_NUMBER.CHUCNHO:
		return ["{0:02}".format(i) for i in range(0, 50)]
	elif code == IMPLICIT_NUMBER.NHOLE:
		return ["{0:02}".format(i) for i in range(1, 50, 2)]
	elif code == IMPLICIT_NUMBER.LONLE:
		return ["{0:02}".format(i) for i in range(51, 100, 2)]    
	elif code == IMPLICIT_NUMBER.NHOCHAN:
		return ["{0:02}".format(i) for i in range(0, 50, 2)]
	elif code == IMPLICIT_NUMBER.LONCHAN:
		return ["{0:02}".format(i) for i in range(50, 100, 2)]
	elif code == IMPLICIT_NUMBER.LENHO:
		return ["{0:02}".format(i) for i in range(0, 100) if (i // 10) % 2 == 1 and (i % 10) % 2 < 5]    
	elif code == IMPLICIT_NUMBER.CHANNHO:
		return ["{0:02}".format(i) for i in range(0, 100) if (i // 10) % 2 == 0 and (i % 10) % 2 < 5]
	elif code == IMPLICIT_NUMBER.CHUCLE:
		return ["{0:02}".format(i) for i in range(1, 100) if (i // 10) % 2 == 1]
	elif code == IMPLICIT_NUMBER.CHUCCHAN:
		return ["{0:02}".format(i) for i in range(0, 100) if (i // 10) % 2 == 0]
	elif code == IMPLICIT_NUMBER.GIAP:
		return ['06', '07', '09', '10', '11', '12', '14', '15', '18', '23', '26', '28', '32', '35', '46', '47', '49', '50', 
		  		'51', '52', '54', '55', '58', '63', '66', '68', '72', '75', '86', '87', '89', '90', '91', '92', '94', '95', '98']
	elif code == IMPLICIT_NUMBER.NGUOCGIAP:
		return ['00', '01', '02', '03', '04', '05', '08', '13', '16', '17', '19', '20', '21', '22', '24', '25', '27', '29', '30', '31', '33', '34', 
		  		'36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '48', '53', '56', '57', '59', '60', '61', '62', '64', '65', '67', '69', 
				'70', '71', '73', '74', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '88', '93', '96', '97', '99']
	elif code == IMPLICIT_NUMBER.GIAP37:
		return ['10', '50', '90', '11', '51', '91', '12', '32', '52', '72', '92', '23', '63', '14', '54', '94', '15', '35', '55', '75', '95', 
		  		'06', '26', '46', '66', '86', '07', '47', '87', '18', '28', '58', '68', '98', '09', '49', '89']
	elif code == IMPLICIT_NUMBER.GIAP44:
		return ['06', '07', '09', '11', '55', '66', '49', '89', '10', '50', '90', '91', '92', '94', '95', '98']
	elif code == IMPLICIT_NUMBER.HE28:
		return ['00', '20', '60', '10', '50', '90', '30', '70', '31', '71', '01', '41', '81', '02', '42', 
		  		'82', '03', '43', '83', '05', '45', '85', '29', '69', '27', '67', '24', '64']
	elif code == IMPLICIT_NUMBER.HE39:
		return ['20', '21', '24', '25', '27', '29', '30', '31', '34', '36', '37', '38', '39', '40', '41', '42', '43', '45', '58', '53', '56', '57', '59', 
		  		'60', '61', '62', '64', '65', '67', '69', '70', '71', '73', '74', '76', '78', '79', '80', '81']
	elif code == IMPLICIT_NUMBER.HE44:
		return ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '11', '22', '33', '44', '55', '66', '77', '88', '99', '19', '29', '39', '49',
		  		'89', '59', '69', '79', '10', '20', '30', '40', '50', '60', '70', '80', '90', '91', '92', '93', '94', '95', '96', '97', '98']
	elif code == IMPLICIT_NUMBER.HE48:
		return ['12', '13', '14', '17', '18', '19', '21', '23', '24', '26', '28', '29', '31', '32', '34', '36', '37', '39', '41', '42', '43', '46', '47', 
		  		'48', '62', '63', '64', '67', '68', '69', '71', '73', '74', '76', '78', '79', '81', '82', '84', '86', '87', '89', '91', '92', '93', '96', '97', '98']
	elif code == IMPLICIT_NUMBER.HE56:
		return ['12', '13', '14', '15', '16', '17', '18', '21', '23', '24', '25', '26', '27', '28', '31', '32', '34', '35', '36', '37', '38', 
		  		'41', '42', '43', '45', '46', '47', '48', '51', '52', '53', '54', '56', '57', '58', '61', '62', '63', '64', '65', '67', '68', 
				'71', '72', '73', '74', '75', '76', '78', '81', '82', '83', '84', '85', '86', '87']
	elif code == IMPLICIT_NUMBER.HE58:
		return ['01', '06', '07', '08', '09', '10', '12', '17', '18', '19', '21', '23', '28', '29', '32', '34', '35', '36', '37', '38', '39', 
		  		'43', '45', '47', '49', '53', '54', '56', '57', '59', '60', '63', '65', '67', '68', '69', '70', '71', '73', '74', '75', '76', '78', '79', 
				'80', '81', '82', '83', '86', '87', '90', '91', '92', '93', '94', '95', '96', '97']
	elif code == IMPLICIT_NUMBER.TONGNHO:
		celing = 10
		rs = []
		for i in range(0,10):
			for j in range(0, 10):
				if j < celing:
					rs.append(f"{i}{j}")
				else:
					break
			celing -= 1
		return rs
	else:
		return []
#endregion