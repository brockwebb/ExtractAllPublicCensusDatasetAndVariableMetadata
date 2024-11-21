from tqdm import tqdm

def track_progress(iterable, description="Processing", total=None, unit="items"):
    """
    Wrap an iterable with a progress bar for tracking execution.

    Parameters:
    -----------
    iterable : iterable
        Any iterable object (e.g., list, DataFrame rows) to process.
    description : str, optional
        A description displayed with the progress bar (default: "Processing").
    total : int, optional
        Total number of iterations, useful if the iterable length isn't directly available (default: None).
    unit : str, optional
        Unit name displayed in the progress bar (default: "items").

    Returns:
    --------
    generator
        A generator wrapped with a tqdm progress bar.

    Examples:
    ---------
    >>> from progress_tracker import track_progress
    >>> for item in track_progress(range(10), description="Counting"):
    >>>     print(item)
    """
    return tqdm(iterable, desc=description, total=total, unit=unit)

