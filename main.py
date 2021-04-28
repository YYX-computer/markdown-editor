from tkinter.filedialog import askopenfilename as aof,asksaveasfilename as asf
from tkinter.messagebox import askyesno as askyn
from PIL import Image,ImageDraw,ImageTk
import tkinter.font as tkFont
from tkinter import ttk
import tkinter as tk
import requests
import time
import io
import re
fontname = ...
d = tk.Tk()
display = tk.Text(d,font=(fontname,15,''))
display.grid(row=0,column=0)
writer = tk.Toplevel()
text = tk.Text(writer)
text.grid(row=0,column=0)
cont = ''
def clear():
	global display
	display.delete(0.0,tk.END)
def proc(text):
	res = text.split('$')
	for i in range(len(res)):
		if(i % 2):
			imgTk = get_KaTeX(res[i])
			res[i] = tk.Label(display,image=imgTk)
			res[i].image = imgTk
	newres = []
	for i in range(len(res)):
		if(not isinstance(res[i],str)):
			newres.append(res[i])
			continue
		s = res[i].split('`')
		for j in range(len(s)):
			if(j % 2):
				font = tkFont.nametofont("TkFixedFont")
				newres.append(tk.Label(display,text=s[j],font=font))
			else:
				newres.append(s[j])
	d = {
		"italic":["\*[^\*_~]+\*","_[^\*_~]+_"],
		"bold":["\*\*[^\*_~]+\*\*","__[^\*_~]+__"],
		"overstrike":["~~[^\*_~]+~~"],
		"italic bold":
			[
				"\*\*\*[^\*_~]+\*\*\*",
				"___[^\*_~]+___",
				"_\*\*[^\*_~]+\*\*_",
				"\*\*_[^\*_~]+_\*\*",
				"\*__[^\*_~]+__\*"
				"__\*[^\*_~]+\*__"
			],
		"italic overstrike":
			[
				"~~\*[^\*_~]+\*~~",
				"\*~~[^\*_~]+~~\*",
				"~~_[^\*_~]+_~~",
				"_~~[^\*_~]+~~_"
			],
		"bold overstrike":
			[
				"~~\*\*[^\*_~]+\*\*~~",
				"\*\*~~[^\*_~]+~~\*\*",
				"~~__[^\*_~]+__~~",
				"__~~[^\*_~]+~~__"
			],
		"italic bold overstrike":
			[
				"~~\*\*\*[^\*_~]+\*\*\*~~",
				"\*~~\*\*[~\*_~]+\*\*~~\*",
				"\*\*~~\*[^\*_~]+\*\*\*~~",
				"\*\*\*~~[^\*_~]+\*\*\*~~",
				"~~___[^\*_~]+___~~",
				"_~~__[^\*_~]+__~~_",
				"__~~_[^\*_~]+_~~__",
				"___~~[^\*_~]+~~___",
				"~~_\*\*[^\*_~]+\*\*_~~",
				"_~~\*\*[^\*_~]+\*\*~~_",
				"_\*\*~~[^\*_~]+~~\*\*_",
				"~~\*__[^\*_~]+__\*~~",
				"\*~~__[^\*_~]+__~~\*",
				"\*__~~[^\*_~]+~~__\*",
				"~~__\*[^\*_~]+\*__~~",
				"__~~\*[^\*_~]+\*~~__",
				"__\*~~[^\*_~]+~~\*__",
				"~~\*\*_[^\*_~]+_\*\*~~",
				"\*\*~~_[^\*_~]+_~~\*\*",
				"\*\*_~~[^\*_~]+~~_\*\*"
			]
	}
	def legal(s):
		try:
			f = re.match('[\*_~]+',s).group()
		except:
			return False
		rf = f[::-1]
		f = f.replace('*','\*')
		rf = rf.replace('*','\*')
		pat = f + '[^\*_~]+' + rf
		mat = re.match(pat,s)
		return mat and mat.group() == s
	res = []
	r = []
	for i in d.values():
		r.extend(i)
	r = sorted(r,key=lambda a:-len(a))
	for i in newres:
		if(not isinstance(i,str)):
			res.append(i)
			continue
		sp = [i]
		for j in r:
			_sp = sp[:]
			sp = []
			for k in _sp:
				if(legal(k)):
					sp.append(k)
				else:
					sp.extend(re.split('(%s)'%j,k))
		for j in sp:
			flag = False
			for k in d:
				for l in d[k]:
					if(re.match(l,j)):
						flag = True
						if(k.endswith('overstrike')):
							font = (fontname,15,k[:-10])
							font = tkFont.Font(font=font,overstrike=True)
						else:
							font = (fontname,15,k)
							font = tkFont.Font(font=font)
						txt = re.search('[^\*_~]+',j).group()
						lb = tk.Label(display,text=txt,font=font)
						res.append(lb)
						break
				if(flag):break
			if(not flag):
				lb = tk.Label(display,text=j)
				res.append(lb)
	return res
