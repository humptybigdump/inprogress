
#include "Util.hpp"
using namespace util;
using namespace glsl;
#define BUFFER_OFFSET	UTIL_GL_BUFFER_OFFSET

#ifndef M_PI
#define M_PI		3.1415926535897932384626433832795f
#endif

/******************************************************************************/

template <typename T>
class Column {
public:
	inline Column(int i, int width, T * pixels) : i(i), width(width), pixels(pixels) {
	}

	inline const T & operator[](int j) const {
		return pixels[i + width * j];
	}

	inline T & operator[](int j) {
		return pixels[i + width * j];
	}

private:
	int i;
	int width;
	T * pixels;
};

template <typename T>
class Image {
public:
	Image() : width(0), height(0), pixels(0) {
	}

	Image(int width, int height) : width(width), height(height), pixels(new T [width * height]) {
	}

	Image(const Image & other) : width(other.width), height(other.height), pixels(new T [width * height]) {
		for (int k = 0; k < width * height; k++) {
			pixels[k] = other.pixels[k];
		}
	}

	~Image() {
		delete [] pixels;
	}

	Image & operator=(const Image & other) {
		if (&other != this) {
			delete [] pixels;
			width  = other.width;
			height = other.height;
			pixels = new T [width * height];
			for (int k = 0; k < width * height; k++) {
				pixels[k] = other.pixels[k];
			}
		}
		return *this;
	}

	inline const Column<T> operator[](int i) const {
		return Column<T>(i, width, pixels);
	}

	inline Column<T> operator[](int i) {
		return Column<T>(i, width, pixels);
	}

	int width;
	int height;
	T * pixels;
};


class ScalarField2D {

public:
	ScalarField2D() : width(0), height(0), field(NULL) {
	}

	float evaluate(float x, float y) {

		if(x < -1.0f || x > 1.0f || y < -1.0f || y > 1.0f)
			return 0.0f;

		float ox = (x - (-1.0f)) / 2.0f;
		float oy = (y - (-1.0f)) / 2.0f;

		float vx = ox * width - 0.5f;
		float vy = oy * width - 0.5f;

		int ix = (int)floorf(vx);
		int iy = (int)floorf(vy);

		float dx = vx - ix;
		float dy = vy - iy;

		float v00 = getScalar(ix  , iy  );
		float v01 = getScalar(ix+1, iy  );
		float v10 = getScalar(ix  , iy+1);
		float v11 = getScalar(ix+1, iy+1);

		return Bilerp(dx, dy, v00, v01, v10, v11);
	}

	bool load(std::string filename) {

		FILE *fp;
		fp = fopen(filename.c_str(), "rb");

		if(fp != NULL) {

			fread(&width, sizeof(int), 1, fp);
			fread(&height, sizeof(int), 1, fp);

			if(field)
				delete [] field;
			field = new float[width*height];

			fread(field, sizeof(float), width*height, fp);
			fclose(fp);

			rescale(0.0f, 1.0f);

			return true;
		}
		else {

			fprintf(stderr, "ERROR: Could not open file %s.\n", filename.c_str());
			fflush(stderr);

			return false;
		}
	}

protected:
	// linear interpolation of scalar
	float Lerp(float x, float v1, float v2) {

		return (1.f - x) * v1 + x * v2;
	}

	// bilinear interpolation of scalar
	float Bilerp(float x, float y, float v00, float v01, float v10, float v11) {

		float f0 = Lerp(x, v00, v01);
		float f1 = Lerp(x, v10, v11);
		return Lerp(y, f0, f1);
	}

	// returns 1D index
	int getIndex(int x, int y) { return y*width + x; }

	// returns scalar at pixel (x, y)
	float getScalar(int x, int y) { 
		
		x = clampInt(x, 0, width-1);
		y = clampInt(y, 0, height-1);
		return field[getIndex(x, y)]; 
	}

	// clamps integer c to [a,b]
	int clampInt(int c, int a, int b) {

		if(c < a) return a;
		if(c > b) return b;

		return c;
	}

	// rescale scalar field to [min, max] range
	void rescale(float min, float max) {

		float current_max = 0.0f;
		float current_min = std::numeric_limits<float>::max();
		for(int y = 0; y < height; ++y) {
			for(int x = 0; x < width; ++x) {

				float s = field[getIndex(x, y)];
				if(s > current_max)
					current_max = s;
				if(s < current_min)
					current_min = s;
			}
		}

		for(int y = 0; y < height; ++y) {
			for(int x = 0; x < width; ++x) {

				float s = field[getIndex(x, y)];
				s = map(s, current_min, current_max, min, max);
				field[getIndex(x, y)] = s;
			}
		}
	}

protected:
	int width;
	int height;
	float* field;
};


