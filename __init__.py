def baseN(num,b,numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
	return ((num == 0) and  "0" ) or ( baseN(num // b, b).lstrip("0") + numerals[num % b])