# Design and Analysis of Alogrithm Project
# Abstract
This project presents the implementation and analysis of five convex hull algorithms—Brute
Force, Jarvis March, Gramham Scan, Quick Elimination, and Andrew’s Algorithm, as
well as a Line Segment Intersection algorithm using three different methods—Algebraic,
CCW Computation, and Vector Cross Product. The implementation is carried out in
Python, featuring a graphical user interface (GUI) for visualizing the results of both sets
of algorithms. These algorithms are applied to respective sets of points and line segments,
and their time and space complexities are thoroughly analyzed. The report aims to provide a comprehensive understanding of the performance characteristics and suitability of
each algorithm in their respective problem domains.

# Introduction
In the realm of computational geometry, convex hull algorithms stand as pivotal solutions
to the challenge of identifying the convex hull within a given set of points. This report
delves into the exploration of five distinct algorithms, each bringing its own unique approach to resolving the convex hull problem. Concurrently, the report also delves into the
intricacies of Line Segment Intersection—a fundamental problem in computational geometry. This particular challenge involves determining the intersection of two provided
line segments. Within this context, the report scrutinizes three different algorithms, each
offering its distinct methodology for tackling the Line Segment Intersection problem.

# Programming Design
0.2.1
# Convex Hull Algorithms:
# 0.2.1 Brute Force Convex Hull Algorithm:
The Brute Force algorithm iteratively checks every triplet of points for a valid convex
hull. This algorithm has a time complexity of O(n^4) and a space complexity of O(n).
# 0.2.2 Jarvis March Convex Hull Algorithm:
Jarvis March, also known as the Gift Wrapping algorithm, selects the point with the lowest
y-coordinate as the starting point and iteratively selects the next point with the smallest
polar angle. The time complexity of Jarvis March is O(n^2), with a space complexity of
O(n). 
# 0.2.3 Graham Scan Convex Hull Algorithm:
The Graham Scan algorithm involves sorting points based on their polar angles and constructing the convex hull in a counterclockwise manner. The time complexity of Graham
Scan is O (n log n), and its space complexity is O(n).
# 0.2.4 Quick Elimination Convex Hull Algorithm:
Quick Elimination is an optimization of Graham Scan, where the point set is divided into
smaller subsets, and Graham Scan is applied to each subset. The time complexity is O (n
log h), and the space complexity is O(n).
# 0.2.5 Andrew’s Monotone Chain Convex Hull Algorithm:
Andrew’s Algorithm sorts the points and computes the convex hull in two separate chains—lower
and upper. The time complexity is O (n log n), and the space complexity is O(n).
1
# 0.3 Line Segment Algorithms:
0.3.1
# 0.2.6 Algebraic Line Segment Intersection Algorithm:
The Algebraic method calculates the slopes of the line segments and checks for intersection using algebraic equations. The time complexity is dependent on the solution of a
system of equations and is analyzed further in the results section.
# 0.2.7 CCW Computation Line Segment Intersection Algorithm:
The CCW (Counter Clockwise) computation method involves determining the orientation
of three points. The algorithm checks the orientations of relevant point triplets to identify
intersections efficiently.
# 0.2.8 Vector Cross Product Line Segment Intersection Algorithm:
The Vector Cross Product method utilizes vector operations to determine whether two line
segments intersect. This approach offers an alternative computational perspective.

# Experimental Execution:
# For Convex Hull Algorithms:
Measure the execution time using the time library. Measure space complexity using
sys.getsizeof(). Update the GUI labels with time and space complexity results.
# For Line Segment Intersection Algorithm:
Implement methods to check intersection using different techniques. Update the GUI
labels with intersection results.

# CONCLUSION:
In conclusion, the choice of a convex hull algorithm depends on the specific requirements
of the application. For large datasets, Graham Scan and Quick Elimination prove to be
efficient, while Jarvis March and Andrew’s Algorithm strike a balance between performance and simplicity. Additionally, the choice of a Line Segment Intersection algorithm
depends on specific requirements and considerations. The CCW computation and Vector Cross Product methods demonstrate efficient and reliable intersection detection. The
algebraic method, while accurate, may have variable computational costs. The provided
GUI enhances user interaction and visualization of the algorithms.