def read_md(file):
 	with open(file) as f:
 			return f.read()
def write_md(file,cont):
 	with open(file,'w') as f:
 		f.write(cont)
def get_KaTeX_io(katex):
	resp = requests.get('https://latex.codecogs.com/png.image?\dpi{110} ' + katex)
	return io.BytesIO(resp.content)
def get_image_io(link):
	resp = requests.get(link)
	return io.BytesIO(resp.content)
def get_KaTeX(katex):
	img_io = get_KaTeX_io(katex)
	img = Image.open(img_io)
	return ImageTk.PhotoImage(img)
def get_image(link):
	img_io = get_image_io(link)
	img = Image.open(img_io)
	return ImageTk.PhotoImage(img)
def get_spliter():
	w = max(1,display.winfo_width() - 6)
	img = Image.new('RGB',(w,1),(221,221,221))
	return ImageTk.PhotoImage(img)
def render_md():
	d.update()
	clear()
	l = 0
	code = False
	buf = ''
	n = 0
	for i in cont.split('\n'):
		if(n):
			n -= 1
			continue
		if(code and i != '```'):
			buf += i + '\n'
			continue
		if(i.startswith('# ')):
			lb = tk.Label(display,text=i[2:],font=(fontname,40,'bold'))
		elif(i.startswith('## ')):
			lb = tk.Label(display,text=i[3:],font=(fontname,35,'bold'))
		elif(i.startswith('### ')):
			lb = tk.Label(display,text=i[4:],font=(fontname,30,'bold'))
		elif(i.startswith('#### ')):
			lb = tk.Label(display,text=i[5:],font=(fontname,25,'bold'))
		elif(i.startswith('##### ')):
			lb = tk.Label(display,text=i[6:],font=(fontname,20,'bold'))
		elif(i.startswith('###### ')):
			lb = tk.Label(display,text=i[7:],font=(fontname,15,'bold'))
		elif(i.startswith('- [ ] ')):
			cbtn = tk.Checkbutton(display,text='',state=tk.DISABLED)
			lb = [cbtn] + proc(i[6:])
		elif(i.startswith('- [x] ')):
			cbtn = tk.Checkbutton(display,text='',state=tk.DISABLED)
			cbtn.select()
			lb = [cbtn] + proc(i[6:])
		elif(i.startswith('- ') or i.startswith('* ') or i.startswith('+ ')):
			i = '● ' + i[2:]
			lb = proc(i)
		elif(i.startswith(': ')):
			lb = proc('\t'+i[2:])
		elif(i.startswith('$$') and i.endswith('$$') and i not in ('$$','$$$')):
			imgTk = get_KaTeX(i[2:-2])
			lb = tk.Label(display,image=imgTk)
			lb.image = imgTk
		elif(set(i) in ({'-'},{'*'}) and len(i) >= 3):
			imgTk = get_spliter()
			lb = tk.Label(display,image=imgTk)
			lb.image = imgTk
		elif(i == '```'):
			if(code):
				lb = tk.Text(display)
				lb.insert(0.0,buf)
				h = float(lb.index(tk.END)) - 2
				lb.config(height=h)
				buf = ''
				code = False
			else:
				code = True
				continue
		else:
			try:
				head = i.split('|')
				check = cont.split('\n')[l + 1].split('|')
				assert len(head) == len(check)
				assert set(''.join(check)) == {'-'}
				assert all(check)
				body = []
				after = cont.split('\n')[l + 2:]
				n = 1
				for j in after:
					if(len(j.split('|')) == len(head)):
						body.append(j.split('|'))
					else:
						break
					l += 1
					n += 1
				assert body
				lb = ttk.Treeview(display,columns=[i for i in range(len(head))],show='headings')
				for j in range(len(head)):
					lb.heading(j,text=head[j])
				for j in body:
					lb.insert('','end',value=j)
			except:
				n = 0
				lb = proc(i)
		if(not isinstance(lb,list)):
			lb = [lb]
		for i in lb:
			display.window_create(tk.INSERT,window=i)
		display.insert(tk.INSERT,'\n')
		l += 1
def update_writer():
	global cont
	writer.update()
	cont = text.get(0.0,tk.END)
def main():
	global cont
	writer.title('writer')
	d.title('displayer')
	file = aof(title='open a markdown file')
	if(file):
		cont = read_md(file)
	text.insert(0.0,cont)
	while(1):
		try:
			update_writer()
			render_md()
		except:
			try:
				writer.destroy()
			except:
				pass
			try:
				display.destroy()
			except:
				pass
			if(file):
				write_md(file,cont)
			else:
				tk.Tk().withdraw()
				while(1):
					file = asf(title='save as ...')
					if(not file):
						if(not askyn('Do you want to keep this new document?','Do you want to keep this new document?')):
							exit()
					write_md(file)
if(__name__ == '__main__'):
	main()