class VectorField2D {

public:
	VectorField2D() : width(0), height(0), field(NULL) {
	}

	vec2 evaluate(float x, float y) {

		if(x < -1.0f || x > 1.0f || y < -1.0f || y > 1.0f)
			return vec2(0.0f, 0.0f);

		float ox = (x - (-1.0f)) / 2.0f;
		float oy = (y - (-1.0f)) / 2.0f;

		float vx = ox * width - 0.5f;
		float vy = oy * width - 0.5f;

		int ix = (int)floorf(vx);
		int iy = (int)floorf(vy);

		float dx = vx - ix;
		float dy = vy - iy;

		vec2 v00 = getVector(ix  , iy  );
		vec2 v01 = getVector(ix+1, iy  );
		vec2 v10 = getVector(ix  , iy+1);
		vec2 v11 = getVector(ix+1, iy+1);

		return Bilerp(dx, dy, v00, v01, v10, v11);
	}

	bool load(std::string filename) {

		FILE *fp;
		fp = fopen(filename.c_str(), "rb");
		float* buffer = NULL;

		if(fp != NULL) {

			fread(&width, sizeof(int), 1, fp);
			fread(&height, sizeof(int), 1, fp);

			buffer = new float[2*width*height];

			fread(buffer, 2*sizeof(float), width*height, fp);
			fclose(fp);

			if(field)
				delete [] field;
			field = new vec2[width*height];

			for(int y = 0; y < height; ++y) {
				for(int x = 0; x < width; ++x) {

					int index = getIndex(x, y);
					float vx = buffer[2*index];
					float vy = buffer[2*index+1];
					field[index] = vec2(vx, vy);	
				}
			}

			delete [] buffer;

			rescaleMagnitude(1.0f);

			return true;
		}
		else {

			fprintf(stderr, "ERROR: Could not open file %s.\n", filename.c_str());
			fflush(stderr);

			return false;
		}
	}

protected:
	// linear interpolation of vector
	vec2 Lerp(float x, vec2 v1, vec2 v2) {

		return vec2((1.f - x) * v1.x + x * v2.x, (1.f - x) * v1.y + x * v2.y);
	}

	// bilinear interpolation of vector
	vec2 Bilerp(float x, float y, vec2 v00, vec2 v01, vec2 v10, vec2 v11) {

		vec2 f0 = Lerp(x, v00, v01);
		vec2 f1 = Lerp(x, v10, v11);
		return Lerp(y, f0, f1);
	}

	// returns 1D index
	int getIndex(int x, int y) { return y*width + x; }

	// returns vector at pixel (x, y)
	vec2 getVector(int x, int y) { 
		
		x = clampInt(x, 0, width-1);
		y = clampInt(y, 0, height-1);
		return field[getIndex(x, y)]; 
	}

	// clamps integer c to [a,b]
	int clampInt(int c, int a, int b) {

		if(c < a) return a;
		if(c > b) return b;

		return c;
	}

	// rescale magnitude of the vector field to [0, max] range
	void rescaleMagnitude(float max) {

		float current_max = 0.0f;
		for(int y = 0; y < height; ++y) {
			for(int x = 0; x < width; ++x) {

				float m = magnitude(field[getIndex(x, y)]);
				if(m > current_max)
					current_max = m;
			}
		}

		float r = max / current_max;
		for(int y = 0; y < height; ++y) {
			for(int x = 0; x < width; ++x) {

				vec2 v = field[getIndex(x, y)];
				v.x *= r;
				v.y *= r;
				field[getIndex(x, y)] = v;
			}
		}
	}

	// returns magnitude of vector
	float magnitude(vec2 v) {

		return sqrtf(v.x*v.x + v.y*v.y);
	}

protected:
	int width;
	int height;
	vec2* field;
};

/******************************************************************************/

void CreateScalarTexture(GLuint texture, int w, int h, const float * scalars) {
	glBindTexture(GL_TEXTURE_2D, texture);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP,    GL_TRUE);

