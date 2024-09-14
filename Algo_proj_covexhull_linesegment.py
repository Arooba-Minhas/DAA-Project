import tkinter as tk
import matplotlib.pyplot as plt
from functools import cmp_to_key
import time
import sys
from sympy import symbols,Eq,solve,Point,Point2D


# Line segment algorithms start
class LineSegmentIntersectionApp:
    # GUI
    def __init__ (self,root):
        self.root = root
        self.root.title ("Line Segment Intersection")

        self.canvas = tk.Canvas (root,width=500,height=500,bg='white')
        self.canvas.pack (pady=20)

        self.create_cartesian_plane ()

        self.points = [ ]
        self.lines = [ ]
        self.add_point_enabled = False  # Flag to enable point addition
        self.points_limit = 4  # Limit points to 4 (two points for each line)

        self.intersection_label = tk.Label (root,text="Intersection: None",font=("Helvetica",10,"bold"),bg="white",
                                            fg="teal")
        self.intersection_label.pack (side=tk.TOP,pady=10)

        self.add_point_button = tk.Button (root,text="Add Point",command=self.enable_add_point,
                                           font=("Helvetica",10,"bold"),bg="white",fg="teal")
        self.add_point_button.pack (side=tk.TOP,padx=10,pady=5)

        self.clear_button = tk.Button (root,text="Clear",command=self.clear_canvas,font=("Helvetica",10,"bold"),
                                       bg="white",fg="teal")
        self.clear_button.pack (side=tk.TOP,padx=10,pady=5)

        # Adding a dropdown menu to select the intersection method
        self.method_var = tk.StringVar (root)
        self.method_var.set ("Choice")  # default choice
        self.method_dropdown = tk.OptionMenu (root,self.method_var,"Algebraic","CCW Computation","Vector Cross Product")
        self.method_dropdown.pack (side=tk.TOP,padx=10)

        self.canvas.bind ("<Button-1>",self.on_click)

    def enable_add_point (self):
        if len (self.points) < self.points_limit:
            self.add_point_enabled = True
        else:
            tk.messagebox.showinfo ("Info","Only 4 points (2 for each line) are allowed.")

    def add_point (self):
        if self.add_point_enabled:
            x,y = self.points[ -1 ] if self.points else (0,0)
            point = self.canvas.create_oval (x - 5,y - 5,x + 5,y + 5,fill='black')
            self.points.append ((x,y))

            if len (self.points) == 2:
                line = self.canvas.create_line (self.points,fill='blue')
                self.lines.append (line)
                self.points = [ ]
                self.check_intersection ()
                self.add_point_enabled = False  # Disable further point addition
        else:
            tk.messagebox.showinfo ("Info","Please click 'Add Point' to enable adding points.")

    def on_click (self,event):
        if self.add_point_enabled:
            x,y = event.x,event.y
            self.add_point_at (x,y)
        else:
            tk.messagebox.showinfo ("Info","Please click 'Add Point' to enable adding points.")

    def add_point_at (self,x,y):
        point = self.canvas.create_oval (x - 5,y - 5,x + 5,y + 5,fill='black')
        self.points.append ((x,y))

        if len (self.points) == 2:
            line = self.canvas.create_line (self.points,fill='blue')
            self.lines.append (line)
            self.points = [ ]
            self.check_intersection ()
            self.add_point_enabled = False  # Disable further point addition

    def clear_canvas (self):
        self.canvas.delete ("all")
        self.create_cartesian_plane ()
        self.points = [ ]
        self.lines = [ ]
        self.intersection_label.config (text="Intersection: None")
        self.add_point_enabled = False

    def check_intersection (self):
        x1,y1,x2,y2 = self.canvas.coords (self.lines[ 0 ])
        x3,y3,x4,y4 = self.canvas.coords (self.lines[ 1 ])

        method = self.method_var.get ()

        if method == "Algebraic":
            self.check_algebraic_intersection (x1,y1,x2,y2,x3,y3,x4,y4)
        elif method == "CCW Computation":
            self.check_ccw_computation (x1,y1,x2,y2,x3,y3,x4,y4)
        elif method == "Vector Cross Product":
            self.check_vector_cross_product (x1,y1,x2,y2,x3,y3,x4,y4)

    def check_algebraic_intersection (self,x1,y1,x2,y2,x3,y3,x4,y4):
        # Calculate slopes
        m1 = (y2 - y1) / (x2 - x1) if x2 != x1 else float ('inf')
        m2 = (y4 - y3) / (x4 - x3) if x4 != x3 else float ('inf')

        if m1 != m2:

            x_int,y_int = symbols ('x_int y_int')

            eq1 = Eq (y_int,m1 * (x_int - x1) + y1)
            eq2 = Eq (y_int,m2 * (x_int - x3) + y3)

            intersection_point = solve ((eq1,eq2),(x_int,y_int))

            if intersection_point:
                x_int,y_int = intersection_point[ x_int ],intersection_point[ y_int ]
                if min (x1,x2) <= x_int <= max (x1,x2) and min (x3,x4) <= x_int <= max (x3,x4):
                    self.intersection_label.config (text="Intersection: Yes")
                else:
                    self.intersection_label.config (text="Intersection: No")
            else:
                self.intersection_label.config (text="Intersection: No")
        else:
            self.intersection_label.config (text="Intersection: No")

    def check_ccw_computation (self,x1,y1,x2,y2,x3,y3,x4,y4):
        orientation1 = self.ccw ((x1,y1),(x2,y2),(x3,y3))
        orientation2 = self.ccw ((x1,y1),(x2,y2),(x4,y4))
        orientation3 = self.ccw ((x3,y3),(x4,y4),(x1,y1))
        orientation4 = self.ccw ((x3,y3),(x4,y4),(x2,y2))

        if orientation1 * orientation2 < 0 and orientation3 * orientation4 < 0:
            self.intersection_label.config (text="Intersection: Yes")
        else:
            self.intersection_label.config (text="Intersection: No")

    def check_vector_cross_product (self,x1,y1,x2,y2,x3,y3,x4,y4):
        cross_product1 = self.vector_cross_product ((x1,y1),(x2,y2),(x3,y3))
        cross_product2 = self.vector_cross_product ((x1,y1),(x2,y2),(x4,y4))

        if cross_product1 * cross_product2 < 0:
            self.intersection_label.config (text="Intersection: Yes")
        else:
            self.intersection_label.config (text="Intersection: No")

    def ccw (self,p1,p2,p3):
        return (p2[ 0 ] - p1[ 0 ]) * (p3[ 1 ] - p1[ 1 ]) - (p2[ 1 ] - p1[ 1 ]) * (p3[ 0 ] - p1[ 0 ])

    def vector_cross_product (self,p1,p2,p3):
        vector1 = Point2D (p2[ 0 ] - p1[ 0 ],p2[ 1 ] - p1[ 1 ])
        vector2 = Point2D (p3[ 0 ] - p1[ 0 ],p3[ 1 ] - p1[ 1 ])
        return vector1[ 0 ] * vector2[ 1 ] - vector1[ 1 ] * vector2[ 0 ]

    def create_cartesian_plane (self):

        self.canvas.create_line (50,250,450,250,width=2)
        for i in range (50,451,50):
            self.canvas.create_line (i,245,i,255)
            self.canvas.create_text (i,260,text=str (i - 250),anchor=tk.N)

        self.canvas.create_line (250,50,250,450,width=2)
        for i in range (50,451,50):
            self.canvas.create_line (245,i,255,i)
            self.canvas.create_text (260,i,text=str (250 - i),anchor=tk.W)


