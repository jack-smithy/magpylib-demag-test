import numpy as np
from magpylib.magnet import Cuboid
from magpylib_material_response import meshing, demag

# dimensions of the cuboid (m)
A, B, C = 100e-6, 10e-6, 10e-6

# polarization of the cuboid before demagnetization effects (T)
POLARIZATION = (0, 0, 1)

# number of cells to discretise the magnet into
TARGET_ELEMS = 100

# chi_x, chi_y, chi_z - if material is isotropic, replace with a scalar
# honestly i don't really know what value would be appropriate
SUSCEPTIBILITY = (1, 1, 1)


def main():
    # define the magnet with homogeneous magnetization
    cuboid = Cuboid(dimension=(A, B, C), polarization=POLARIZATION)

    # apply self-demagnetization effects
    mesh = meshing.mesh_Cuboid(cuboid=cuboid, target_elems=TARGET_ELEMS)
    demag.apply_demag(mesh, inplace=True, susceptibility=SUSCEPTIBILITY)

    # make measurement grid 1.5micro m below bottom surface of magnet
    xx = np.linspace(-A / 2, A / 2, 5)
    yy = np.linspace(-B / 2, B / 2, 5)
    z = -C / 2 - 1.5e-6

    observers = np.array([[(x, y, z) for x in xx] for y in yy]).reshape(-1, 3)

    # get the field
    H = cuboid.getH(observers)

    print(H)


if __name__ == "__main__":
    main()
