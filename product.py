from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class productClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+138")
		self.root.title("Inventory Management System | Developed by Nikhil | Pratham and Anthony")
		self.root.config(bg="WHITE")
		self.root.focus_force()
		self.root.resizable(0,0)

#*******************************Variables*********************************************************************************************
		self.var_pid=StringVar()
		
		self.var_txt=StringVar()
		self.var_searchby=StringVar()
		
		self.var_cat=StringVar()
		self.var_sup=StringVar()
		self.cat_list=[]
		self.sup_list=[]
		self.fetch_cat_sup()
		self.var_name=StringVar()
		self.var_price=StringVar()
		self.var_qty=StringVar()
		self.var_status=StringVar()

#******************************************Product Details Frame***************************************************************************8
		product_Frame=Frame(self.root,bg="WHITE",bd=4,relief=RIDGE,)
		product_Frame.place(x=10,y=10,width=450,height=480)

		title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",21,"bold"),bg="#FF6013",fg="white",bd=4)
		title.pack(side=TOP,fill=X)

		lbl_category=Label(product_Frame,text="Category",font=("goudy old style",19,"bold"),bg="White",bd=4).place(x=20,y=50)
		cmb_category=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",15))
		cmb_category.place(x=150,y=55,width=180)
		cmb_category.current(0)	
		
		lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",19,"bold"),bg="White",bd=4).place(x=20,y=100)
		cmb_supplier=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",15))
		cmb_supplier.place(x=150,y=105,width=180)
		cmb_supplier.current(0)

		lbl_name=Label(product_Frame,text="Name",font=("goudy old style",19,"bold"),bg="White",bd=4).place(x=20,y=150)
		txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=165,y=168,width=180)
		
		lbl_price=Label(product_Frame,text="Price",font=("goudy old style",19,"bold"),bg="White",bd=4).place(x=20,y=200)
		txt_price=Entry(self.root,textvariable=self.var_price,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=165,y=220,width=180)
		
		lbl_qty=Label(product_Frame,text="QTY",font=("goudy old style",19,"bold"),bg="White",bd=4).place(x=20,y=250)
		txt_qty=Entry(self.root,textvariable=self.var_qty,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=165,y=270,width=180)
		
		lbl_status=Label(product_Frame,text="Status",font=("goudy old style",19,"bold"),bg="White",bd=4).place(x=20,y=310)
		cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
		cmb_status.place(x=150,y=315,width=180)
		cmb_status.current(0)


		btn_save=Button(product_Frame,text="Save",command=self.save, font=("goudy old style",15,"bold"),bg="#8A2BE2",fg="BLACK",bd=4,cursor="hand2").place(x=10,y=400,height=35,width=105)
		btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15,"bold"),bg="#FF6013",fg="BLACK",bd=4,cursor="hand2").place(x=118,y=400,height=35,width=105)
		btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15,"bold"),bg="#DC143C",fg="BLACK",bd=4,cursor="hand2").place(x=225,y=400,height=35,width=105)
		btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15,"bold"),bg="#CAFF70",fg="BLACK",bd=4,cursor="hand2").place(x=333,y=400,height=35,width=105)


#******************************Search Frame***********************************************************************************************************
		SearchFrame=LabelFrame(self.root,text="Search Product",bg="WHITE",font=("Arial 12 bold"),bd=2,relief=RIDGE)
		SearchFrame.place(x=475,y=5,width=600,height=70)

		#********************************Option*********************************************************************************************************
		cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Search","Supplier","Category","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
		cmb_search.place(x=10,y=10,width=180)
		cmb_search.current(0)

		txt_search=Entry(SearchFrame,textvariable=self.var_txt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
		btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="green",fg="white",bd=4,cursor="hand2").place(x=420,y=10,height=28,width=150)

