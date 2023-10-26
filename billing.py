from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class BillClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1350x700+0+0")
		self.root.title("Inventory Management System | Developed by Nikhil | Pratham and Anthony")
		self.root.config(bg="WHITE")

		self.cart_list=[]
		self.chk_print=0
		
#******************************************Title***********************************************************************************************
		self.TitleLogo=Image.open("images/2.png")
		self.TitleLogo=self.TitleLogo.resize((50,50),Image.ANTIALIAS)
		self.TitleLogo=ImageTk.PhotoImage(self.TitleLogo)

		title=Label(self.root,text="Inventory Management System",image=self.TitleLogo,compound=LEFT,font=("Ariel" ,35, "bold"),bg="#000080",fg="White",anchor="w",padx=30)
		title.pack(fill=X)

#***********************************************************button logout**********************************************************************************
		btn_logout=Button(self.root,text="LOGOUT",font=("Ariel" ,15,"bold"),bg="Yellow").place(x=1150,y=10,height=40,width=150)

#****************************************************clock*************************************************************************************************************************************
		self.lbl_clock=Label(self.root,text=" Welcome   to  Inventory  Management  System\t\t Date: DD-MM-YYYY\t\tTime:HH:MM:SS",font=("Ariel" ,15),bg="#FFB90F",bd=1,relief=RIDGE,fg="#000")
		self.lbl_clock.place(x=0,y=61,relwidth=1,height=30)

#********************************************Product Frame***********************************************************************
		ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="WHITE")
		ProductFrame1.place(x=6,y=110,width=410,height=540)

		ptitle=Label(ProductFrame1,text="All Product",font=("goudy old style",20,"bold"),bg="#876482",fg="White")
		ptitle.pack(side=TOP,fill=X)

#*******************************Product Search Frame*************************************************************
		self.var_search=StringVar()
		ProductFrame2=Frame(ProductFrame1,bd=4,relief=RIDGE,bg="WHITE")
		ProductFrame2.place(x=2,y=42,width=398,height=90)

		lbl_search=Label(ProductFrame2,text="Search Product | By Name",font=("goudy old style",15,"bold"),bg="White",fg="black").place(x=2,y=5)		
		txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=129,y=47,width=150,height=26)
		btn_search=Button(ProductFrame2,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=283,y=45,width=100,height=26)
		btn_show_all=Button(ProductFrame2,text="Show All",command=self.show,font=("goudy old style",15,"bold"),bg="#680492",fg="white",cursor="hand2").place(x=283,y=10,width=100,height=26)

		lbl_name=Label(ProductFrame2,text="Product Name",font=("goudy old style",15,"bold"),bg="white",fg="black")
		lbl_name.place(x=2,y=45)

#******************************Product Details***********************************************************************************************************************
		ProductFrame3=Frame(ProductFrame1,bg="#DCDCDC",bd=3,relief=RIDGE)
		ProductFrame3.place(x=2,y=140,width=400,height=360)

		scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
		scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

		self.Product_Table=ttk.Treeview(ProductFrame3,columns=("pid","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM,fill=X)
		scrolly.pack(side=RIGHT,fill=Y)
		scrolly.config(command=self.Product_Table.yview)
		scrollx.config(command=self.Product_Table.xview)

		self.Product_Table.heading("pid",text="PID")
		self.Product_Table.heading("name",text="Name")
		self.Product_Table.heading("price",text="Price")
		self.Product_Table.heading("qty",text="QTY")
		self.Product_Table.heading("status",text="Status")


		self.Product_Table["show"]="headings"

		self.Product_Table.column("pid",width=50)
		self.Product_Table.column("name",width=100)
		self.Product_Table.column("price",width=50)
		self.Product_Table.column("qty",width=50)
		self.Product_Table.column("status",width=100)
		self.Product_Table.pack(fill=BOTH,expand=1)
		self.Product_Table.bind("<ButtonRelease-1>",self.get_data)
		self.root.focus_force()
		lbl_note=Label(ProductFrame1,text="Note:Enter 0 Quantity to remove product from the Cart",font=("goudy old style",13,"bold"),bg="white",fg="red",anchor="w").pack(side=BOTTOM,fill=X)

#****************************Customer Frame*********************************************************************************************************
		self.var_cname=StringVar()
		self.var_contact=StringVar()

		CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="WHITE")
		CustomerFrame.place(x=420,y=110,width=530,height=70)

		ctitle=Label(CustomerFrame,text="Customer Details",font=("goudy old style",15,"bold"),bg="#468299",fg="White")
		ctitle.pack(side=TOP,fill=X)

		lbl_name=Label(CustomerFrame,text="Name",font=("goudy old style",15,"bold"),bg="White",fg="black").place(x=5,y=35)		
		txt_name=Entry(CustomerFrame,textvariable=self.var_cname,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=65,y=31,width=180,height=31)
		
		lbl_contact=Label(CustomerFrame,text="Contact No.",font=("goudy old style",15,"bold"),bg="White",fg="black").place(x=260,y=35)		
		txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=365,y=31,width=150,height=31)
		

