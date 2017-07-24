#t=int(raw_input())
t=5
# S=[]
# for x in range(0:t):
# 	S.append(raw_input())

S=['ab','bb','hefg','dhck', 'dkhc']

def decide(s):
	the_sorted="".join(sorted(s,reverse=True))
	if the_sorted==s:
		print "no answer"
	else:
		#Whats the second highest after s[0]
		#print the_sorted[the_sorted.index(s[0])-1]
		the_min=min(s)
		#print the_min , "is the min"
		next_min=the_sorted[the_sorted.index(s[0])-1]
		print next_min, "is the next min after ",s[0], ": " ,
		pos_switch=s.index(next_min)
		#print pos_switch
		new_string=s[0:pos_switch]+s[pos_switch+1:]
		new_string=''.join(sorted(new_string))

		print next_min+new_string
		
		#print the_min,next_min
		# for start in range(0,len(s)-1):


		return

for s in S:
	decide(s)
	
					





		


