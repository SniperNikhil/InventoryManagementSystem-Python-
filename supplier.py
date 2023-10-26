from tkinter import*
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class supplierClass:
	def __init__(self,root):
		self.root=root
		self.root.geometry("1100x500+220+138")
		self.root.title("Inventory Management System | Developed by Nikhil | Pratham and Anthony")
		self.root.config(bg="WHITE")
		self.root.focus_force()
		self.root.resizable(0,0)
#*****************************************************************************************************************************************************
		#**********************All Variables******************************************************************************************************************
		self.var_searchby=StringVar()
		self.var_txt=StringVar()

		self.var_invoice=StringVar()
		self.var_sname=StringVar()
		self.var_scontact=StringVar()
		
#********************************Input Option*********************************************************************************************************
		lbl_invoice=Label(self.root,text="Invoice No",font=("goudy old style",15,"bold"),bg="White",bd=4).place(x=650,y=50)
		txt_invoice=Entry(self.root,textvariable=self.var_txt,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=750,y=50,width=180)
			
		btn_search=Button(self.root,text="Search",command=self.search,font=("goudy old style",15,"bold"),bg="green",fg="white",bd=4,cursor="hand2").place(x=940,y=50,height=28,width=150)

#******************************************Title**********************************************************************************************
		title=Label(self.root,text="Manage Supplier Details",font=("goudy old style",19,"bold"),bg="#FF6013",fg="white",bd=4).place(x=0,y=0,relwidth=1)

#******************************************Content*********************************************************************************************
		#********************************************Row 1*********************************************************************************************

		lbl_invoice=Label(self.root,text="Invoice No",font=("goudy old style",15,"bold"),bg="White",bd=4).place(x=50,y=50)
		txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=190,y=50,width=180)
				
		#********************************************Row 2*********************************************************************************************
		lbl_sname=Label(self.root,text="Supplier Name",font=("goudy old style",15,"bold"),bg="White",bd=4).place(x=50,y=100)
		txt_sname=Entry(self.root,textvariable=self.var_sname,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=190,y=100,width=180)
		
		#********************************************Row 3*********************************************************************************************
		lbl_scontact=Label(self.root,text="Contact",font=("goudy old style",15,"bold"),bg="White",bd=4).place(x=50,y=150)
		txt_scontact=Entry(self.root,textvariable=self.var_scontact,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4).place(x=190,y=150,width=180)
		
		#********************************************Row 4*********************************************************************************************
		lbl_descr=Label(self.root,text="Description",font=("goudy old style",15,"bold"),bg="White",bd=4).place(x=50,y=200)
		self.txt_descr=Text(self.root,font=("goudy old style",15,"bold"),bg="lightyellow",bd=4)
		self.txt_descr.place(x=190,y=200,width=450,height=150)

		btn_save=Button(self.root,text="Save",command=self.save,font=("goudy old style",17,"bold"),bg="#8A2BE2",fg="BLACK",bd=4,cursor="hand2").place(x=220,y=380,height=40,width=150)
		btn_update=Button(self.root,text="Update",command=self.update,font=("goudy old style",17,"bold"),bg="#FF6013",fg="BLACK",bd=4,cursor="hand2").place(x=400,y=380,height=40,width=150)
		btn_delete=Button(self.root,text="Delete",command=self.delete,font=("goudy old style",17,"bold"),bg="#DC143C",fg="BLACK",bd=4,cursor="hand2").place(x=220,y=440,height=40,width=150)
		btn_clear=Button(self.root,text="Clear",command=self.clear,font=("goudy old style",17,"bold"),bg="#CAFF70",fg="BLACK",bd=4,cursor="hand2").place(x=400,y=440,height=40,width=150)