#*******************************Calculator and Cart Frame*************************************************************
		Cal_Cart_Frame=Frame(self.root,bd=7,relief=RIDGE,bg="white")
		Cal_Cart_Frame.place(x=420,y=186,width=530,height=360)


#*******************************Calculator Frame*************************************************************
		#calculator Frame
		self.var_txt=StringVar()
		self.var_operator=''

		#Function to print values on calculator
		def btn_click(num): 
			self.var_operator=self.var_operator+str(num)
			self.var_txt.set(self.var_operator)

		#Performs calulations
		def result():
			res=str(eval(self.var_operator))	#eval is inbuilt function that performs arithmatic operation
			self.var_txt.set(res)
			self.var_operator='' 				#for clear screen

		def clear():
			self.var_txt.set('')
			self.var_operator=''
		CalculatorFrame=Frame(Cal_Cart_Frame,bd=7,relief=RIDGE,bg="white")
		CalculatorFrame.place(x=2,y=2,width=260,height=340)

		lbl_calculator=Label(CalculatorFrame,text="Calculator",font="arial 20 bold",bg="Red").place(x=0,y=0,relwidth=1,height=50)

		txt_cal=Entry(CalculatorFrame,textvariable=self.var_txt,font="arial 30 bold",bg="lightgrey",fg="black",
			justify=RIGHT,state='readonly').place(x=0,y=50,relwidth=1)

		# Cal Button row 1
		btn_7=Button(CalculatorFrame,text="7",command=lambda:btn_click(7),
			font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=0,y=100,width=63,height=60)
		btn_8=Button(CalculatorFrame,text="8",command=lambda:btn_click(8),
			font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=63,y=100,width=63,height=60)
		btn_9=Button(CalculatorFrame,text="9",command=lambda:btn_click(9),
			font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=126,y=100,width=63,height=60)
		btn_div=Button(CalculatorFrame,text="/",command=lambda:btn_click('/'),
			font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=189,y=100,width=61,height=60)

		# Cal Button row 2
		btn_4=Button(CalculatorFrame,text="4",command=lambda:btn_click(4),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=0,y=160,width=63,height=57)
		btn_5=Button(CalculatorFrame,text="5",command=lambda:btn_click(5),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=63,y=160,width=63,height=57)
		btn_6=Button(CalculatorFrame,text="6",command=lambda:btn_click(6),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=126,y=160,width=63,height=57)
		btn_mul=Button(CalculatorFrame,text="*",command=lambda:btn_click('*'),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=189,y=160,width=61,height=57)

		#cal Button row 3
		btn_1=Button(CalculatorFrame,text="1",command=lambda:btn_click(1),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=0,y=217,width=63,height=60)
		btn_2=Button(CalculatorFrame,text="2",command=lambda:btn_click(2),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=63,y=217,width=63,height=60)
		btn_3=Button(CalculatorFrame,text="3",command=lambda:btn_click(3),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=126,y=217,width=63,height=60)
		btn_sub=Button(CalculatorFrame,text="-",command=lambda:btn_click('-'),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=189,y=217,width=61,height=60)

		# cal Button row4
		btn_0=Button(CalculatorFrame,text="0",command=lambda:btn_click(0),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=0,y=277,width=63,height=50)
		btn_clear=Button(CalculatorFrame,text="C",command=clear,font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=63,y=277,width=63,height=50)
		btn_plus=Button(CalculatorFrame,text="+",command=lambda:btn_click('+'),font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=126,y=277,width=63,height=50)
		btn_equal=Button(CalculatorFrame,text="=",command=result,font="arial 20 bold",bg="tan",fg="black",cursor="hand2").place(x=189,y=277,width=61,height=50)
		