# convex hull algorithms start
class Point:
    def __init__ (self,x,y):
        self.x = x
        self.y = y


def orientation (p,q,r):
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
    if val == 0:
        return 0
    return 1 if val > 0 else 2


def compare (p1,p2):
    o = orientation (p0,p1,p2)
    if o == 0:
        return (p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2 - ((p2.x - p0.x) ** 2 + (p2.y - p0.y) ** 2)
    return -1 if o == 2 else 1


def graham_scan (points):
    global p0
    n = len (points)
    if n < 3:
        return points

    ymin = min (points,key=lambda p: p.y).y
    p0 = min (filter (lambda p: p.y == ymin,points),key=lambda p: p.x)

    sorted_points = sorted (points,key=cmp_to_key (compare))
    hull = [ sorted_points[ 0 ],sorted_points[ 1 ] ]

    for i in range (2,n):
        while len (hull) > 1 and orientation (hull[ -2 ],hull[ -1 ],sorted_points[ i ]) != 2:
            hull.pop ()
        hull.append (sorted_points[ i ])

    return hull


def quick_elimination_convex_hull (points):
    def orientation (p,q,r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def compare (p1,p2):
        o = orientation (p0,p1,p2)
        if o == 0:
            return (p1.x - p0.x) ** 2 + (p1.y - p0.y) ** 2 - ((p2.x - p0.x) ** 2 + (p2.y - p0.y) ** 2)
        return -1 if o == 2 else 1

    def graham_scanq (sub_points):
        n = len (sub_points)
        if n < 3:
            return sub_points

        ymin = min (sub_points,key=lambda p: p.y).y
        global p0
        p0 = min (filter (lambda p: p.y == ymin,sub_points),key=lambda p: p.x)

        sorted_points = sorted (sub_points,key=cmp_to_key (compare))
        hull = [ sorted_points[ 0 ],sorted_points[ 1 ] ]

        for i in range (2,n):
            while len (hull) > 1 and orientation (hull[ -2 ],hull[ -1 ],sorted_points[ i ]) != 2:
                hull.pop ()
            hull.append (sorted_points[ i ])

        return hull

    chunk_size = 5
    sub_sets = [ points[ i:i + chunk_size ] for i in range (0,len (points),chunk_size) ]

    hull = [ ]
    for sub_set in sub_sets:
        sub_hull = graham_scanq (sub_set)
        hull.extend (sub_hull)

    return graham_scanq (hull)


def andrews_algorithm (points):
    def left_to_right (p1,p2,p3):
        return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x) >= 0

    points = sorted (points,key=lambda point: (point.x,point.y))
    lower = [ ]
    upper = [ ]

    for point in points:
        while len (lower) >= 2 and not left_to_right (lower[ -2 ],lower[ -1 ],point):
            lower.pop ()
        lower.append (point)

    for point in reversed (points):
        while len (upper) >= 2 and not left_to_right (upper[ -2 ],upper[ -1 ],point):
            upper.pop ()
        upper.append (point)

    return lower[ :-1 ] + upper[ :-1 ]


def brute_force_convex_hull (points):
    def orientation (p,q,r):
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)
        if val == 0:
            return 0
        return 1 if val > 0 else 2

    def is_on_segment (p1,p2,p,q):
        return (
                min (p1.x,p2.x) <= p.x <= max (p1.x,p2.x)
                and min (p1.y,p2.y) <= p.y <= max (p1.y,p2.y)
                and min (p1.x,p2.x) <= q.x <= max (p1.x,p2.x)
                and min (p1.y,p2.y) <= q.y <= max (p1.y,p2.y)
        )

    n = len (points)
    hull = [ ]

    for i in range (n):
        for j in range (i + 1,n):
            is_valid = True
            for k in range (n):
                if k != i and k != j and orientation (points[ i ],points[ j ],points[ k ]) == 0 and not is_on_segment (
                        points[ i ],points[ j ],points[ k ],points
                ):
                    is_inside = False
                    for m in range (n):
                        if (
                                m != i
                                and m != j
                                and m != k
                                and is_on_segment (points[ i ],points[ j ],points[ k ],points[ m ])
                        ):
                            is_inside = True
                            break
                    if not is_inside:
                        hull.append (points[ i ])
                        hull.append (points[ j ])
                        is_valid = False
                        break
            if not is_valid:
                break

    return hull


