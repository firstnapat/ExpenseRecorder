# GUIBasic2-Expense.py
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime
import csv
#############Database##########################
#basicsqlite3.py

import sqlite3

#สร้างดาต้าเบส
conn = sqlite3.connect('expense.sqlite3')
#สร้างตัวดำเนินการ (อยากได้อะไรใช้ตัวนี้ได้เลย)
c = conn.cursor()

# สร้าง table ด้วยภาษา SQL
'''
กำหนดลักษณะข้อมูลว่าควรจะเป็นอะไร
 ['รหัส(transactionid) TEXT',
 'วันเวลา(datetime)TEXT',
 'รายการ(title)TEXT',
 'ค่าใช้จ่าย(expense)REAL(FLOAT)',
 'จำนวน(quantity)INTEGER',
 'รวม(total)REAL']
 '''
c.execute("""CREATE TABLE IF NOT EXISTS expenselist (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                transactionid TEXT,
                datetime TEXT,
                title TEXT,
                expense REAL,
                quantity INTEGER,
                total REAL
            )""")

def insert_expense(transactionid,datetime,title,expense,quantity,total):
    ID = None
    with conn:
        c.execute("""INSERT INTO expenselist VALUES (?,?,?,?,?,?,?)""",
            (ID,transactionid,datetime,title,expense,quantity,total))        
    conn.commit() #การบันทึกข้อมูลลงในฐานข้อมูล ถ้าไม่รันตัวนี้จะไม่บันทึก
    print("Insert Success!")

insert_expense('2021156454545','วันศุกร์ 2021-07-09','ข้าวสาร',45,2,90)
##################################

# ttk is theme of Tk

GUI = Tk()
GUI.title('โปรแกรมบันทึกค่าใช้จ่าย by Uncle Engineer')
##GUI.geometry('720x700+500+50')

w = 720
h = 600

ws = GUI.winfo_screenwidth() #screen width
hs = GUI.winfo_screenheight() #screen height

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')

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
	print('About Menu')
	messagebox.showinfo('About','สวัสดีครับ โปรแกรมนี้คือโปรแกรมบันทึกข้อมูล\nสนใจบริจาคเราไหม? ที่พร้อมเพย์ 0970726419' )

helpmenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=helpmenu)
helpmenu.add_command(label='About',command=About)

