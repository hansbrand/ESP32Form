import numpy as np
import DataContainer as DC
import FileManager as FM
import DataPoint as DP
import open3d as o3d
import trimesh
import numpy as np
import pyglet
#from vtkplotter import *


def createmesh(filename):


    pcd = o3d.io.read_point_cloud(filename)
    pcd.estimate_normals()

    # estimate radius for rolling ball
    distances = pcd.compute_nearest_neighbor_distance()
    avg_dist = np.mean(distances)
    radius = 3.0 * avg_dist   

    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(
               pcd,
               o3d.utility.DoubleVector([radius, radius * 2]))

    # create the triangular mesh with the vertices and faces from open3d
    tri_mesh = trimesh.Trimesh(np.asarray(mesh.vertices), np.asarray(mesh.triangles),
                              vertex_normals=np.asarray(mesh.vertex_normals))
    #n = tri_mesh.vertices.shape[0]
   # pc1 = Points(mesh.vertices, r=10)
    #pc1.colorVerticesByArray(range(n)) 

    trimesh.convex.is_convex(tri_mesh)
    #trimesh.export("test.stl")
    tri_mesh.show()
    return
