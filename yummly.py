
# coding: utf-8

# In[1]:


import requests
import json
import pprint
import numpy as np
import math
from bokeh.plotting import figure, show, output_file,output_notebook, ColumnDataSource
from bokeh.models import HoverTool,WheelZoomTool,PanTool
from bokeh.charts import Scatter, output_file, show
from bokeh.io import save
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.embed import components
import string

app_id='fe5797c1'
key='d5a953efaeeb4f854defde290177c340'
auth_string='_app_id='+app_id+'&_app_key='+key
ingr='lemon'
recipe='key lime pie'
recipe.replace(' ','%20')
pp = pprint.PrettyPrinter(indent=4)


# In[2]:


def get_recipe_string(recipe_id):
    return


# In[3]:


def get_search_url(recipe=False,ingr=False,max=500):
    stub='http://api.yummly.com/v1/api/recipes?'
    if recipe and not ingr:
        query='&q='+recipe.replace(' ','%20')+'&maxResult='+str(max)
        return stub+auth_string+query #your search parameters
    elif ingr and not recipe:
        query='&allowedIngredient[]='+ingr+'&maxResult='+str(max)
        return stub+auth_string+query
    elif ingr and recipe:
        query=stub+auth_string+'&q='+recipe.replace(' ','%20')+'&allowedIngredient[]='+ingr+'&maxResult='+str(max)
        return query
    else:
        query='q='+'black bean soup'.replace(' ','%20')
        return 'http://api.yummly.com/v1/api/recipes?'+auth_string+'&'+query


# In[4]:


def pull_recipes(the_json): #receives a json, returns a dictionary of recipes
    data = json.loads(the_json)
    print "data got loaded"
    recipes={}
    count=0
    running_total=0
    ingr_count=0.0
    for this_entry in data['matches']:
        if ingr_count==0.0:
            print "Entered the for loop"
        this_recipe={}
        this_recipe['title']=this_entry['recipeName']
        this_recipe['rating']=this_entry['rating']
        this_recipe['ingredients']=this_entry['ingredients']
        print "Assigned three dictionary entries"
        recipes[this_entry['id']]=this_recipe
        ingr_count+=len(this_recipe['ingredients'])
        count+=1
        running_total+=this_entry['rating']
    recipes['AVG']=float(running_total)/count
    recipes['COUNT']=(count)
    recipes['INGRS']=ingr_count/count
    print "exited the for loop."
    return recipes


# In[5]:


def analyze_recipes(recipes): #gets a dict of recipes, returns a dict of ingredients
    all_ingredients={}
    for recipe in recipes:
        if recipe not in ['AVG','COUNT','INGRS']:
            ingr_list=recipes[recipe]['ingredients']
            for ingredient in ingr_list:
                if ingredient not in all_ingredients:
                    all_ingredients[ingredient]=[recipes[recipe]['rating']]
                else:
                    all_ingredients[ingredient].append(recipes[recipe]['rating'])
    avg_value={}
    appr_count=0
    for ingr in all_ingredients:
        avg_value[ingr]={}
        avg_value[ingr]['AVG']=float(sum(all_ingredients[ingr]))/float(len(all_ingredients[ingr]))
        avg_value[ingr]['COUNT']=len(all_ingredients[ingr]) #this is how many recipes it appears in!  duh!
        avg_value[ingr]['sansAVG']=((recipes['COUNT']*recipes['AVG'])-(avg_value[ingr]['COUNT']*avg_value[ingr]['AVG']))/(recipes['COUNT']-avg_value[ingr]['COUNT'])
        try:
            avg_value[ingr]['diff']=(avg_value[ingr]['AVG']-avg_value[ingr]['sansAVG'])/avg_value[ingr]['AVG']
        except:
            avg_value[ingr]['diff']=(avg_value[ingr]['AVG']-avg_value[ingr]['sansAVG'])/(avg_value[ingr]['AVG']+1)
        
       
        avg_value[ingr]['apprRATE']=avg_value[ingr]['COUNT'] /float(len(recipes)-2) #how many ingr its in/how many recs there are
        appr_count+=avg_value[ingr]['apprRATE'] #this appears in 10, previous ore was in 15. when we divide this by #ingr!
        #print ingr, "'s app_rate is", avg_value[ingr]['COUNT'], "/ ", len(recipes)-2, "= ", avg_value[ingr]['apprRATE']
        #print "now apprcount is ", appr_count
        #that actually appears to be correct.

    appr_avg=appr_count/float(len(all_ingredients)) #this is how many ingre*recipes /total distinct ingr
    #print appr_count , "was probably like 6000"
    #print appr_avg , " is the appr avg, which might be right  now."
    
    
    for ingr in avg_value:
        avg_value[ingr]['CONF']=(avg_value[ingr]['apprRATE'])/appr_avg #the conf rating is 
        #print ingr, "confidence rate; ", (avg_value[ingr]['CONF']*100) 
    return avg_value,appr_avg


# In[6]:


# def print_ingredients_somehow(ingr):
#     sort_diff=sorted(ingr, key=lambda x: (ingr[x]['diff']))

