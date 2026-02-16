def plotBarScale(dataToPlot: dict[str, int], maxBarSize: int = 50) -> None:
    """
    Generates a list of office-wide projects formatted for the CSV file.

    Args:
        dataToPlot (dict[str, int]): Dictionary of names (keys) and numbers (values) to visualize.
        maxBarSize (int): Maximum length of the bar. The default is given.

    Returns:
        None
    """
    if not dataToPlot:
        return None

    charBar: str = "█"  # Default bar character
    dataNames: list[str] = list(dataToPlot.keys())
    countDataPlot: list[int] = [x for x in dataToPlot.values()]
    maxDataPLot: int = max(countDataPlot)  # Calculatalue longest value
    lenStrData = len(str(maxDataPLot))  # Calculate number padding

    for index, number in enumerate(countDataPlot):
        name = dataNames[index]
        # Calculate bar length in relationship to maxBarSize
        numberBar: str = charBar * int(number / maxDataPLot * maxBarSize)
        print(f"{name} | {str(number).rjust(lenStrData)}: {numberBar}")


""""
---- SAMPLE ----
nameA | countA ███████████
nameB | countB █████
"""
