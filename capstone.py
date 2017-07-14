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

@app.route('/',methods=['GET','POST'])

def index():
		print "index got called here."
		return render_template('index.html')

@app.route('/choose/',methods=['GET','POST'])
def choose():
		#print "got here."
		if request.method == 'POST':
			print "line 22"
			choice=request.form['choice']
			print "line24"
			item=request.form['food']
			print "line 26"
			print "The choice was ", choice, "and item was ", item
			if choice=='dish':
					print "in the if."
					url=get_search_url(recipe=item) #determine correct url
					print url
					results_json=requests.get(url) #get json from yummly
					print results_json.text[:50]
					recipes=pull_recipes(results_json.text) #pull apart recipes
					print "Recipes Zero:", recipes[0]
					ingr,recipes['appr']=analyze_recipes(recipes) #analyse ingredients
					print "Recipes appr: ", recipes['appr']
					div_stats=recipe_stats(recipes,item,ingr)
					div_bets=bets(ingr)
					script_diff_conf,div_diff_conf=diff_by_conf_plot(ingr,item) #produce the correct graph
					script_AbD,div_AbD=AVG_by_diff_plot(ingr,item)
					table_div=ingr_table(ingr)
					return render_template('dish.html', ingr=item, div_conf=div_diff_conf,script_conf=script_diff_conf,div_stats=div_stats,div_bets=div_bets,table_div=table_div,script_AbD=script_AbD,div_AbD=div_AbD)
			# elif (choice=='ingr'):
		# 		return render_template('ingr.html', dish=item)
		# 	else:
		# 		return render_template('index.html', ingr=ingr)
		# else:
			return render_template('index.html', ingr=ingr)



@app.route('/ingredient/<ingr>/',methods=['GET','POST'])
def ingredient(ingr=None):
	print "Ingredient function"
	return render_template('ingr.html', ingr=ingr)

@app.route('/dish/<dish>/',methods=['GET','POST'])
def dish(dish=None):
	print "Dish function"
	return render_template('dish.html', dish=dish)

if __name__ == '__main__':
    app.run(debug=True)
    app.run(host='bref-saucisson-83835.herokuapp.com/', port=5000)
    #app.run(host='127.0.0.1', port=5000)