
# coding: utf-8

# In[24]:




# In[9]:

import Tkinter as tk
import ttk
import tkMessageBox
import tkFileDialog
import copy
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pylab



class IncorrectNodeException(Exception):
    pass

#main class GUI
class SeaofBTCapp(tk.Tk):
    
    #def __init__ is the function that is called automatically upon an object's construction
    
    def __init__(self, *args, **kwargs):
         
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Computer Networks Project")
        
        #container for all the frames
        
        self.container = tk.Frame(self)
        
        #self is used to reference the object itself
        
        self.container.pack(fill="both", expand = True)

        self.container.grid_rowconfigure(1, weight=2)
        self.container.grid_columnconfigure(1, weight=3)
                
        self.frames =dict()
        # this is a dictionary of frames
        
        # static windows stored in this frame
        for fra in (StartPage, enter_initial_router_node,selection_page,remove_node_page,remove_edge_page,recover_node_page):

            frame = fra(self.container, self)

            self.frames[fra] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)
        
        
    #to show frame
    
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        #tkraise shows one window at a time by bringing a window in front of the other
        
    #Funcion to create  connection table    
    def connect_tab(self,pre, initial_router, g):
       
        a=copy.copy(pre)
        connect=dict()
        connect['r'+str(initial_router)]='-'
        for i in a.keys():
            if i == initial_router:
                continue
            j=i
            for v in a[j]:
                while j != initial_router:
                    lr=j
                    j=a[lr][0]
            connect['r'+str(i)]=lr    
                
        return connect
        #returns a dictionary of values in the connection table

        
    def dijkstra_algorithm(self,data,initial_router):
        
        #implementation of dijkstra algorithm
        
        
        distances = dict()
        predict = dict()
        deque = list()
        for i in range(len(data)):
            distances[i] = 100  
            predict[int(data[i][0][1:])] = [-1]
            deque.append(i)
        distances[initial_router] = 0
        
        
        while len(deque) != 0:
            n_distances = dict()
            for i in range(len(deque)):
                n_distances[deque[i]] = distances[deque[i]]
            min_val = min(n_distances.items(), key=lambda x: x[1])
            min_val = min_val[0]
            deque.remove(min_val)
            for i in range(len(data)):
                if data[min_val][1][i] not in [0,-1]:
                    updated_distance = distances[min_val] + data[min_val][1][i]
                    if updated_distance < distances[i]:
                        distances[i] = updated_distance
                        predict[int(data[i][0][1:])] = [min_val]
                    elif updated_distance == distances[i]:
                        predict[int(data[i][0][1:])].append(min_val)
                
        
                           
        return predict
    

    
    def enter_the_file(self):
        
            #reading the matrix file that is taken as an input from the user
        try:
            file = tkFileDialog.askopenfile(parent=self,mode='rb',title='Choose a file')
            data=file.read()
            
            g=[]
            x=[]
            cp=[]
            v=[]
            data = data.split('\n')
            # storing the values commama separted
            for i in data:
                g.append(map(int,i.split()))
                cp.append(map(int,i.split()))
            for i in range(len(g)):
                x.append((('r'+str(i)),g[i]))
                v.append((('r'+str(i)),cp[i]))  
            #print(x)
            # storing the values in the dictionary in the form of tuples having the router name
            dc={0:x,1:v}
            self.data= dc
              
            self.show_frame(enter_initial_router_node)
        #Exception for invalid entry like special characters or any other combinations.
        except ValueError:
            tkMessageBox.showerror(
            "File Error",
            "Please enter a valid tex.txt' file..."
        )
    
    #method to get the initial_router node entry from the user
    def get_initial_router(self, initial_router):
        
        try:
            self.initial_router = int(initial_router.get())
            
            #Checking if initial_router entered not a valid node from topology, then an exception will be raised
            if self.initial_router < 0:
                raise IncorrectNodeException
            
            if self.initial_router > (len(self.data[0])-1):
                raise IncorrectNodeException
        
            self.show_frame(selection_page)
        
        #Exception for invalid entry like special characters or any other combinations.
        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "NOT A VALID SOURCE INPUT."
        )
        
        #Custom exception for incorrect node or any other integer other than node entered
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "This Source Node is not present in the topology")
        return
    
  
    
    #Function to process the destination router
    def enter_target_router(self):
        
        try:
            self.pre = self.dijkstra_algorithm(self.data[0],self.initial_router)
        
            self.connection = self.connect_tab(self.pre,self.initial_router,self.data[0])
        
            target_frame = enter_target_page(self.container, self)

            self.frames[enter_target_page] = target_frame

            target_frame.grid(row=0, column=0, sticky="nsew")
        
            self.show_frame(enter_target_page)
        
        except IndexError:
            tkMessageBox.showerror(
            "Error",
            " Too many destinations loaded please enter the file again ."
        )
        return
    
    #method to get the destination node from the user
    def net_to_target(self,entry):
        
        try:
        
            self.target = int(entry.get())
            
            #Handling the execption if destination entered not a valid node from topology matrix,
            
            if self.target > (len(self.data[0])-1):
                raise IncorrectNodeException
        
            frame = net_to_target_page(self.container, self)

            self.frames[net_to_target_page] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        
            self.show_frame(net_to_target_page)
        
        
        #handling invalid entry like special characters, spaces .
        except ValueError:
            tkMessageBox.showerror(
             "Input Error",
            "Please enter a valid destination node."
        )
        
        #Custom exception for incorrect node or any other integer other than destination node entered
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "please enter a valid node available in the network topoogy.."
        )
        return
        
    #method to create an object of connection table frame and raising it above other windows   
    def display_connect_tab(self):
        
        try:
        
            self.pre = self.dijkstra_algorithm(self.data[0],self.initial_router)
        
            self.connection = self.connect_tab(self.pre,self.initial_router,self.data[0])
        
            display_frame = display_connect_tab_page(self.container, self)

            self.frames[display_connect_tab_page] = display_frame

            display_frame.grid(row=0, column=0, sticky="nsew")
        
        

            self.show_frame(display_connect_tab_page)
        
        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "Please Try loading the file"
        )
        
        return
    
    #method to create an object of display shortest path frame and raising it above other windows
    def show_smallest_path(self):
        
        
        
            self.pre = self.dijkstra_algorithm(self.data[0],self.initial_router)
        
            self.connection = self.connect_tab(self.pre,self.initial_router,self.data[0])
        
                
            path_frame = display_shortest_path_page(self.container, self)

            self.frames[display_shortest_path_page] = path_frame

            path_frame.grid(row=0, column=0, sticky="nsew")
        
            self.show_frame(display_shortest_path_page)
        
        
    #method to remove a node    
    def remove_node(self,new_node):
        
        try:
        
            
            self.new_node = new_node.get().split()
            self.new_node = map(int,self.new_node)
            print(self.new_node)
            #Checking if node entered not a valid node from topology, then an exception will be raised
            
            self.new_weight=-1
            del(self.data[0][self.new_node[0]])
            for i in range(len(self.data[0])): 
                del(self.data[0][i][1][self.new_node[0]])
            
            self.show_frame(selection_page)

        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "That was not a valid input.."
        )
        except IndexError:
            tkMessageBox.showerror(
            "Input Error",
            "Please reload the file again"
        )
            
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "That was not a valid number of node. Please Try with %s nodes..." % len(self.data[0])
        )
        return

    
    
    #method to recover a node    
    def recover_node(self,new_node):
        
        try:
        
            self.new_node = new_node.get().split()
            self.new_node = map(int,self.new_node)
           
            for i in range(len(self.data[0])): 
                self.data[0][i][1].insert(self.new_node[0],self.data[1][i][1][self.new_node[0]])
            self.data[0].insert(self.new_node[0],self.data[1][self.new_node[0]])     
            
            
            self.show_frame(selection_page)

            
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "That was not a valid number of node. Please Try with %s nodes..." % len(self.data[0])
        )
        return
 
    
    #method to remove an edge
    def remove_edge(self,new_edge,new_weight):
        
        try:
            
            self.new_edge = new_edge.get().split()
            self.new_edge = map(int,self.new_edge)
            
            
            for i in self.new_edge:
                if i not in range(0, len(self.data[0])):
                    raise IncorrectNodeException
        
            self.new_weight = new_weight
            self.data[0][self.new_edge[0]][1][self.new_edge[1]] = self.new_weight
            self.data[1][self.new_edge[0]][1][self.new_edge[1]] = self.new_weight
            self.data[0][self.new_edge[1]][1][self.new_edge[0]] = self.new_weight
            self.data[1][self.new_edge[1]][1][self.new_edge[0]] = self.new_weight
            
        
            self.show_frame(selection_page)
        
        except ValueError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a valid weight..."
        )
        except IndexError:
            tkMessageBox.showerror(
            "Input Error",
            "Oops! That was not a valid input. Please Try again with a space between values..."
        )
            
        #Custom exception for incorrect node or any other integer other than destination node entered
        except IncorrectNodeException:
             tkMessageBox.showerror(
            "Node Error",
            "Oops! That was not a valid node for the topology selected. Please Try again with a valid Node for Edge..."
        )
        return
              
