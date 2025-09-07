#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include <GL/glut.h>

/******************************************************************************/

// Simple vector library
namespace glsl {

struct vec2 {
	vec2() {
	}

	vec2(float x, float y) : x(x), y(y) {
	}

	float x, y;
};

float mix(float a, float b, float t) {
	return a + (b - a) * t;
}

float distance(const vec2 & a, const vec2 & b) {
	float dx = a.x - b.x;
	float dy = a.y - b.y;
	return sqrtf(dx * dx + dy * dy);
}

}

/******************************************************************************/

using namespace glsl;

// Number of polynom bases in x/y direction
#define NUM_POLYS_X				1
#define NUM_POLYS_Y				1

// Number of data points
#define NUM_SAMPLES				30

// RBF kernel support divisor
#define RBF_SUPPORT				1.f

// Number of subdivisions along heightfield (display only)
#define DISPLAY_DIV_X			16
#define DISPLAY_DIV_Y			16

/******************************************************************************/

// Solve a linear system A x = b
// NOTE: This will destroy the inputs and return the result in vector b!
// Based on Eric Lengyel's version in 'Mathematics for 3D Game Programming and Computer Graphics'

#define SOLVE_LINEAR_SYSTEM_EPSILON			1e-9f

int SolveLinearSystem(int N, float * A, float * b) {
	int result = 0;

	// Compute a normalization value for each row
	float * scalers = new float [N];
	// For each row...
	for (int i = 0; i < N; i++) {
		// ...find entry with maximal magnitude
		float maxMag = fabsf(A[i * N]);
		for (int j = 1; j < N; j++) {
			float newMag = fabsf(A[i * N + j]);
			if (newMag > maxMag) {
				maxMag = newMag;
			}
		}

		// Check for singularity
		if (maxMag < SOLVE_LINEAR_SYSTEM_EPSILON) {
			result = 0;
			goto end;
		}

		// Store normalization value
		scalers[i] = 1.0f / maxMag;
	}

	// Perform elimination
	for (int j = 0; j < N - 1; j++) {
		// Find pivot element
		int i_pivot = -1;
		float maxMag = SOLVE_LINEAR_SYSTEM_EPSILON;
		for (int i = j; i < N; i++) {
			float newMag = fabsf(A[i * N + j]) * scalers[i];
			if (newMag > maxMag) {
				maxMag = newMag;
				i_pivot = i;
			}
		}

		if (i_pivot != j) {
			// Check for singularity
			if (i_pivot == -1) {
				result = 0;
				goto end;
			}

			// Swap rows j and i_pivot
			for (int k = 0; k < N; k++) {
				float temp = A[i_pivot * N + k];
				A[i_pivot * N + k] = A[j * N + k];
				A[j * N + k] = temp;
			}

			float temp = b[i_pivot];
			b[i_pivot] = b[j];
			b[j] = temp;

			scalers[i_pivot] = scalers[j];
		}

		float denom = 1.0f / A[j * N + j];
		for (int i = j + 1; i < N; i++) {
			float factor = A[i * N + j] * denom;
			b[i] -= b[j] * factor;
			for (int k = 0; k < N; k++) {
				A[i * N + k] -= A[j * N + k] * factor;
			}
		}
	}

	// Perform backward substitution
	for (int i = N - 1; i >= 0; i--) {
		float sum = b[i];
		for (int k = i + 1; k < N; k++) {
			sum -= A[i * N + k] * b[k];
		}
		b[i] = sum / A[i * N + i];
	}
	result = 1;

end:
	delete [] scalers;

	return result;
}

// Return a random float value in [0, 1)
float RandomFloat() {
	return (float) rand() / (float) (RAND_MAX - 1);
}

/******************************************************************************/

// Sample positions
vec2 sample_positions[NUM_SAMPLES];

// Sample values
float sample_values[NUM_SAMPLES];

// RBF kernel
float phi(float r) {
	return expf(-(r * RBF_SUPPORT) * (r * RBF_SUPPORT));
}

// Polynomial basis
float p(int m, int n, const vec2 & pos) {
	// We just use the monomial basis
	return powf(pos.x, (float) m) * powf(pos.y, (float) n);
}

// RBF_WEIGHTS
float lambda[NUM_SAMPLES];

// Polynomial basis weights
#if NUM_POLYS_X * NUM_POLYS_Y == 0
float * c = new float [NUM_POLYS_X * NUM_POLYS_Y];
#else
float c[NUM_POLYS_X * NUM_POLYS_Y];
#endif

/******************************************************************************/

// Evaluate the input heightfield/patch patch
float Exact(const vec2 & pos) {
	// Assume there's a bilinear heightfield patch
	static const float _v[2][2] = {
		//{ 1.2f, 0.5f },
		//{ 1.1f, 1.4f },
		{ +0.2f, +0.0f },
		{ -0.6f, +1.1f },
	};

	// Compute patch parameters
	float u = (pos.x + 1.0f) / 2.0f;
	float v = (pos.y + 1.0f) / 2.0f;

	// Bilinear interpolation
	return mix(mix(_v[0][0], _v[1][0], u), mix(_v[0][1], _v[1][1], u), v);
}

