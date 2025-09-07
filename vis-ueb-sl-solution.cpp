
#include "Util.hpp"
using namespace util;
using namespace glsl;

/******************************************************************************/

#ifndef M_PI
#define M_PI		3.1415926535897932384626433832795f
#endif

// Clamped cosine
float c(float x) {
	return util::glsl::abs(x) <= 0.5f * M_PI ? cosf(x) : 0.0f;
}

// Vector field from "Time-Dependent 2-D Vector Field Topology: An Approach Inspired by Lagrangian Coherent Structures" by Sadlo & Weiskopf
vec2 v2(float x, float y, float t) {
	//static const float a = 0.4f;
	t *= 0.1f;

	float a = sinf(2.0f * M_PI * t) / 3.0f;

	float p = M_PI;
	float px = p * x;
	float py = p * y;
	if (-0.5f <= x && x <= 0.5f && -0.5f <= y && y <= 0.5f) {
		float cpx = cosf(px);
		float spx = sinf(px);
		float cpy = cosf(py);
		float spy = sinf(py);

		return vec2(
			-spx * cpy + a * spy * cpx, 
			+spy * cpx - a * spx * cpy);
	} else {
		float k = (y >= util::glsl::abs(x) ? 1.0f : 0.0f) - (y <= -util::glsl::abs(x) ? 1.0f : 0.0f);
		float l = (x >  util::glsl::abs(y) ? 1.0f : 0.0f) - (x <  -util::glsl::abs(y) ? 1.0f : 0.0f);

		return vec2(
			k * a * c(px - a * p * (y - 0.5f * k)) - l * c(py - a * p * (x - 0.5f * l)), 
			k * c(px - a * p * (y - 0.5f * k)) - l * a * c(py - a * p * (x - 0.5f * l)));
	}
}

vec2 v1(float x, float y, float t) {
	// Vector field from lecture slides
	x *= 2.0f;
	y *= 2.0f;

	//x += sinf(t);
	//y += cosf(t);

	vec2 v_ = vec2(
		(x - 0.5f) * x + (y - 0.5f) * y,
		0.5f * (x - y));

	v_ *= map(sinf(t), -1, 1, 0.5f, 1.8f);

	return v_;
}

/******************************************************************************/

enum {
	INTEGRATOR_EULER,
	INTEGRATOR_MIDPOINT,
	INTEGRATOR_RK4,
	INTEGRATOR_COUNT,
};

enum {
	FIELD_ONE,
	FIELD_TWO,
	FIELD_MIX,
	FIELD_COUNT,
};

#define MAX_PARTICLES		100
#define MAX_STREAM_LINES	100

vec2 streamLines[MAX_STREAM_LINES][MAX_PARTICLES];
vec2 seedPos[MAX_STREAM_LINES];

int particleCount   = MAX_PARTICLES;
int particleCounts[MAX_STREAM_LINES];

int streamLineCount = 0;

int integrator = INTEGRATOR_EULER;
int field      = FIELD_ONE;

// Integration interval, i.e. temporal distance between first and last particle 
// in a stream line
float intInt = 1.0f;

// Screen size
int width, height;

// Pause the animation?
bool paused = true;

// Display hedgehogs?
bool hedgehogs = false;

// Step size doubling?
bool doubling = false;

// Squared error for step size doubling
float sqrErr = 0.01f;

float timeValue = 0.0f;

/******************************************************************************/

// Analytic vector field
vec2 v(float x, float y, float t) {
	if (field == FIELD_ONE) {
		return v1(x, y, t);
	} else if (field == FIELD_TWO) {
		return v2(x, y, t);
	} else {
		return mix(v1(x, y, cosf(t)), v2(x, y, t), vec2(cos(t), sin(t)));
	}
}

inline 
vec2 v(const vec2 & r, float t) {
	return v(r.x, r.y, t);
}

/******************************************************************************/

float length_sqr(const vec2 & a) {
	return dot(a, a);
}

float distance_sqr(const vec2 & a, const vec2 & b) {
	return length_sqr(a - b);
}