class StartPage(tk.Frame):
    
    #StartPage is inheriting from TK FRAME
    
    #here controller represents the container
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        
        #creating a label
        
        ttk.Style().configure("TButton", padding=6, relief="ridge", background="#ccc")
        label = ttk.Label(self, text="Link State Routing Algorithm",background='red',relief='ridge',foreground='black',font=("Helvetica", 28))
        label.pack(pady=50)


        #creating a button 
        button = ttk.Button(self,text="Load the network matrix topology",width=20,command=lambda: controller.enter_the_file())
        button.pack(fill='x', expand='1')

        
class enter_initial_router_node(tk.Frame):
    
    #enter_initial_router_node is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        
        l_sn = ttk.Label(self, font=("Helvetica", 28),text=" Enter the source node",justify="right")
        l_sn.pack()
        
        entry = ttk.Entry(self,widget=None,width=20)
        
        entry.pack(pady=40)
        
        #creating a button
        
        b_ps = ttk.Button(self,  text="Enter to proceed",width=25, 
                            command=lambda: controller.get_initial_router(entry))
        b_ps.pack()
        
        b_rh = ttk.Button(self, text="Return to Home", width=25,
                            command=lambda: controller.show_frame(StartPage))
        b_rh.pack(pady=15)
        
class selection_page(tk.Frame):
     
    #selection_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        
        l_se = ttk.Label(self, text="Select from the options below",relief='ridge',foreground='red',font=("Helvetica", 28))
        l_se.pack(padx=15,pady=15)
        
        #creating buttons
        
        #click button to display the network frame
        
        
        #click button to display the connection table frame
        
        b_dis = ttk.Button(self,text="Show the connection table",width=40,
                            command=lambda: controller.display_connect_tab())
        b_dis.pack(pady=15)
        
        #click button to display the shortest path to all nodes frame
        
        but = ttk.Button(self, text="Shortest path to all nodes",
                            command=lambda: controller.show_smallest_path())
        but.pack(pady=10,padx=10)
        
        #click button to display path to a destination frame
        
        b_sh = ttk.Button(self,text="Path to the destination",width=50,
                            command=lambda: controller.enter_target_router())
        b_sh.pack(pady=15)
        
        #click button to add an extra node frame
        
        b_rm = ttk.Button(self, text="Remove a router",width=30,
                            command=lambda: controller.show_frame(remove_node_page))
        b_rm.pack(pady=15)
        
        #click button to remove

        b_re = ttk.Button(self, text="Remove an edge",width=20,
                            command=lambda: controller.show_frame(remove_edge_page))
        b_re.pack(pady=15)
        #click button to recover router frame

        b_rn = ttk.Button(self, text="Recover the node",width=30,
                            command=lambda: controller.show_frame(recover_node_page))
        b_rn.pack(pady=15)
        
        #click button to take us back to the home page frame

        b_h = ttk.Button(self, text="Back to Home",width=30,
                            command=lambda: controller.show_frame(StartPage))
        b_h.pack(pady=15)
        
        #click button to take us back to the selection page frame
        
        but_sn = ttk.Button(self,  text="Return Source Node Selection Page",width=50,
                            command=lambda: controller.show_frame(enter_initial_router_node))
        but_sn.pack(pady=15)

    
        
