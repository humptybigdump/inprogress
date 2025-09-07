#include <stdlib.h>
#include <cstdio>
#include <vector>
#include <cassert>
#include <GL/glut.h>
#include <algorithm>

#include "GLSL.hpp"

using namespace std;

/** Uniform grid **/
struct Grid
{
    /** Returns the scalar value in cell (x, y).
     * x and y must be integers in [0, width) and [0, height)
     */
    float getCell(int x, int y) const {
        assert(x < width&& y < height);

        return scalarField[y * width + x];
    }

    int width;
    int height;

    vector<float> scalarField;
};

/** Contains scattered positions and values */
struct ScatteredData
{
    vector<glsl::vec2> positions;
    vector<float> values;
};

/** Interpolates at point (x, y), where x and y are in [0, width) and [0, height), respectively **/
float InterpolateBilinear(const Grid& grid, float x, float y) {
    //TODO implement bilinear interpolation

    x -= 0.5f;
    y -= 0.5f;

    int x_low = max(static_cast<int>(floor(x)), 0);
    int x_high = min(x_low + 1, grid.width - 1);
    int y_low = max(static_cast<int>(floor(y)), 0);
    int y_high = min(y_low + 1, grid.height - 1);

    float v00 = grid.getCell(x_low, y_low);
    float v10 = grid.getCell(x_high, y_low);
    float v01 = grid.getCell(x_low, y_high);
    float v11 = grid.getCell(x_high, y_high);

    float xt = x - static_cast<float>(x_low);
    float yt = y - static_cast<float>(y_low);

    return v00 * (1.f - xt) * (1.f - yt) + v01 * (1.f - xt) * yt + v10 * xt * (1.f - yt) + v11 * xt * yt;
}

/** Interpolates at point (x, y), where x and y are in [0, width] and [0, height], respectively **/
float InterpolateShepard(const ScatteredData& sdata, float x, float y) {
    //TODO implement Shepard interpolation

    float value = 0.0f;
    float wsum = 0.0f;

    float p = 3.f;  // low: global influence, high: local influence

    glsl::vec2 pt(x, y);

    for (int i = 0; i < sdata.values.size(); ++i)
    {
        float dist = sqrt(glsl::dot(pt - sdata.positions[i], pt - sdata.positions[i]));

        float w;
        if (dist == 0.0f)
            return sdata.values[i];
        else
            w = 1.0f / pow(dist, p);

        value += w * sdata.values[i];
        wsum += w;
    }

    return value / wsum;
}

/** Initializes the scalar field. Feel free to change the values! */
void InitScalarField(Grid& g, ScatteredData& s) {
    g.width = 4;
    g.height = 4;
    g.scalarField.resize(g.width * g.height);

    // 1st row
    g.scalarField[0] = 0.75f;
    g.scalarField[1] = 0.75f;
    g.scalarField[2] = 0.75f;
    g.scalarField[3] = 0.75f;

    // 2nd row
    g.scalarField[4] = 0.0f;
    g.scalarField[5] = 0.0f;
    g.scalarField[6] = 0.0f;
    g.scalarField[7] = 0.0f;

    // 3rd row
    g.scalarField[8] = 0.0f;
    g.scalarField[9] = 0.f;
    g.scalarField[10] = 0.f;
    g.scalarField[11] = 0.0f;

    // 4th row
    g.scalarField[12] = 1.0f;
    g.scalarField[13] = 1.0f;
    g.scalarField[14] = 1.0f;
    g.scalarField[15] = 1.0f;

    // Init scattered data
    s.values = g.scalarField;

    // Convert grid to scattered data representation
    for (int y = 0; y < g.height; ++y)
    {
        for (int x = 0; x < g.width; ++x)
        {
            s.positions.push_back(glsl::vec2(x + 0.5f, y + 0.5f));
        }
    }
}

// Global variables
bool g_ShowBilinear = true;
GLuint g_Tex;

int texWidth = 128;
int texHeight = 128;

// Create an OpenGL texture
void InitTexture(const vector<float>& scalarField, int w, int h) {
    glGenTextures(1, &g_Tex);
    glBindTexture(GL_TEXTURE_2D, g_Tex);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE, w, h, 0, GL_LUMINANCE, GL_FLOAT, scalarField.data());
    glBindTexture(GL_TEXTURE_2D, 0);
}

// Creates an OpenGL texture by calling the bilinear or Shepard interpolation functions
vector<float> Interpolate() {
    Grid g;
    ScatteredData s;
    InitScalarField(g, s);

    vector<float> texture;

    // Interpolate values to put them in a texture for display
    for (int yi = 0; yi < texHeight; ++yi)
    {
        for (int xi = 0; xi < texWidth; ++xi)
        {
            float x = xi / static_cast<float>(texWidth) * g.width;
            float y = yi / static_cast<float>(texHeight) * g.height;

            if (g_ShowBilinear)
                texture.push_back(InterpolateBilinear(g, x, y));
            else
                texture.push_back(InterpolateShepard(s, x, y));
        }
    }
    return texture;
}

void Exit() {
}

void Keyboard(unsigned char key, int x, int y) {
    if (key == 27) {
        exit(0);
    }
    else
    {
        // If any key other than the ESC key is pressed, toggle
        // display between bilinear and shepard interpolation
        g_ShowBilinear = !g_ShowBilinear;

        glDeleteTextures(1, &g_Tex);
        InitTexture(Interpolate(), texWidth, texHeight);

        glutPostRedisplay();
    }

}

void Reshape(int width, int height) {
    glViewport(0, 0, width, height);
}

void Display() {
    // Clear the color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT);

    glMatrixMode(GL_PROJECTION);

    glBindTexture(GL_TEXTURE_2D, g_Tex);
    glEnable(GL_TEXTURE_2D);
    glBegin(GL_QUADS);
    glTexCoord2i(0, 0); glVertex2f(-1, -1);
    glTexCoord2i(0, 1); glVertex2f(-1, 1);
    glTexCoord2i(1, 1); glVertex2f(1, 1);
    glTexCoord2i(1, 0); glVertex2f(1, -1);
    glEnd();
    glDisable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, 0);

    // Display the result
    glutSwapBuffers();
}

int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE);
    glutInitWindowSize(512, 512);
    glutCreateWindow("Interpolation");

    InitTexture(Interpolate(), texWidth, texHeight);

    glutKeyboardFunc(&Keyboard);
    glutReshapeFunc(&Reshape);
    glutDisplayFunc(&Display);

    atexit(&Exit);
    glutMainLoop();

    return 0;
}
