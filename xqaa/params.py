""" Parameters for the xqaa algorithm. """


from dataclasses import dataclass, field

# Add a few methods to be shared by them all
@dataclass
class myDataClass:
    @property
    def fields(self):
        return list(self.__dataclass_fields__.keys())
    def meta(self, attribute_name):
        return self.__dataclass_fields__[attribute_name].metadata
    def chk_options(self, attribute_name):
        options = self.__dataclass_fields__[attribute_name].metadata['options']



# FRB Energetics -- energy
@dataclass
class XQAAParams(myDataClass):
    bbmin: float = field(
        default=600.0,
        metadata={
            "help": "Minimum wavelength for backscattering coefficient",
            "unit": "nm",
            "Notation": "b_{\\rm b,min}",
        },
    )
    bbmax: float = field(
        default=650.0,
        metadata={
            "help": "Maximum wavelength for backscattering coefficient",
            "unit": "nm",
            "Notation": "b_{\\rm b,max}",
        },
    )
    amin: float = field(
        default=400.0,
        metadata={
            "help": "Minimum wavelength for absorption coefficient",
            "unit": "nm",
            "Notation": "a_{\\rm min}",
        },
    )
    amax: float = field(
        default=450.0,
        metadata={
            "help": "Maximum wavelength for absorption coefficient",
            "unit": "nm",
            "Notation": "a_{\\rm max}",
        },
    )
    dataset: str = field(
        default="loisel23",
        metadata={
            "help": "Dataset to use for the inversion",
            "options": ["loisel23"],
        },
    )
    L23_X: int = field(
        default=1,
        metadata={
            "help": "X index for Loisel23 dataset",
            "Notation": "X",
        },
    )
    L23_Y: int = field(
        default=0,
        metadata={
            "help": "Y index for Loisel23 dataset",
            "Notation": "Y",
        },
    )