class display_connect_tab_page(tk.Frame):
    
    #display_connection_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a scrollbar to scroll through the connection table frame
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side = tk.RIGHT, fill= tk.Y)
       
        connection_table_list = tk.Listbox(self, yscrollcommand = scrollbar.set ) 
        connection_table_list.insert(tk.END, "\nShowing Router %s Connection Table \n" % controller.initial_router)
        
        connection_table_list.insert(tk.END, "{:<8} {:<15}".format(' Final Destination ',' Interface'))
        connection_table_list.insert(tk.END, "{:<8} {:<15}".format('Destination ',' Interface'))
                       
        for dest,inter in controller.connection.iteritems():
            connection_table_list.insert(tk.END,"\t {:<8} \t {:<15}".format(dest, inter))
            connection_table_list.insert(tk.END,"\n")
            
        connection_table_list.pack(fill = "both",expand=True)   
        
        #creating a button and click the button to get back to selection page
        
        b_s = ttk.Button(self, text="Return Selection Page",width=35,
                            command=lambda: controller.show_frame(selection_page))
        
        b_s.pack()
        
class display_shortest_path_page(tk.Frame):
    
    #display_shortest_path_page is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        print(controller.data[0])
        g = nx.Graph()
        i=0
        for row in controller.data[0]:
            j=0
            for col in row[1]:
                if col not in [0,-1]:
                    #print(controller.data[0][i][0],controller.data[0][j][0],int(controller.data[0][i][1][j]))
                    g.add_edge(controller.data[0][i][0],controller.data[0][j][0], weight = int(controller.data[0][i][1][j]) )

                j = j+1
            i = i+1
            
        print(g)
        #creating scrollbar to scroll through the shortest path frame
        scrollbar = tk.Scrollbar(self)
        scrollbar.pack(side = tk.RIGHT, fill= tk.Y)
        
        mylist = tk.Listbox(self, yscrollcommand = scrollbar.set )
        self.a = copy.copy(controller.pre)
        for i in range(len(controller.data[0])):
            

            if i == controller.initial_router:
                continue
            
            mylist.insert(tk.END,"shortest path from  %s to %s" % (controller.data[0][controller.initial_router][0],controller.data[0][i][0]))
            
               
            paths = nx.all_shortest_paths(g,source=controller.data[0][controller.initial_router][0],target= controller.data[0][i][0], weight = 'weight')
            
            for path in paths:
                print('path',path)
                mylist.insert(tk.END,"path = %s" % path)
            
                self.cost = self.total_cost(path,controller.data[1])
            
                mylist.insert(tk.END,"Cost = %s " % self.cost)
                mylist.insert(tk.END,"\n")
        
        
        scrollbar.config( command = mylist.yview )
        mylist.pack(fill = "both",expand=True)
            
            
        button1 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
               
        button1.pack()
        
        
    #method for calculating total cost                    
    def total_cost(self,l,data):
        total = 0
        x_index = 0
        y_index = 1
        for r in range(len(l)-1):
            total = total + data[int(l[x_index][1:])][1][int(l[y_index][1:])]
            x_index += 1 
            y_index += 1
            
        return total


        
        
