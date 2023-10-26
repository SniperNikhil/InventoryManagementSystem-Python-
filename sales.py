from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import os
class salesClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+138")
		self.root.title("Inventory Management System | Developed by Nikhil | Pratham and Anthony")
		self.root.config(bg="WHITE")
		self.root.focus_force()
		self.root.resizable(0,0)

		self.bill_list=[]
		self.var_invoice=StringVar()
		#**************************************title*************************************************************
		lbl_title=Label(self.root,text="View Customer Bills",font=("goudy old style",28),bg="#EE7600",fg="white").pack(side=TOP,fill=X)

		lbl_invoice=Label(self.root,text="Invoice No.",font=("goudy old style",19,"bold"),bg="White",bd=4).place(x=30,y=80)

		txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=165,y=83,width=180)

		btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",18,"bold"),bg="green",fg="black",bd=4,cursor="hand2").place(x=360,y=83,width=150,height=32)
		btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",18,"bold"),bg="#CAFF70",fg="BLACK",bd=4,cursor="hand2").place(x=520,y=83,width=150,height=32)

		sales_Frame=Frame(self.root,bd=3,relief=RIDGE)
		sales_Frame.place(x=30,y=135,width=210,height=340)

		scrolly=Scrollbar(sales_Frame,orient=VERTICAL)
		self.Sales_List=Listbox(sales_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
		scrolly.pack(side=RIGHT,fill=Y)
		scrolly.config(command=self.Sales_List.yview)
		self.Sales_List.pack(fill=BOTH,expand=1)
		self.Sales_List.bind("<ButtonRelease-1>",self.get_data)

		#***************************************Bill Area**********************************************************************
		bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
		bill_Frame.place(x=260,y=135,width=410,height=340)

		lbl_title2=Label(bill_Frame,text="Customer Bill Area",font=("goudy old style",20),bg="#8A2BE2",fg="white").pack(side=TOP,fill=X)


		scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
		self.bill_area=Text(bill_Frame,font=("goudy old style",12),bg="lightyellow",yscrollcommand=scrolly2.set)
		scrolly2.pack(side=RIGHT,fill=Y)
		scrolly2.config(command=self.bill_area.yview)
		self.bill_area.pack(fill=BOTH,expand=1)


		#**************************************Images*********************************************************************
		self.bill_photo=Image.open("images/1.png")
		self.bill_photo=self.bill_photo.resize((380,300),Image.ANTIALIAS)
		self.bill_photo=ImageTk.PhotoImage(self.bill_photo)

		lbl_image=Label(self.root,image=self.bill_photo,bd=0)
		lbl_image.place(x=700,y=110)

		self.show()

#*************************************************************************************************************************************
	def show(self):
		del self.bill_list[:]
		self.Sales_List.delete(0,END)
		#print(os.listdir('C:/Users/ADmin/Desktop/Inventory manegement Project'))
		for i in os.listdir('bill'):
			#print(i.split('.'),i.split('.')[-1])
			if i.split('.')[-1]=='txt':
				self.Sales_List.insert(END,i)
				self.bill_list.append(i.split('.')[0])


	def get_data(self,ev):
		index_=self.Sales_List.curselection()
		file_name=self.Sales_List.get(index_)
		#print(file_name)
		self.bill_area.delete('1.0',END)
		fp=open(f'bill/{file_name}','r')
		for i in fp:
			self.bill_area.insert(END,i)
		fp.close()
		self.var_invoice.set(file_name.split('.')[0])

	def search(self):
		if self.var_invoice.get()=="":
			messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
		else:
			if self.var_invoice.get() in self.bill_list:
				fp=open(f'bill/{self.var_invoice.get()}.txt','r')
				self.bill_area.delete('1.0',END)
				for i in fp:
					self.bill_area.insert(END,i)
				fp.close()
			else:
				messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)

	def clear(self):
		self.show()
		self.bill_area.delete('1.0',END)
		self.var_invoice.set("")

if __name__=="__main__":		
	root=Tk()
	c=salesClass(root)
	root.mainloop()
