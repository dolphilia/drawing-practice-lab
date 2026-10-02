"""Geometric checks on declared 2D correspondences, not image scoring."""
import math


def points(data):
    if not isinstance(data,dict) or not data: raise ValueError('nonempty ID-to-point mapping required')
    out={}
    for key,value in data.items():
        if not isinstance(key,str) or not key: raise ValueError('nonempty string IDs required')
        if not isinstance(value,(list,tuple)) or len(value)!=2: raise ValueError('missing or malformed point')
        if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) for v in value):
            raise ValueError('finite numeric coordinates required')
        out[key]=tuple(value)
    return out


def paired(reference, observed):
    r,o=points(reference),points(observed)
    if r.keys()!=o.keys(): raise ValueError('ID sets differ; select the same subset explicitly')
    return r,o


def positive(value):
    if isinstance(value,bool) or not isinstance(value,(float,int)) or not math.isfinite(value) or value<=0:
        raise ValueError('finite positive length required')
    return value


def position_error(reference, observed, normalizer):
    r,o=paired(reference,observed); length=positive(normalizer)
    return sum(math.hypot(o[k][0]-r[k][0],o[k][1]-r[k][1]) for k in r)/len(r)/length


def angle_error(reference, observed, start_id, end_id):
    r,o=paired(reference,observed)
    if start_id not in r or end_id not in r: raise ValueError('axis IDs absent')
    vectors=[]
    for p in [r,o]:
        v=tuple(p[end_id][i]-p[start_id][i] for i in [0,1])
        if math.hypot(*v)<=1e-12: raise ValueError('axis collapsed')
        vectors.append(v)
    a,b=vectors
    return math.degrees(math.atan2(abs(a[0]*b[1]-a[1]*b[0]),a[0]*b[0]+a[1]*b[1]))


def ratio_error(ref_numerator, ref_denominator, obs_numerator, obs_denominator):
    a,b,c,d=map(positive,[ref_numerator,ref_denominator,obs_numerator,obs_denominator])
    return abs(math.log(c)-math.log(d)-math.log(a)+math.log(b))


def align(reference, observed, mode='translation'):
    """Return transformed observations and parameters; never silently align a score.

    modes: translation, rigid (translation + rotation), similarity (+uniform scale).
    A rotation/reflection ambiguity in collapsed data is rejected. Reflection is
    never fitted. The original observations are not modified.
    """
    r,o=paired(reference,observed)
    if mode not in {'translation','rigid','similarity'}: raise ValueError('unknown alignment')
    rc=tuple(sum(v[i] for v in r.values())/len(r) for i in [0,1])
    oc=tuple(sum(v[i] for v in o.values())/len(o) for i in [0,1])
    theta,scale=0.,1.
    if mode!='translation':
        rv=[(v[0]-rc[0],v[1]-rc[1]) for v in r.values()]
        ov=[(o[k][0]-oc[0],o[k][1]-oc[1]) for k in r]
        xx=sum(a[0]*b[0]+a[1]*b[1] for a,b in zip(ov,rv))
        xy=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(ov,rv))
        ss=sum(x*x+y*y for x,y in ov)
        if ss<=1e-12 or math.hypot(xx,xy)<=1e-12: raise ValueError('degenerate alignment')
        theta=math.atan2(xy,xx)
        if mode=='similarity': scale=math.hypot(xx,xy)/ss
    c,s=math.cos(theta),math.sin(theta)
    transformed={k:(rc[0]+scale*(c*(v[0]-oc[0])-s*(v[1]-oc[1])),
                    rc[1]+scale*(s*(v[0]-oc[0])+c*(v[1]-oc[1]))) for k,v in o.items()}
    return transformed,{'mode':mode,'rotation_deg':math.degrees(theta),'scale':scale,
                        'reference_centroid':rc,'observed_centroid':oc}