class remove_node_page(tk.Frame):
    
    #remove_node_page 

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        
        label = ttk.Label(self, text="Enter the node to be removed", font=("Helvetica", 28))
        label.pack(pady=10,padx=10)
        
        entry = ttk.Entry(self, width=10)
        entry.pack(pady=10,padx=10)
        
        #creating buttons
        
        #click the button to add the node taken as input from user to the network
        
        but_rn = ttk.Button(self, text="Remove Node",
                            command=lambda: controller.remove_node(entry))
        but_rn.pack(pady=10,padx=10)
        
        #click button to go back to selection page frame
        
        but_s = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        but_s.pack()
        
        #click button to go back to home page frame
        
        but_h = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        but_h.pack(pady=10,padx=10)

class recover_node_page(tk.Frame):
    
    #remove_node_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        
        label = ttk.Label(self, text="Enter the node to be recover", font=("Helvetica", 28))
        label.pack(pady=10,padx=10)
        
        entry = ttk.Entry(self, width=10)
        entry.pack(pady=10,padx=10)
        
        #creating buttons
        
        #click the button to remove the node taken as input from user to the network
        
        button = ttk.Button(self, text="Recover Node",
                            command=lambda: controller.recover_node(entry))
        button.pack(pady=10,padx=10)
        
        #click button to go back to selection page frame
        
        butt = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        butt.pack()
        
        #click button to go back to home page frame
        
        butt_1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        butt_1.pack(pady=10,padx=10)
        
        