#******************************* cart Frame*************************************************************
		CartFrame=Frame(Cal_Cart_Frame,bg="#DCDCDC",bd=3,relief=RIDGE)
		CartFrame.place(x=265,y=2,width=250,height=345)
		self.ctitle=Label(CartFrame,text="Cart\tTotal Product: [0]",font=("goudy old style",15,"bold"),bg="#468299",fg="White")
		self.ctitle.pack(side=TOP,fill=X)


		scrolly=Scrollbar(CartFrame,orient=VERTICAL)
		scrollx=Scrollbar(CartFrame,orient=HORIZONTAL)

		self.CartTable=ttk.Treeview(CartFrame,columns=("pid","name","price","qty"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM,fill=X)
		scrolly.pack(side=RIGHT,fill=Y)
		scrolly.config(command=self.CartTable.yview)
		scrollx.config(command=self.CartTable.xview)

		self.CartTable.heading("pid",text="PID")
		self.CartTable.heading("name",text="Name")
		self.CartTable.heading("price",text="Price")
		self.CartTable.heading("qty",text="QTY")


		self.CartTable["show"]="headings"

		self.CartTable.column("pid",width=40)
		self.CartTable.column("name",width=100)
		self.CartTable.column("price",width=90)
		self.CartTable.column("qty",width=40)
		self.CartTable.pack(fill=BOTH,expand=1)
		self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)
		self.root.focus_force()

#*******************************Add cart wigets Frame*************************************************************
		self.var_pid=StringVar()
		self.var_pname=StringVar()
		self.var_price=StringVar()
		self.var_qty=StringVar()		
		self.var_stock=StringVar()

		Add_CartwidgetsFrame=Frame(self.root,bd=7,relief=RIDGE,bg="white")
		Add_CartwidgetsFrame.place(x=420,y=545,width=530,height=105)

		lbl_p_name=Label(Add_CartwidgetsFrame,text="Product Name",font=("goudy old style",15,"bold"),bg="white").place(x=5,y=5)
		txt_p_name=Entry(Add_CartwidgetsFrame,textvariable=self.var_pname,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4,state='readonly').place(x=5,y=35,width=190,height=28)

		lbl_p_price=Label(Add_CartwidgetsFrame,text="Price Per Qty",font=("goudy old style",15,"bold"),bg="white").place(x=230,y=5)
		txt_p_price=Entry(Add_CartwidgetsFrame,textvariable=self.var_price,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4,state='readonly').place(x=230,y=35,width=150,height=28)

		lbl_p_qty=Label(Add_CartwidgetsFrame,text="Quantity",font=("goudy old style",15,"bold"),bg="white").place(x=390,y=5)
		txt_p_qty=Entry(Add_CartwidgetsFrame,textvariable=self.var_qty,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=390,y=35,width=100,height=28)

		self.lbl_inStock=Label(Add_CartwidgetsFrame,text="In Stock",font=("goudy old style",15,"bold"),bg="white")
		self.lbl_inStock.place(x=5,y=64)
		
		btn_clear_cart=Button(Add_CartwidgetsFrame,text="Clear",command=self.clear_cart,font="arial 15 bold",bg="#CAFF70",fg="black",bd=4,cursor="hand2").place(x=170,y=64,width=150,height=28)
		btn_add_cart=Button(Add_CartwidgetsFrame,command=self.add_update_cart,text="Add | Update Cart",font="arial 15 bold",bg="orange",fg="black",bd=4,cursor="hand2").place(x=328,y=64,width=185,height=28)

#***********************************************Billing Area***********************************************************************************
		billFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
		billFrame.place(x=953,y=110,height=410,width=395)

		title_billFrame=Label(billFrame,text="Customer Bill Area",font=("goudy old style",20,"bold"),bg="#193584",fg="White")
		title_billFrame.pack(side=TOP,fill=X)

		scrolly=Scrollbar(billFrame,orient=VERTICAL)
		scrolly.pack(side=RIGHT,fill=Y)
		self.txt_bill_area=Text(billFrame,font=("goudy old style",12,"bold"))
		self.txt_bill_area.pack(fill=BOTH,expand=1)
		scrolly.config(command=self.txt_bill_area.yview)

