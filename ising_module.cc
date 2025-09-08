/**************************************************************************
 * @file     ising_module.cc
 * @brief    Test for the pybind11 binding and cairo rendering in C++
 * @author   Markus Quandt  \n<markus.quandt@uni-tuebingen.de>
 *************************************************************************/

#include <vector>
#include <random>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <cairo/cairo.h>
namespace py11 = pybind11;

using Grid = std::vector<std::vector<int>>;

Grid init_grid(int N, bool hot = true) 
{
    Grid grid(N, std::vector<int>(N));
    if(hot)
    {
        std::random_device rd;
        std::mt19937 gen(rd());
        std::uniform_int_distribution<> d(0, 1);
        for (auto& row : grid)
            for (auto& cell : row)
                cell = d(gen) ? 1 : -1;
    }
    else
    {
        for (auto& row : grid)
            for (auto& cell : row)
                cell = -1;
    }
    return grid;
}


void run_ising(Grid& grid, double T, int steps) 
{
    int N = grid.size();
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> idx(0, N - 1);
    std::uniform_real_distribution<> prob(0.0, 1.0);

    for (int s = 0; s < steps * N * N; ++s) 
    {
        int i = idx(gen), j = idx(gen);
        int up = grid[(i - 1 + N) % N][j];
        int down = grid[(i + 1) % N][j];
        int left = grid[i][(j - 1 + N) % N];
        int right = grid[i][(j + 1) % N];
        int dE = 2 * grid[i][j] * (up + down + left + right);
        if (dE <= 0 || prob(gen) < std::exp(-dE / T)) grid[i][j] *= -1;
    }
}

void render_grid(const Grid& grid, py11::array_t<uint8_t> buffer) 
{
    auto buf = buffer.request();
    uint8_t* data = static_cast<uint8_t*>(buf.ptr);
    int N = grid.size();
    cairo_surface_t* surface = cairo_image_surface_create_for_data(data, CAIRO_FORMAT_RGB24, N, N, N * 4);
    cairo_t* cr = cairo_create(surface);

    for (int i = 0; i < N; ++i) 
    {
        for (int j = 0; j < N; ++j) 
        {
            if (grid[i][j] == 1)
                cairo_set_source_rgb(cr, 1, 0, 0); // red
            else
                cairo_set_source_rgb(cr, 0, 0, 1); // blue
            cairo_rectangle(cr, j, i, 1, 1);
            cairo_fill(cr);
        }
    }
    cairo_destroy(cr);
    cairo_surface_destroy(surface);
}

PYBIND11_MODULE(ising_module, m) 
{
    py11::class_<Grid>(m, "Grid");
    m.def("init_grid", &init_grid);
    m.def("run_ising", &run_ising);
    m.def("render_grid", &render_grid);
}