class remove_edge_page(tk.Frame):
    
    #remove_edge_page is inheriting from TK FRAME

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating labels
        
        label = ttk.Label(self, text="Enter the edge to change the weight(For ex:4 5)", font=("Helvetica", 28))
        label.pack(pady=10,padx=10)
        
        entry_edge = ttk.Entry(self, width=10)
        entry_edge.pack(pady=10,padx=10)
        
        entry_weight= -1
        
        #creating buttons
        
        #click button to make the changes to the network
        
        but_re = ttk.Button(self, text="Remove Edge",
                            command=lambda: controller.remove_edge(entry_edge, entry_weight))
        #calling the function remove_edge to make changes in the network
        
        but_re.pack(pady=10,padx=10)
        
        #click button to go to the Selection page frame
        but_sp = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        but_sp.pack()
        
        #click button to go to back to home page frame
        but_h = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        but_h.pack(pady=10,padx=10)
        


class enter_target_page(tk.Frame):
    
    #enter_target_page is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        #creating a label
        label = ttk.Label(self, text="Please Enter the destination node", font=("Helvetica", 28))
        label.pack(pady=10,padx=10)
        
        entry = ttk.Entry(self, width=10)
        entry.pack(pady=10,padx=10)
        
        #creating buttons
        button = ttk.Button(self, text="click Enter",
                            command=lambda: controller.net_to_target(entry))
        button.pack(pady=10,padx=10)
        
        #click button to go to back to selection page frame
        button1 = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        button1.pack()

        
        
class net_to_target_page(tk.Frame):
    
    #net_to_target_page is inheriting from TK FRAME
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        
        g = nx.Graph()
        i=0
        for row in controller.data[0]:
            j=0
            for col in row[1]:
                if col not in [0,-1]:
                    g.add_edge(controller.data[0][i][0],controller.data[0][j][0], weight = int(controller.data[0][i][1][j]) )

                j = j+1
            i = i+1
            
            
        graph = nx.Graph()
        edge_labels = {}
        for paths in nx.all_shortest_paths(g,source=controller.data[0][controller.initial_router][0],target=controller.data[0][controller.target][0], weight = 'weight'):
            

            edge = []

            for i in range(len(paths)-1):
                edge = [paths[i],paths[i+1]]
                print(edge,'edge')
                graph.add_edge(edge[0],edge[1])
                edge_labels[(paths[i],paths[i+1])] = int(controller.data[0][int(paths[i][1:])][1][int(paths[i+1][1:])])

        f = plt.figure(figsize=(5,4))
        pos = nx.circular_layout(graph)
        nx.draw(graph,pos,with_labels = True)
        nx.draw_networkx_edge_labels(graph,pos,edge_labels = edge_labels)
       
   
        #creating a canvas to draw the shortest path network     
        canvas = FigureCanvasTkAgg(f, master=self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        canvas.draw()
        
        #click button to go to back to selection page frame
        
        bu = ttk.Button(self, text="Back to Selection Page",
                            command=lambda: controller.show_frame(selection_page))
        
        bu.pack()
                    

#object of sea class
app = SeaofBTCapp()

#for recursive call
app.mainloop()






# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



