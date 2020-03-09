import base64
import hashlib


async def A(f):
    F = ord;E = len;return await _B(f, E, F)


async def _B(f, E, F):
    R = base64.standard_b64encode;q = hashlib.sha256;G = f.challenge.encode();A = R(G);B = q(A).hexdigest();B = '%s' % B;Q = f.completed;A = A.decode('utf-8');C = E(A);D = E(B)
    if C > D:B = await _C(B, C - D)
    elif D > C:A = await _C(A, D - C)
    H = ''.join([chr(F(C) ^ F(D)) for (C, D) in zip(B, A)]);
    if Q:return '%s' % q(R(H.encode())).hexdigest()
    else:return await _C('%s' % q(R(H.encode())).hexdigest(), 15)


async def _C(s, a):
    return s + ''.join(['0' for A in range(a)])