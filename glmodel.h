#pragma once

#include <string>
#include <vector>
#include <iostream>
#include <glm/glm.hpp>
#include <array>


// texture surface range in index buffer
struct GLObjModelSurface
{
	unsigned int startIndex;
	unsigned int endIndex;
	unsigned int gl_texKd = 0;
	unsigned int gl_texKs = 0;
	unsigned int gl_texBump = 0;
	glm::vec3 kd, ks;
};

unsigned int loadGLTexture(const std::string& filename, float gamma);

class GLObjModel
{
public:
	unsigned int vao = 0, buf_vertex = 0, buf_normal = 0, buf_texcoord = 0, buf_index = 0;
	int num_indices = 0;
	int flags = 0;
	enum {
		DEFAULT = 0,
		ADJACENCY = 1 << 0,
	};

	std::vector<GLObjModelSurface> modelSurfaceRange;

	GLObjModel(const std::string &path, int flags = DEFAULT);
	~GLObjModel();
	void draw();
	void draw(int surface_range_idx);

	int index_count() const;
};
