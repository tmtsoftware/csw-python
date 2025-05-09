
class Separator:
    Hyphen = "-"

    def hyphenate(*arg: str) -> str:
        return Separator.Hyphen.join(arg)
