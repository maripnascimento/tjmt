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
	#import pdb; pdb.set_trace()
	text = parsed.text
	number = get_number(text)

	lawsuit = {
		'number':number,
	}

	return lawsuit	

def get_number(text):
	print('extraindo o numero do processo')


	cnj = re.search(r'\d{7}-\d{2}.\d{4}.\d.\d{2}.\d{4}', text)
	return cnj.group()


print(get_lawsuit('1036189-73.2020.8.11.0002'))