#     for thing in sort_diff:
#         #print ingr[thing]['CONF'], ingr[thing]['apprRATE'], thing, ingr[thing]['diff'] ,ingr[thing]['AVG']
#         #print thing , " changes the rating by %02.2f"%(ingr[thing]['diff']*100), " with a confidence rating of %02.2f"%(ingr[thing]['CONF']*100)

#     #print recipes['AVG']
#     #print recipes['COUNT']

#     return


# In[175]:



def plot_ingr(ingr,recipe,average):
    the_title="Ingredient Analysis for ", recipe
    output_file("ingr5.html",title=the_title)
    TOOLS="hover,crosshair,pan,wheel_zoom,box_zoom,undo"
    
    x=np.array(list(ingr[thing]['diff'] for thing in ingr))
    y=np.array(list(ingr[thing]['apprRATE'] for thing in ingr))
    r=np.array(list((math.log(ingr[thing]['CONF']+1)/10.0) for thing in ingr))
    h=np.array(list(ingr for thing in ingr))
    
    p = figure(tools=TOOLS)
    p.scatter(x,r,radius=.01,fill_alpha=.1, line_color=None,color="Blue")
     
    save(p)
           
    return


# In[8]:


# the_recipe='hummus'
#results_json=requests.get(get_search_url(recipe=the_recipe)) #not calling this so i dont bug the api


# In[ ]:


#pp.pprint(results_json.text)


# In[101]:


# import pickle
# #recipes=pickle.load(open("recipes.p","rb"))
# recipes=pull_recipes(results_json.text)
# #pp.pprint(recipes)


# # In[102]:


# ingr,recipes['appr']=analyze_recipes(recipes)
# #pp.pprint(ingr)


# # In[103]:



# pickle.dump(recipes, open( "recipes.p", "wb" ) )


# # In[122]:


# plot_ingr(ingr,the_recipe,recipes['AVG']) #calls the plotting function.


# # In[191]:


# from pandas import DataFrame

# def dataframe_test(ingr,recipe):
#     ingr_df=DataFrame.from_dict(ingr,orient='index')
#     the_title="Ingredient Analysis for ", recipe
#     output_file("ingr6.html",title=the_title)

#     hover = HoverTool(
#         tooltips=[
#             ("index", "$index"),
#             ("(x,y)", "($x, $y)"),
#             ("desc", "@desc"),
#         ]
#     )
#     TOOLS="hover"#,crosshair,pan,wheel_zoom,box_zoom,undo,hover"
#     p = Scatter(ingr_df, x='diff', y='apprRATE', title="Count versus Diff", xlabel="Appearances", ylabel="Differential")
#     #return ingr_df
#     #p = Scatter(df, x='mpg', y='hp', title="HP vs MPG",
#     #        xlabel="Miles Per Gallon", ylabel="Horsepower")
#     save(p)

# dataframe_test(ingr,the_recipe)


# In[189]:


def another_test(ingr,recipe_name,file_name):
    the_title=recipe_name + " Ingredient Analysis"
    output_file(file_name,title=the_title)
    
    x1=np.array(list(ingr[thing]['diff'] for thing in ingr))
    y1=np.array(list(ingr[thing]['apprRATE'] for thing in ingr))
    r1=np.array(list((math.log(ingr[thing]['CONF']+1)/10.0) for thing in ingr))
    desc1=np.array(list(thing for thing in ingr))
    TOOLS="hover,crosshair,pan,wheel_zoom,box_zoom,undo,hover"
    source = ColumnDataSource(
            data=dict(
                x=x1[:100],
                y=r1[:100],
                desc=desc1[:100],
            )
        )

    hover = HoverTool(
            tooltips=[
                #("index", "$index"),
                ("Ingr:", "@desc"),
                ("Value Added:", "$x"),
                ("Rarity", "$y"),
                
            ]
        )
    zoom = WheelZoomTool()
    #p = figure(tools=TOOLS)
    graph_title=the_title+": Added Value(x) versus Confidence(y)"
    p = figure(plot_width=800, plot_height=600,
               title=graph_title, tools=[hover,zoom])

    p.circle('x', 'y', size=10, source=source,fill_alpha=.1,color="Green")

    save(p)
    return


# In[ ]:

def AVG_by_diff_plot(ingr,recipe_name):
    the_title=recipe_name + " Ingredient Analysis"
    #output_file(file_name,title=the_title)
    
    x1=np.array(list(ingr[thing]['diff'] for thing in ingr))
    y1=np.array(list(ingr[thing]['AVG'] for thing in ingr))
    r1=np.array(list((math.log(ingr[thing]['CONF']+1)/10.0) for thing in ingr))
    desc1=np.array(list(thing for thing in ingr))
    TOOLS="hover,crosshair,pan,wheel_zoom,box_zoom,undo,hover"
    source = ColumnDataSource(
            data=dict(
                x=x1,
                y=y1,
                desc=desc1,
            )
        )

    hover = HoverTool(
            tooltips=[
                #("index", "$index"),
                ("Ingr:", "@desc"),
                ("Value Added:", "$x"),
                ("Avg Rate", "$y"),
                
            ]
        )
    zoom = WheelZoomTool()
    pan=PanTool()
    #p = figure(tools=TOOLS)
    graph_title=the_title+": Added Value(x) versus Average Value(y)"
    p = figure(plot_width=600, plot_height=400,
               title=graph_title, tools=[pan,hover,zoom],toolbar_location="above")

    p.circle('x', 'y', size=10, source=source,fill_alpha=.1,color="Orange")

    save(p)
    return components(p)