//	glTexImage2D(GL_TEXTURE_2D, 0, GL_R32F, w, h, 0, GL_R, GL_FLOAT, scalars);
	glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE32F_ARB, w, h, 0, GL_LUMINANCE, GL_FLOAT, scalars);

	glBindTexture(GL_TEXTURE_2D, 0);
}

void CreateVectorTexture(GLuint texture, int w, int h, const vec2 * vectors) {
	glBindTexture(GL_TEXTURE_2D, texture);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP,    GL_TRUE);

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RG32F, w, h, 0, GL_RG, GL_FLOAT, vectors);

	glBindTexture(GL_TEXTURE_2D, 0);
}

void CreateMatrixTexture(GLuint texture, int w, int h, const mat2 * matrices) {
	glBindTexture(GL_TEXTURE_2D, texture);

	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S,     GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T,     GL_CLAMP_TO_BORDER);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
	glTexParameteri(GL_TEXTURE_2D, GL_GENERATE_MIPMAP,    GL_TRUE);

	glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA32F, w, h, 0, GL_RGBA, GL_FLOAT, matrices);

	glBindTexture(GL_TEXTURE_2D, 0);
}

/******************************************************************************/

#define FIELD_SIZE_X		256
#define FIELD_SIZE_Y		256

#define TEXTURE_SCALAR_FIELD			0
#define TEXTURE_SCALAR_GRADIENT			1
#define TEXTURE_SCALAR_DIVERGENCE		2
#define TEXTURE_VECTOR_FIELD			3
#define TEXTURE_VECTOR_JACOBIAN			4
#define TEXTURE_VECTOR_DIVERGENCE		5
#define TEXTURE_VECTOR_VORTICITY		6
#define TEXTURE_COUNT					7

int texID = TEXTURE_VECTOR_FIELD;
GLuint textures[TEXTURE_COUNT];

GLuint program = 0;

// Display hedgehogs?
bool hedgehogs = false;

// Final color scale
float scale = 1.0f;

// Discrete scalar field
ScalarField2D scalarField;

// Discrete vector field
VectorField2D vectorField;

/******************************************************************************/

// Clamped cosine
float c(float x) {
	return util::glsl::abs(x) <= 0.5f * M_PI ? cosf(x) : 0.0f;
}


// Analytic vector field
vec2 va(float x, float y) {

#if 0
	// Simple linear, curl-free 2D field
	return vec2(sqrtf(x*x+y*y)*x, sqrtf(x*x+y*y)*y);
#endif

#if 0
	// Simple linear, divergence-free 2D field
	return vec2(-y*sqrtf(x*x+y*y), x*sqrtf(x*x+y*y));
#endif

#if 0
	// Simple linear 2D field
	return vec2(x - y, x + y);
#endif

#if 0
	// Simple quadratic 2D field
	return vec2(x * x, y * y);
#endif

#if 1
	// Vector field from "Time-Dependent 2-D Vector Field Topology: An Approach Inspired by Lagrangian Coherent Structures" by Sadlo & Weiskopf
	static const float a = 0.4f;

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
#endif
}


// discrete vector field
vec2 vd(float x, float y) {

	return vectorField.evaluate(x, y);
}


// vector field
vec2 v(float x, float y) {

#if 0
	// analytic vector field
	return va(x, y);
#endif

#if 1
	// discrete vector field
	return vd(x, y);
#endif
}


// analytic scalar field
float rhoa(float x, float y) {

	return x * x + y * y - 1.0f;
}


// discrete scalar field
float rhod(float x, float y) {

	return scalarField.evaluate(x, y);
}


// scalar field
float rho(float x, float y) {
	
#if 0
	// analytic scalar field
	return rhoa(x, y);
#endif

#if 1
	// discrete scalar field
	return rhod(x, y);
#endif
}

/******************************************************************************/