// Evaluate the RBF/polynomial function (see lecture slides)
float Interpolate(const vec2 & pos) {
	float sum = 0.0f;

	// Add polynomial contribution
	for (int n = 0; n < NUM_POLYS_Y; n++) {
		for (int m = 0; m < NUM_POLYS_X; m++) {
			sum += c[m + NUM_POLYS_X * n] * p(m, n, pos);
		}
	}

	// Add RBF contribution
	for (int i = 0; i < NUM_SAMPLES; i++) {
		float r = distance(sample_positions[i], pos);
		sum += lambda[i] * phi(r);
	}

	return sum;
}

// Generate the data set we later want to interpolate with RBFs
void GenerateSamples() {
	// Sample the bilinear patch
	for (int i = 0; i < NUM_SAMPLES; i++) {
		// Sample [0, 1] x [0, 1]
		float u = RandomFloat();
		float v = RandomFloat();

		// Compute the sample position
		sample_positions[i].x = 2.0f * u - 1.0f;
		sample_positions[i].y = 2.0f * v - 1.0f;

		// Compute the value
		sample_values[i] = Exact(sample_positions[i]);
	}
}

// Compute the RBF/polynomial weights from the given samples
void ComputeWeights() {
	// Compute RGB weights
	for (int i = 0; i < NUM_SAMPLES; i++) {
		lambda[i] = 0.0f;
	}

	// Compute polynomial weights
	for (int i = 0; i < NUM_POLYS_X * NUM_POLYS_Y; i++) {
		c[i] = 0.0f;
	}

	// TODO: Create linear system...
	int N = NUM_SAMPLES + (NUM_POLYS_X * NUM_POLYS_Y);
	float * A = new float [N * N];
	float * b = new float [N];
	// ...

	// Top-left block of A contains kernel of sample pairs
	for (int i = 0; i < NUM_SAMPLES; i++) {
		for (int j = 0; j < NUM_SAMPLES; j++) {
			const vec2 & si = sample_positions[i];
			const vec2 & sj = sample_positions[j];
			A[i + N * j] = phi(distance(si, sj));
		}
	}

	// Top-right/bottom-left blocks contain polynomials
	for (int i = 0; i < NUM_SAMPLES; i++) {
		for (int j = NUM_SAMPLES; j < N; j++) {
			// Figure out polynomial degrees
			int m = (j - NUM_SAMPLES) % NUM_POLYS_X;
			int n = (j - NUM_SAMPLES) / NUM_POLYS_X;

			// Evaluate polynomial
			const vec2 & si = sample_positions[i];
			float pj = p(m, n, si);

			// Store symmetric matrix entries
			A[i + N * j] = A[j + N * i] = pj;
		}
	}

	// Bottom-right block of A contains zeros
	for (int i = NUM_SAMPLES; i < N; i++) {
		for (int j = NUM_SAMPLES; j < N; j++) {
			A[i + N * j] = 0.0f;
		}
	}

	// Top part of b contains function values
	for (int i = 0; i < NUM_SAMPLES; i++) {
		float vi = sample_values[i];
		b[i] = vi;
	}

	// Bottom part of b contains zeros
	for (int i = NUM_SAMPLES; i < N; i++) {
		b[i] = 0.0f;
	}

	// Solve the system
	if (!SolveLinearSystem(N, A, b)) {
		fprintf(stderr, "Error: system is singular!\n");
		exit(1);
	}

	// Write back the results...

	// Top part of x contains RBF coefficients
	for (int i = 0; i < NUM_SAMPLES; i++) {
		lambda[i] = b[i];
	}

	// Bottom part contains polynomial coefficients
	for (int i = NUM_SAMPLES; i < N; i++) {
		c[i - NUM_SAMPLES] = b[i];
	}

	// Clean up
	delete [] A;
	delete [] b;
}

/******************************************************************************/

// Mouse position
int mx = 0, my = 0;
int dx = 0, dy = 0;
int rotating = 0;
int dollying = 0;

// Camera
float pitch = 30.0f, yaw = 60.0f, dist = 5.0f;

void Mouse(int button, int state, int x, int y) {
	if (button == GLUT_LEFT_BUTTON) {
		rotating = state == GLUT_DOWN;
	}
	if (button == GLUT_RIGHT_BUTTON) {
		dollying = state == GLUT_DOWN;
	}

	mx = x;
	my = y;
}

void Motion(int x, int y) {
	// Compute delta movement
	dx = x - mx;
	dy = y - my;

	// Update mouse position
	mx = x;
	my = y;
}

void Keyboard(unsigned char key, int x, int y) {
	if (key == 27) {
		exit(0);
	}
}

void Init() {
	// Generate samples on the heightfield
	GenerateSamples();

	// Compute the RBF weights
	ComputeWeights();

	// Initialize OpenGL state
	glEnable(GL_DEPTH_TEST);
	glPointSize(5.0f);

	glEnable(GL_POINT_SMOOTH);
	glHint(GL_POINT_SMOOTH_HINT, GL_NICEST);

	glEnable(GL_LINE_SMOOTH);
	glHint(GL_LINE_SMOOTH_HINT, GL_NICEST);

	glEnable(GL_BLEND);
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
}