def jarvis_march (points):
    n = len (points)
    if n < 3:
        return points

    hull = [ ]
    start_point = min (points,key=lambda p: (p.y,p.x))

    while True:
        hull.append (start_point)
        endpoint = points[ 0 ]

        for i in range (1,n):
            if endpoint == start_point or orientation (start_point,points[ i ],endpoint) == 2:
                endpoint = points[ i ]

        start_point = endpoint

        if start_point == hull[ 0 ]:
            break

    return hull


# GUI
class ConvexHullApp:
    def __init__ (self,master):
        self.master = master
        self.master.title ("Convex Hull Algorithms")
        self.points = [ ]

        self.canvas = tk.Canvas (self.master,width=600,height=400,bg="black")
        self.canvas.pack ()

        self.canvas.bind ("<Button-1>",self.add_point)

        self.compute_graham_button = tk.Button (self.master,text="Compute Graham Scan Convex Hull",
                                                font=("Helvetica",10,"bold"),bg="white",fg="teal",
                                                command=self.compute_graham_convex_hull)
        self.compute_graham_button.pack (pady=5)

        self.compute_jarvis_button = tk.Button (self.master,text="Compute Jarvis March Convex Hull",
                                                font=("Helvetica",10,"bold"),bg="white",fg="teal",
                                                command=self.compute_jarvis_convex_hull)
        self.compute_jarvis_button.pack (pady=5)
        self.compute_quick_elimination_button = tk.Button (self.master,text="Compute Quick Elimination Convex Hull",
                                                           font=("Helvetica",10,"bold"),bg="white",fg="teal",
                                                           command=self.compute_quick_elimination_convex_hull)
        self.compute_quick_elimination_button.pack (pady=5)
        self.compute_andrew_button = tk.Button (self.master,text="Compute Andrew's Monotone Chain Convex Hull",
                                                font=("Helvetica",10,"bold"),bg="white",fg="teal",
                                                command=self.compute_andrew_convex_hull)
        self.compute_andrew_button.pack (pady=5)
        self.compute_brute_force_button = tk.Button (self.master,text="Compute Brute Force Convex Hull",
                                                     font=("Helvetica",10,"bold"),bg="white",fg="teal",
                                                     command=self.compute_brute_force_convex_hull)
        self.compute_brute_force_button.pack (pady=5)
        self.clear_points_button = tk.Button (self.master,text="Clear Points",font=("Helvetica",10,"bold"),bg="white",
                                              fg="teal",command=self.clear_points)
        self.clear_points_button.pack (pady=5)
        self.time_label = tk.Label (self.master,text="Time Complexity: ",font=("Helvetica",10,"bold"),bg="white",
                                    fg="teal")
        self.time_label.pack (pady=5)

        self.space_label = tk.Label (self.master,text="Space Complexity: ",font=("Helvetica",10,"bold"),bg="white",
                                     fg="teal")
        self.space_label.pack (pady=5)

        self.convex_hull = [ ]

    def add_point (self,event):
        x,y = event.x,event.y
        point = Point (x,y)
        self.points.append (point)
        self.canvas.create_oval (x - 3,y - 3,x + 3,y + 3,fill="blue")

    def compute_graham_convex_hull (self):
        start_time = time.time ()
        self.convex_hull = graham_scan (self.points)
        end_time = time.time ()
        total_time = end_time - start_time

        # Update time label with total time for Graham Scan
        self.time_label.config (text=f"Time Complexity (Graham Scan): O(n log n), {total_time:.6f} seconds")

        start_space = sys.getsizeof (self.points)
        self.convex_hull = graham_scan (self.points)  # Using Graham Scan for space complexity measurement
        end_space = sys.getsizeof (self.convex_hull)
        space_complexity = end_space - start_space
        self.space_label.config (text=f"Space Complexity (Graham Scan): O(n), {space_complexity} bytes")

        self.draw_convex_hull ()

    def compute_brute_force_convex_hull (self):
        start_time = time.time ()
        self.convex_hull = brute_force_convex_hull (self.points)
        end_time = time.time ()
        total_time = end_time - start_time
        self.time_label.config (text=f"Time Complexity (Brute Force): O(n^4),{total_time:.6f} seconds")
        start_space = sys.getsizeof (self.points)
        self.convex_hull = brute_force_convex_hull (self.points)
        end_space = sys.getsizeof (self.convex_hull)
        space_complexity = end_space - start_space
        self.space_label.config (text=f"Space Complexity (Brute Force): O(n),{space_complexity} bytes")
        self.draw_convex_hull ()

    def compute_jarvis_convex_hull (self):
        start_time = time.time ()
        self.convex_hull = jarvis_march (self.points)
        end_time = time.time ()
        total_time = end_time - start_time
        self.time_label.config (text=f"Time Complexity (Jarvis March): O(n^2), {total_time:.6f} seconds")

        start_space = sys.getsizeof (self.points)
        end_space = sys.getsizeof (self.convex_hull)
        space_complexity = end_space - start_space
        self.space_label.config (text=f"Space Complexity (Jarvis March): O(n), {space_complexity} bytes")

        self.draw_convex_hull ()

    def compute_andrew_convex_hull (self):
        start_time = time.time ()
        self.convex_hull = andrews_algorithm (self.points)
        end_time = time.time ()
        total_time = end_time - start_time
        self.time_label.config (text=f"Time Complexity (Andrew's Algorithm): O(n log n),{total_time:.6f} seconds")
        start_space = sys.getsizeof (self.points)
        self.convex_hull = andrews_algorithm (self.points)
        end_space = sys.getsizeof (self.convex_hull)
        space_complexity = end_space - start_space
        self.space_label.config (text="Space Complexity: O(n), {} bytes".format (end_space - start_space))
        self.draw_convex_hull ()

    def compute_quick_elimination_convex_hull (self):
        start_time = time.time ()
        self.convex_hull = quick_elimination_convex_hull (self.points)
        end_time = time.time ()
        total_time = end_time - start_time
        self.time_label.config (text=f"Time Complexity (Quick Elimination): O(n log h), {total_time:.6f} seconds")
        start_space = sys.getsizeof (self.points)
        self.convex_hull = quick_elimination_convex_hull (self.points)
        end_space = sys.getsizeof (self.convex_hull)
        space_complexity = end_space - start_space
        self.space_label.config (
            text="Space Complexity (Quick Elimination): O(n), {} bytes".format (end_space - start_space))
        self.draw_convex_hull ()

    def draw_convex_hull (self):
        if len (self.convex_hull) < 3:
            return
        hull_points = [ (p.x,p.y) for p in self.convex_hull ]
        hull_points.append ((self.convex_hull[ 0 ].x,self.convex_hull[ 0 ].y))
        self.canvas.create_line (hull_points,fill="red",width=2)
        plt.plot (*zip (*hull_points),marker='o',color='r',ls='-',ms=5)
        plt.show ()

    def clear_points (self):
        self.points = [ ]
        self.convex_hull = [ ]
        self.canvas.delete ("all")