# Donate
donatemenu = Menu(menubar,tearoff=0)
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

	if expense == '':
		#print('No Data')
		messagebox.showwarning('Error','กรุณากรอกข้อมูลค่าใช้จ่าย')
		return
	elif price == '':
		messagebox.showwarning('Error','กรุณากรอกราคา')
		return
	elif quantity == '':
		quantity = 1  #ให้defaultจำนวนเป็น 1

	total = float(price) * float(quantity)
	try:
		total =  float(price)*float(quantity)
		# .get() คือดึงค่ามาจาก v_expense = StringVar()
		print('รายการ: {} ราคา: {} จำนวน: {} รวมทั้งหมด: {}'.format(expense,price,quantity,total))
		text = 'รายการ: {} ราคา: {}\n'.format(expense,price)
		text = text + 'จำนวน: {} รวมทั้งหมด: {}'.format(quantity,total)
		v_result.set(text)
		# clear ข้อมูลเก่า
		v_expense.set('')
		v_price.set('')
		v_quantity.set('')

		# บันทึกข้อมูลลง csv อย่าลืม import csv ด้วย
		today = datetime.now().strftime('%a') # days['Mon'] = 'จันทร์'
		#print(today)
		stamp = datetime.now()
		dt = stamp .strftime('%Y-%m-%d-%H:%M:%S')
		transactionid = stamp.strftime('%Y%m%d%H%M%f')
		dt = days[today] + '-' + dt
		
		insert_expense(transactionid,dt,expense,float(price),int(quantity),total)

		with open('savedata.csv','a',encoding='utf-8',newline='') as f:
			# with คือสั่งเปิดไฟล์แล้วปิดอัตโนมัติ
			# 'a' การบันทึกเรื่อยๆ เพิ่มข้อมูลต่อจากข้อมูลเก่า
			# newline='' ทำให้ข้อมูลไม่มีบรรทัดว่าง
			fw = csv.writer(f) #สร้างฟังชั่นสำหรับเขียนข้อมูล
			data = [transactionid,dt,expense,price,quantity,total]
			fw.writerow(data)

		# ทำให้เคอเซอร์กลับไปตำแหน่งช่องกรอก E1
		E1.focus()
		update_table()
	except Exception as e: #เพื่อให้เตือนว่าไม่สามารถบันทึกได้เมื่อเปิดไฟล์.csvไว้

		print('ERROR:',e)
		messagebox.showinfo('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showwarning('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		#messagebox.showerror('Error','กรุณากรอกข้อมูลใหม่ คุณกรอกตัวเลขผิด')
		v_expense.set()
		v_price.set()
		v_quantity.set()
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
B2.pack(ipadx=50,ipady=20,pady=20)

v_result = StringVar()
v_result.set('--------ผลลัพธ์-------')
result = ttk.Label(F1, textvariable=v_result,font=FONT1)
result.pack(pady=20)
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

header = ['รหัส','วันเวลา','รายการ','ค่าใช้จ่าย','จำนวน','รวม']
resulttable = ttk.Treeview(T2,columns=header,show='headings',height=10) 
#show='headings'ทำให้หัวข้อไม่มีการซอยย่อยลงมา
resulttable.pack()

#for i in range(len(header)):
#	resulttable.heading(header[i],text=header[i])

for h in header:
	resulttable.heading(h,text=h)

headerwidth = [120,150,170,80,80,80]
for h,w in zip(header, headerwidth):
	resulttable.column(h,width=w)

#resulttable.insert('',0,value=['จันทร์','น้ำดื่ม',30,5,150])
#resulttable.insert('','end',value=['อังคาร','น้ำดื่ม',30,5,150])
alltransaction = {}

def updateCSV():
	with open('savedata.csv','w',newline='',encoding='utf-8') as f: 
		fw = csv.writer(f)
		#เตรียมข้อมูลให้กลายเป็น list
		data = list(alltransaction.values())
		fw.writerows(data) # multiple line from nested list [],[],[]
		print('Table was upated')
		
def DeleteRecord(event=None):
	check = messagebox.askyesno('Confirm?','คุณต้องการลบข้อมูลใช่หรือไม่')
	print('YES/NO:',check)

	if check == True:
		#print('delete')
		select = resulttable.selection()
		#print(select)
		data = resulttable.item(select)
		data = data['values']
		transactionid = data[0]
		#print(transactionid)
		del alltransaction[str(transactionid)] #delete data in dict
		#print(alltransaction)
		updateCSV()
		update_table()
	else:
		print('cancel')


Bdelete = ttk.Button(T2,text='delete',command=DeleteRecord)
Bdelete.place(x=50,y=550)

resulttable.bind('<Delete>', DeleteRecord)

def update_table():
	resulttable.delete(*resulttable.get_children())
	#for c in resulttable.get_children():
	# resulttable.delete(c)
	try:
		data = read_csv()
		for d in data:
			#create transaction data
			alltransaction[d[0]] = d  #d[0] = transactionid
			resulttable.insert('',0,values=d)
		print(alltransaction)
	except Exception as e:
		print('No File')
		print('ERROR:',e)

#########Rightclickmenu###########
def EditRecord():
	POPUP = Toplevel()
	POPUP.title('Edit Record')
	#POPUP.geometry('500x400')
	w = 500
	h = 400

	ws = GUI.winfo_screenwidth() #screen width
	hs = GUI.winfo_screenheight() #screen height


	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)

	POPUP.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


	#------text1--------
	L = ttk.Label(POPUP,text='รายการค่าใช้จ่าย',font=FONT1).pack()
	v_expense = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E1 = ttk.Entry(POPUP,textvariable=v_expense,font=FONT1)
	E1.pack()
	#-------------------
	#------text2--------
	L = ttk.Label(POPUP,text='ราคา (บาท)',font=FONT1).pack()
	v_price = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E2 = ttk.Entry(POPUP,textvariable=v_price,font=FONT1)
	E2.pack()
	#-------------------
	#------text3--------
	L = ttk.Label(POPUP,text='จำนวน (ชิ้น)',font=FONT1).pack()
	v_quantity = StringVar()
	# StringVar() คือ ตัวแปรพิเศษสำหรับเก็บข้อมูลใน GUI
	E3 = ttk.Entry(POPUP,textvariable=v_quantity,font=FONT1)
	E3.pack()
	#-------------------

	def Edit():
		print(transactionid)
		print(alltransaction)
		olddata = alltransaction[str(transactionid)]
		print('OLD',olddata)
		v1 = v_expense.get()
		v2 = float(v_price.get())
		v3 = float(v_quantity.get())
		total = v2 * v3
		newdata = [olddata[0],olddata[1],v1,v2,v3,total]
		alltransaction[str(transactionid)] = newdata
		updateCSV()
		update_table()
		POPUP.destroy() #สั่งปิด POPUP

	icon_b1 = PhotoImage(file='b1_expensesave.png')

	B2 = ttk.Button(POPUP,text=f'{"Save":>{10}}',image = icon_b1,compound ='left' ,command=Edit)
	B2.pack(ipadx=50,ipady=20,pady=20)	

	#get data in selected record
	select = resulttable.selection()
	print(select)
	data = resulttable.item(select)
	data = data['values']
	print(data)
	transactionid = data[0]
	
	# สั่งเซ็ตค่าเกด่าไว้ตรงช่องกรอก
	v_expense.set(data[2])
	v_price.set(data[3])
	v_quantity.set(data[4])

	POPUP.mainloop()


rightclick = Menu(GUI,tearoff=0)
rightclick.add_command(label='Edit',command=EditRecord)
rightclick.add_command(label='Delete',command=DeleteRecord)


def menupopup(event):
	#print(event.x_root, event.y_root)
	rightclick.post(event.x_root,event.y_root)

resulttable.bind('<Button-3>',menupopup) #หากมีการคลิกขวาที่resulttableจะเปิดหน้าpopup

update_table()
#print('GET CHILD:',resulttable.get_children())
GUI.bind('<Tab>',lambda x: E2.focus())
GUI.mainloop()

 
