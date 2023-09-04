from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table1 = soup.find_all('a',attrs={'class':'n'})

row=soup.find_all('span',attrs={'class':'w'})
print(len(row))
jumlahbaris=(len(row))

jumlahbaris = len(jumlahbaris)

temp = [] #initiating a list 

for i in range(1, jumlahbaris):
#insert the scrapping process here

for i in range(0, jumlahbaris):
    #get tanggal
    tanggal =soup.find_all('a',attrs={'class':'n'})[i].text

    #get nilai mata uang
    nilai_uang = soup.find_all('span',attrs={'class':'w'})[i].text

    temp.append((tanggal,nilai_uang))
    
temp = temp[::-1]

#change into dataframe
ws1 = pd.DataFrame(temp,columns=('tanggal','nilai_uang'))

#insert data wrangling here

ws1['mata_uang']=ws1['nilai_uang'].str.split().str[2]
ws1=ws1[['tanggal','mata_uang']]
ws1['tanggal']=ws1['tanggal'].astype('datetime64[ns]')
ws1['mata_uang']=ws1['mata_uang'].str.replace(',','')
ws1['mata_uang']=ws1['mata_uang'].str.replace('Rp','')
ws1['mata_uang']=ws1['mata_uang'].astype('float64')
ws1=ws1.set_index('tanggal')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{ws1["mata_uang"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = ws1.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)