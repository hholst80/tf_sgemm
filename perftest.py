import os
import timeit
import tensorflow as tf
import tf_blas_matmul  # noqa
sess = tf.InteractiveSession(config=tf.ConfigProto(
    inter_op_parallelism_threads=1, intra_op_parallelism_threads=1))

if 'OMP_NUM_THREADS' not in os.environ or \
   int(os.environ['OMP_NUM_THREADS']) > 1:
    print("WARNING: Using multicore BLAS. Was this intended?")

for N in [1000, 2000, 3000, 4000, 5000]:
    prev_delta = None
    for matmul in [tf.matmul, tf_blas_matmul.blas_matmul]:
        print('{name} {size}'.format(name=matmul.__name__, size=N))

        A = tf.Variable(initial_value=tf.random_uniform([N, N]))
        B = tf.Variable(initial_value=tf.random_uniform([N, N]))
        C = tf.Variable(initial_value=tf.zeros([N, N]))

        op = C.assign(matmul(A, B))

        sess.run(A.initializer)
        sess.run(B.initializer)

        s0 = timeit.default_timer()
        sess.run(op)
        s1 = timeit.default_timer()

        delta = s1 - s0
        if prev_delta is not None:
            print(delta, 'speedup {0:.1f}'.format(prev_delta/delta))
        else:
            print(delta)
            prev_delta = delta