void Exit() {
}

void Idle() {
	// Compute time elapsed since last frame
	static float t0 = (float) glutGet(GLUT_ELAPSED_TIME) * 0.001f;
	float t1 = (float) glutGet(GLUT_ELAPSED_TIME) * 0.001f;
	float dt = t1 = t0;
	t0 = t1;

	// Update the camera
	int w = glutGet(GLUT_WINDOW_WIDTH);
	int h = glutGet(GLUT_WINDOW_HEIGHT);

	float fdx = (float) dx / (float) w;
	float fdy = (float) dy / (float) h;

	if (rotating) {
		pitch += 0.1f * 360.0f * fdy * dt;
		yaw   += 0.1f * 360.0f * fdx * dt;
	}

	if (dollying) {
		dist -= 0.1f * 3.0f * fdy * dt;
	}

	glutPostRedisplay();
}

void Reshape(int width, int height) {
	glViewport(0, 0, width, height);

	float aspect = (float) width / (float) height;

	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(60.0f, aspect, 0.001f, 100.0f);
}

void DrawFunction(int W, int H, float (* eval)(const vec2 &)) {
	for (int i = 0; i <= W; i++) {
		glBegin(GL_LINE_STRIP);
		for (int j = 0; j <= H; j++) {
			vec2 pos;
			pos.x = 2.0f * (float) ((float) i / (float) W) - 1.0f;
			pos.y = 2.0f * (float) ((float) j / (float) H) - 1.0f;
			glVertex3f(pos.x, eval(pos), -pos.y);
		}
		glEnd();
	}
	for (int j = 0; j <= H; j++) {
		glBegin(GL_LINE_STRIP);
		for (int i = 0; i <= W; i++) {
			vec2 pos;
			pos.x = 2.0f * (float) ((float) i / (float) W) - 1.0f;
			pos.y = 2.0f * (float) ((float) j / (float) H) - 1.0f;
			glVertex3f(pos.x, eval(pos), -pos.y);
		}
		glEnd();
	}
}

void Display() {
	// Clear the color and depth buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// Set the modelview matrix
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
	glTranslatef(0.0f, 0.0f, -dist);
	glRotatef(pitch, 1.0f, 0.0f, 0.0f);
	glRotatef(yaw, 0.0f, 1.0f, 0.0f);

#if 0
	// Display the patch domain
	glBegin(GL_LINE_LOOP);
	glColor3ub(16, 91, 99);
	glVertex3f(-1.0f, 0.0f, -1.0f);
	glVertex3f(-1.0f, 0.0f, +1.0f);
	glVertex3f(+1.0f, 0.0f, +1.0f);
	glVertex3f(+1.0f, 0.0f, -1.0f);
	glEnd();
#endif

	// Display the source function/heightfield
	glLineWidth(1.0f);
	glColor3ub(189, 73, 50);
	DrawFunction(DISPLAY_DIV_X, DISPLAY_DIV_Y, Exact);

#if 1
	// Display the samples
	glBegin(GL_POINTS);
	glColor3ub(255, 250, 213);
	for (int i = 0; i < NUM_SAMPLES; i++) {
		glVertex3f(sample_positions[i].x, sample_values[i], -sample_positions[i].y);
	}
	glEnd();
#endif

	// Display the interpolated function
	glLineWidth(1.0f);
	glColor3ub(255, 211, 73);
	DrawFunction(DISPLAY_DIV_X, DISPLAY_DIV_Y, Interpolate);

#if 1
	// Draw the axes
	glLineWidth(1.5f);
	glBegin(GL_LINES);
	glColor3f(1.0f, 0.0f, 0.0f); glVertex3f(0.0f, 0.0f, 0.0f); glVertex3f(+1.0f, 0.0f, 0.0f);
	glColor3f(0.0f, 1.0f, 0.0f); glVertex3f(0.0f, 0.0f, 0.0f); glVertex3f(0.0f, 0.0f, -1.0f);
	glColor3f(0.0f, 0.0f, 1.0f); glVertex3f(0.0f, 0.0f, 0.0f); glVertex3f(0.0f, 1.0f, 0.0f);
	glEnd();
#endif

	// Display the result
	glutSwapBuffers();
}

// The main function
int main(int argc, char ** argv) {
	// Initialize GLUT
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH);
	glutInitWindowSize(512, 512);
	glutCreateWindow("Radial Basis Function Interpolation");

	Init();

	glutIdleFunc(&Idle);
	glutMouseFunc(&Mouse);
	glutMotionFunc(&Motion);
	glutPassiveMotionFunc(&Motion);
	glutKeyboardFunc(&Keyboard);
	glutReshapeFunc(&Reshape);
	glutDisplayFunc(&Display);

	atexit(&Exit);
	glutMainLoop();

	return 0;
}
