"""
3D vector helper
"""

"3D Vector Constants"
ORIGIN = [0, 0, 0]
POSITIVE_X = [1, 0, 0]
NEGATIVE_X = [-1, 0, 0]
POSITIVE_Y = [0, 1, 0]
NEGATIVE_Y = [0, -1, 0]
POSITIVE_Z = [0, 0, 1]
NEGATIVE_Z = [0, 0, -1]

"3D Vector Operation"
add = lambda x, y: [x[0]+y[0], x[1]+y[1], x[2]+y[2]]

sub = lambda x, y: [x[0]-y[0], x[1]-y[1], x[2]-y[2]]

dot = lambda x, y: x[0]*y[0] + x[1]*y[1] + x[2]*y[2]

scalar_mul = lambda k, v: [v[0]*k, v[1]*k, v[2]*k]

cross = lambda x, y: [  x[1]*y[2] - x[2]*y[1], 
                        x[2]*y[0] - x[0]*y[2], 
                        x[0]*y[1] - x[1]*y[0] ]

# Rodrigues' rotation formula
def rotate(v, a):
    return add(cross(a, v), scalar_mul(dot(v, a), a))


if __name__ == '__main__':
    v = [1, 0, 1]
    a = POSITIVE_Z
    assert(rotate(v, a) == [0, 1, 1])

