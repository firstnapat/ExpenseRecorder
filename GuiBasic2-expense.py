# GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import csv
# ttk is theme of Tk

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Uncle Engineer')
GUI.geometry('600x700+500+50')

# B1 = Button(GUI,text='Hello')
# B1.pack(ipadx=50,ipady=20) #.pack() ติดปุ่มเข้ากับ GUI หลัก

###################
menubar = Menu(GUI)
GUI.config(menu=menubar)

# file menu
filemenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=filemenu)
filemenu.add_command(label='Import CSV')
filemenu.add_command(label='Export to Googlesheet')
# help
def About():
	messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ที่พร้อมเพย์ 0970726419' )

helpmenu = Menu(menubar)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)
# Donate
donatemenu = Menu(menubar)
menubar.add_cascade(label='Donate',menu=donatemenu)



###################




Tab = ttk.Notebook(GUI)
T1 = Frame(Tab,width = 400,height = 400)
T2 = Frame(Tab,width = 400)
Tab.pack(fill = BOTH, expand = 1)

icon_t1 = PhotoImage(file='t1_expense.png').subsample(3)  #.subsample(3)>>ย่อรูป3เท่า
icon_t2 = PhotoImage(file='t2_expense.png').subsample(3)  #ต้องเป็น pngถึงใช้คำสั่งนี้ได้

Tab.add(T1, text =f'{"ค่าใช้จ่าย":^{30}}',image=icon_t1,compound='top')
Tab.add(T2, text =f'{"ค่าใช้จ่ายทั้งหมด":^{30}}',image=icon_t2,compound='top')

F1 = Frame(T1)
#F1.place(x=100,y=50)
F1.pack()
days = {'Mon':'จันทร์',
		'Tue':'อังคาร',
		'Wed':'พุธ',
		'Thu':'พฤหัส',
		'Fri':'ศุกร์',
		'Sat':'เสาร์',
		'Sun':'อาทิตย์'}

def Save(event=None):
	expense = v_expense.get()
	price = v_price.get()
	quantity = v_quantity.get()

	if expense == ''  :
		print('No Data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return
	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกราคา')
		return
	elif quantity == '':
		quantity = 1  #ให้defaultจำนวนเป็น 1

	try:
		total =  float(price)*float(quantity)
		
		# .get() คือดึงค่ามาจาก v_expense = StringVar()
		print('รายการ: {} ราคา: {} จำนวน: {} รวมทั้งหมด: {}'.format(expense,price,quantity,total))
		text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
		text2 = text + 'จำนวน: {} รวมทั้งหมด: {}'.format(quantity,total)
		v_result.set(text2)
		
		# clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')

		# บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
		today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์'
		print(today)
		dt = datetime.now() .strftime('%Y-%m-%d-%H:%M:%S')
		dt = days[today] + '-' + dt
		with open('savedata.csv','a',encoding='utf-8',newline='') as f:
			# with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
			# 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
			# newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
			fw = csv.writer(f) #สร้างฟังชั่นสำหรับเขียนข้อมูล
			data = [dt, expense,price,quantity,total]
			fw.writerow(data)

		# ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
		E1.focus()
		update_table()

	except Exception as e: #เพื่อให้เตือนว่าไม่สามารถบันทึกได้เมื่อเปิดไฟล์.csvไว้

		print('ERROR:',e)
		messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')

# ทำให้สามารถกด enter ได้
GUI.bind('<Return>',Save) #ต้องเพิ่มใน def Save(event=None) ด้วย

FONT1 = (None,20) # None เปลี่ยนเป็น 'Angsana New'

#-----------Image---------
main_icon = PhotoImage(file='money.png')

Main_icon = Label(F1,image= main_icon )
Main_icon.pack()

#------text1--------
L = ttk.Label(F1,text='รายการค่าใช้จ่าย',font=FONT1).pack()
v_expense = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E1 = ttk.Entry(F1,textvariable=v_expense,font=FONT1)
E1.pack()
#-------------------
#------text2--------
L = ttk.Label(F1,text='ราคา (บาท)',font=FONT1).pack()
v_price = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E2 = ttk.Entry(F1,textvariable=v_price,font=FONT1)
E2.pack()
#-------------------
#------text3--------
L = ttk.Label(F1,text='จำนวน (ชิ้น)',font=FONT1).pack()
v_quantity = StringVar()
# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
E3 = ttk.Entry(F1,textvariable=v_quantity,font=FONT1)
E3.pack()
#-------------------

icon_b1 = PhotoImage(file='b1_expensesave.png')

B2 = ttk.Button(F1,text=f'{"Save":>{10}}',image = icon_b1,compound ='left' ,command=Save)
B2.pack(ipadx=10,ipady=10)

v_result = StringVar()
v_result.set('--------ผลลัพธ์-------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1)
result.pack(pady=5)
########################TAB2######################

def read_csv():
	with open('savedata.csv',newline='',encoding='utf-8') as f: 
		#with คือ สั่งเปิดไฟล์แล้วปิดอัตโนมัติ
		fr = csv.reader(f)
		data = list(fr)	
	return data 
		#print(data)
		#print('------')
		#print(data[0][0])
		#for a,b,c,d,e in data:
		#	print(a)
# table
L = ttk.Label(T2,text='ตารางแสดงผลลัพธ์ทั้งหมด',font=FONT1).pack(pady=20)

header = ['วันเวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10) 
#show='headings'ทำให้หัวข้อไม่มีการซอยย่อยลงมา
resulttable.pack()

#for i in range(len(header)):
#	resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [150,170,80,80,80]
for h,w in zip(header, headerwidth):
	resulttable.column(h,width=w)

#resulttable.insert('',0,value=['จันทร์','น้ำดื่ม',30,5,150])
#resulttable.insert('','end',value=['อังคาร','น้ำดื่ม',30,5,150])

def update_table():
	resulttable.delete(*resulttable.get_children())
	#for c in resulttable.get_children():
	# resulttable.delete(c)
	data = read_csv()
	for d in data:
		resulttable.insert('',0,values=d)


update_table()
print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()

 