#**************************************************Billing Buttons****************************************************************************
		billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
		billMenuFrame.place(x=953,y=520,height=130,width=395)

		self.lbl_amt=Label(billMenuFrame,text="Bill Amount\n[0]",font=("goudy old style",17,"bold"),bg="#FF6A6A",fg="Black",bd=2)
		self.lbl_amt.place(x=1,y=1,width=136,height=70)

		self.lbl_discount=Label(billMenuFrame,text="Discount\n[5%]",font=("goudy old style",17,"bold"),bg="orange",fg="Black",bd=2)
		self.lbl_discount.place(x=138,y=1,width=114,height=70)

		self.lbl_net_pay=Label(billMenuFrame,text="Net Pay\n[0]",font=("goudy old style",17,"bold"),bg="#00B2EE",fg="Black",bd=2)
		self.lbl_net_pay.place(x=253,y=1,width=137,height=70)

		btn_print=Button(billMenuFrame,text="Print",command=self.print_bill,font=("goudy old style",15,"bold"),bg="#8A2BE2",fg="Black",bd=4,cursor="hand2")
		btn_print.place(x=1,y=74,width=130,height=50)

		btn_clear_all=Button(billMenuFrame,text="Clear All",command=self.clear_all,font=("goudy old style",15,"bold"),bg="#7AC5CD",fg="Black",bd=4,cursor="hand2")
		btn_clear_all.place(x=130,y=74,width=130,height=50)

		btn_generate=Button(billMenuFrame,text="Generate/\nSave Bill ",command=self.generate_bill,font=("goudy old style",15,"bold"),bg="#CD5B45",fg="Black",bd=4,cursor="hand2")
		btn_generate.place(x=260,y=74,width=130,height=50)

