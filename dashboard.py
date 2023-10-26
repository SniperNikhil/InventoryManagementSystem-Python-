from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
import sqlite3
import os
import time
from tkinter import messagebox
class IMS:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1350x700+0+0")
		self.root.title("Inventory Management System | Developed by Nikhil | Pratham and Anthony")
		self.root.config(bg="WHITE")

#******************************************Title***********************************************************************************************
		self.TitleLogo=Image.open("images/2.png")
		self.TitleLogo=self.TitleLogo.resize((50,50),Image.ANTIALIAS)
		self.TitleLogo=ImageTk.PhotoImage(self.TitleLogo)

		LeftLogo=Frame(self.root,bd=2,relief=RIDGE,bg="#000080")
		LeftLogo.place(x=0,y=0,width=200,height=565)

		lbl_titleLogo=Label(LeftLogo,image=self.TitleLogo)
		lbl_titleLogo.pack(side=TOP,fill=X)

		title=Label(self.root,text="Inventory Management System",image=self.TitleLogo,compound=LEFT,font=("Ariel" ,35, "bold"),bg="#000080",fg="White",anchor="w",padx=30)
		title.pack(fill=X)

#***********************************************************button logout**********************************************************************************

		btn_logout=Button(self.root,text="LOGOUT",font=("Ariel" ,15,"bold"),bg="Yellow").place(x=1150,y=10,height=40,width=150)

#****************************************************clock*************************************************************************************************************************************
		self.lbl_clock=Label(self.root,text=" Welcome   to  Inventory  Management  System\t\t Date: DD-MM-YYYY\t\tTime:HH:MM:SS",font=("Ariel" ,15),bg="#FFB90F",bd=1,relief=RIDGE,fg="#000")
		self.lbl_clock.place(x=0,y=61,relwidth=1,height=30)

#************************MENU Logo******************************************************************************************************************8***********************
		self.MenuLogo=Image.open("images/1.png")
		self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
		self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

		LeftMenu=Frame(self.root,bd=6,relief=GROOVE,bg="#000080")
		LeftMenu.place(x=0,y=91,width=200,height=570)

		lbl_menuLogo=Label(LeftMenu,image=self.MenuLogo)
		lbl_menuLogo.pack(side=TOP,fill=X)
#***********************************Button Title Menu***********************************************************************************************************************
		lbl_menu=Label(LeftMenu,text="MENU",font=("ANTON",35,"bold"),bg="#FFB90F").pack(side=TOP,fill=X,pady=2)

#**********************************************LeftMenu Frame Buttoms**************************************************************************************************
		btn_employee=Button(LeftMenu,text=">>> Employee",command=self.employee,font=("Ariel" ,16,"bold"),bg="white",bd=3,cursor="hand2",anchor="w").pack(side=TOP,fill=X,pady=2)

		btn_supplier=Button(LeftMenu,text=">>> Supplier",command=self.supplier,font=("Ariel" ,16,"bold"),bg="white",bd=3,cursor="hand2",anchor="w").pack(side=TOP,fill=X,pady=2)

		btn_category=Button(LeftMenu,text=">>> Category",command=self.category ,font=("Ariel" ,16,"bold"),bg="white",bd=3,cursor="hand2",anchor="w").pack(side=TOP,fill=X,pady=2)

		btn_product=Button(LeftMenu,text=">>> Product",command=self.product,font=("Ariel" ,16,"bold"),bg="white",bd=3,cursor="hand2",anchor="w").pack(side=TOP,fill=X,pady=2)

		btn_sales=Button(LeftMenu,text=">>> Sales",command=self.sales,font=("Ariel" ,16,"bold"),bg="white",bd=3,cursor="hand2",anchor="w").pack(side=TOP,fill=X,pady=2)

		btn_exit=Button(LeftMenu,text=">>> Exit",command=self.Exit_app,font=("Ariel" ,16,"bold"),bg="white",bd=3,cursor="hand2",anchor="w").pack(side=TOP,fill=X,pady=2)

#***************************** Home Content************************************************************************************************************************
		self.lbl_employee=Label(self.root,text="Total Employees\n[ 0 ]",font=("goudy old style",20,"bold"),bg="#E066FF",fg="BLACK",bd=5,relief=RIDGE)
		self.lbl_employee.place(x=300,y=120,width=300,height=150)

		self.lbl_supplier=Label(self.root,text="Total Supplier\n[ 0 ]",font=("goudy old style",20,"bold"),bg="#FF4500",fg="BLACK",bd=5,relief=RIDGE)
		self.lbl_supplier.place(x=650,y=120,width=300,height=150)

		self.lbl_category=Label(self.root,text="Total Category\n[ 0 ]",font=("goudy old style",20,"bold"),bg="#E9967A",fg="BLACK",bd=5,relief=RIDGE)
		self.lbl_category.place(x=1000,y=120,width=300,height=150)

		self.lbl_product=Label(self.root,text="Total Products\n[ 0 ]",font=("goudy old style",20,"bold"),bg="#00688B",fg="BLACK",bd=5,relief=RIDGE)
		self.lbl_product.place(x=300,y=300,width=300,height=150)

		self.lbl_sales=Label(self.root,text="Total Sales\n[ 0 ]",font=("goudy old style",20,"bold"),bg="#8B6914",fg="BLACK",bd=5,relief=RIDGE)
		self.lbl_sales.place(x=650,y=300,width=300,height=150)


#**************************************Footer************************************************************************************************************
		lbl_footer=Label(self.root,text="IMS  Inventory Management System | Developed by Nikhil and Pratham \nFor any Technical issue Contact:7019xxxx96",font=("Ariel" ,12),bg="#FFB90F",bd=4,relief=RIDGE,fg="#000").pack(side=BOTTOM,fill=X)
		self.lbl_clock.place(x=0,y=61,relwidth=1,height=30)

		self.update_content()
		self.update_date_time()


#******************************************************All Function****************************************************************
	def employee(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=employeeClass(self.new_win)

	def supplier(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=supplierClass(self.new_win)

	def category(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=categoryClass(self.new_win)

	def product(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=productClass(self.new_win)

	def sales(self):
		self.new_win=Toplevel(self.root)
		self.new_obj=salesClass(self.new_win)

	def update_content(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			cur.execute("select *from product")
			product=cur.fetchall()
			self.lbl_product.config(text=f"Total Products\n[ {str(len(product))} ]")

			cur.execute("select *from supplier")
			supplier=cur.fetchall()
			self.lbl_supplier.config(text=f"Total Supplier\n[ {str(len(supplier))} ]")

			cur.execute("select *from category")
			category=cur.fetchall()
			self.lbl_category.config(text=f"Total Category\n[ {str(len(category))} ]")
			
			cur.execute("select *from employee")
			employee=cur.fetchall()
			self.lbl_employee.config(text=f"Total Employees\n[ {str(len(employee))} ]")
			
			bill=str(len(os.listdir('bill')))
			self.lbl_sales.config(text=f'Total Sales\n[ {str(bill)} ]')
			self.update_date_time()
			self.lbl_clock.after(200,self.update_content)

		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def update_date_time(self):
		time_=time.strftime("%I:%M:%S")
		date_=time.strftime("%d-%m-%Y")
		self.lbl_clock.config(text=f" Welcome   to  Inventory  Management  System\t\t Date: {str(date_)}\t\tTime:{str(time_)}",)
		
	def Exit_app(self):
		op=messagebox.askyesno("EXIT","Do you really want to exit?")
		if op>0:
			self.root.destroy()


if __name__=="__main__":		
	root=Tk()
	c=IMS(root)
	root.mainloop()


