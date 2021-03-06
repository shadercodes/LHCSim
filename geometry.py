import taichi as ti
import random
from utils import clamp, particle_idx, vec3


# cube / cuboid
@ti.data_oriented
class cube:
    def __init__(self, x_start, x_end, y_start, y_end, z_start, z_end):
        self.type = "cube"

        # parameters
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.z_start = z_start
        self.z_end = z_end

    @ti.kernel
    def voxelize(self, px: ti.template(), world: ti.f32, n_grid: ti.i32,
                 bound_grid: ti.i32, npar: ti.i32):
        dx = world / n_grid
        bound = bound_grid * dx
        space_x = dx / npar

        for i, j, k in ti.ndrange(n_grid, n_grid, n_grid):
            x = (i + 0.5) * dx
            y = (j + 0.5) * dx
            z = (k + 0.5) * dx

            if self.x_start < x < self.x_end and self.y_start < y < self.y_end and self.z_start < z < self.z_end:
                for ix in range(npar):
                    for jx in range(npar):
                        for kx in range(npar):
                            xp = clamp(
                                i * dx + (ix + random.random()) * space_x,
                                bound + 1e-4, world - bound - 1e-4)
                            yp = clamp(
                                j * dx + (jx + random.random()) * space_x,
                                bound + 1e-4, world - bound - 1e-4)
                            zp = clamp(
                                k * dx + (kx + random.random()) * space_x,
                                bound + 1e-4, world - bound - 1e-4)

                            px[particle_idx(i, j, k, ix, jx, kx, n_grid,
                                            npar)] = vec3(xp, yp, zp)

# Sphere
@ti.data_oriented
class sphere:
    def __init__(self, c_x, c_y, c_z, r):
        self.type = "sphere"

        self.c_x = c_x
        self.c_y = c_y
        self.c_z = c_z
        self.r = r

    @ti.kernel
    def voxelize(self, px: ti.template(), world: ti.f32, n_grid: ti.i32, bound_grid: ti.i32, npar: ti.i32):
        dx = world / n_grid
        bound = bound_grid * dx
        space_x = dx / npar

        for i, j, k in ti.ndrange(n_grid, n_grid, n_grid):
            x = (i + 0.5) * dx
            y = (j + 0.5) * dx
            z = (k + 0.5) * dx

            if (x - self.c_x) ** 2 + (y - self.c_y) ** 2 + (z - self.c_z) ** 2 - self.r**2 < 0:
                for ix in range(npar):
                    for jx in range(npar):
                        for kx in range(npar):
                            xp = clamp(
                                i * dx + (ix + random.random()) * space_x,
                                bound + 1e-4, world - bound - 1e-4)
                            yp = clamp(
                                j * dx + (jx + random.random()) * space_x,
                                bound + 1e-4, world - bound - 1e-4)
                            zp = clamp(
                                k * dx + (kx + random.random()) * space_x,
                                bound + 1e-4, world - bound - 1e-4)

                            px[particle_idx(i, j, k, ix, jx, kx, n_grid,
                                            npar)] = vec3(xp, yp, zp)