void CreateTextures() {

	// Create textures
	glGenTextures(TEXTURE_COUNT, textures);

	// Create scalar field
	Image<float> scalarField(FIELD_SIZE_X, FIELD_SIZE_Y);
	{
		for (int j = 0; j < FIELD_SIZE_Y; j++) {
			for (int i = 0; i < FIELD_SIZE_X; i++) {
				float x = map(i + 0.5f, 0, FIELD_SIZE_X, -1.0f, +1.0f);
				float y = map(j + 0.5f, 0, FIELD_SIZE_Y, -1.0f, +1.0f);

				// Evaluate scalar field at (x,y)
				scalarField[i][j] = rho(x, y);
			}
		}

	}
	glActiveTexture(GL_TEXTURE0 + TEXTURE_SCALAR_FIELD);
	CreateScalarTexture(textures[TEXTURE_SCALAR_FIELD], FIELD_SIZE_X, FIELD_SIZE_Y, scalarField.pixels);

	// Create vector field
	Image<vec2> vectorField(FIELD_SIZE_X, FIELD_SIZE_Y);
	{

		for (int j = 0; j < FIELD_SIZE_Y; j++) {
			for (int i = 0; i < FIELD_SIZE_X; i++) {
				float x = map(i + 0.5f, 0, FIELD_SIZE_X, -1.0f, +1.0f);
				float y = map(j + 0.5f, 0, FIELD_SIZE_Y, -1.0f, +1.0f);

				// Evaluate vector field at (x,y)
				vectorField[i][j] = v(x, y);
			}
		}

	}
	glActiveTexture(GL_TEXTURE0 + TEXTURE_VECTOR_FIELD);
	CreateVectorTexture(textures[TEXTURE_VECTOR_FIELD], FIELD_SIZE_X, FIELD_SIZE_Y, vectorField.pixels);

	// Compute gradient of scalar field
	Image<vec2> scalarGradient(FIELD_SIZE_X, FIELD_SIZE_Y);
	{
		for (int j = 0; j < FIELD_SIZE_Y; j++) {
			for (int i = 0; i < FIELD_SIZE_X; i++) {
				float x = map(i + 0.5f, 0, FIELD_SIZE_X, -1.0f, +1.0f);
				float y = map(j + 0.5f, 0, FIELD_SIZE_Y, -1.0f, +1.0f);

				float dx = 2.0f / FIELD_SIZE_X;
				float dy = 2.0f / FIELD_SIZE_Y;

				vec2 & g = scalarGradient[i][j];

				// TODO: Compute gradient
				//g = ...;
//SNIP
#if 1
				// Approximate by differencing
				if (i > 0 && i < FIELD_SIZE_X - 1 && j > 0 && j < FIELD_SIZE_Y - 1) {
					float rhopx = scalarField[i + 1][j];
					float rhonx = scalarField[i - 1][j];
					float rhopy = scalarField[i][j + 1];
					float rhony = scalarField[i][j - 1];

					float drho_dx = (rhopx - rhonx) / (2.0f * dx);
					float drho_dy = (rhopy - rhony) / (2.0f * dy);

					g.x = drho_dx;
					g.y = drho_dy;
				} else {
					// Ignore borders
					g = vec2(0);
				}
#endif
//SNAP
			}
		}
	}
	glActiveTexture(GL_TEXTURE0 + TEXTURE_SCALAR_GRADIENT);
	CreateVectorTexture(textures[TEXTURE_SCALAR_GRADIENT], FIELD_SIZE_X, FIELD_SIZE_Y, scalarGradient.pixels);

	// Compute divergence of gradient (i.e. Laplace operator) of scalar field
	Image<float> scalarDivergence(FIELD_SIZE_X, FIELD_SIZE_Y);
	{
		for (int j = 0; j < FIELD_SIZE_Y; j++) {
			for (int i = 0; i < FIELD_SIZE_X; i++) {
				float x = map(i + 0.5f, 0, FIELD_SIZE_X, -1.0f, +1.0f);
				float y = map(j + 0.5f, 0, FIELD_SIZE_Y, -1.0f, +1.0f);

				float dx = 2.0f / FIELD_SIZE_X;
				float dy = 2.0f / FIELD_SIZE_Y;

				float & div = scalarDivergence[i][j];
				// TODO: Compute divergence of scalar field
				//div = ...;
				div = 0.0f;
//SNIP
#if 1
				// Approximate by differencing
				if (i > 0 && i < FIELD_SIZE_X - 1 && j > 0 && j < FIELD_SIZE_Y - 1) {
					float rhopx = scalarField[i + 1][j + 0];
					float rhonx = scalarField[i - 1][j + 0];
					float rho00 = scalarField[i + 0][j + 0];
					float rhopy = scalarField[i + 0][j + 1];
					float rhony = scalarField[i + 0][j - 1];

                    // second-order central differences
                    // similar to discrete laplacian operator:
					// filter [1, -2, 1] from convolving [-1,1] with itself
					float d2rho_dx2 = (rhonx - 2.0f * rho00 + rhopx) / (dx * dx);
					float d2rho_dy2 = (rhony - 2.0f * rho00 + rhopy) / (dy * dy);

					div = d2rho_dx2 + d2rho_dy2;
				}
#endif
//SNAP
			}
		}
	}
	glActiveTexture(GL_TEXTURE0 + TEXTURE_SCALAR_DIVERGENCE);
	CreateScalarTexture(textures[TEXTURE_SCALAR_DIVERGENCE], FIELD_SIZE_X, FIELD_SIZE_Y, scalarDivergence.pixels);

	// Compute Jacobian of vector field
	Image<mat2> vectorJacobian(FIELD_SIZE_X, FIELD_SIZE_Y);
	{
		for (int j = 0; j < FIELD_SIZE_Y; j++) {
			for (int i = 0; i < FIELD_SIZE_X; i++) {
				float x = map(i + 0.5f, 0, FIELD_SIZE_X, -1.0f, +1.0f);
				float y = map(j + 0.5f, 0, FIELD_SIZE_Y, -1.0f, +1.0f);

				float dx = 2.0f / FIELD_SIZE_X;
				float dy = 2.0f / FIELD_SIZE_Y;

				mat2 & J = vectorJacobian[i][j];
				// TODO: Compute Jacobian
				// NOTE: GLSL matrix indices are column-major
				//J[0][0] = ...;
				//J[1][0] = ...;
				//J[0][1] = ...;
				//J[1][1] = ...;
				J = mat2(0.0f);
//SNIP
#if 1
				// Approximate by differencing
				if (i > 0 && i < FIELD_SIZE_X - 1 && j > 0 && j < FIELD_SIZE_Y - 1) {
					float vxpx = vectorField[i + 1][j + 0].x;
					float vxnx = vectorField[i - 1][j + 0].x;
					float vxpy = vectorField[i + 0][j + 1].x;
					float vxny = vectorField[i + 0][j - 1].x;

					float vypx = vectorField[i + 1][j + 0].y;
					float vynx = vectorField[i - 1][j + 0].y;
					float vypy = vectorField[i + 0][j + 1].y;
					float vyny = vectorField[i + 0][j - 1].y;

					float dvx_dx = (vxpx - vxnx) / (2.0f * dx);
					float dvx_dy = (vxpy - vxny) / (2.0f * dy);
					float dvy_dx = (vypx - vynx) / (2.0f * dx);
					float dvy_dy = (vypy - vyny) / (2.0f * dy);

					J[0][0] = dvx_dx;
					J[0][1] = dvy_dx;
					J[1][0] = dvx_dy;
					J[1][1] = dvy_dy;
				}
#endif
//SNAP
			}
		}
	}
	glActiveTexture(GL_TEXTURE0 + TEXTURE_VECTOR_JACOBIAN);
	CreateMatrixTexture(textures[TEXTURE_VECTOR_JACOBIAN], FIELD_SIZE_X, FIELD_SIZE_Y, vectorJacobian.pixels);

	// Compute divergence of vector field
	Image<float> vectorDivergence(FIELD_SIZE_X, FIELD_SIZE_Y);
	{
		for (int j = 0; j < FIELD_SIZE_Y; j++) {
			for (int i = 0; i < FIELD_SIZE_X; i++) {
				float x = map(i + 0.5f, 0, FIELD_SIZE_X, -1.0f, +1.0f);
				float y = map(j + 0.5f, 0, FIELD_SIZE_Y, -1.0f, +1.0f);

				float dx = 2.0f / FIELD_SIZE_X;
				float dy = 2.0f / FIELD_SIZE_Y;

				float & div = vectorDivergence[i][j];
				// TODO: Compute divergence of vector field
				//div = ...;
				div = 0.0f;
//SNIP
#if 1
				if (i > 0 && i < FIELD_SIZE_X - 1 && j > 0 && j < FIELD_SIZE_Y - 1) {
					float vxpx = vectorField[i + 1][j].x;
					float vxnx = vectorField[i - 1][j].x;

					float vypy = vectorField[i][j + 1].y;
					float vyny = vectorField[i][j - 1].y;

					float dvx_dx = (vxpx - vxnx) / (2.0f * dx);
					float dvy_dy = (vypy - vyny) / (2.0f * dy);

					div = dvx_dx + dvy_dy;
				}
#endif
//SNAP
			}
		}
	}
	glActiveTexture(GL_TEXTURE0 + TEXTURE_VECTOR_DIVERGENCE);
	CreateScalarTexture(textures[TEXTURE_VECTOR_DIVERGENCE], FIELD_SIZE_X, FIELD_SIZE_Y, vectorDivergence.pixels);

	// Compute vorticity of vector field
	Image<float> vectorVorticity(FIELD_SIZE_X, FIELD_SIZE_Y);
	{
		for (int j = 0; j < FIELD_SIZE_Y; j++) {
			for (int i = 0; i < FIELD_SIZE_X; i++) {
				float x = map(i + 0.5f, 0, FIELD_SIZE_X, -1.0f, +1.0f);
				float y = map(j + 0.5f, 0, FIELD_SIZE_Y, -1.0f, +1.0f);

				float dx = 2.0f / FIELD_SIZE_X;
				float dy = 2.0f / FIELD_SIZE_Y;

				float & rot = vectorVorticity[i][j];
				// TODO: Compute vorticity of vector field v
				//rot = ...;
				rot = 0.0f;
//SNIP
#if 1
				if (i > 0 && i < FIELD_SIZE_X - 1 && j > 0 && j < FIELD_SIZE_Y - 1) {

					float vxpy = vectorField[i][j + 1].x;
					float vxny = vectorField[i][j - 1].x;

					float vypx = vectorField[i + 1][j].y;
					float vynx = vectorField[i - 1][j].y;

					float dvx_dy = (vxpy - vxny) / (2.0f * dy);
					float dvy_dx = (vypx - vynx) / (2.0f * dx);

					rot = dvy_dx - dvx_dy;
				}
#endif
//SNAP
			}
		}
	}
	// Select the right texture unit
	glActiveTexture(GL_TEXTURE0 + TEXTURE_VECTOR_VORTICITY);
	CreateScalarTexture(textures[TEXTURE_VECTOR_VORTICITY], FIELD_SIZE_X, FIELD_SIZE_Y, vectorVorticity.pixels);

	// Activate default texture unit
	glActiveTexture(GL_TEXTURE0);
}