/******************************************************************************/

vec2 EulerStep(const vec2 & r, float t, float dt) {
	// TODO: Do an Euler integration step
	//return  ...;
//SNIP
#if 1
	// Explicit Euler forward integration
	return dt * v(r, t);
#endif
//SNAP
	return vec2(0);
}

vec2 MidpointStep(const vec2 & r, float t, float dt) {
	// TODO: Do a midpoint method integration step
	//return  ...;
//SNIP
#if 1
	// Midpoint method
	vec2 dr = dt * v(r, t);

	return dt * v(r + 0.5f * dr, t + 0.5f * dt);
#endif
//SNAP
	return vec2(0);
}

vec2 RungeKutta4Step(const vec2 & r, float t, float dt) {
	// TODO: Do a fourth-order Runge-Kutta integration step
	//return  ...;
//SNIP
#if 1
	// 4th-order Runge-Kutta method
	vec2 k1  = dt * v(r,             t            );
	vec2 k2  = dt * v(r + 0.5f * k1, t + 0.5f * dt);
	vec2 k3  = dt * v(r + 0.5f * k2, t + 0.5f * dt);
	vec2 k4  = dt * v(r +        k3, t + dt);
	return (k1 + k4) / 6.0f + (k2 + k3) / 3.0f;
#endif
//SNAP
	return vec2(0);
}

// Compute one numerical intergration step in the time interval [t0, t0 + dt]
vec2 Step(const vec2 & r, float t0, float dt) {
	if (integrator == INTEGRATOR_EULER) {
		return EulerStep(r, t0, dt);
	} else if (integrator == INTEGRATOR_MIDPOINT) {
		return MidpointStep(r, t0, dt);
	} else if (integrator == INTEGRATOR_RK4) {
		return RungeKutta4Step(r, t0, dt);
	}
	return vec2(0);
}

// Compute one adaptive integration step with stepsize doubling
vec2 AdaptiveStep(const vec2 & r, float t0, float dt) {
//SNIP
#if 1
	// Full step
	vec2 r1 = Step(r, t0, dt);
    vec2 r2 = vec2(0);

    for(int steps=2; steps <= (1<<12); steps*=2)
    {
        r2 = vec2(0);
        // Smaller steps
        for(int j=0; j < steps; j++)
            r2 += Step(r + r2, t0 + j * dt/steps, dt/steps);

	    // Check error 
	    if(distance_sqr(r1, r2) < sqrErr)
		    return r2; 

        // error is still too high: use double the steps in next run
        r1 = r2;  
    }	
    return r2;




/*  // Recursive solution:
    // Full step
	vec2 r1 = Step(r, t0, dt);
	
	// Two half steps
	vec2 r2_1 = Step(r, t0, 0.5f * dt);
	vec2 r2_2 = Step(r + r2_1, t0 + 0.5f * dt, 0.5f * dt);
	vec2 r2 = r2_1 + r2_2;

	// Check error 
	if(dt < sqrErr/2.f || distance_sqr(r1, r2) < sqrErr)
		return r2;
	
	else {

		vec2 ra1 = AdaptiveStep(r, t0, 0.5f * dt);
		vec2 ra2 = AdaptiveStep(r + ra1, t0 + 0.5f * dt, 0.5f * dt);

		return ra1 + ra2;
	}
*/
#endif
//SNAP
	// TODO: Implement stepsize doubling here
	// return ...;
	return Step(r, t0, dt);
}

void DoParticleTracing(float t0) {
	// For each stream line
	for (int i = 0; i < streamLineCount; i++) {
		// Fetch the start position
		vec2 r = seedPos[i];

		// Compute the start time
		float t = t0;

		// Compute the time step
		float dt = intInt / particleCount;

		// Iterate over all particles in this stream line
		for (int j = 0; j < particleCount; j++) {
			// Store previous position
			streamLines[i][j] = r;

			if (doubling) {
				r += AdaptiveStep(r, t, dt);
			} else {
				r += Step(r, t, dt);
			}

			t += dt;
		}
	}
}

