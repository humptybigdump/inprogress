
#include <stdlib.h>
#include <math.h>
#include <vector>

#include <GL/glut.h>

#ifndef M_PI
#define M_PI		3.141592654f
#endif

#define POINT_COUNT		200
#define CONE_RADIUS		0.5f
#define CONE_STEPS		64

// Simple function to create random floating point numbers in [0, 1)
float RandomFloat() {
	return (float) rand() / (float) (RAND_MAX - 1);
}

// Simple struct for 2D vectors
struct vec2 {
	vec2() {
	}

	vec2(GLfloat k) : x(k), y(k) {
	}

	vec2(GLfloat x, GLfloat y) : x(x), y(y) {
	}

	GLfloat x, y;
};

vec2 operator*(const vec2 & a, float b) {
	return vec2(a.x * b, a.y * b);
}

vec2 operator-(const vec2 & a, const vec2 & b) {
	return vec2(a.x - b.x, a.y - b.y);
}

// Create a "random" hash value
GLuint hash(GLuint n) {
	n = (n + 0x7ed55d16) + (n << 12);
	n = (n ^ 0xc761c23c) ^ (n >> 19);
	n = (n + 0x165667b1) + (n << 5);
	n = (n + 0xd3a2646c) ^ (n << 9);
	n = (n + 0xfd7046c5) + (n << 3);
	n = (n ^ 0xb55a4f09) ^ (n >> 16);
	return n;
}

// Draws a cone centered at (x, y)
void DrawCone(float x, float y) {

	glBegin(GL_TRIANGLE_FAN);
	glVertex3f(x, y, -1.0f);
	for (int i = 0; i <= CONE_STEPS; i++) {
		float phi = 2.0f * M_PI * (float) i / (float) CONE_STEPS;
		float dx = CONE_RADIUS * cosf(phi);
		float dy = CONE_RADIUS * sinf(phi);
		glVertex3f(x + dx, y + dy, 0.0f);
	}
	glEnd();
}

// Points for tessellation
std::vector<vec2> points;

void Init() {
	// Create point data set
	for (int i = 0; i < POINT_COUNT; i++) {
		points.push_back(vec2(RandomFloat(), RandomFloat()) * 2.0f - vec2(1.0f));
	}

	glPointSize(4.0f);
}

void Exit() {
}

void Keyboard(unsigned char key, int x, int y) {
	if (key == 27) {
		exit(0);
	}
}

void Reshape(int width, int height) {
	glViewport(0, 0, width, height);
}

void Display() {
	// Clear the color and depth buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// Draw the cones
	glEnable(GL_DEPTH_TEST);
	for (int i = 0; i < (int) points.size(); i++) {
		GLuint bits = hash((GLuint) i);
		GLubyte r = (GLubyte) (bits >> 24 & 0xff);
		GLubyte g = (GLubyte) (bits >> 12 & 0xff);
		GLubyte b = (GLubyte) (bits >>  0 & 0xff);

		glColor3ub(r, g, b);

		const vec2 & p = points[i];
		DrawCone(p.x, p.y);
	}
	
	// Draw the points
	glDisable(GL_DEPTH_TEST);
	glBegin(GL_POINTS);
	glColor3f(1.0f, 1.0f, 1.0f);
	for (int i = 0; i < (int) points.size(); i++) {
		glVertex2fv((const GLfloat *) &points[i]);
	}
	glEnd();
	
	// Display the result
	glutSwapBuffers();
}

int main(int argc, char ** argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(512, 512);
	glutCreateWindow("Voronoi Tessellation in OpenGL");

	Init();

	glutKeyboardFunc(&Keyboard);
	glutReshapeFunc(&Reshape);
	glutDisplayFunc(&Display);

	atexit(&Exit);
	glutMainLoop();

	return 0;
}
