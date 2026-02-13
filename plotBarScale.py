def plotBarScale(dataToPlot: list[str], maxBarSize: int = 50) -> None:
    """
    Generates a list of office-wide projects formatted for the CSV file.

    Args:
        dataToPlot (list[str]): List of string to visualize.
        maxBarSize (int): Maximum length of the bar. The default is given.

    Returns:
        None
    """
    if not dataToPlot:
        return None

    charBar: str = "█"  # Default bar character
    countDataPlot: list[int] = [
        len(x) for x in dataToPlot
    ]  # Calculate length of every item
    maxDataPLot: int = max(countDataPlot)  # Calculatalue longest value
    lenStrData = len(str(maxDataPLot))  # Calculate number padding

    for number in countDataPlot:
        # Calculate bar length in relationship to maxBarSize
        numberBar: str = charBar * int(number / maxDataPLot * maxBarSize)
        print(f"{str(number).rjust(lenStrData)}: {numberBar}")