def diff_by_conf_plot(ingr,recipe_name):
    the_title=recipe_name + " Ingredient Analysis"
    #output_file(file_name,title=the_title)
    
    x1=np.array(list(ingr[thing]['diff'] for thing in ingr))
    y1=np.array(list(ingr[thing]['apprRATE'] for thing in ingr))
    r1=np.array(list((math.log(ingr[thing]['CONF']+1)/10.0) for thing in ingr))
    desc1=np.array(list(thing for thing in ingr))
    TOOLS="hover,crosshair,pan,wheel_zoom,box_zoom,undo,hover"
    source = ColumnDataSource(
            data=dict(
                x=x1,
                y=r1,
                desc=desc1,
            )
        )

    hover = HoverTool(
            tooltips=[
                #("index", "$index"),
                ("Ingr:", "@desc"),
                ("Value Added:", "$x"),
                ("Rarity", "$y"),
                
            ]
        )
    zoom = WheelZoomTool()
    pan=PanTool()
    #p = figure(tools=TOOLS)
    graph_title=the_title+": Added Value(x) versus Confidence(y)"
    p = figure(plot_width=600, plot_height=400,
               title=graph_title, tools=[pan,hover,zoom],toolbar_location="above")

    p.circle('x', 'y', size=10, source=source,fill_alpha=.1,color="Orange")

    save(p)
    return components(p)


# In[190]:


# another_test(ingr,the_recipe,"hummus.html")


# In[199]:


def recipes_to_graph(recipe_type):
    url=get_search_url(recipe=recipe_type)
    results_json=requests.get(url)
    recipes=pull_recipes(results_json.text)
    ingr,recipes['appr']=analyze_recipes(recipes)
    file_name=recipe_type+'.html'
    another_test(ingr,recipe_type,file_name)
def recipe_stats(recipes,the_recipe,ingr):
    return_string='<div class="whatever">'
    return_string+="There are "+ str(recipes['COUNT'])+ " total recipes for <b>"+ the_recipe+ "</b><br>"
    return_string+="The average rating is "+ str(recipes['AVG'])+ "<br>"
    return_string+="There are a total of "+ str(len(ingr)) +" distinct ingredients used in these recipes"+"<br>"
    return_string+= "Each recipe has an average of "+str(recipes['INGRS'])+" total ingredients <br>"
    common=np.array(list((float(ingr[thing]['apprRATE']),thing) for thing in ingr))
    
    most_common=sorted(common,reverse=True,key=lambda x:x[0])
    most_common=[x[1] for x in most_common[:5]]
    top_5=most_common[0]+", "+most_common[1]+", "+most_common[2]+", "+most_common[3]+", and "+most_common[4]
    return_string+= "The most common ingredients are: "+top_5+ "<br>"
    
    most_common=sorted(common,key=lambda x:x[0])
    most_common=[x[1] for x in most_common[:5]]
    top_5=most_common[0]+", "+most_common[1]+", "+most_common[2]+", "+most_common[3]+", and "+most_common[4]
    return_string+= "The least common ingredients are: "+ top_5+ "<br></div>"
    return return_string

def bets(ingr):
    return_string='<tr><td></td><td class="whatever"><div class="whatever">'
    confidence=np.array(list((float(1+ingr[thing]['diff']**2*(((1+ingr[thing]['CONF'])**2))),thing) for thing in ingr))
    conf_sorted=sorted(confidence,reverse=True,key=lambda x:float(x[0]))
    #print conf_sorted
#     print conf_sorted[0:5]
#     print conf_sorted[-6:-1]
    best_bets=conf_sorted[0][1]+", "+conf_sorted[1][1]+", "+conf_sorted[2][1]+", "+conf_sorted[3][1]+", and "+conf_sorted[4][1]
    
    worst_bets=conf_sorted[-1][1]+", "+conf_sorted[-2][1]+", "+conf_sorted[-3][1]+", "+conf_sorted[-4][1]+", and "+conf_sorted[-5][1]
    return_string+="Your best bets are "+best_bets+"<br>"+"Your worst bets are "+worst_bets+'<br>'
    return_string+="</div></td></tr>"
    return return_string

def ingr_table(ingr):
    from pandas import DataFrame
    import string
    ingr_df=DataFrame.from_dict(ingr,orient='index')
    return_string=ingr_df.to_html()
    sortable=string.replace(return_string,'dataframe','sortable')
    return sortable
    #return return_string