/******************************************************************************/

void LoadShaders() {
	gl::RecreateProgramFromFiles(program, NULL, NULL, "main-solution.frag", "Util.glsl");
}

void KillShaders() {
	gl::DeleteProgram(program);
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
		LoadShaders();
	}
}

void Mouse(int button, int state, int x, int y) {
	// Let AntTweakBar preempt mouse button events
	if (TwEventMouseButtonGLUT(button, state, x, y)) {
		return;
	}
}

void Motion(int x, int y) {
	// Let AntTweakBar preempt mouse motion events
	if (TwEventMouseMotionGLUT(x, y)) {
		return;
	}
}

void Init() {

	// Load discrete scalar field
	if(!scalarField.load(std::string("pressure.dat")))
		exit(1);

	// Load discrete vector field
	if(!vectorField.load(std::string("velocity.dat")))
		exit(1);

	// Initialize AntTweakBar GUI
	TwInit(TW_OPENGL, NULL);

	TwBar * bar = TwNewBar("Settings");

	TwEnumVal texEnum[TEXTURE_COUNT] = {
		{ TEXTURE_SCALAR_FIELD,      "Scalar: Field"        }, 
		{ TEXTURE_SCALAR_GRADIENT,   "Scalar: Gradient"     }, 
		{ TEXTURE_SCALAR_DIVERGENCE, "Scalar: Divergence"   }, 
		{ TEXTURE_VECTOR_FIELD,      "Vector: Field"        }, 
		{ TEXTURE_VECTOR_JACOBIAN,   "Vector: Jacobian"     }, 
		{ TEXTURE_VECTOR_DIVERGENCE, "Vector: Divergence"   }, 
		{ TEXTURE_VECTOR_VORTICITY,  "Vector: Vorticity"    }, 
	};
	TwType texType = TwDefineEnum("TEXTURE_TYPE", texEnum, TEXTURE_COUNT);
	TwAddVarRW(bar, "Source",    texType,         &texID,     "key=space");
	TwAddVarRW(bar, "Hedgehogs", TW_TYPE_BOOLCPP, &hedgehogs, "key=h");
	TwAddVarRW(bar, "Scale",     TW_TYPE_FLOAT,   &scale,     "step=0.001");

	// Create the textures
	CreateTextures();

	// Load the shader program(s)
	LoadShaders();
}

