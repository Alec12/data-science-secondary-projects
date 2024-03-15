import pandas as pd

def create_bins(mv, qcuts, dim):
    """create quartile bins for column"""
    # Filter out empty strings and convert to float
    mv[dim] = mv[dim].apply(lambda x: float(x) if x != '' else None)

    # Calculate bin labels
    levels = [f"{dim}_level_{x}" for x in range(qcuts)]

    # Perform binning
    mv[dim] = pd.qcut(mv[dim], qcuts, labels=levels).astype(str)

    return mv