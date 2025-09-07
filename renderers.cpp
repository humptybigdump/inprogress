#include <cglib/core/assert.h>
#include <cglib/gl/fbo.h>

#include <cglib/gl/renderer.h>
#include <cglib/gl/glmodel.h>
#include <cglib/rt/aabb.h>
#include <cglib/rt/texture.h>
#include <cglib/core/image.h>
#include <cglib/gl/prefilter_envmap.h>
#include <cglib/gl/scene_graph.h>
#include <cglib/gl/util.h>

#include <glm/gtx/transform.hpp>
#include <glm/gtc/matrix_inverse.hpp>
#include <glm/gtc/type_ptr.hpp>
#include <cglib/core/glmstream.h>

#include <random>

#include <cglib/imgui/imgui.h>

#include "renderers.h"


ShadowVolumes::
ShadowVolumes()
{
	MapNameProgramDefinition mpd = {
		{	"point_light",
			{ { "shader/point_light.vert" }
			, { "shader/point_light.frag" }
			}
		},
		{	"ambient",
			{ { "shader/ambient.vert" }
			, { "shader/ambient.frag" }
			}
		},
		{	"tonemap",
			{ { "shader/tonemap.vert" }
			, { "shader/tonemap.frag" }
			}
		},
		{	"light_source",
			{ { "shader/light.vert" }
			, { "shader/light.frag" }
			}
		},
	};

	{
		ProgramDefinition p;
		p.files_vertex.push_back("shader/shadow_volumes.vert");
		p.files_fragment.push_back("shader/shadow_volumes.frag");
		p.files_geom.push_back("shader/shadow_volumes.geom");
		mpd.insert({"shadow_volumes", p});
	}

	shader_manager.set_program_definitions(mpd);
}

void ShadowVolumes::
_resize(int width, int height)
{
	// create a FBO with a 8bit stencil buffer
	fbo = std::make_shared<FBO>(
			FBOInit(width, height)
				.attach_color(0, GL_RGBA16F)
				.attach_rb(GL_DEPTH24_STENCIL8)
	);
}


int ShadowVolumes::
_initialize()
{
	glm::vec3 cam_pos(6.5, 6.1, 5.2);
	glm::vec3 cam_center(0.f, 0.f, 0.0f);

	camera = std::make_shared<RTFreeFlightCamera>(cam_pos, normalize(cam_center - cam_pos), 0.0f);

	// load scenes with triangle adjacency information
	monkey     = std::make_shared<GLObjModel>("assets/suzanne.obj", GLObjModel::ADJACENCY);
	dinosaurs  = std::make_shared<GLObjModel>("assets/dinosaurs.obj", GLObjModel::ADJACENCY);
	sponza     = std::make_shared<GLObjModel>("assets/crytek-sponza/sponza_triag.obj", GLObjModel::ADJACENCY);
	sphere     = std::make_shared<GLObjModel>("assets/new_sphere.obj", GLObjModel::ADJACENCY);
	cube       = std::make_shared<GLObjModel>("assets/cube.obj", GLObjModel::ADJACENCY);

	fstri      = std::make_shared<GLObjModel>("assets/fstri.obj");

	return 0;
}

void ShadowVolumes::
_destroy()
{
	monkey = sphere = dinosaurs = fstri = cube = sponza = nullptr;
}

void ShadowVolumes::
draw_scene(Shader &shader, const glm::mat4 &VP)
{
	// apply scaling to sponza scene
	float s = scene == SCENE_SPONZA ? 1e-2 : 1.0;
	glm::mat4 M = glm::mat4(1.0);
	M[0][0] = M[1][1] = M[2][2] = s;

	shader.bind()
		.uniform("MVP", VP * M)
		.uniform("VP", VP)
		.uniform("M", M)
		;

	switch(scene) {
	case SCENE_DINOSAURS: dinosaurs->draw(); break;
	case SCENE_SPONZA:    sponza->draw();    break;
	case SCENE_CUBE:      cube->draw();      break;
	default: break;
	}
}