#******************************Product Frame Treeview***************************************************************************************************************************
		emp_frame=Frame(self.root,bg="#DCDCDC",bd=3,relief=RIDGE)
		emp_frame.place(x=475,y=80,width=600,height=408)

		scrolly=Scrollbar(emp_frame,orient=VERTICAL)
		scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

		self.SupplierTable=ttk.Treeview(emp_frame,columns=("pid","supplier","category","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM,fill=X)
		scrolly.pack(side=RIGHT,fill=Y)
		scrolly.config(command=self.SupplierTable.yview)
		scrollx.config(command=self.SupplierTable.xview)

		self.SupplierTable.heading("pid",text="P ID")
		self.SupplierTable.heading("category",text="Category")
		self.SupplierTable.heading("supplier",text="Supplier")
		self.SupplierTable.heading("name",text="Name")
		self.SupplierTable.heading("price",text="Price")
		self.SupplierTable.heading("qty",text="QTY")
		self.SupplierTable.heading("status",text="Status")


		self.SupplierTable["show"]="headings"

		self.SupplierTable.column("pid",width=50)
		self.SupplierTable.column("category",width=70)
		self.SupplierTable.column("supplier",width=70)
		self.SupplierTable.column("name",width=100)
		self.SupplierTable.column("price",width=100)
		self.SupplierTable.column("qty",width=100)
		self.SupplierTable.column("status",width=100)

		self.SupplierTable.pack(fill=BOTH,expand=1)
		self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
		self.root.focus_force()
		self.show()

#************************************************All Functions***********************************************************************************
	def fetch_cat_sup(self):
		self.sup_list.append("Empty")
		self.cat_list.append("Empty")

		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			cur.execute("Select name from category")
			cat=cur.fetchall()
			if len(cat) > 0 :
				del self.cat_list[:]
				self.cat_list.append("Select")
				for i in cat:
					self.cat_list.append(i[0])

			cur.execute("Select sname from supplier")
			sup=cur.fetchall()
			if len(sup) > 0 :
				del self.sup_list[:]
				self.sup_list.append("Select")
				for i in sup:
					self.sup_list.append(i[0])

		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def save(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_cat.get()=="SELECT" or  self.var_cat.get()=="Empty"   or self.var_sup.get()=="SELECT" or  self.var_cat.get()=="Empty"  or self.var_name.get()=="":
				messagebox.showerror("Error","Please Enter All Fields",parent=self.root)
			else:
				cur.execute("Select *from product where name=?",(self.var_name.get(),))
				row=cur.fetchone()
				if row!=None:
					messagebox.showerror("Error","Product already present ,try different",parent=self.root)
				else:
					cur.execute("Insert into product (category,supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
												self.var_cat.get(),
												self.var_sup.get(),												
												self.var_name.get(),
												self.var_price.get(),
												self.var_qty.get(),
												self.var_status.get(),
							))	
					con.commit()
					messagebox.showinfo("Success","Product Added Succesfully",parent=self.root)
					self.show()
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")


	def show(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			cur.execute("Select *from product")
			rows=cur.fetchall()
			self.SupplierTable.delete(*self.SupplierTable.get_children())
			for row in rows:
				self.SupplierTable.insert('',END,values=row)
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def get_data(self,ev):
		f=self.SupplierTable.focus()
		content=(self.SupplierTable.item(f))
		row=content['values']
		self.var_pid.set(row[0])
		self.var_sup.set(row[1])
		self.var_cat.set(row[2])												
		self.var_name.set(row[3])
		self.var_price.set(row[4])
		self.var_qty.set(row[5])
		self.var_status.set(row[6])

	def update(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_pid.get()=="":
				messagebox.showerror("Error","Please Select Product from List",parent=self.root)
			else:
				cur.execute("Select *from product where pid=?",(self.var_pid.get(),))
				row=cur.fetchone()
				if row==None:
					messagebox.showerror("Error","Invalid Product",parent=self.root)
				else:
					cur.execute("Update product set category=?,supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
									self.var_cat.get(),
									self.var_sup.get(),												
									self.var_name.get(),
									self.var_price.get(),
									self.var_qty.get(),
									self.var_status.get(),
									self.var_pid.get()			
							))	
					con.commit()
					messagebox.showinfo("Success","Product Updated Succesfully",parent=self.root)
					self.show()
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def delete(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_pid.get()=="":
				messagebox.showerror("Error","Please Select Product from List",parent=self.root)
			else:
				cur.execute("Select *from product where pid=?",(self.var_pid.get(),))
				row=cur.fetchone()
				if row==None:
					messagebox.showerror("Error","Invalid Product",parent=self.root)
				else:
					op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
					if op==True:						
						cur.execute("delete from product where pid=?",(self.var_pid.get(),))
						con.commit()
						messagebox.showinfo("Delete","Product Deleted Succesfully",parent=self.root)
						self.clear()
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def clear(self):
		self.var_cat.set("Select")
		self.var_sup.set("Select")												
		self.var_name.set("")
		self.var_price.set("")
		self.var_qty.set("")
		self.var_status.set("Active")
		self.var_pid.set("")
		self.var_txt.set("")
		self.var_searchby.set("Search")
		self.show()

	def search(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_searchby.get()=="Search":
				messagebox.showerror("Error","Select Search By Option",parent=self.root)
			elif self.var_txt.get()=='':
				messagebox.showerror("Error","Required Search input",parent=self.root)
			else:
				cur.execute("Select *from product where "+self.var_searchby.get()+" LIKE '%" + self.var_txt.get() + "%'")
				rows=cur.fetchall()
				if len(rows)!=0:				
					self.SupplierTable.delete(*self.SupplierTable.get_children())
					for row in rows:
						self.SupplierTable.insert('',END,values=row)
				else:
					messagebox.showerror("Error","No Record Found",parent=self.root)
		except Exception as e:
			print(e)
			messagebox.showerror("Error",f"Error due to : {str(e)}")


if __name__=="__main__":		
	root=Tk()
	c=productClass(root)
	root.mainloop()