#**************************************Footer************************************************************************************************************
		lbl_footer=Label(self.root,text="IMS  Inventory Management System | Developed by Nikhil and Pratham \nFor any Technical issue Contact:7019xxxx96",font=("Ariel" ,13),bg="#FFB90F",bd=4,relief=RIDGE,fg="#000").pack(side=BOTTOM,fill=X)
		self.show()
		self.update_date_time()

	def show(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			cur.execute("Select pid,name,price,qty,status from product where status='Active' ")
			rows=cur.fetchall()
			self.Product_Table.delete(*self.Product_Table.get_children())
			for row in rows:
				self.Product_Table.insert('',END,values=row)
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")
	
	def search(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_search.get()=='':
				messagebox.showerror("Error","Required Search input",parent=self.root)
			else:
				cur.execute("Select pid,name,price,qty,status from product where name LIKE '%" + self.var_search.get() + "%' and status=='Active'")
				rows=cur.fetchall()
				if len(rows)!=0:				
					self.Product_Table.delete(*self.Product_Table.get_children())
					for row in rows:
						self.Product_Table.insert('',END,values=row)
				else:
					messagebox.showerror("Error","No Record Found",parent=self.root)
		except Exception as e:
			print(e)
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def get_data(self,ev):
		f=self.Product_Table.focus()
		content=(self.Product_Table.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_pname.set(row[1])
		self.var_price.set(row[2])	
		self.lbl_inStock.config(text=f"In Stock \t[{str(row[3])}]")
		self.var_stock.set(row[3])
		self.var_qty.set('1')	

	def get_data_cart(self,ev):
		f=self.CartTable.focus()
		content=(self.CartTable.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_pname.set(row[1])
		self.var_price.set(row[2])	
		self.var_qty.set(row[3])
		self.lbl_inStock.config(text=f"In Stock \t[{str(row[4])}]")
		self.var_stock.set(row[4])
	


	def add_update_cart(self):

		if self.var_pid.get()=='':
			messagebox.showerror("Error","Please Select Product from the list",parent=self.root)
		elif self.var_qty.get()=='':
			messagebox.showerror("Error","Quantity is Required",parent=self.root)
		elif int(self.var_qty.get())>int(self.var_stock.get()):
			messagebox.showerror("Error","Invalid Quantity",parent=self.root)
		
		else:			
			#price_cal=float(int(self.var_qty.get())*float(self.var_price.get()))
			price_cal=self.var_price.get()
			cart_data=[self.var_pid.get(),self.var_pname.get(),price_cal,self.var_qty.get(),self.var_stock.get()]
			#*********************************Update_Cart************************************
			present='no'
			index_=0
			for row in self.cart_list:
				if self.var_pid.get()==row[0]:
					present='yes'
					break
				index_+=1
			#print(present,index_)
			if present=='yes':
				op=messagebox.askyesno('Confirm',"Product already present\nDo you wnt to Update| Remove from the Cart List",parent=self.root)
				if op==True:
					if self.var_qty.get()=="0":
						self.cart_list.pop(index_)
					else:
						#self.cart_list[index_][2]=price_cal #price
						self.cart_list[index_][3]=self.var_qty.get()#qty
			else:
				self.cart_list.append(cart_data)
			self.show_cart()
			self.bill_updates()

	def bill_updates(self):
		self.bill_amnt=0
		self.net_pay=0
		self.discount=0
		for row in self.cart_list:
			self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))

		self.discount=(self.bill_amnt*5)/100
		self.net_pay=self.bill_amnt-self.discount

		self.lbl_amt.config(text=f'Bill Amount\n{str(self.bill_amnt)}')
		self.lbl_net_pay.config(text=f'Net Amount\n{str(self.net_pay)}')
		self.ctitle.config(text=f"Cart\tTotal Product: [{str(len(self.cart_list))}]")


	def show_cart(self):
		try:
			self.CartTable.delete(*self.CartTable.get_children())
			for row in self.cart_list:
				self.CartTable.insert('',END,values=row)
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")
	
	def generate_bill(self):
		if self.var_cname.get()=='' or self.var_contact.get()=='':
			messagebox.showerror("Error","Customer Details are Required",parent=self.root)
		elif len(self.cart_list)==0:
			messagebox.showerror("Error","Please Add Product to the Cart!!!",parent=self.root)			
		else:
			#*************Bill Top**********************************************************
			self.bill_top()
			#*************Bill Middle**********************************************************
			self.bill_middle()
			#*************Bill Bottom**********************************************************
			self.bill_bottom()

			fp=open(f'bill/{str(self.invoice)}.txt','w')
			fp.write(self.txt_bill_area.get('1.0',END))
			fp.close()
			messagebox.showinfo('Saved',"Bill has been generated/Saved in Backend",parent=self.root)
			self.chk_print=1

	def bill_top(self):
		self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
		bill_top_temp=f'''
\t\tXYZ-Inventory
\t Phone No. 70195***** ,Karnataka-590001
{str("="*46)}
Customer Name: {self.var_cname.get()}
Ph no. :{self.var_contact.get()}
Bill No. {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*46)}
Product Name\t\t\tQTY\tPrice
{str("="*46)}
		'''
		self.txt_bill_area.delete('1.0',END)
		self.txt_bill_area.insert('1.0',bill_top_temp)

	def bill_bottom(self):
		bill_bottom_temp=f'''
{str("="*46)}
Bill Amount\t\t\t\tRs.{self.bill_amnt}
Discount\t\t\t\tRs.{self.discount}
Net Pay\t\t\t\tRs.{self.net_pay}
{str("="*46)}
		'''
		self.txt_bill_area.insert(END,bill_bottom_temp)


	def bill_middle(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			for row in self. cart_list:
				pid=row[0]
				name=row[1]
				qty=int(row[4])-int(row[3])
				if int(row[3])==int(row[4]):
					status='Inactive'
				if int(row[3])!=int(row[4]):
					status='Active'
					
				price=float(row[2])*int(row[3])
				price=str(price)
				self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tRs."+price)
				#****************Update QTY in Product Table**********************
				cur.execute("Update product set qty=?,status=? where pid=?",(
								qty,
								status,
								pid			
							))
				con.commit()
			con.close()
			self.show()
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")



	def clear_cart(self):
		self.var_pid.set('')
		self.var_pname.set('')
		self.var_price.set('')	
		self.var_qty.set('')
		self.lbl_inStock.config(text=f"In Stock")
		self.var_stock.set('')
	
	def clear_all(self):
		del self.cart_list[:]
		self.var_cname.set('')
		self.var_contact.set('')
		self.var_search.set('')
		self.txt_bill_area.delete('1.0',END)
		self.ctitle.config(text=f"Cart\tTotal Product: [0]")
		self.chk_print=0
		self.clear_cart()
		self.show()
		self.show_cart()


	def update_date_time(self):
		time_=time.strftime("%I:%M:%S")
		date_=time.strftime("%d-%m-%Y")
		self.lbl_clock.config(text=f" Welcome   to  Inventory  Management  System\t\t Date: {str(date_)}\t\tTime:{str(time_)}",)
		self.lbl_clock.after(200,self.update_date_time)

	def print_bill(self):
		if self.chk_print==1:
			messagebox.showinfo('Print',"PLease wait while Printing",parent=self.root)
			new_file=tempfile.mktemp('.txt')
			open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
			os.startfile(new_file,'print')
		else:
			messagebox.showerror('Print',"Please Generate Bill, to print the receipt",parent=self.root)



if __name__=="__main__":		
	root=Tk()
	c=BillClass(root)
	root.mainloop()