/******************************************************************************/

void Keyboard(unsigned char key, int x, int y) {
	// Let AntTweakBar preempt keyboard events
	if (TwEventKeyboardGLUT(key, x, y)) {
		return;
	}

	// Exit on escape
	if (key == 27) {
		exit(0);
		return;
	}
}

void Special(int key, int x, int y) {
	// Let AntTweakBar preempt keyboard events
	if (TwEventSpecialGLUT(key, x, y)) {
		return;
	}

	// Reload shaders with F5
	if (key == GLUT_KEY_F5) {
		//LoadShaders();
	}
}

void Mouse(int button, int state, int x, int y) {
	// Let AntTweakBar preempt mouse button events
	if (TwEventMouseButtonGLUT(button, state, x, y)) {
		return;
	}

	if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {
		GLint vp[4];
		glGetIntegerv(GL_VIEWPORT, vp);
		GLdouble M[16], P[16];
		glGetDoublev(GL_MODELVIEW_MATRIX, M);
		glGetDoublev(GL_PROJECTION_MATRIX, P);
		GLdouble dx, dy, dz;
		gluUnProject(x, ::height - 1 - y, 0, M, P, vp, &dx, &dy, &dz);

		if (dx > -1 && dx < 1 && dy > -1 && dy < 1) {
			if (streamLineCount < MAX_STREAM_LINES) {
				seedPos[streamLineCount].x = (float) dx;
				seedPos[streamLineCount].y = (float) dy;
				streamLineCount++;
			} else {
				streamLineCount = 0;
			}
		}
	}

	if (button == GLUT_RIGHT_BUTTON && state == GLUT_DOWN) {
		streamLineCount = 0;
	}
}

void Motion(int x, int y) {
	// Let AntTweakBar preempt mouse motion events
	if (TwEventMouseMotionGLUT(x, y)) {
		return;
	}
}

namespace atb {
	// Utility funcition to add printf-style arguments to definitions
	int TwAddVarRW(TwBar *bar, const char *name, TwType type, void *var, const char *fmt, ...) {
		if (fmt) {
		char def [4086];
		va_list ap;
		va_start(ap, fmt);
		vsprintf(def, fmt, ap);
		va_end(ap);
			return ::TwAddVarRW(bar, name, type, var, def);
		} else {
			return ::TwAddVarRW(bar, name, type, var, NULL);
		}
	}
}

void Init() {
	// Initialize AntTweakBar GUI
	TwInit(TW_OPENGL, NULL);

	TwBar * bar = TwNewBar("Settings");

	TwEnumVal fieldEnum[FIELD_COUNT] = {
		{ FIELD_ONE, "# 1" }, 
		{ FIELD_TWO, "# 2" }, 
		{ FIELD_MIX, "Mix" }, 
	};
	TwType fieldType = TwDefineEnum("FIELD_TYPE", fieldEnum, FIELD_COUNT);
	TwAddVarRW(bar, "Field", fieldType,  &field, "keyincr=f keydecr=F");
	TwAddSeparator(bar, NULL, NULL);

	TwEnumVal intEnum[INTEGRATOR_COUNT] = {
		{ INTEGRATOR_EULER,    "Explicit Euler"        }, 
		{ INTEGRATOR_MIDPOINT, "Midpoint Method"       }, 
		{ INTEGRATOR_RK4,      "4th Order Runge-Kutta" }, 
	};
	TwType intType = TwDefineEnum("INTEGRATOR_TYPE", intEnum, INTEGRATOR_COUNT);
	atb::TwAddVarRW(bar, "# Particles", TW_TYPE_INT32,   &particleCount, "min=1 max=%d", MAX_PARTICLES);
	TwAddSeparator(bar, NULL, NULL);
	TwAddVarRW(bar, "Integrator",           intType,         &integrator, "keyincr=i keydecr=I");
	TwAddVarRW(bar, "Integration Interval", TW_TYPE_FLOAT,   &intInt,     "min=0 step=0.001");
	TwAddSeparator(bar, NULL, NULL);
	TwAddVarRW(bar, "Stepsize Doubling",    TW_TYPE_BOOLCPP, &doubling,   "key=d");
	TwAddVarRW(bar, "Max Squared Error",    TW_TYPE_FLOAT,   &sqrErr,     "min=0 step=0.00001");
	TwAddSeparator(bar, NULL, NULL);
	TwAddVarRW(bar, "Hedgehogs",            TW_TYPE_BOOLCPP, &hedgehogs,  "key=h");
	TwAddVarRW(bar, "Pause Animation",      TW_TYPE_BOOLCPP, &paused,     "key=space");

	// Load the shader program(s)
	//LoadShaders();

	glPointSize(8.0f);
}