# main page GUI
root = tk.Tk ()
root.title ("Algorithm Project")

frame = tk.Frame (root,bg="white")
frame.pack (expand=True,fill="both",padx=20,pady=(50,50))

heading_label = tk.Label (frame,text="Convex Hull and Line Segment",font=("Helvetica",20,"bold"),bg="white",fg="teal")
heading_label.grid (row=0,column=0,columnspan=2,pady=(50,10),sticky="n")

# Add group members in the middle
group_label = tk.Label (frame,text="Group Members:",font=("Helvetica",16,"bold"),bg="white",fg="teal")
group_label.grid (row=1,column=0,columnspan=2,pady=(50,5))

members = [ "21K-3081 Bushra Khan","21K- 3094 Arooba Minhas","21K-3155 Alaina Usmani" ]
for i,member in enumerate (members,start=2):
    member_label = tk.Label (frame,text=member,font=("Helvetica",16,"bold"),bg="white",fg="teal")
    member_label.grid (row=i,column=0,columnspan=2,pady=(50,2),sticky="ew")  # Added sticky="ew"

frame.columnconfigure (0,weight=1)
frame.columnconfigure (1,weight=1)

line_segment_button = tk.Button (frame,text="Line Segment Algorithm",
                                 command=lambda: LineSegmentIntersectionApp (tk.Toplevel (root)),
                                 font=("Helvetica",12,"bold"),bg="teal",fg="white")
line_segment_button.grid (row=i + 1,column=0,pady=(130,0),padx=10,sticky="ew")

convex_hull_button = tk.Button (frame,text="Convex Hull Algorithm",font=("Helvetica",12,"bold"),
                                command=lambda: ConvexHullApp (tk.Toplevel (root)),bg="teal",fg="white")
convex_hull_button.grid (row=i + 1,column=1,pady=(130,0),padx=10,sticky="ew")

root.mainloop ()
