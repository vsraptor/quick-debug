import inspect

"""
Quick debugging : if you are like me and are not used to a debuger
 or logging is too cumbersome, then this is for you.

Do all your printing with :

   > say(debug_lvl, ... ) 

debug_lvl : can be str, int or float

By default all say() print the rest of the arguments, except the first.

You can set globally what levels to exclude by using :

> OFF.off(1)

or specifically per object :

> a = ABC()
> a.off = 1

The global and local configurations are merged.

Here are possible ways to specify the configuration.

> a.off = 1  
> a.off = 1.1
> a.off = 'a'
> a.off = [1,2]
> a.off = [1,1.1,3,'b']
> a.off = '*' #disable all
> a.off = [(1,3)] #range from 1 to 3
> a.off = [(1,2),'a',3] 

"""

class OFF(object):
	off = None
	@classmethod
	def set(cls, value): cls.off = value
	@classmethod
	def get(cls): return cls.off
	@classmethod
	def reset(cls): cls.off = None


def say(*args, **kwargs) :

	def check(off,lvl) :
		if isinstance(off,str)   and isinstance(lvl,str)    and (lvl == off or off == '*') : return None
		if isinstance(off,int)   and isinstance(lvl,int)    and  lvl == off : return None
		if isinstance(off,float) and isinstance(lvl,float)  and  lvl == off : return None
		return True


	lvl = args[0]
	frame = inspect.currentframe().f_back.f_locals
	obj = frame['self'] if 'self' in frame else None
	if obj is None : raise Exception("use only in objects")

	deny = OFF.get() #global override
	if deny is None : deny = [] 
	elif not isinstance(deny,list): deny = [deny]

	if hasattr(obj, 'off') : 
		if isinstance(obj.off, list) : deny += obj.off
		else : deny += [obj.off]


	if deny is not None :
		#first check for simple types
		if check(deny, lvl) is None : return None

		if isinstance(deny, list) : 
			for off in deny :
				#check range
				if isinstance(off, tuple) and not isinstance(lvl,str) and (off[0] <= lvl <= off[1]) : return None 
				if check(off, lvl) is None : return None

	print(*args[1:], **kwargs)

def nope(*args, **kwargs): return None


class ABC:

	def test(self):
		say(1, 'level 1')	
		say(2, 'level 2')	
		say(3, 'level 3')	
		say(10, 'level 10')	
		say(1.1, 'level 1.1')
		say(1.2, 'level 1.2')	
		say('a', 'level a')	
		say('b', 'level b')	
		say(2.2, 'level 2.2')	