void Exit() {
	/*
	// Shut down AntTweakBar
	TwTerminate();

	// Delete textures
	glDeleteTextures(TEXTURE_COUNT, textures);

	// Delete shader programs
	KillShaders();
	*/
}

void Reshape(int width, int height) {
	// Update AntTweakBar window size
	TwWindowSize(width, height);

	// Update viewport
	glViewport(0, 0, width, height);
}

void Display() {
	// Clear the buffers
	//glClear(GL_COLOR_BUFFER_BIT);

	// Draw the field
	{
		glUseProgram(program);
		glUniform1i(glGetUniformLocation(program, "TexID"),               texID);
		glUniform1i(glGetUniformLocation(program, "ScalarFieldTex"),      TEXTURE_SCALAR_FIELD);
		glUniform1i(glGetUniformLocation(program, "ScalarGradientTex"),   TEXTURE_SCALAR_GRADIENT);
		glUniform1i(glGetUniformLocation(program, "ScalarDivergenceTex"), TEXTURE_SCALAR_DIVERGENCE);
		glUniform1i(glGetUniformLocation(program, "VectorFieldTex"),      TEXTURE_VECTOR_FIELD);
		glUniform1i(glGetUniformLocation(program, "VectorJacobianTex"),   TEXTURE_VECTOR_JACOBIAN);
		glUniform1i(glGetUniformLocation(program, "VectorDivergenceTex"), TEXTURE_VECTOR_DIVERGENCE);
		glUniform1i(glGetUniformLocation(program, "VectorVorticityTex"),  TEXTURE_VECTOR_VORTICITY);
		glUniform1f(glGetUniformLocation(program, "Scale"),               scale);
		//glUseProgram(0);
#if 0
		glEnable(GL_TEXTURE_2D);
		glActiveTexture(GL_TEXTURE0 + texID);
		glBindTexture(GL_TEXTURE_2D, textures[texID]);
#else
		for (int texID = 0; texID < TEXTURE_COUNT; texID++) {
			glActiveTexture(GL_TEXTURE0 + texID);
			glBindTexture(GL_TEXTURE_2D, textures[texID]);
		}
#endif

		glBegin(GL_QUADS);
		glColor3f(1.0f, 1.0f, 1.0f);
		glTexCoord2f(0.0f, 0.0f); glVertex2f(-1.0f, -1.0f);
		glTexCoord2f(1.0f, 0.0f); glVertex2f(+1.0f, -1.0f);
		glTexCoord2f(1.0f, 1.0f); glVertex2f(+1.0f, +1.0f);
		glTexCoord2f(0.0f, 1.0f); glVertex2f(-1.0f, +1.0f);
		glEnd();

		glUseProgram(0);
#if 0
		glDisable(GL_TEXTURE_2D);
		glBindTexture(GL_TEXTURE_2D, 0);
		glActiveTexture(GL_TEXTURE0);
#else
		for (int texID = 0; texID < TEXTURE_COUNT; texID++) {
			glActiveTexture(GL_TEXTURE0 + texID);
			glBindTexture(GL_TEXTURE_2D, 0);
		}
#endif
	}

	// Draw the vectors
	if (hedgehogs && texID >= TEXTURE_VECTOR_FIELD && texID < TEXTURE_COUNT) {
		glBegin(GL_LINES);
		glColor3f(1, 0, 1);
		for (int j = 0; j < 40; j++) {
			for (int i = 0; i < 40; i++) {
				vec2 p = map(vec2(i + 0.5, j + 0.5), vec2(0), vec2(40), vec2(-1), vec2(1));
				vec2 v = ::v(p.x, p.y);
				glVertex2fv(p);
				glVertex2fv(p + v * scale * 0.1f);
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
}

int main(int argc, char ** argv) {
	glutInit(&argc, argv);
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE);
	glutInitWindowSize(1024, 1024);
	glutCreateWindow("Vector Analysis");

	glewInit();

	Init();

	glutKeyboardFunc(&Keyboard);
	glutSpecialFunc(&Special);
	glutMouseFunc(&Mouse);
	glutMotionFunc(&Motion);
	glutPassiveMotionFunc(&Motion);
	glutReshapeFunc(&Reshape);
	glutDisplayFunc(&Display);
	glutIdleFunc(&Idle);

	atexit(&Exit);
	glutMainLoop();

	return 0;
}
