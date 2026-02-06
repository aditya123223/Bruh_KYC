def liveness_check(f1, f2):

    # Require motion difference
    import numpy as np

    diff = np.mean(np.abs(f1.astype(float) - f2.astype(float)))

    print("Liveness motion diff:", diff)

    return diff > 5  # tune threshold



