
import re 
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Regex Application"

@app.route("/getRegex")
def get_regex():
    req_data = request.get_json()
    resp = createRegex(req_data['text'])
    return resp


countries = ('AD','AE','AF','AG','AI','AL','AM','AO','AQ','AR','AS','AT','AU','AW','AX','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BL','BM','BN','BO','BQ','BR','BS','BT','BV','BW','BY','BZ','CA','CC','CD','CF','CG','CH','CI','CK','CL','CM','CN','CO','CR','CU','CV','CW','CX','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','EH','ER','ES','ET','FI','FJ','FK','FM','FO','FR','GA','GB','GD','GE','GF','GG','GH','GI','GL','GM','GN','GP','GQ','GR','GS','GT','GU','GW','GY','HK','HM','HN','HR','HT','HU','ID','IE','IL','IM','IN','IO','IQ','IR','IS','IT','JE','JM','JO','JP','KE','KG','KH','KI','KM','KN','KP','KR','KW','KY','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MF','MG','MH','MK','ML','MM','MN','MO','MP','MQ','MR','MS','MT','MU','MV','MW','MX','MY','MZ','NA','NC','NE','NF','NG','NI','NL','NO','NP','NR','NU','NZ','OM','PA','PE','PF','PG','PH','PK','PL','PM','PN','PR','PS','PT','PW','PY','QA','RE','RO','RS','RU','RW','SA','SB','SC','SD','SE','SG','SH','SI','SJ','SK','SL','SM','SN','SO','SR','SS','ST','SV','SX','SY','SZ','TC','TD','TF','TG','TH','TJ','TK','TL','TM','TN','TO','TR','TT','TV','TW','TZ','UA','UG','UM','US','UY','UZ','VA','VC','VE','VG','VI','VN','VU','WF','WS','YE','YT','ZA','ZM','ZW')
currencies = ("AFA", "ALL", "DZD", "AOA", "ARS", "AMD", "AWG", "AUD", "AZN", "BSD", "BHD", "BDT", "BBD", "BYR", "BEF", "BZD", "BMD", "BTN", "BTC", "BOB", "BAM", "BWP", "BRL", "GBP", "BND", "BGN", "BIF", "KHR", "CAD", "CVE", "KYD", "XOF", "XAF", "XPF", "CLP", "CLF", "CNY", "COP", "KMF", "CDF", "CRC", "HRK", "CUC", "CZK", "DKK", "DJF", "DOP", "XCD", "EGP", "ERN", "EEK", "ETB", "EUR", "FKP", "FJD", "GMD", "GEL", "DEM", "GHS", "GIP", "GRD", "GTQ", "GNF", "GYD", "HTG", "HNL", "HKD", "HUF", "ISK", "INR", "IDR", "IRR", "IQD", "ILS", "ITL", "JMD", "JPY", "JOD", "KZT", "KES", "KWD", "KGS", "LAK", "LVL", "LBP", "LSL", "LRD", "LYD", "LTC", "LTL", "MOP", "MKD", "MGA", "MWK", "MYR", "MVR", "MRO", "MUR", "MXN", "MDL", "MNT", "MAD", "MZM", "MMK", "NAD", "NPR", "ANG", "TWD", "NZD", "NIO", "NGN", "KPW", "NOK", "OMR", "PKR", "PAB", "PGK", "PYG", "PEN", "PHP", "PLN", "QAR", "RON", "RUB", "RWF", "SVC", "WST", "STD", "SAR", "RSD", "SCR", "SLL", "SGD", "SKK", "SBD", "SOS", "ZAR", "KRW", "SSP", "XDR", "LKR", "SHP", "SDG", "SRD", "SZL", "SEK", "CHF", "SYP", "TJS", "TZS", "THB", "TOP", "TTD", "TND", "TRY", "TMT", "UGX", "UAH", "AED", "UYU", "USD", "UZS", "VUV", "VEF", "VND", "YER", "ZMK", "ZWL")
def specialCharReg(s): 
    regex = re.compile('[0-9-@_!#$%^&*()<>?/\|}{~:]') 
    dateRegex = re.compile('\d{2,4}/\d{2}/\d{2,4}') 
    timeRegex = re.compile("\d{2}:\d{2}:\d{2}(\s\w{2})?") 
    if(regex.search(s) == None or s.isalnum()): 
       return s 
    elif(dateRegex.match(s) != None): 
        return "(\d{2,4}/\d{2}/\d{2,4})" 
    elif(timeRegex.match(s) != None): 
        return "(\d{2}:\d{2}:\d{2}(\s\w{2})?)" 
    for i in s: 
        if not i.isalpha() and not i.isdigit() and not i == " ": 
            ch = i 
            break 
    w_list = s.split(ch) 
    if ch == "-": 
        return "\s*" + w_list[0] + "(\s*|" + ch + "|.)" + w_list[1] + "\s*" 
    if ch == "/": 
        return "((\s*" + w_list[0] + "(\s*|" + ch + "|.)" + w_list[1] + "\s*)|\s*"+ w_list[0] + "\s*|\s*" + w_list[1]+"\s*)" 

def cleanData(raw_text): 
    raw_text = raw_text.upper() 
    regex_clean_html = re.compile('<.*?>') 
    cleantext = re.sub(regex_clean_html,' ',raw_text) 
    cleantext = re.sub(' +',' ', cleantext) 
    cleantext = cleantext.replace(u'\xa0', u' ') 
    cleantext = cleantext.upper() 
    return cleantext 

def createRegex(raw_texts): 
    raw_text = str(raw_texts)
    ini_str = cleanData(raw_text) 
    ll = ini_str.split(" ") 
    country_regex = "\w{2}\s*" 
    currency_regex = "\w{3}\s*" 
    regex_str = "" 
    for i in ll: 
        if i.isdigit(): 
            regex_str += "\d+(.\d+)?" 
        elif specialCharReg(i) != i: 
            regex_str += specialCharReg(i) 
        elif i in countries: 
            regex_str += country_regex 
        elif i in currencies: 
            regex_str += currency_regex 
        else: 
            regex_str += i 
            regex_str += "\s*" 
    res_regex = regex_str.replace("\s*\s*\s*", "\s*") 
    res_regex = regex_str.replace("\s*\s*", "\s*") 
    return res_regex 
