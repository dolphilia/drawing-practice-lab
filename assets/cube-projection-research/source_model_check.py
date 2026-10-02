"""Independent conditional check of the plane interpretation in Ishikawa fig 4.

This is an original numeric example, not digitization of the source figure.
"""
from pathlib import Path
import json, math
from geometry import dot, norm, sub, mul, cross, intersection


def main():
    # Side view: horizontal Z, vertical Y; O=(0,0), P=(100,0).
    # Front bottom C/D=(100,-100), top A/B=(100,-40), edge length 60.
    P=[100.,0.]; bottom=[100.,-100.]; top=[100.,-40.]
    Q=mul(bottom,100/norm(bottom)) # OQ = OP, exactly the stated length construction.
    R=intersection([0,0],top,P,Q)
    source_height=norm(sub(P,Q))-norm(sub(P,R))
    up_side=mul(sub(P,Q),1/norm(sub(P,Q)))
    right=[1.,0.,0.]
    up=[0.,up_side[1],up_side[0]]
    normal=cross(right,up);f=dot([0,0,100],normal)
    widths=[]
    for y in (-40.,-100.):
        zcamera=dot([0,y,100],normal)
        widths.append(60*f/zcamera)
    assert abs(widths[0]-widths[1])>1
    assert all(abs(w-60)>1 for w in widths)
    result={'date':'2026-10-02','kind':'original conditional geometric reconstruction',
            'source_figure':'Ishikawa 2015 fig 4 / section 2(1) steps 4–7',
            'side_input':{'O':[0,0],'P':P,'front_top':top,'front_bottom':bottom},
            'Q':Q,'R':R,'plane_distance':f,
            'source_rectangle_width':60,'source_rectangle_height':source_height,
            'same_plane_central_projection_width_top':widths[0],
            'same_plane_central_projection_width_bottom':widths[1],
            'conclusion':'The equal-width rectangle construction is not the central projection onto the plane represented by PQ in this example. Do not use it as the ground-truth model for this project.',
            'scope':'Does not assess artistic usefulness, author intention beyond stated plane, or empirical learning outcomes.'}
    Path(__file__).with_name('source-model-check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
