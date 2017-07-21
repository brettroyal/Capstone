from flask import Flask, render_template, request, redirect
from yummly import *
app = Flask(__name__)


def bokeh_practice():
		from bokeh.plotting import figure
		from bokeh.embed import components
		plot = figure(plot_width=600, plot_height=250, toolbar_location="below")
		plot.circle([1,2], [3,4])
		#plot_width=400, plot_height=400
		return components(plot) 	

def error_html(item):
	return '<tr><td></td><td class="whatever"><div class="whatever">Sorry, we forgot to set a timer and the '+item +' burned.<br>Try something else?</div></td></tr>'

def generate_dish_html(recipes,item,ingr):
	gen_html=''
	gen_html+=recipe_stats(recipes,item,ingr) #ADD RECIPE STATS
	script_diff_conf,div_diff_conf=diff_by_conf_plot(ingr,item) #produce the correct graph
	gen_html+='<tr><td></td><td><div align="center">'+div_diff_conf+script_diff_conf+'</div></td></tr>'
	gen_html+=bets(ingr)
	script_AbD,div_AbD=AVG_by_diff_plot(ingr,item)
	#print div_AbD
	gen_html+='<tr><td></td><td><div align="center">'+div_AbD+script_AbD+'</div></td></tr>'
	gen_html+=above_below_html(recipes,ingr)
	s,d=expected_actual(recipes,ingr)
	gen_html+='<tr><td></td><td><div align="center">'+d+s+'</div></td></tr>'
	gen_html+=ingr_table(ingr)
	return gen_html



@app.route('/',methods=['GET','POST'])
def index():
		print "index got called here."
		return render_template('index.html')

@app.route('/choose/',methods=['GET','POST'])
def choose():
		#print "got here."
		if request.method == 'POST':
			#choice=request.form['choice']
			choice='dish'
			item=request.form['food']
			if choice=='dish':
					try:
						url=get_search_url(recipe=item) #determine correct url
						results_json=requests.get(url) #get json from yummly
						recipes=pull_recipes(results_json.text) #pull apart recipes
						ingr,recipes['appr']=analyze_recipes(recipes) #analyse ingredients
					except:
						gen_html=error_html(item)
						return render_template('dish.html',ingr=item,gen_html=gen_html)	
					gen_html=generate_dish_html(recipes,item,ingr)
					return render_template('dish.html',ingr=item,gen_html=gen_html)

			return render_template('index.html', ingr=ingr)

@app.route('/ingredient/<ingr>/',methods=['GET','POST'])
def ingredient(ingr=None):
	print "Ingredient function"
	return render_template('ingr.html', ingr=ingr)

@app.route('/dish/<dish>/',methods=['GET','POST']) 
def dish(dish=None):
	if request.method == 'POST':
			return render_template('dish.html', dish=dish)
	else:
			#choice=request.form['choice']
			#item=request.args['food']
			item=dish
			print item, "was the item"
			try:
				url=get_search_url(recipe=item) #determine correct url
				results_json=requests.get(url) #get json from yummly
				recipes=pull_recipes(results_json.text) #pull apart recipes
				ingr,recipes['appr']=analyze_recipes(recipes) #analyse ingredients
			except:
				gen_html=error_html(item)
				return render_template('dish.html',ingr=item,gen_html=gen_html)	
			
			gen_html=generate_dish_html(recipes,item,ingr)
			return render_template('dish.html',ingr=item,gen_html=gen_html)
	return render_template('dish.html', dish=dish)

@app.route('/dish',methods=['GET','POST']) 
def dishblank(dish=None):
		return render_template('dish.html', dish=dish)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='bref-saucisson-83835.herokuapp.com/', port=5000)
    #app.run(host='127.0.0.1', port=5000)