void Exit() {
	// Shut down AntTweakBar
	//TwTerminate();

	// Delete shader programs
	//KillShaders();
}

void Reshape(int width, int height) {
	// Update AntTweakBar window size
	TwWindowSize(width, height);

	::width = width;
	::height = height;

	// Set up OpenGL matrices
	{
		glMatrixMode(GL_PROJECTION);
		glLoadIdentity();

		// Make sure we always see the [-1, 1]^2 domain
		glMatrixMode(GL_MODELVIEW);
		glLoadIdentity();
		if (width > height) {
			glScalef((float) height / (float) width, 1.0f, 1.0f);
		} else {
			glScalef(1.0f, (float) width / (float) height, 1.0f);
		}
	}

	// Update viewport
	glViewport(0, 0, width, height);
}

void Display() {
	// Clear the buffers
	glClear(GL_COLOR_BUFFER_BIT);

	// Draw the vector field domain
	glBegin(GL_LINE_LOOP);
	glColor3f(1, 1, 1);
	glVertex2f(-1.0f, -1.0f);
	glVertex2f(+1.0f, -1.0f);
	glVertex2f(+1.0f, +1.0f);
	glVertex2f(-1.0f, +1.0f);
	glEnd();

	// Draw the stream lines
	for (int i = 0; i < streamLineCount; i++) {
		
		glBegin(GL_LINE_STRIP);
		for (int j = 0; j < particleCount; j++) {
			float u = (float) j / (float) (particleCount - 1);
			glColor3f(u, 1 - u, 0);
			glVertex2fv(streamLines[i][j]);
		}
		glEnd();
	}

	// Draw the vectors
	if (hedgehogs) {
		glBegin(GL_LINES);
		glColor3f(1, 1, 0);
		for (int j = 0; j < 40; j++) {
			for (int i = 0; i < 40; i++) {
				vec2 p = map(vec2(i + 0.5, j + 0.5), vec2(0), vec2(40), vec2(-1), vec2(1));
				vec2 v = ::v(p.x, p.y, timeValue);
				glVertex2fv(p);
				glVertex2fv(p + v * 0.01f);
			}
		}
		glEnd();
	}

	// Draw the GUI
	TwDraw();

	// Show the image
	glutSwapBuffers();
}

void Idle() {
	// Draw a new frame
	glutPostRedisplay();

	// Update elapsed time
	if (!paused) {
		timeValue = (float) glutGet(GLUT_ELAPSED_TIME) / 1000.0f;
	}

	// Do the particle tracing
	DoParticleTracing(timeValue);
}

int main(int argc, char ** argv) {
	// Initialize GLUT and create a window
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE);
	glutInitWindowSize(1024, 1024);
	glutCreateWindow("Interactive Stream Lines");

	// Initialize GLEW
	glewInit();

	// Call the user init callback
	Init();

	// Set up GLUT callbacks
	glutKeyboardFunc(&Keyboard);
	glutSpecialFunc(&Special);
	glutMouseFunc(&Mouse);
	glutMotionFunc(&Motion);
	glutPassiveMotionFunc(&Motion);
	glutReshapeFunc(&Reshape);
	glutDisplayFunc(&Display);
	glutIdleFunc(&Idle);

	// Register exit callback and run the main loop
	atexit(&Exit);
	glutMainLoop();

	return 0;
}