void ShadowVolumes::
draw_debug()
{
	glm::mat4 VP = projection * camera->get_view_matrix(Camera::Mono);

	glDisable(GL_CULL_FACE);

	// render scene
	static bool wireframe_object = true;
	glPolygonMode(GL_FRONT_AND_BACK, wireframe_object ? GL_LINE : GL_FILL);
	static bool render_object = true;
	ImGui::Checkbox("Render Object", &render_object);
	ImGui::Checkbox("Wireframe Object", &wireframe_object);
	if(render_object) {
		glDepthFunc(GL_LEQUAL);
		glEnable(GL_DEPTH_TEST);
		glDepthMask(GL_TRUE);
		glDepthFunc(GL_LEQUAL);
		glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE);

		auto &shd = shader_manager["ambient"].bind();
		shd.uniform("ambient", glm::vec3(0, 1, 0));
		draw_scene(shd, VP);
	} 
	
	// render shadow volumes
	static bool wireframe_shadow_volumes = true;
	ImGui::Checkbox("Wireframe Shadow Volumes", &wireframe_shadow_volumes);
	glPolygonMode(GL_FRONT_AND_BACK, wireframe_shadow_volumes ? GL_LINE : GL_FILL);
	if(render_shadow_volumes) {
		auto &shd = shader_manager["shadow_volumes"].bind();
		shd.uniform("light_position", light_position);
		shd.uniform("light_intensity", glm::vec3(1, 0, 0));
		draw_scene(shd, VP);
		glDisable(GL_STENCIL_TEST);
		glDepthMask(GL_TRUE);
		glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE);
	}
	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

	glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);

	// draw light
	shader_manager["light_source"].bind()
		.uniform("light_intensity", light_intensity)
		.uniform("MVP", VP * glm::translate(light_position) * glm::scale(glm::vec3(0.1f)))
		;
	sphere->draw();
}

void ShadowVolumes::
draw_shadowed()
{
	ImGui::DragFloat("shadow volume intensity", &shadow_volume_intensity, 0.0001f); 
	ImGui::DragFloat3("ambient", &ambient[0], 0.01f); 

	glm::mat4 VP = projection * camera->get_view_matrix(Camera::Mono);

	// first geometry pass, render ambient lighting
	{
		// draw ambient term of the scene (can be black as well). It is
		// important to create a valid depth buffer for the subsequent shadow
		// volume passes.
		
		// todo: configure OpenGL state

		auto &shd = shader_manager["ambient"].bind();
		shd.uniform("ambient", ambient);
		draw_scene(shd, VP);
	} 

	// Second geometry pass, extract silhouettes from mesh and draw
	// corresponding shadow volumes. The stencil should be configured to
	// counts front and backsides.
	{
		// todo: configure OpenGL state

		if(render_shadow_volumes) {
			// optional: configure blending to visualize shadow volumes
		}
		else {
			// todo: disable writes to the color buffer, only stencil buffer should
			// be updated
		}

		auto &shd = shader_manager["shadow_volumes"].bind();
		shd.uniform("light_position", light_position);
		shd.uniform("light_intensity", light_intensity * shadow_volume_intensity * 0.01f);
		draw_scene(shd, VP);

	}

	// Third geometry pass. Resubmit geometry with point-light shader where
	// the stencil test masks out pixels which are in shadow. The contribution
	// of the point-light is added to the ambient term already present in the
	// framebuffer (hint: blending).
	{
		// todo: configure OpenGL state

		auto &shd = shader_manager["point_light"].bind();
		shd.uniform("light_position", light_position);
		shd.uniform("light_intensity", light_intensity);
		draw_scene(shd, VP);
		glDisable(GL_STENCIL_TEST);
		glDisable(GL_BLEND);
	}

	// draw light
	{
		shader_manager["light_source"].bind()
			.uniform("light_intensity", light_intensity)
			.uniform("MVP", VP * glm::translate(light_position) * glm::scale(glm::vec3(0.1f)))
			;
		sphere->draw();
	}
}

void ShadowVolumes::
_draw()
{
	ImGui::Combo("View Mode", &render_mode, render_mode_names, NUM_MODES);
	ImGui::Combo("Scene", &scene, scene_names, NUM_SCENES);
	ImGui::DragFloat("Exposure", &exposure, 0.01f);
	ImGui::DragFloat3("Light Position", &light_position[0], 0.01f); 
	ImGui::DragFloat3("Light Intensity", &light_intensity[0], 0.01f); 
	ImGui::Checkbox("Show shadow volumes", &render_shadow_volumes);

	// Enable gamma correction for the default framebuffer
	glEnable(GL_FRAMEBUFFER_SRGB);

	// render into off-screen floating point framebuffer
	{
		fbo->bind();
		glClearColor(0, 0, 0, 0);
		glStencilMask(~0);
		glClearStencil(0);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT);

		switch(render_mode) {
		case MODE_NORMAL: draw_shadowed(); break;
		case MODE_DEBUG:  draw_debug();    break;
		default: break;
		}

		fbo->unbind();
	}

	// blit the off-screen framebuffer into the default framebuffer
	{
		glClearColor(1, 0, 1, 0);
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
		glDisable(GL_DEPTH_TEST);

		shader_manager["tonemap"].bind()
			.uniform("tex_framebuffer", 1)
			.uniform("exposure", std::exp2f(exposure))
			;
		glActiveTexture(GL_TEXTURE1);
		glBindTexture(GL_TEXTURE_2D, fbo->tex_color[0]);
		glActiveTexture(GL_TEXTURE0);

		fstri->draw();
	}

	// disable gamma correction
	glDisable(GL_FRAMEBUFFER_SRGB);
}
// CG_REVISION 5ad5f3ea62d3114bee96949072042ec297d654c5
