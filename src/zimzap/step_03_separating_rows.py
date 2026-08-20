"""This module contains step 3, separating the rows of the image into 
the two mutually orthogonal polarisation directions."""

def separate_rows(img, phase:{"0", "pi"}):
    """This function separates the rows of the image into the two 
    mutually orthogonal polarisation directions. 
    
    It returns a tuple where the 1st element is the intensity of the 
    ordinary ray and the 2nd is the intensity of the extraordinary ray.
    
    **Inputs:**
    
    `img`: The input image
    
    `phase`:    The phase mode that the image was recorded in. This must 
                be "0" or "pi".
    
    **Outputs:**
    
    0 -`o_0` or `o_pi`: The intensity of the ordinary ray
    
    1 -`e_0` or `e_pi`: The intensity of the extraordinary ray"""

    if phase not in {"0", "pi"}:
        raise ValueError("Phase must be 0 or pi.")

    if phase=="0":
        o_0 = img[:,  1::2, :]
        e_0 = img[:, ::2, :]
        return o_0, e_0
    elif phase=="pi":
        o_pi = img[:,  ::2, :]
        e_pi = img[:, 1::2, :]
        return o_pi, e_pi