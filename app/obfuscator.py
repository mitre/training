import base64
import hashlib


async def A(f, cls):
    F = ord;E = len;return await _B(f, E, F, cls(999,'foo','bar','splat', None))


async def _B(f, E, F, cls):
    R = base64.standard_b64encode;q = hashlib.sha256;CM=hashlib.sha224;r=hashlib.sha3_256;G = f.challenge.encode();A = R(G);B = q(A).hexdigest();B = '%s' % B;Q = f.completed;A = A.decode('utf-8');C = E(A);D = E(B)
    if C > D:B = await _C(B, C - D)
    elif D > C:A = await _C(A, D - C)
    H = ''.join([chr(F(C) ^ F(D)) for (C, D) in zip(B, A)]);
    if cls.completed:return await _C('%s' % r(R(H.encode())).hexdigest(), 1)
    elif Q:return '%s' % q(R(H.encode())).hexdigest()
    else:return await _C('%s' % CM(R(H.encode())).hexdigest(), 15)


async def _C(s, a):
    return s + ''.join(['0' for A in range(a)])