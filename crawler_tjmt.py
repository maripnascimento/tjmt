import requests
from bs4 import BeautifulSoup
import re

def get_lawsuit(number):
	print('fazendo requisicao do cabecalho do processo')	

	data = {
		'instancia':'1',
		'comarca':'',
		'cpfCnpj':'',
		'processo':number
	}

	response = requests.post('http://www.tjmt.jus.br/Home/RedirecionarConsulta',data=data,verify=False)
	lawsuit = parse(response.content)


	return lawsuit

def parse(data):
	print('filtrando as informacoes')

	parsed = BeautifulSoup(data,'html.parser')

	text = parsed.text
	#import pdb; pdb.set_trace()

	lawsuit = {
		'number': get_number(text),
		'court_section': get_court_section(text),
		'judge': get_judge(text),
		'kind': get_kind(text),
		'court': get_court(text),
		'activity_list': get_activity_list(parsed),
		}

	return lawsuit	

def get_number(text):
	print('extraindo o numero do processo')


	cnj = re.search(r'\d{7}-\d{2}.\d{4}.\d.\d{2}.\d{4}',text)
	return cnj.group()

def get_court_section(text):
	court_section = re.search(r'Comarca:\n(.*)',text)
	if court_section:
		return court_section.group(1)

def get_kind(text):
	kind = re.search(r'Tipo:\n(.*)',text)
	if kind:
		return kind.group(1)

def get_court(text):
	court = re.search(r'Lot.*o:\n(.*)',text)
	if court:
		return court.group(1)

def get_judge(text):
	judge = re.search(r'Juiz.*:\n(.*)',text)
	if judge:
		return judge.group(1)

def get_activity_list(data):
	activity_list =[]
	div = data.find('div', id='listaAndamento') 
	trs = div.find_all('tr')
	for tr in trs:
		tds = tr.find_all('td')
		activity = {
		'data':tds[0].text,
		'texto':tds[1].text
		}
		activity_list.append(activity)


	return activity_list
	
		




print(get_lawsuit('1036189-73.2020.8.11.0002'))