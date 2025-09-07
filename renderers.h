#pragma once

#include <cglib/gl/renderer.h>

class ShadowVolumes : public Renderer
{
public:
	ShadowVolumes();

	const char * get_name() override { return "Shadow Volumes"; }
protected:
	void _draw() override;
	void _destroy() override;
	int  _initialize() override;
	void _resize(int width, int height) override;

	void draw_scene(Shader &shader, const glm::mat4 &VP);
	void draw_debug();
	void draw_shadowed();

	std::shared_ptr<GLObjModel> monkey, sphere, dinosaurs, fstri, cube, sponza;

	glm::vec3 light_position = glm::vec3(0, 5.5, 0);
	glm::vec3 light_intensity = glm::vec3(40, 40, 40);
	glm::vec3 ambient = glm::vec3(0.004);
	float exposure = 0.0f;

	float shadow_volume_intensity = 0.01f;

	bool render_shadow_volumes = true;

	std::shared_ptr<FBO> fbo;

	enum { MODE_NORMAL, MODE_DEBUG, NUM_MODES };
	const char *render_mode_names[NUM_MODES] = { "Shadowed", "Debug" };
	int render_mode = MODE_DEBUG;

	enum { SCENE_DINOSAURS, SCENE_SPONZA, SCENE_CUBE, NUM_SCENES };
	const char *scene_names[NUM_SCENES] = { "Dinosaurs", "Sponza", "Cube" };
	int scene = SCENE_CUBE;
};
// CG_REVISION 5ad5f3ea62d3114bee96949072042ec297d654c5
