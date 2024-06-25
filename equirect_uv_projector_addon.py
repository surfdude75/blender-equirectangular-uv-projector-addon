bl_info = {
    "name": "Equirectangular UV Projector",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import math
import mathutils

class EquirectangularUVProjector(bpy.types.Operator):
    """Equirectangular UV Projector"""
    bl_idname = "object.equirectangular_uv_projector"
    bl_label = "Equirectangular UV Projector"
    bl_options = { 'REGISTER', 'UNDO' }
    
    def calc_uv(v):
        xyl = v.xy.length
        if xyl == 0:
            alfa = math.pi/2
            if v.z > 0:
                V = 1
            else:
                V = 0
        else:
            alfa = math.atan(v.z/xyl)
            V = alfa/math.pi+0.5
        U = math.atan2(v.y,v.x)/math.pi/2+0.5
        return mathutils.Vector((U, V))
    
    def execute(self, context): 
        obj = context.active_object
        cl = context.scene.cursor.location
        me = obj.data
        for f in me.polygons:
            for i in f.loop_indices: # &lt;-- python Range object with the proper indices already set
                l = me.loops[i] # The loop entry this polygon point refers to
                v = me.vertices[l.vertex_index] # The vertex data that loop entry refers to
                uv = EquirectangularUVProjector.calc_uv(v.co-cl)
                ul =  me.uv_layers.active
                ul.data[l.index].uv = uv
            for i in f.loop_indices:
                l = me.loops[i]
                vi = l.vertex_index
                ul =  me.uv_layers.active
                uv = ul.data[l.index].uv
                if uv.x > 0.9999:
                    u = 0
                    count = 0
                    for j in f.loop_indices:
                        l2 = me.loops[j]
                        uv2 = ul.data[l2.index].uv
                        edge = me.edges[l2.edge_index]
                        if uv2.x < 0.5:
                            count = count + 1
                    if count > 0:
                        uv.x = 0
            for i in f.loop_indices:
                l = me.loops[i]
                vi = l.vertex_index
                ul =  me.uv_layers.active
                uv = ul.data[l.index].uv
                if uv.y == 0 or uv.y == 1:
                    u = 0
                    count = 0
                    for j in f.loop_indices:                            
                        l2 = me.loops[j]
                        uv2 = ul.data[l2.index].uv
                        edge = me.edges[l2.edge_index]
                        if j != i:
                            if uv2.y != 0 or uv2.y != 1:
                                u = u + uv2.x
                                count = count + 1
                    u = u / count
                    uv.x = u
        return { 'FINISHED' }

def menu_func(self, context):
    self.layout.operator(EquirectangularUVProjector.bl_idname)

def register():
    bpy.utils.register_class(EquirectangularUVProjector)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(EquirectangularUVProjector)


if __name__ == "__main__":
    register()