#******************************Employee Details Treeview***********************************************************************************************************************
		emp_frame=Frame(self.root,bg="#DCDCDC",bd=3,relief=RIDGE)
		emp_frame.place(x=655,y=100,width=435,height=380)

		scrolly=Scrollbar(emp_frame,orient=VERTICAL)
		scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

		self.SupplierTable=ttk.Treeview(emp_frame,columns=("invoice","sname","scontact","descr"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
		scrollx.pack(side=BOTTOM,fill=X)
		scrolly.pack(side=RIGHT,fill=Y)
		scrolly.config(command=self.SupplierTable.yview)
		scrollx.config(command=self.SupplierTable.xview)

		self.SupplierTable.heading("invoice",text="Invoice ID")
		self.SupplierTable.heading("sname",text="Supplier NAME")
		self.SupplierTable.heading("scontact",text="Contact")
		self.SupplierTable.heading("descr",text="Description")

		self.SupplierTable["show"]="headings"

		self.SupplierTable.column("invoice",width=50)
		self.SupplierTable.column("sname",width=50)
		self.SupplierTable.column("scontact",width=50)
		self.SupplierTable.column("descr",width=100)
		self.SupplierTable.pack(fill=BOTH,expand=1)
		self.SupplierTable.bind("<ButtonRelease-1>",self.get_data)
		self.root.focus_force()

		self.show()

#************************************************************************************************************************************************
	def save(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_invoice.get()=="":
				messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
			else:
				cur.execute("Select *from supplier where invoice=?",(self.var_invoice.get(),))
				row=cur.fetchone()
				if row!=None:
					messagebox.showerror("Error","Invoice No. already assigned, try different",parent=self.root)
				else:
					cur.execute("Insert into supplier (invoice,sname,scontact,descr) values(?,?,?,?)",(
												self.var_invoice.get(),
												self.var_sname.get(),
												self.var_scontact.get(),																								
												self.txt_descr.get('1.0',END),
							))	
					con.commit()
					messagebox.showinfo("Success","Supplier Added Succesfully",parent=self.root)
					self.show()
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def show(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			cur.execute("Select *from supplier")
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
		#print(row)
		self.var_invoice.set(row[0])
		self.var_sname.set(row[1])
		self.var_scontact.set(row[2])												
		self.txt_descr.delete('1.0',END)
		self.txt_descr.insert(END,row[3])

	def update(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_invoice.get()=="":
				messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
			else:
				cur.execute("Select *from supplier where invoice=?",(self.var_invoice.get(),))
				row=cur.fetchone()
				if row==None:
					messagebox.showerror("Error","Invalid Invoice No",parent=self.root)
				else:
					cur.execute("Update supplier set sname=?,scontact=?,descr=? where invoice=?",(
												self.var_sname.get(),
												self.var_scontact.get(),																	
												self.txt_descr.get('1.0',END),
												self.var_invoice.get()
							))	
					con.commit()
					messagebox.showinfo("Success","Supplier Updated Succesfully",parent=self.root)
					self.show()
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def delete(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_invoice.get()=="":
				messagebox.showerror("Error","Invoice No. must be required",parent=self.root)
			else:
				cur.execute("Select *from supplier where invoice=?",(self.var_invoice.get(),))
				row=cur.fetchone()
				if row==None:
					messagebox.showerror("Error","Invalid Invoice No.",parent=self.root)
				else:
					op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
					if op==True:						
						cur.execute("delete from supplier where invoice=?",(self.var_invoice.get(),))
						con.commit()
						messagebox.showinfo("Delete","Supplier Deleted Succesfully",parent=self.root)
						self.clear()
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

	def clear(self):
		self.var_invoice.set("")
		self.var_sname.set("")
		self.var_scontact.set("")												
		self.txt_descr.delete('1.0',END)
		self.var_txt.set("")
		self.show()

	def search(self):
		con=sqlite3.connect(database=r'ims.db')
		cur=con.cursor()
		try:
			if self.var_txt.get()=='':
				messagebox.showerror("Error","Required Search input",parent=self.root)
			else:
				cur.execute("Select *from supplier where invoice=?",(self.var_txt.get(),))
				row=cur.fetchone()
				if row!=None:				
					self.SupplierTable.delete(*self.SupplierTable.get_children())
					self.SupplierTable.insert('',END,values=row)
				else:
					messagebox.showerror("Error","No Record Found",parent=self.root)
		except Exception as e:
			messagebox.showerror("Error",f"Error due to : {str(e)}")

if __name__=="__main__":		
	root=Tk()
	c=supplierClass(root)
	root.mainloop()

